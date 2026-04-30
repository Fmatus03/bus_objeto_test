# Documento de Requisitos — Bus de Objetos en C

## 1\. Requisitos Funcionales (RF)

Cada requisito incluye: ID, descripción, precondición, postcondición y flujo alternativo.  
Cobertura: Todas las operaciones de **List**, **Stack** y **Tree**, gestión de instancias y manejo de errores del servidor.

| ID | Descripción | Precondición | Postcondición | Flujo Alternativo |
| :---- | :---- | :---- | :---- | :---- |
| **RF-001** | **Crear Lista** — El cliente envía `LIST|CREATE|0|` para solicitar la creación de una nueva instancia de List en el servidor. | El servidor está activo y escuchando en el puerto configurado. El número de instancias activas es menor que `MAX_INSTANCES` (256). | El servidor asigna un ID único ≥ 0, registra el slot como activo y responde `OK|<ID>`. | Si el número de instancias activas alcanza `MAX_INSTANCES`, el servidor no crea la instancia y responde `ERROR|SERVER_ERROR`. |
| **RF-002** | **Insertar en Lista** — El cliente envía `LIST|INSERT|<ID>|<valor>` para agregar un entero al final de la lista identificada por `<ID>`. | La instancia de List con `<ID>` existe y está activa en `object_server`. El campo `<valor>` es un entero representable en 32 bits. | El entero es insertado al final de la lista enlazada. El `size` de la lista se incrementa en 1\. Se responde `OK|`. | Si `<ID>` no corresponde a ninguna instancia activa, se responde `ERROR|INSTANCE_NOT_FOUND`. Si `<valor>` no es un entero válido, se responde `ERROR|INVALID_MESSAGE`. |
| **RF-003** | **Obtener Elemento de Lista** — El cliente envía `LIST|GET|<ID>|<pos>` para recuperar el entero almacenado en la posición `<pos>` de la lista. | La instancia de List con `<ID>` existe. `<pos>` es un entero. | El servidor retorna el entero en la posición `<pos>` respondiendo `OK|<valor>`. | Si `<pos>` \< 0 o `<pos>` ≥ `size`, se responde `ERROR|OUT_OF_BOUNDS`. Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-004** | **Remover Elemento de Lista** — El cliente envía `LIST|REMOVE|<ID>|<pos>` para eliminar el elemento en la posición `<pos>` de la lista. | La instancia de List con `<ID>` existe. `<pos>` es un entero. | El nodo en `<pos>` es desvinculado y se libera su memoria (`free()`). El `size` se decrementa en 1\. Los índices posteriores se reordenan. Se responde `OK|`. | Si `<pos>` \< 0 o `<pos>` ≥ `size`, se responde `ERROR|OUT_OF_BOUNDS`. Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-005** | **Tamaño de Lista** — El cliente envía `LIST|SIZE|<ID>|` para obtener el número de elementos actuales en la lista. | La instancia de List con `<ID>` existe y está activa. | El servidor responde `OK|<n>` donde `<n>` es el entero que representa el número de nodos enlazados. | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-006** | **Contiene Elemento en Lista** — El cliente envía `LIST|CONTAINS|<ID>|<valor>` para verificar si `<valor>` existe en algún nodo de la lista. | La instancia de List con `<ID>` existe. `<valor>` es un entero. | El servidor recorre la lista y responde `OK|TRUE` si el valor existe, o `OK|FALSE` si no fue encontrado. | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. Si la lista está vacía, se responde `OK|FALSE` (no es error). |
| **RF-007** | **Limpiar Lista** — El cliente envía `LIST|CLEAR|<ID>|` para vaciar completamente la lista, liberando todos sus nodos. | La instancia de List con `<ID>` existe y está activa. | Todos los nodos son desvinculados y su memoria liberada (`free()` por nodo). El `size` se establece en 0\. Se responde `OK|`. | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. Si la lista ya está vacía, la operación es idempotente y responde `OK|` igualmente. |
| **RF-008** | **Crear Pila** — El cliente envía `STACK|CREATE|0|` para solicitar la creación de una nueva instancia de Stack. | El servidor está activo. El número de instancias activas es menor que `MAX_INSTANCES`. | El servidor asigna un ID único, registra el slot y responde `OK|<ID>`. | Si no hay slots disponibles, se responde `ERROR|SERVER_ERROR`. |
| **RF-009** | **Push en Pila** — El cliente envía `STACK|PUSH|<ID>|<valor>` para agregar un entero al tope de la pila. | La instancia de Stack con `<ID>` existe y está activa. `<valor>` es un entero válido. | El entero se inserta como nuevo nodo en el tope. El `size` se incrementa en 1\. Se responde `OK|`. | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. Si `<valor>` no es entero, se responde `ERROR|INVALID_MESSAGE`. |
| **RF-010** | **Pop en Pila** — El cliente envía `STACK|POP|<ID>|` para extraer el elemento del tope de la pila (LIFO). | La instancia de Stack con `<ID>` existe y está activa. El `size` es mayor que 0\. | El nodo del tope es desvinculado y su memoria liberada. El valor extraído se retorna como `OK|<valor>`. El `size` se decrementa en 1\. | Si la pila está vacía (`size == 0`), se responde `ERROR|EMPTY_STRUCTURE`. Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-011** | **Peek en Pila** — El cliente envía `STACK|PEEK|<ID>|` para consultar el valor del tope sin extraerlo. | La instancia de Stack con `<ID>` existe y está activa. El `size` es mayor que 0\. | El servidor lee el valor del nodo `top` y responde `OK|<valor>`. El `size` permanece invariable. | Si la pila está vacía (`size == 0`), se responde `ERROR|EMPTY_STRUCTURE`. Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-012** | **Consultar si Pila está Vacía** — El cliente envía `STACK|IS_EMPTY|<ID>|` para verificar si la pila no contiene elementos. | La instancia de Stack con `<ID>` existe y está activa. | El servidor responde `OK|TRUE` si `size == 0`, o `OK|FALSE` si `size > 0`. | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-013** | **Crear Árbol BST** — El cliente envía `TREE|CREATE|0|` para solicitar la creación de una nueva instancia de árbol binario de búsqueda. | El servidor está activo. El número de instancias activas es menor que `MAX_INSTANCES`. | El servidor asigna un ID único, aloja la estructura `Tree` en heap y responde `OK|<ID>`. | Si no hay slots disponibles, se responde `ERROR|SERVER_ERROR`. |
| **RF-014** | **Insertar en Árbol** — El cliente envía `TREE|INSERT|<ID>|<valor>` para agregar un nodo con el entero `<valor>` al BST. | La instancia de Tree con `<ID>` existe. `<valor>` es un entero. El valor no está duplicado en el árbol. | El nodo es insertado en la posición correcta para mantener la propiedad BST. El `size` se incrementa en 1\. Se responde `OK|`. | Si `<valor>` ya existe en el árbol, se responde `ERROR|DUPLICATE_VALUE`. Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-015** | **Buscar en Árbol** — El cliente envía `TREE|SEARCH|<ID>|<valor>` para verificar si un valor existe en el BST. | La instancia de Tree con `<ID>` existe. `<valor>` es un entero. | El servidor recorre el árbol siguiendo la propiedad BST y responde `OK|TRUE` si el valor fue encontrado, o `OK|FALSE` en caso contrario. | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. Si el árbol está vacío, la respuesta es `OK|FALSE` (comportamiento normal, no error). |
| **RF-016** | **Eliminar Nodo de Árbol** — El cliente envía `TREE|DELETE|<ID>|<valor>` para eliminar el nodo con el valor indicado, manteniendo la propiedad BST. | La instancia de Tree con `<ID>` existe. `<valor>` es un entero que se encuentra en el árbol. | El nodo es eliminado usando el algoritmo del sucesor inorden para el caso de nodo con dos hijos. La propiedad BST se mantiene. Se libera la memoria del nodo. Se responde `OK|`. | Si `<valor>` no existe en el árbol, se responde `ERROR|NOT_FOUND`. Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. |
| **RF-017** | **Recorrido Inorden del Árbol** — El cliente envía `TREE|INORDER|<ID>|` para obtener todos los valores del BST en orden ascendente. | La instancia de Tree con `<ID>` existe y está activa. | El servidor recorre el árbol inorden y responde `OK|<v1>,<v2>,...,<vN>` en formato CSV. Si el árbol está vacío, responde `OK|` (cadena vacía). | Si `<ID>` no existe, se responde `ERROR|INSTANCE_NOT_FOUND`. El resultado CSV está limitado al tamaño del buffer del protocolo (`MAX_MSG_LEN`). |
| **RF-018** | **Crear Instancia de Estructura**  *(Ej: Nuevo Stack)* | El servidor debe tener memoria disponible y no haber superado el límite máximo de instancias activas. | Se reserva memoria para la estructura, se inicializa vacía y se retorna al cliente un ID (UUID) único. | **Fallo por límite de capacidad:** Si el servidor alcanzó el límite máximo de instancias, se aborta la creación y se retorna al cliente un mensaje de error "ERR\_MAX\_INSTANCES". El estado del servidor no cambia. |
| **RF-019** | **Eliminar Instancia**  *(Limpieza)* | El ID proporcionado por el cliente debe corresponder a una instancia activa en el Bus. | La memoria de la estructura se libera en el servidor y el ID asociado queda permanentemente invalidado. | **ID Inexistente:** Si el cliente envía un ID que no existe (o que ya fue eliminado), el servidor no hace nada y retorna una excepción "ERR\_INSTANCE\_NOT\_FOUND". |
| **RF-020** | **Bloqueo de Instancia**  *(Manejo de Concurrencia)* | La instancia debe existir y no estar bloqueada actualmente por otro cliente. | El cliente obtiene acceso exclusivo a la estructura (ej: para hacer múltiples *push* seguidos). | **Condición de Carrera (Ocupado):** Si otro cliente ya tiene bloqueada la instancia en ese milisegundo, el servidor deniega la petición y retorna un estado "ERR\_LOCKED\_TRY\_LATER". |

---

## 2\. Requisitos No Funcionales (RNF) — Con Métricas Verificables

## 

| ID | Nombre | Descripción / Métrica Verificable |
| :---- | :---- | :---- |
| **NFR-001** | **Latencia Máxima P95** | El tiempo de respuesta de cualquier operación que no modifique iterativamente la estructura entera no debe superar los **200 ms** medidos como P95 usando 1 cliente. |
| **NFR-002** | **Conexiones Concurrentes** | El servidor debe poder aceptar y manejar peticiones de al menos **5 clientes simultáneos** concurrentes (usando threading o asyncio), respondiendo a todos sin caídas de socket ni excepciones de conexión. |
| **NFR-003** | **Seguridad ante Desconexión Abrupta** | Si un programa cliente finaliza forzosamente (p.ej.: finalización súbita) en medio de la sesión, el servidor atrapará el ConnectionResetError o BrokenPipeError y recuperará sus recursos **sin sufrir un crash de proceso**. El hilo del cliente se terminará gracefully. |
| **NFR-004** | **Consumo Máximo de Memoria** | El servidor consumirá como máximo **40 MB** de RAM para el alojamiento de 256 instancias con 10,000 nodos acumulados globalmente. No habrá retención excesiva de referencias (memory leak en Python), verificado perfilando con módulos como tracemalloc. |
| **NFR-005** | **Integridad de Datos Thread-Safe** | Ningún hilo reescribirá datos mientras otro está modificando la misma estructura. La tasa de corrupción por *Race Conditions* o excepciones como RuntimeError en colecciones modificadas concurrentemente será del **0%** durante las pruebas de estrés. |

# Especificación Formal del Protocolo — Bus de Objetos en C

## 1\. Gramática EBNF del Formato de Mensaje

\<Message\>       ::= \<Request\> | \<Response\>

\<Request\>       ::= \<ObjectType\> "|" \<Operation\> "|" \<InstanceID\> "|" \<Data\> "\\n"

\<Response\>      ::= \<OKResponse\> | \<ErrorResponse\>

\<OKResponse\>    ::= "OK|" \<ResponseData\> "\\n"

\<ErrorResponse\> ::= "ERROR|" \<ErrorCode\> "\\n"

\<ObjectType\>    ::= "LIST" | "STACK" | "TREE"

\<Operation\>     ::= "CREATE" | "INSERT" | "GET" | "REMOVE" | "SIZE"

                  | "CONTAINS" | "CLEAR"

                  | "PUSH" | "POP" | "PEEK" | "IS\_EMPTY"

                  | "SEARCH" | "DELETE" | "INORDER"

\<InstanceID\>    ::= \<Digit\> { \<Digit\> }

\<Data\>          ::= { \<Char\> }

\<Char\>          ::= \<Letter\> | \<Digit\> | " " | "-"

\<ResponseData\>  ::= \<Value\> { "," \<Value\> } | ""

\<Value\>         ::= "TRUE" | "FALSE" | \<IntegerLiteral\> | ""

\<IntegerLiteral\>::= \[ "-" \] \<Digit\> { \<Digit\> }

\<ErrorCode\>     ::= \<Letter\> { \<Letter\> | "\_" }

\<Digit\>         ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

\<Letter\>        ::= "A" | "B" | ... | "Z" | "a" | "b" | ... | "z"

**Restricciones semánticas no expresadas en EBNF:**

- El campo `<InstanceID>` en mensajes `CREATE` es ignorado por el servidor (por convención se envía `0`).  
- El campo `<Data>` debe ser un entero decimal válido en el rango `[INT_MIN, INT_MAX]` cuando la operación lo requiera.  
- El terminador `\n` (0x0A) es **obligatorio**. Mensajes sin él provocan bloqueo del `recv()` o respuesta `ERROR|INVALID_MESSAGE` si se implementa timeout.  
- El separador `|` (0x7C) no puede aparecer dentro del campo `<Data>`.

## 2\. Tabla Completa de Operaciones

Cubre los tres objetos soportados: **LIST**, **STACK** y **TREE**.

| Objeto | Operación | Dato Enviado (`<Data>`) | Respuesta OK (`OK|<dato>`) | Respuestas ERROR posibles |
| :---- | :---- | :---- | :---- | :---- |
| **LIST** | CREATE | (vacío) | ID asignado (entero ≥ 0\) | `SERVER_ERROR` |
| **LIST** | INSERT | valor entero | (vacío) → `OK|` | `INSTANCE_NOT_FOUND`, `INVALID_MESSAGE` |
| **LIST** | GET | posición (entero ≥ 0\) | valor en la posición | `OUT_OF_BOUNDS`, `INSTANCE_NOT_FOUND` |
| **LIST** | REMOVE | posición (entero ≥ 0\) | (vacío) → `OK|` | `OUT_OF_BOUNDS`, `INSTANCE_NOT_FOUND` |
| **LIST** | SIZE | (vacío) | Número de elementos (entero ≥ 0\) | `INSTANCE_NOT_FOUND` |
| **LIST** | CONTAINS | valor entero | `TRUE` o `FALSE` | `INSTANCE_NOT_FOUND` |
| **LIST** | CLEAR | (vacío) | (vacío) → `OK|` | `INSTANCE_NOT_FOUND` |
| **STACK** | CREATE | (vacío) | ID asignado (entero ≥ 0\) | `SERVER_ERROR` |
| **STACK** | PUSH | valor entero | (vacío) → `OK|` | `INSTANCE_NOT_FOUND`, `INVALID_MESSAGE` |
| **STACK** | POP | (vacío) | valor extraído del tope | `EMPTY_STRUCTURE`, `INSTANCE_NOT_FOUND` |
| **STACK** | PEEK | (vacío) | valor del tope (sin extraer) | `EMPTY_STRUCTURE`, `INSTANCE_NOT_FOUND` |
| **STACK** | IS\_EMPTY | (vacío) | `TRUE` o `FALSE` | `INSTANCE_NOT_FOUND` |
| **TREE** | CREATE | (vacío) | ID asignado (entero ≥ 0\) | `SERVER_ERROR` |
| **TREE** | INSERT | valor entero | (vacío) → `OK|` | `DUPLICATE_VALUE`, `INSTANCE_NOT_FOUND` |
| **TREE** | SEARCH | valor entero | `TRUE` o `FALSE` | `INSTANCE_NOT_FOUND` |
| **TREE** | DELETE | valor entero | (vacío) → `OK|` | `NOT_FOUND`, `INSTANCE_NOT_FOUND` |
| **TREE** | INORDER | (vacío) | valores CSV ascendentes (`v1,v2,...`) o vacío | `INSTANCE_NOT_FOUND` |

---

## 3\. Tabla de Códigos de Error

| Código de Error | Condición que lo activa | Módulo que lo genera |
| :---- | :---- | :---- |
| `INSTANCE_NOT_FOUND` | El campo `<InstanceID>` no corresponde a ningún slot activo en `object_server`. | `dispatcher.c` → `object_server_get()` retorna \-1 |
| `EMPTY_STRUCTURE` | Se invoca `POP` o `PEEK` sobre una pila con `size == 0`, o `GET` sobre una lista vacía. | `dispatcher.c` → `stack_pop()` / `stack_peek()` retornan `STACK_EMPTY` |
| `OUT_OF_BOUNDS` | El índice `<pos>` enviado en `GET` o `REMOVE` satisface `pos < 0` o `pos >= size`. | `dispatcher.c` → `list_get()` / `list_remove()` retornan `LIST_OUT_OF_BOUNDS` |
| `DUPLICATE_VALUE` | Se intenta insertar en el BST un entero que ya existe en un nodo del árbol. | `dispatcher.c` → `tree_insert()` retorna `TREE_DUPLICATE` |
| `NOT_FOUND` | Se intenta eliminar (`DELETE`) del BST un entero que no existe en ningún nodo. | `dispatcher.c` → `tree_delete()` retorna \-1 |
| `INVALID_OBJECT` | El campo `<ObjectType>` no es `LIST`, `STACK` ni `TREE` (ej. `QUEUE`, `MAP`, `DICT`). | `dispatcher.c` → `switch(msg->obj_type)` rama `default` |
| `INVALID_OPERATION` | La operación existe en el protocolo pero no está definida para el tipo de objeto indicado (ej. `LIST|SEARCH`, `TREE|POP`). | `dispatcher.c` → `dispatch_list/stack/tree()` rama `default` del switch de operación |
| `INVALID_MESSAGE` | El mensaje no tiene el número correcto de separadores `|`, le falta el terminador `\n`, o un campo numérico obligatorio contiene caracteres no numéricos. | `serializer.c` → `deserialize_message()` retorna \-1 |
| `SERVER_ERROR` | `malloc()` falla al crear una nueva instancia, o no hay slots libres en `slots[MAX_INSTANCES]`, u otro error interno irrecuperable. | `object_server.c` → `object_server_create()` retorna \-1 |

## 4\. Ejemplos de Intercambio Cliente / Servidor

Se muestran ≥12 casos comentados, cubriendo flujos estándar y todos los códigos de error.

| N° | Tipo | Descripción del Caso | Request (C → S) | Response (S → C) | Código de Error Activado |
| :---: | :---- | :---- | :---- | :---- | :---- |
| **1** | ESTÁNDAR | Crear lista vacía. El servidor asigna ID=1 al primer slot libre. | `LIST|CREATE|0|\n` | `OK|1\n` | — |
| **2** | ESTÁNDAR | Insertar el entero 42 en la lista ID=1 (primer elemento). | `LIST|INSERT|1|42\n` | `OK|\n` | — |
| **3** | ESTÁNDAR | Obtener el elemento en posición 0 de la lista ID=1 (valor: 42). | `LIST|GET|1|0\n` | `OK|42\n` | — |
| **4** | ESTÁNDAR | Crear pila; el servidor asigna ID=2. | `STACK|CREATE|0|\n` | `OK|2\n` | — |
| **5** | ESTÁNDAR | Push del valor 99 en la pila ID=2. | `STACK|PUSH|2|99\n` | `OK|\n` | — |
| **6** | ESTÁNDAR | Pop de la pila ID=2: extrae y retorna 99\. | `STACK|POP|2|\n` | `OK|99\n` | — |
| **7** | ESTÁNDAR | Crear árbol BST; servidor asigna ID=3. Insertar 5, luego verificar con SEARCH. | `TREE|CREATE|0|\n` → `TREE|INSERT|3|5\n` → `TREE|SEARCH|3|5\n` | `OK|3\n` → `OK|\n` → `OK|TRUE\n` | — |
| **8** | ESTÁNDAR | INORDER del árbol ID=3 con nodos {1, 3, 5, 7, 9} ya insertados. | `TREE|INORDER|3|\n` | `OK|1,3,5,7,9\n` | — |
| **9** | ESTÁNDAR | CLEAR de la lista ID=1: todos los nodos son liberados. | `LIST|CLEAR|1|\n` | `OK|\n` | — |
| **10** | ERROR: FORMATO | Mensaje sin separadores (falta el `|`). `deserialize_message()` no puede tokenizar. | `LISTINSERT1|42\n` | `ERROR|INVALID_MESSAGE\n` | `INVALID_MESSAGE` |
| **11** | ERROR: BOUNDS | GET en lista ID=1 con solo 3 elementos, solicitando posición 312\. | `LIST|GET|1|312\n` | `ERROR|OUT_OF_BOUNDS\n` | `OUT_OF_BOUNDS` |
| **12** | ERROR: INSTANCE | INORDER de un árbol con ID=999, que no existe en el servidor. | `TREE|INORDER|999|\n` | `ERROR|INSTANCE_NOT_FOUND\n` | `INSTANCE_NOT_FOUND` |
| **13** | ERROR: EMPTY | POP en pila ID=2 que fue vaciada previamente con pops anteriores. | `STACK|POP|2|\n` | `ERROR|EMPTY_STRUCTURE\n` | `EMPTY_STRUCTURE` |
| **14** | ERROR: DUPLICADO | INSERT de valor 5 en árbol ID=3 donde 5 ya existe. | `TREE|INSERT|3|5\n` | `ERROR|DUPLICATE_VALUE\n` | `DUPLICATE_VALUE` |
| **15** | ERROR: NOT FOUND | DELETE de valor 99 en árbol ID=3 donde 99 nunca fue insertado. | `TREE|DELETE|3|99\n` | `ERROR|NOT_FOUND\n` | `NOT_FOUND` |
| **16** | ERROR: OBJ INVÁLIDO | Tipo de objeto `QUEUE` no existe en el protocolo. | `QUEUE|CREATE|0|\n` | `ERROR|INVALID_OBJECT\n` | `INVALID_OBJECT` |
| **17** | ERROR: OP INVÁLIDA | `LIST|SEARCH` no existe: SEARCH pertenece solo a TREE. | `LIST|SEARCH|1|5\n` | `ERROR|INVALID_OPERATION\n` | `INVALID_OPERATION` |
| **18** | ERROR: SERVER | El slot 256 está ocupado; no hay slots libres para crear una instancia más. | `LIST|CREATE|0|\n` | `ERROR|SERVER_ERROR\n` | `SERVER_ERROR` |

# Análisis de Secciones Críticas

El Bus de Objetos hace uso de una arquitectura multihilo asíncrona sobre cada cliente conectado, soportado internamente por el módulo `threading`. Como el estado de la aplicación recae sobre un pool único de almacenamiento global (un diccionario o lista en memoria) que almacena los objetos (`object_server`), existen riesgos masivos por condiciones de carrera (*Race Conditions*). Existen áreas de memoria compartidas que por diseño deben protegerse con cerraduras relacionales (`threading.Lock`).

## Inicialización y Asignación de un Nuevo ID de Instancia (Creación)

**Datos compartidos**: El diccionario o registro global (ej. `instances_dict`) y el contador global de IDs asignados (`next_instance_id`).

**Argumentación de su Criterio (Por qué es crítica)**: Cuando dos clientes envían el comando `CREATE` simultáneamente, ambos intentarían leer el `next_instance_id` e incrementarlo al mismo tiempo. Al carecer Python del Global Interpreter Lock (GIL) para garantizar que los incrementos `+= 1` no se pisan si hay *preemption*, ambos hilos podrían obtener el mismo ID, pisándose en el diccionario global y logrando que 2 clientes manipulen 1 misma lista compartidamente por error.

**Mecanismos de Sincronización Propuesto**: El método `object_server_create(type)` contendrá un manejo protegido. Un `threading.Lock()` global (`server_lock`) deberá utilizarse como administrador de contexto (`with server_lock:`) para encapsular las instrucciones de lectura y asignación en el diccionario interno, soltándose finalizado el bloque local.

## Mutación Directa de Estructuras (Modificadores en Objetos)

**Datos compartidos**: Las variables de estado exclusivas internas o apuntadores emulados de las distintas clases base: ej. el array interno (`self.elements`) de STACK o LIST y la variable `self.size`, y la red de `Node` en el Tree.

**Argumentación de su Criterio (Por qué es crítica)**: Una instancia compartida por su ID puede tener mutaciones asincrónicas por dos usuarios. Las operaciones asíncronicas en python como operaciones sobre DataClasses no son atómicas. Si ocurren 2 ejecuciones de `INSERT` sobre la misma lista, dependiendo de cómo la estructuremos con `append` u operaciones de punteros simulados, el estado de `self.size` o la asociación se romperá, o saltaría un `RuntimeError` si otra terminal intentara iterar la estructura.

**Mecanismos de Sincronización Propuesto**: Inmediatamente durante la envoltura en los dispatchers (En `dispatch_list`, `dispatch_stack` y `dispatch_tree`). Se adueñará de *un único Lock Global* o, alternativamente, un *Lock propio por instancia*, bloqueando y protegiendo de la concurrencia a las operaciones Mutables (`INSERT, REMOVE, PUSH, POP, DELETE, CLEAR`). Este mutador previene que la estructura mute internamente si hay una lectura viva.

## Destrucción de la Instancia Global (Eliminación)

**Datos compartidos**: El diccionario central `instances_dict`.

**Argumentación de su Criterio (Por qué es crítica)**: Si el cliente A llama de manera concurrente al borrador (mediante el borrado de referencia `del instances_dict[id]`), y el cliente B poco tiempo después solicita el método `GET` utilizando `get()` en el dispatcher del mismo ID, en plena eliminación de apuntadores la interrupción entre dos hebras podría causar que el Server colapse con un severo `KeyError` no atrapado abortando el socket de servidor al completo.

**Mecanismos de Sincronización Propuesto**: Se protegerá mediante el gestor de contextos `with server_lock:` de `threading` toda la anulación de la instancia en `object_server_destroy_instance(ID)`. Así, una vez garantizada la completitud atómica, cualquier intento de `get` posterior a esa destrucción ya habrá adquirido el cerrojo pero retornará de manera limpia un fallo `INSTANCE_NOT_FOUND`.

