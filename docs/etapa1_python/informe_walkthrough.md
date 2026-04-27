# Informe de Revisión Estática — Walkthrough del Protocolo y Requisitos
**Etapa 1 — Bus de Objetos en C**  
Curso: Pruebas de Software | Proyecto: Bus de Objetos (C99 + TCP/IP + pthreads)

---

## Metodología

Se aplicó la técnica de **walkthrough** con roles alternados: un integrante actúa como **Defensor** (autor del documento) y otro como **Revisor** (auditor externo que busca defectos activamente). El revisor examinó los documentos de Requisitos, Protocolo y Análisis de Secciones Críticas buscando: ambigüedades, inconsistencias, casos no cubiertos y riesgos de implementación.

Se encontraron **8 defectos** documentados a continuación.

---

## Defecto DEF-001 — Ausencia de Especificación del Comportamiento ante Mensaje sin Terminador `\n`

| Campo | Detalle |
|---|---|
| **ID** | DEF-001 |
| **Módulo afectado** | `serializer.c` / Protocolo (Sección 1 — EBNF) |
| **Severidad** | **Crítico** |
| **Tipo de defecto** | Caso no cubierto / Ambigüedad |

**Descripción del defecto:**  
La gramática EBNF define que todo `<Request>` termina con `"\n"`, pero el protocolo original no especificaba qué debe hacer el servidor si el cliente envía un mensaje sin el terminador `\n` (por ejemplo, `LIST|INSERT|1|42` sin newline final). La función `recv()` de sockets TCP es bloqueante: si el mensaje llega sin `\n`, el hilo cliente quedará bloqueado indefinidamente en el bucle de lectura, esperando un byte que nunca llegará.

**Impacto:**  
El hilo queda en estado de espera infinita (*thread starvation*). El socket y sus recursos asociados (descriptor de archivo, memoria del `ClientArgs`) nunca son liberados. Con suficientes clientes que envíen mensajes incompletos, el servidor agota los descriptores de archivo disponibles (`EMFILE`) y deja de aceptar conexiones.

**Propuesta de corrección:**  
1. Implementar `conn.settimeout()` equivalente en C: `setsockopt(client_fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv))` con un timeout de 5 segundos.
2. Implementar un helper `read_line(int fd, char *buf, int max)` que acumule bytes hasta leer `\n` o hasta timeout/error, retornando -1 en caso de timeout.
3. Agregar al RF-020 el flujo alternativo: "Si el mensaje no contiene `\n` dentro de 5 segundos, el servidor cierra el socket del cliente y libera el hilo".

---

## Defecto DEF-002 — Protocolo No Especifica Límite de Tamaño del Campo `<Data>`

| Campo | Detalle |
|---|---|
| **ID** | DEF-002 |
| **Módulo afectado** | `serializer.c` / `bus_server.c` / Protocolo (Sección 1) |
| **Severidad** | **Alto** |
| **Tipo de defecto** | Caso no cubierto / Riesgo de seguridad |

**Descripción del defecto:**  
La gramática define `<Data> ::= { <Char> }` sin límite superior explícito. El campo `data[256]` de `BusMessage` (definido en `protocol.h`) puede ser desbordado si el cliente envía un campo `<Data>` mayor a 255 caracteres. El `deserialize_message()` que usa `strtok_r` sobre el buffer podría escribir más de 256 bytes en `msg.data`, causando un **buffer overflow** en el stack.

**Impacto:**  
Buffer overflow → comportamiento indefinido, posible corrupción del stack del hilo cliente, potencial vector de ejecución remota de código arbitrario (RCE). En el contexto académico: crash del servidor con `SIGSEGV`.

**Propuesta de corrección:**  
1. En `deserialize_message()`: usar `strncpy(msg.data, token, sizeof(msg.data) - 1)` con truncamiento explícito.
2. Agregar al protocolo: "El campo `<Data>` tiene una longitud máxima de 255 caracteres ASCII. Todo dato que exceda este límite será truncado y la operación responderá `ERROR|INVALID_MESSAGE`".
3. Agregar RNF verificable: "El campo `<Data>` nunca causa desbordamiento; verificado con `gcc -fsanitize=address`".

---

## Defecto DEF-003 — Ambigüedad: `INSERT` y `CREATE` Comparten Nombre entre Objetos Distintos con Semánticas Diferentes

| Campo | Detalle |
|---|---|
| **ID** | DEF-003 |
| **Módulo afectado** | `dispatcher.c` / RF-002, RF-009, RF-014 |
| **Severidad** | **Alto** |
| **Tipo de defecto** | Inconsistencia semántica |

**Descripción del defecto:**  
La operación `INSERT` existe para LIST (agrega al final), STACK (equivalente a PUSH en semántica, aunque usa PUSH explícitamente) y TREE (agrega manteniendo propiedad BST con detección de duplicados). El requisito original no especificaba explícitamente que el `dispatcher.c` debe manejar `INSERT` de forma **completamente separada** por tipo de objeto. Un implementador que use un único bloque `if (op == OP_INSERT)` sin considerar el tipo causará que una operación `LIST|INSERT` ejecute la lógica del árbol (o viceversa), generando respuestas incorrectas.

**Impacto:**  
Defectos de integración difíciles de detectar: la operación retorna `OK|` pero el estado interno de la estructura es incorrecto. Por ejemplo, `LIST|INSERT|1|5` podría activar la verificación de duplicados del árbol y rechazar el segundo `INSERT` del mismo valor.

**Propuesta de corrección:**  
1. El `dispatcher.c` implementa funciones separadas: `dispatch_list()`, `dispatch_stack()`, `dispatch_tree()`, cada una con su propio `switch(msg->operation)`.
2. Documentar explícitamente en RF-002, RF-009 y RF-014 que la lógica de enrutamiento es exclusiva por tipo de objeto.
3. Agregar al protocolo la aclaración: "Las operaciones son polimórficas: `INSERT` sobre LIST y `INSERT` sobre TREE tienen comportamientos y errores posibles completamente distintos".

---

## Defecto DEF-004 — Deadlock Potencial si se Retorna Tempranamente sin Liberar `server_mutex`

| Campo | Detalle |
|---|---|
| **ID** | DEF-004 |
| **Módulo afectado** | `dispatcher.c` / `object_server.c` / Análisis de Secciones Críticas |
| **Severidad** | **Crítico** |
| **Tipo de defecto** | Defecto de diseño de concurrencia |

**Descripción del defecto:**  
En el flujo de `dispatch_list()`, si se adquiere `server_mutex` mediante `pthread_mutex_lock()` y luego se detecta que `object_server_get()` falla (ID no existe), se ejecuta un `return` temprano. Si el implementador olvida llamar `pthread_mutex_unlock()` antes del `return`, el mutex queda bloqueado indefinidamente. Todos los hilos posteriores que intenten adquirir `server_mutex` quedarán en espera eterna → **deadlock global del servidor**.

**Impacto:**  
El servidor deja de responder a todos los clientes. El único mecanismo de recuperación es reiniciar el proceso. En producción, esto constituye una interrupción del servicio total (downtime).

**Propuesta de corrección:**  
1. **Patrón obligatorio:** Toda adquisición de `server_mutex` debe estar estructurada como:
```c
object_server_lock();
/* ... lógica ... */
if (error) {
    /* Rellenar resp con error */
    object_server_unlock();  /* ← SIEMPRE antes de return */
    return;
}
/* ... operación exitosa ... */
object_server_unlock();
```
2. Agregar caso de prueba TC-022-4 que mockea un error de `object_server_get` y verifica que el servidor responde a solicitudes posteriores (el mutex fue liberado).
3. Documentar en el análisis de secciones críticas como regla de diseño: "Toda ruta de ejecución dentro de una sección crítica DEBE liberar el mutex antes de retornar, sin excepción".

---

## Defecto DEF-005 — Protocolo No Especifica Comportamiento de INORDER en Árbol Vacío

| Campo | Detalle |
|---|---|
| **ID** | DEF-005 |
| **Módulo afectado** | Protocolo (Sección 2 — Tabla de Operaciones) / RF-017 |
| **Severidad** | **Medio** |
| **Tipo de defecto** | Caso no cubierto / Ambigüedad |

**Descripción del defecto:**  
La tabla de operaciones del protocolo no especificaba el valor de retorno de `TREE|INORDER` cuando el árbol está vacío. Existen al menos tres comportamientos posibles: (1) `OK|` (cadena vacía), (2) `ERROR|EMPTY_STRUCTURE`, o (3) `OK|0` (cero elementos). Sin especificación explícita, diferentes implementadores del cliente y el servidor tomarán decisiones distintas, haciendo el sistema incompatible.

**Impacto:**  
Un cliente que espera `ERROR|EMPTY_STRUCTURE` fallará al recibir `OK|`. Un cliente que usa el resultado para iterar un CSV vacío fallará si recibe un valor numérico. Defecto de compatibilidad entre cliente y servidor.

**Propuesta de corrección:**  
Agregar al RF-017 y a la tabla del protocolo: "Si el árbol está vacío, `TREE|INORDER` retorna `OK|` (campo `ResponseData` vacío, no un error). El cliente debe manejar la respuesta vacía como una iteración de cero elementos." Esta especificación está ahora documentada en la versión corregida del protocolo.

---

## Defecto DEF-006 — `STACK|POP` y `STACK|PEEK` No Documentan INSTANCE_NOT_FOUND en la Tabla Original

| Campo | Detalle |
|---|---|
| **ID** | DEF-006 |
| **Módulo afectado** | Protocolo (Sección 2 — Tabla de Operaciones) / RF-010, RF-011 |
| **Severidad** | **Medio** |
| **Tipo de defecto** | Inconsistencia / Información faltante |

**Descripción del defecto:**  
La versión original de la tabla de operaciones solo listaba `EMPTY_STRUCTURE` como error posible de `STACK|POP` y `STACK|PEEK`. Sin embargo, si el `<InstanceID>` enviado no corresponde a ningún slot activo, el dispatcher debe retornar `INSTANCE_NOT_FOUND` antes de intentar leer el tope de la pila. Este código de error no estaba documentado para esas dos operaciones, lo que llevaría a implementadores de clientes a no manejar ese caso.

**Impacto:**  
Un cliente que no maneja `INSTANCE_NOT_FOUND` en la respuesta de POP interpretará el código de error como un valor de datos, produciendo comportamiento incorrecto en la lógica de la aplicación.

**Propuesta de corrección:**  
Actualizar la tabla del protocolo para que `STACK|POP` y `STACK|PEEK` listen `EMPTY_STRUCTURE, INSTANCE_NOT_FOUND` como errores posibles. Esta corrección está incorporada en la versión mejorada del protocolo (Sección 2).

---

## Defecto DEF-007 — RF-022 (Concurrencia) Mezcla Requisito de Diseño con Requisito Funcional Observable

| Campo | Detalle |
|---|---|
| **ID** | DEF-007 |
| **Módulo afectado** | Documento de Requisitos / RF-022 |
| **Severidad** | **Bajo** |
| **Tipo de defecto** | Ambigüedad estructural |

**Descripción del defecto:**  
El RF-022 original describía la concurrencia como "Clientes paralelos en una misma estructura... usando hilos (`threading`)". Esto mezcla un detalle de implementación interna (uso de pthreads) con un comportamiento observable externamente (el sistema responde correctamente a múltiples clientes). Un requisito funcional debe describir el comportamiento observable del sistema, no su mecanismo interno.

**Impacto:**  
Si el requisito dicta el mecanismo (`pthread_create`), cualquier implementación alternativa igualmente válida (ej. `select()` con E/S no bloqueante) sería rechazada aunque cumpla el comportamiento observable. Los casos de prueba también quedan mal orientados: deben verificar el comportamiento, no el mecanismo.

**Propuesta de corrección:**  
Reformular RF-022 como: "El servidor debe atender solicitudes de múltiples clientes TCP de forma concurrente, garantizando que cada cliente recibe respuestas correctas e independientes, sin mezcla de datos entre sesiones". La implementación con `pthread_create` se documenta en la arquitectura, no en los requisitos.

---

## Defecto DEF-008 — Ausencia de Especificación del Puerto y Límite de Conexiones en los Requisitos

| Campo | Detalle |
|---|---|
| **ID** | DEF-008 |
| **Módulo afectado** | Documento de Requisitos / RNF / Protocolo |
| **Severidad** | **Bajo** |
| **Tipo de defecto** | Información faltante |

**Descripción del defecto:**  
El documento de requisitos original no mencionaba el puerto TCP en el que opera el servidor (`BUS_PORT = 8080`, definido en `protocol.h`), ni el límite de backlog del `listen()`. Un equipo implementador que reciba solo los documentos de Etapa 1 no podría conectar un cliente al servidor sin consultar el código fuente, lo cual invalida el objetivo del protocolo ("que otro equipo pueda implementar un cliente compatible sin leer el código del servidor").

**Impacto:**  
Dependencia implícita en el código fuente. Viola la auto-suficiencia del documento de protocolo. En pruebas de sistema, los scripts de test deben conocer el puerto; si no está documentado, cada desarrollador podría usar un puerto diferente.

**Propuesta de corrección:**  
Agregar al inicio del protocolo: "El servidor TCP escucha en `0.0.0.0:8080` (configurable mediante la constante `BUS_PORT` en `protocol.h`). El `listen()` usa un backlog de 16 conexiones pendientes. El tamaño máximo de mensaje es 1024 bytes (`MAX_MSG_LEN`). El número máximo de instancias simultáneas es 256 (`MAX_INSTANCES`)."

---

## Resumen de Defectos

| ID | Módulo | Severidad | Tipo | Estado |
|:---:|:---|:---:|:---|:---:|
| DEF-001 | `serializer.c` / Protocolo | **Crítico** | Caso no cubierto | ✅ Corregido en protocolo v2 |
| DEF-002 | `serializer.c` / `bus_server.c` | **Alto** | Riesgo de seguridad | ✅ Corregido en RF-020 y protocolo v2 |
| DEF-003 | `dispatcher.c` | **Alto** | Inconsistencia semántica | ✅ Corregido en RF-002/009/014 |
| DEF-004 | `dispatcher.c` / `object_server.c` | **Crítico** | Defecto de concurrencia | ✅ Corregido en SC-1 y SC-2 |
| DEF-005 | Protocolo / RF-017 | **Medio** | Caso no cubierto | ✅ Corregido en RF-017 y protocolo v2 |
| DEF-006 | Protocolo / RF-010, RF-011 | **Medio** | Información faltante | ✅ Corregido en tabla del protocolo v2 |
| DEF-007 | RF-022 | **Bajo** | Ambigüedad estructural | ✅ Corregido en RF-022 v2 |
| DEF-008 | RNF / Protocolo | **Bajo** | Información faltante | ✅ Corregido en protocolo v2 (sección inicial) |
