**ENUNCIADO DETALLADO**

**Proyecto Semestral — Bus de Objetos en C**

Curso: Pruebas de Software | 6 Etapas × 2 Semanas

| Sobre este documento Contiene los enunciados completos de las 6 etapas. Cada uno especifica los objetivos de aprendizaje en pruebas de software, el trabajo técnico a realizar, los entregables requeridos y los criterios mínimos para ser evaluado. El foco siempre está en las pruebas, no solo en construir el sistema. |
| :---- |

| ETAPA 1 — Pruebas Estáticas y Especificación del Protocolo Semanas 1 a 2 | Tipo de prueba: Pruebas Estáticas (Inspección y Walkthrough) |
| :---- |

## **Objetivos de Aprendizaje en Pruebas**

* Comprender la importancia de verificar los requisitos de un sistema distribuido antes de codificar

* Aplicar técnicas de revisión estática (walkthrough e inspección) sobre requisitos y protocolo

* Construir una matriz de trazabilidad entre requisitos y casos de prueba planificados

* Identificar defectos de especificación: ambigüedades, inconsistencias y casos no cubiertos en el protocolo

* Anticipar riesgos de concurrencia antes del desarrollo mediante análisis estático

## **Descripción del Trabajo**

En esta etapa no se escribe código. El equipo actúa como analistas de calidad que deben documentar y verificar los requisitos del Bus de Objetos antes de que el desarrollo comience. La calidad del documento de requisitos y del protocolo tendrá impacto directo en la calidad de las pruebas de las etapas siguientes.

**Parte 1 — Documento de Requisitos**

* Sobre 20 requisitos funcionales con ID, descripción, precondición, postcondición y flujo alternativo. Deben cubrir todas las operaciones de List, Stack y Tree, la gestión de instancias y el comportamiento del servidor ante errores

* Sobre 5 requisitos no funcionales verificables con métricas concretas: latencia máxima por operación, máximo de conexiones simultáneas soportadas, comportamiento ante cliente que desconecta abruptamente, consumo máximo de memoria

**Parte 2 — Especificación Formal del Protocolo**

El protocolo debe quedar tan completo que otro equipo pueda implementar un cliente compatible sin leer el código del servidor. Incluye:

1. Formato exacto del mensaje de solicitud y respuesta

2. Tabla completa: para cada objeto y cada operación, el dato enviado, la respuesta OK y los posibles errores

3. Tabla de códigos de error: al menos 7 códigos distintos con la condición exacta que los activa

4. Más de 10 ejemplos de intercambios comentados, incluyendo casos de error

**Parte 3 — Análisis de Secciones Críticas (Análisis Estático de Concurrencia)**

Antes de codificar, identifica los riesgos de concurrencia del sistema. Este análisis es la primera aplicación de pruebas estáticas a un problema de diseño. Documenta:

* ¿Qué datos serán compartidos entre múltiples hilos del servidor?

* Para cada dato compartido: ¿qué operaciones sobre él son secciones críticas y por qué?

* Al menos 3 secciones críticas identificadas con su mecanismo de sincronización propuesto

**Parte 4 — Matriz de Trazabilidad**

Relaciona cada requisito funcional con al menos un caso de prueba planificado. La matriz es el mapa que guiará las pruebas de todas las etapas siguientes. Para cada relación indica: ID del RF, descripción, ID del caso de prueba propuesto y tipo de prueba (unitaria, integración, sistema o aceptación).

**Parte 5 — Walkthrough del Protocolo**

El equipo se divide en revisor y defensor. El revisor busca activamente defectos en el documento de requisitos y la especificación del protocolo. Documenta al menos 5 defectos con propuesta de corrección:

* ¿Qué pasa si el cliente envía un dato no numérico donde se espera un entero?

* ¿El protocolo especifica qué ocurre si el mensaje no tiene terminador \\n?

* ¿Hay operaciones con el mismo nombre en objetos distintos que podrían confundir?

| Entregables docs/etapa1/requisitos.pdf — Documento de requisitos completo docs/etapa1/protocolo.pdf — Especificación formal del protocolo docs/etapa1/secciones\_criticas.pdf — Análisis estático de concurrencia docs/etapa1/trazabilidad.xlsx — Matriz RF → casos de prueba docs/etapa1/informe\_walkthrough.pdf — Informe con ≥5 defectos y correcciones |
| :---- |
| **Criterios mínimos para ser evaluado** ≥20 RF y ≥5 RNF con métricas. Protocolo con TODAS las operaciones de los 3 objetos. Análisis de ≥3 secciones críticas. Matriz que cubre 100% de los RF. Walkthrough con ≥5 defectos documentados y corregidos. |

| ETAPA 2 — Pruebas Unitarias: List, Stack y Serializer Semanas 3 a 4 | Tipo de prueba: Pruebas Unitarias / Caja Blanca y Negra / TDD |
| :---- |

## **Objetivos de Aprendizaje en Pruebas**

* Implementar pruebas unitarias con Unity aplicando partición de equivalencia y análisis de valores límite

* Medir y mejorar la cobertura de código con gcov y lcov

* Aplicar TDD en al menos uno de los módulos

* Probar el serializer del protocolo con pruebas de caja negra (entradas válidas e inválidas)

* Verificar la ausencia de fugas de memoria con Valgrind

## **Descripción del Trabajo**

Implementa list.c, stack.c y serializer.c siguiendo las interfaces definidas en la Plantilla Base. Para cada módulo, diseñas primero los casos de prueba usando las técnicas del curso, luego implementas (o en el caso de TDD, alternan prueba e implementación).

**Parte 1 — Implementación de list.c y stack.c**

* Gestión dinámica de memoria: malloc por nodo, free en destroy y clear

* Todos los punteros NULL recibidos como parámetro retornan código de error, NUNCA hacen crash

* list\_remove() y stack\_pop() manejan correctamente la estructura vacía

**Parte 2 — Implementación de serializer.c**

* Usa strtok\_r (thread-safe), NO strtok (no es thread-safe y causará bugs en la Etapa 4\)

* deserialize\_message() retorna \-1 ante cualquier mensaje mal formado, nunca produce comportamiento indefinido

* serialize\_response() genera exactamente 'OK|dato\\n' o 'ERROR|codigo\\n'

**Parte 3 — Suite de Pruebas Unitarias con Partición de Equivalencia**

Para cada función, identifica explícitamente las clases de equivalencia en tu informe y diseña al menos 5 casos de prueba cubriendo:

* Clase válida: entrada correcta que produce el resultado esperado

* Clase inválida: entradas incorrectas que deben ser rechazadas con el código de error correcto

* Valor límite inferior: lista/pila vacía, índice 0, un elemento, entero 0

* Valor límite superior: índice \= size-1, insertar en la última posición válida

* Casos especiales: puntero NULL, string vacío (serializer), valor INT\_MIN, valor INT\_MAX

**Parte 4 — TDD en el Serializer**

El serializer es el módulo recomendado para aplicar TDD porque sus entradas y salidas son texto, lo que hace las pruebas muy claras. Para cada función sigue el ciclo:

5. Commit RED: escribe el test que falla porque la función no existe aún

6. Commit GREEN: implementa el código mínimo para que el test pase

7. Commit REFACTOR: mejora el código sin cambiar el comportamiento (si aplica)

**Parte 5 — Reporte de Cobertura**

Ejecuta make coverage y analiza el reporte HTML de lcov. En tu informe responde: ¿qué líneas o ramas no están cubiertas? ¿qué casos de prueba agregarías para mejorar la cobertura? ¿hay código muerto?

|  Entregables src/objects/list.c \+ src/objects/stack.c src/protocol/serializer.c \+ src/protocol/protocol.h tests/unit/test\_list.c \+ test\_stack.c \+ test\_serializer.c reports/ — Reporte HTML de cobertura lcov docs/etapa2/informe\_pruebas.pdf — Clases de equivalencia \+ análisis de cobertura \+ evidencia TDD Pipeline CI/CD funcionando sin errores |
| :---- |

| Criterios mínimos Compilar sin warnings con gcc \-Wall \-Wextra \-std=c99. 100% de pruebas pasando.  Cobertura ≥70% en los 3 módulos. Valgrind 0 fugas.  Historial de commits evidencia TDD. serializer.c usa strtok\_r. |
| :---- |

| ETAPA 3 — Pruebas de Integración: Tree \+ Dispatcher \+ Object Server Semanas 5 a 6 | Tipo de prueba: Pruebas de Integración / Stubs y Drivers |
| :---- |

## **Objetivos de Aprendizaje en Pruebas**

* Comprender y aplicar estrategias de integración: Top-Down, Bottom-Up y Big Bang

* Implementar stubs de socket y drivers para probar módulos de forma aislada

* Detectar y documentar defectos de interfaz entre módulos (parámetros, retornos, efectos secundarios)

* Probar la correctitud del mecanismo de sincronización (mutex) usando múltiples hilos

* Comparar las estrategias de integración en el contexto del bus

## **Descripción del Trabajo**

**Parte 1 — Implementación de tree.c**

* Todas las operaciones de tree.h, incluyendo delete con dos hijos (sucesor inorden)

* tree\_inorder() escribe valores en orden ascendente en el arreglo recibido

* tree\_destroy() libera recursivamente todos los nodos

**Parte 2 — Plan de Integración**

Antes de ejecutar una sola prueba de integración, documenta el plan. El plan determina el orden y la estrategia:

8. Estrategia elegida (Top-Down, Bottom-Up o Big Bang) y justificación técnica

9. Diagrama de dependencias entre módulos

10. Qué módulos requieren stubs o drivers y por qué

11. Orden de integración paso a paso

**Parte 3 — Stubs y Drivers**

Implementa al menos los siguientes:

* Stub de socket: en lugar de enviar por red, escribe el mensaje en un buffer de prueba. Permite probar dispatcher sin necesitar el servidor TCP activo

* Stub de serializer simple: para probar el dispatcher con mensajes pre-construidos en formato BusMessage, sin pasar por deserialize\_message

**Parte 4 — Casos de Prueba de Integración**

Para cada interfaz entre módulos, escribe al menos 3 casos de prueba:

* Serializer ↔ Dispatcher: mensaje válido de cada objeto, mensaje con ID inexistente, mensaje malformado

* Dispatcher ↔ Object Server: crear múltiples instancias simultáneamente, obtener por ID correcto e ID inexistente

* Dispatcher ↔ List / Stack / Tree: operación válida, operación sobre estructura vacía, operación con índice inválido

**Parte 5 — Prueba de Concurrencia del Object Server**

Implementa test\_concurrency.c para verificar que el mutex protege correctamente el object\_server. Mínimo:

* ≥10 hilos llaman a object\_server\_create() simultáneamente: verifica que todos los IDs asignados son distintos

* ≥10 hilos operan simultáneamente sobre la misma instancia: verifica que no hay corrupción de datos

* Ejecuta con Helgrind (valgrind \--tool=helgrind) y verifica que no reporta condiciones de carrera

**Parte 6 — Análisis Comparativo de Estrategias**

Redacta un análisis de una página comparando las 3 estrategias de integración en el contexto del bus: ¿cuál era la más adecuada para este sistema? ¿Por qué? ¿Qué inconvenientes encontraste con la estrategia que elegiste?

| Entregables src/objects/tree.c \+ src/server/dispatcher.c \+ src/server/object\_server.c tests/unit/test\_tree.c tests/integration/test\_dispatcher.c \+ test\_object\_server.c \+ test\_concurrency.c tests/integration/stubs/ — Stubs de socket implementados docs/etapa3/plan\_integracion.pdf — Plan \+ comparación de estrategias docs/etapa3/informe\_integracion.pdf — Resultados \+ defectos encontrados GitHub Issues — Todos los defectos de integración registrados |
| :---- |

| ETAPA 4 — Pruebas de Sistema: Bus TCP Completo con pthreads Semanas 7 a 8 | Tipo de prueba: Pruebas de Sistema / No Funcionales / Rendimiento |
| :---- |

## **Objetivos de Aprendizaje en Pruebas**

* Verificar que el sistema completo cumple con los requisitos funcionales definidos en la Etapa 1

* Ejecutar pruebas funcionales end-to-end a través del bus TCP

* Aplicar pruebas de robustez del protocolo (mensajes malformados, errores de red)

* Medir el rendimiento del bus bajo carga concurrente

* Actualizar la matriz de trazabilidad con los resultados reales de ejecución

## **Descripción del Trabajo**

**Parte 1 — Implementación del Bus Server y Client**

* bus\_server.c: acepta múltiples conexiones TCP con pthread\_create() por cliente. Maneja desconexión abrupta sin crash. Usa el dispatcher para procesar mensajes

* bus\_client.c: implementa todas las funciones de client\_api.h. Serializa solicitudes y deserializa respuestas usando serializer.c

**Parte 2 — Pruebas Funcionales End-to-End (≥4 flujos completos)**

* Flujo 1 — List completo: create → insert×5 → get×5 (verificar valores) → remove×2 → size (verificar \= 3\)

* Flujo 2 — Stack LIFO: create → push(10,20,30) → pop×3 (verificar orden: 30,20,10)

* Flujo 3 — Tree BST: create → insert(5,3,8,1,4) → search(4)=TRUE → search(9)=FALSE → inorder \= '1,3,4,5,8'

* Flujo 4 — Multi-instancia: crear List1, List2 y Stack1. Insertar 10 en List1, 20 en List2. Verificar aislamiento: get(List1,0)=10 y get(List2,0)=20

**Parte 3 — Pruebas de Protocolo y Robustez**

Verifica la respuesta ERROR del servidor ante cada uno de estos casos (el servidor NUNCA debe crashear):

* Mensaje sin separadores (sin el carácter '|')

* Tipo de objeto inválido (QUEUE|CREATE|0|)

* ID de instancia que no existe (LIST|GET|999|0)

* Operación sobre estructura vacía (STACK|POP|1| con pila vacía)

* Índice fuera de rango (LIST|GET|1|100 en lista de 3 elementos)

**Parte 4 — Pruebas de Rendimiento Bajo Carga**

Escribe benchmark.c que mida la latencia round-trip con 1, 5 y 10 clientes simultáneos:

* 1000 operaciones INSERT por cliente

* Reporta: latencia promedio, mínima, máxima y percentil 95 en microsegundos

* Analiza: ¿aumenta la latencia con más clientes? ¿se observa degradación lineal o exponencial?

**Parte 5 — Actualización de la Matriz de Trazabilidad**

Actualiza la matriz de la Etapa 1 marcando cada RF como: Verificado (prueba pasó), Fallido (prueba falló — defecto registrado) o No probado (justifica por qué).

| Entregables src/server/bus\_server.c (pthreads) \+ src/client/bus\_client.c \+ client\_api.h src/client/test\_client.c (modo interactivo para UAT) tests/system/test\_bus\_system.c (4 flujos end-to-end) tests/system/test\_protocol.c (5 casos de error del protocolo) tests/system/benchmark.c (3 niveles de carga) docs/etapa4/informe\_sistema.pdf — Resultados \+ matriz actualizada \+ defectos |
| :---- |

| ETAPA 5 — Regresión y Automatización Semanas 9 a 10 | Tipo de prueba: Pruebas de Regresión / Automatización / CI-CD |
| :---- |

## **Objetivos de Aprendizaje en Pruebas**

* Construir y mantener una suite de regresión automatizada para un sistema concurrente

* Implementar un pipeline CI/CD que detecte regresiones automáticamente ante cada cambio

* Demostrar que la suite detecta una regresión introducida deliberadamente

* Definir criterios para seleccionar qué pruebas automatizar en sistemas con componentes no determinísticos (red, hilos)

## **Descripción del Trabajo**

**Parte 1 — Suite de Regresión Consolidada**

Crea tests/test\_regresion.c que sea la suite maestra. Debe incluir:

* Las pruebas más críticas de List, Stack, Tree (≥5 por objeto)

* Pruebas críticas del Serializer (≥4: mensajes válidos, inválidos, round-trip)

* Pruebas críticas del Dispatcher (≥4: un objeto \+ error de ID \+ mensaje inválido)

* ≥2 pruebas de concurrencia de object\_server (usando stubs, sin servidor TCP)

* Ejecutable con make regresion. Imprime al final: 'N pruebas ejecutadas, M fallidas'

**Parte 2 — Pipeline CI/CD Completo**

Actualiza .github/workflows/ci.yml para que ejecute en este orden exacto:

12. Compilar con \-Werror (falla ante cualquier warning)

13. Ejecutar la suite de regresión completa

14. Ejecutar test\_concurrency (pruebas de hilos)

15. Generar reporte de cobertura y publicarlo como artefacto en GitHub Actions

16. Ejecutar Valgrind sobre la suite de regresión

**Parte 3 — Demostración de Detección de Regresión**

Elige uno de los siguientes cambios deliberados y documenta el ciclo completo con capturas de pantalla:

* Cambio A: Elimina pthread\_mutex\_lock en object\_server\_create(). Las pruebas de concurrencia deben detectar IDs duplicados

* Cambio B: Cambia el separador del serializer de '|' a ':'. Las pruebas de deserialización deben fallar

* Cambio C: Hace que stack\_pop() retorne siempre 0\. Las pruebas de Stack LIFO deben detectar el error

Ciclo completo a documentar: (1) introduce el cambio, (2) haz push al repositorio, (3) captura el pipeline fallando en GitHub Actions, (4) identifica qué prueba específica detectó la regresión, (5) revierte el cambio, (6) verifica que el pipeline vuelve a pasar.

**Parte 4 — Criterios de Selección de Pruebas a Automatizar**

Documenta los criterios que usaste. Los criterios deben abordar:

* Frecuencia de ejecución: ¿en cada commit o solo en releases?

* Estabilidad: ¿la prueba es determinística o puede fallar aleatoriamente? (las pruebas de red son no determinísticas)

* Costo-beneficio: ¿el tiempo de automatización vale el riesgo que cubre?

* Pruebas excluidas: ¿qué pruebas decidiste no automatizar? ¿por qué? (ej: pruebas que requieren el servidor TCP activo)

| Entregables tests/test\_regresion.c \+ Makefile actualizado con target regresion .github/workflows/ci.yml actualizado con todos los pasos docs/etapa5/informe\_automatizacion.pdf — Criterios \+ ciclo de demostración \+ capturas del pipeline |
| :---- |

| ETAPA 6 — Pruebas de Aceptación y Cierre del Proyecto Semanas 11 a 12 | Tipo de prueba: Pruebas de Aceptación / UAT / Informe de Calidad |
| :---- |

## **Objetivos de Aprendizaje en Pruebas**

* Preparar y ejecutar pruebas de aceptación con usuarios externos al equipo

* Consolidar las métricas de calidad del proyecto completo

* Reflexionar sobre el proceso de pruebas en un sistema distribuido y concurrente

* Comunicar resultados de calidad de forma oral con demostración en vivo

## **Descripción del Trabajo**

**Parte 1 — Preparación del Entorno UAT**

* test\_client debe funcionar en modo interactivo: el usuario puede ingresar comandos del protocolo o usar un menú simple

* Prepara datos precargados: script que inicia el servidor y crea instancias de prueba automáticamente

* Guión de pruebas de aceptación: lista de 8-10 tareas que el usuario simulado debe ejecutar

**Parte 2 — Criterios de Aceptación**

Define criterios binarios (pasa/no pasa) para cada funcionalidad principal:

| Funcionalidad | Criterio de aceptación | Resultado |
| ----- | ----- | ----- |
| Crear objeto remoto | CREATE retorna un ID numérico en \<200ms | Pendiente |
| Insertar en lista | insert×3 \+ get×3 retorna valores en orden de inserción | Pendiente |
| Pila LIFO | push(1,2,3) \+ pop×3 retorna 3,2,1 (LIFO correcto) | Pendiente |
| Árbol búsqueda | search de valor insertado \= TRUE; no insertado \= FALSE | Pendiente |
| Múltiples instancias | List1 y List2 operan de forma completamente aislada | Pendiente |
| Robustez protocolo | Mensaje malformado retorna ERROR sin crashear el servidor | Pendiente |
| Concurrencia básica | 2 clientes simultáneos reciben respuestas correctas sin interferencia | Pendiente |

**Parte 3 — Ejecución del UAT con Usuarios Simulados**

Coordina con ≥2 integrantes de otro equipo para actuar como usuarios simulados. El proceso:

17. El usuario simulado ejecuta el guión de tareas usando test\_client

18. Tu equipo observa sin intervenir y registra incidencias

19. El usuario registra si cada criterio pasa o no, y anota feedback libre

20. Al finalizar: firma el acta de UAT con los resultados

**Parte 4 — Informe Final de Calidad**

21. Resumen ejecutivo (1 página): estado final del sistema

22. Métricas por módulo: líneas de código, número de pruebas, defectos encontrados/resueltos, cobertura

23. Evolución de defectos por etapa: tabla o gráfico con tendencia

24. Análisis del diseño concurrente: ¿las secciones críticas identificadas en Etapa 1 eran correctas? ¿encontraron alguna que no habían previsto?

25. Resultados UAT: tabla de criterios con resultado final

26. Lecciones aprendidas: ≥5 reflexiones concretas sobre el proceso de pruebas en sistemas distribuidos y concurrentes

27. Trabajo pendiente: defectos no resueltos con justificación

**Parte 5 — Presentación Oral (15 minutos)**

* Demo en vivo: iniciar el servidor y conectar ≥2 clientes simultáneamente en terminales separadas

* Ejecución del pipeline CI/CD en vivo y mostrar el reporte de cobertura en el navegador

* Presentar las métricas de calidad finales

* Reflexionar sobre el mayor desafío de pruebas encontrado durante el semestre

| Entregables finales docs/etapa6/plan\_uat.pdf — Plan con criterios y guión de pruebas docs/etapa6/acta\_uat.pdf — Acta firmada por ≥2 usuarios simulados docs/etapa6/informe\_final\_calidad.pdf — Informe completo con métricas y lecciones README.md con instrucciones completas de compilación y ejecución Sistema compilable y ejecutable con 0 warnings y 0 fugas Valgrind |
| :---- |

# **Checklist Final del Proyecto**

Verifica que tu repositorio tenga todos los elementos antes de la presentación:

| Elemento | Etapa | ¿Listo? |
| ----- | ----- | ----- |
| ≥20 RF \+ ≥5 RNF con métricas | 1 | ☐ |
| Protocolo completo con tabla de operaciones y 7+ códigos de error | 1 | ☐ |
| Análisis de ≥3 secciones críticas con mutex propuesto | 1 | ☐ |
| Walkthrough con ≥5 defectos documentados y corregidos | 1 | ☐ |
| Matriz de trazabilidad con 100% de RF cubiertos | 1 | ☐ |
| list.c \+ stack.c compilando sin warnings ni errores | 2 | ☐ |
| serializer.c usando strtok\_r (thread-safe) | 2 | ☐ |
| Cobertura ≥70% en los 3 módulos (reporte lcov) | 2 | ☐ |
| Evidencia de TDD en historial de commits | 2 | ☐ |
| Valgrind 0 fugas en todos los módulos unitarios | 2 | ☐ |
| tree.c con delete de dos hijos (sucesor inorden) | 3 | ☐ |
| object\_server.c con mutex en todas las secciones críticas | 3 | ☐ |
| Plan de integración con estrategia justificada | 3 | ☐ |
| Stubs de socket implementados | 3 | ☐ |
| test\_concurrency.c con ≥10 hilos \+ Helgrind limpio | 3 | ☐ |
| Análisis comparativo de estrategias de integración | 3 | ☐ |
| bus\_server.c con pthread\_create/detach por cliente | 4 | ☐ |
| bus\_client.c \+ client\_api.h completos | 4 | ☐ |
| 4 flujos end-to-end ejecutados y verificados | 4 | ☐ |
| 5 casos de error del protocolo verificados | 4 | ☐ |
| Benchmark con 3 niveles de carga documentado | 4 | ☐ |
| Matriz de trazabilidad actualizada con resultados reales | 4 | ☐ |
| Suite de regresión ejecutable con make regresion | 5 | ☐ |
| Pipeline CI/CD completo y funcionando (5 pasos) | 5 | ☐ |
| Demostración de regresión con capturas del pipeline | 5 | ☐ |
| Criterios de selección de pruebas documentados | 5 | ☐ |
| Acta UAT firmada por ≥2 usuarios externos | 6 | ☐ |
| Informe final con análisis de concurrencia \+ métricas | 6 | ☐ |
| Demo en vivo con ≥2 clientes simultáneos preparada | 6 | ☐ |
| README con instrucciones completas | Todas | ☐ |
| Todos los defectos en GitHub Issues con formato correcto | Todas | ☐ |
| Rotación de roles documentada en cada entregable | Todas | ☐ |

