

**RÚBRICAS DE EVALUACIÓN**

**Proyecto Semestral — Bus de Objetos en C**

Curso: Pruebas de Software | pthreads \+ TCP/IP \+ Serialización

Cada etapa tiene un puntaje máximo de 100 puntos. La evaluación se realiza sobre los entregables subidos al repositorio GitHub al cierre de cada etapa. El docente verificará: el historial de commits, el reporte de CI/CD, los archivos de prueba, el reporte de cobertura y los documentos de la etapa.

# **Resumen de Etapas y Ponderación**

| Etapa | Sem. | Tipo de Prueba | Entregable principal | Peso |
| ----- | ----- | ----- | ----- | ----- |
| 1 | 1–2 | Estáticas / Requisitos | Requisitos \+ Protocolo \+ Secciones críticas \+ Walkthrough | 10% |
| 2 | 3–4 | Unitarias | list.c \+ stack.c \+ serializer.c \+ cobertura \+ TDD | 20% |
| 3 | 5–6 | Integración | tree.c \+ dispatcher \+ object\_server \+ stubs \+ concurrencia | 20% |
| 4 | 7–8 | Sistema | bus\_server.c \+ bus\_client.c \+ end-to-end \+ rendimiento | 20% |
| 5 | 9–10 | Regresión / Automatización | Suite regresión \+ CI/CD \+ demo fallo \+ criterios | 20% |
| 6 | 11–12 | Aceptación / UAT | Plan UAT \+ acta \+ informe final \+ presentación | 10% |

# **Etapa 1: Pruebas Estáticas y Revisión de Requisitos (Sem. 1–2)**

Entregable: Documento de requisitos \+ Especificación del protocolo \+ Análisis de secciones críticas \+ Informe de walkthrough

| Criterio de Evaluación | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0%) | Pts. |
| ----- | ----- | ----- | ----- | ----- | :---: |
| **Requisitos funcionales del bus** | ≥20 RF con ID, descripción, precondición, postcondición y flujo alternativo. Cubre todas las operaciones de List, Stack y Tree más gestión de instancias y errores del servidor | 15-19 RF completos, mayoría de operaciones cubiertas | 10-14 RF básicos sin flujos alternativos | \<10 RF o sin estructura definida | **15 pts** |
| **Especificación formal del protocolo** | Protocolo completo: formato EBNF o tabla, TODAS las operaciones de los 3 objetos, 9 códigos de error documentados con condición que los activa, ejemplos de sesión comentados | Protocolo con 2 objetos completos, 6-8 códigos de error | Solo formato del mensaje sin tabla de operaciones | Sin especificación de protocolo | **20 pts** |
| **Requisitos no funcionales verificables** | ≥5 RNF con métricas concretas: latencia máxima por operación, máx. conexiones simultáneas, comportamiento ante cliente que corta abruptamente, consumo de memoria | 3-4 RNF con métricas parciales | 1-2 RNF genéricos no verificables | Sin RNF o no verificables | **15 pts** |
| **Análisis de secciones críticas (concurrencia)** | Identifica ≥3 secciones críticas del servidor con datos compartidos, justifica por qué son críticas y propone mecanismo de sincronización (mutex) para cada una | Identifica 2 secciones críticas con justificación parcial | Menciona la concurrencia sin identificar secciones concretas | Sin análisis de concurrencia | **20 pts** |
| **Matriz de trazabilidad RF → casos de prueba** | 100% de RF relacionados con al menos un caso de prueba planificado, indicando tipo de prueba (unitaria, integración, sistema) | 80-99% de RF cubiertos en la matriz | 50-79% de RF cubiertos | \<50% o matriz ausente | **15 pts** |
| **Informe de revisión estática (walkthrough)** | ≥5 defectos documentados en requisitos o protocolo (ambigüedades, inconsistencias, casos no cubiertos) con propuesta de corrección para cada uno | 3-4 defectos con documentación básica | 1-2 defectos superficiales | Sin walkthrough o vacío | **15 pts** |

| PUNTAJE TOTAL DE LA ETAPA | 100 pts |
| ----: | :---: |

# **Etapa 2: Pruebas Unitarias: List, Stack y Serializer (Sem 3–64**

Entregable: list.c \+ stack.c \+ serializer.c \+ suites con Unity \+ reporte de cobertura gcov/lcov

| Criterio de Evaluación | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0%) | Pts. |
| ----- | ----- | ----- | ----- | ----- | :---: |
| **Calidad y cantidad de casos de prueba (≥5 por función)** | Cubre clase válida, clase inválida, valores límite inferior y superior, punteros NULL y mensajes malformados (serializer). Nombres descriptivos en cada test | 3-4 pruebas por función, mayoría de clases cubiertas | 2 pruebas por función, solo casos válidos | \<2 pruebas por función o pruebas triviales | **25 pts** |
| **Aplicación de partición equivalencia y valores límite** | Todas las clases de equivalencia identificadas explícitamente en el informe y casos de prueba para cada clase y valor límite (0, 1, MAX, MAX-1, \-1) | Mayoría de clases identificadas, algunos valores límite | Solo clases válidas, sin valores límite | Sin evidencia de técnicas aplicadas | **20 pts** |
| **Cobertura de código (gcov/lcov)** | Cobertura de líneas ≥90% y ramas ≥80% en list.c, stack.c y serializer.c. Reporte HTML generado | Cobertura de líneas 75-89% | Cobertura de líneas 50-74% | \<50% o sin reporte de cobertura | **20 pts** |
| **TDD en al menos un módulo** | Historial de commits evidencia ciclo Red-Green-Refactor completo para list.c, stack.c o serializer.c. Commits con mensajes '\[etapa-2\] test: ...' antes de '\[etapa-2\] feat: ...' | Evidencia parcial de TDD en al menos 3 funciones | Menciona TDD sin evidencia en commits | Sin aplicación de TDD | **20 pts** |
| **Corrección e implementación thread-safe** | Compila sin warnings con \-Wall \-Wextra. serializer.c usa strtok\_r (no strtok). Valgrind 0 fugas y 0 errores. Todas las pruebas pasan en CI/CD | Compila con 1-2 warnings. Valgrind limpio | Compila con varios warnings. Algunas pruebas fallan | No compila o mayoría de pruebas fallan | **15 pts** |

| PUNTAJE TOTAL DE LA ETAPA | 100 pts |
| ----: | :---: |

# **Etapa 3: Pruebas de Integración: Tree \+ Dispatcher \+ Object Server (Sem 5–6)**

Entregable: tree.c \+ dispatcher.c \+ object\_server.c (thread-safe) \+ plan de integración \+ stubs/drivers \+ defectos

| Criterio de Evaluación | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0%) | Pts. |
| ----- | ----- | ----- | ----- | ----- | :---: |
| **Plan de integración documentado** | Documenta estrategia elegida (Top-Down, Bottom-Up o Big Bang), justificación técnica, orden de integración con diagrama de dependencias, stubs y drivers necesarios | Plan con estrategia y orden parcial, stubs mencionados | Plan básico sin justificación ni diagrama | Sin plan de integración | **20 pts** |
| **Implementación de stubs y drivers** | Stubs de socket implementados para probar dispatcher sin red. Drivers para invocar object\_server sin dispatcher. Bien documentados y determinísticos | Stubs básicos implementados con comportamiento parcial | Stubs triviales que no simulan comportamiento real | Sin stubs ni drivers | **15 pts** |
| **Casos de prueba de integración por interfaz** | ≥3 casos por interfaz: Serializer↔Dispatcher, Dispatcher↔ObjectServer, Dispatcher↔List/Stack/Tree. Incluye casos de error (ID inexistente, estructura vacía) | 2 casos por interfaz principal | 1 caso por interfaz, sin casos de error | Sin pruebas de integración reales | **25 pts** |
| **Object Server thread-safe y prueba de concurrencia** | Mutex protege todas las secciones críticas identificadas en Etapa 1\. test\_concurrency.c con ≥10 hilos verifica IDs únicos y ausencia de corrupción. Helgrind limpio | Mutex presente, 1 sección crítica desprotegida. 5 hilos en prueba | Mutex declarado pero no todas las secciones protegidas | Sin mutex o sin prueba de concurrencia | **25 pts** |
| **Análisis comparativo de estrategias \+ defectos** | Compara Top-Down, Bottom-Up y Big Bang en el contexto del bus. Todos los defectos de integración en GitHub Issues con severidad, pasos y estado | Compara 2 estrategias con argumentos parciales, defectos básicos registrados | Menciona estrategias sin análisis. Algunos defectos registrados | Sin análisis comparativo ni registro de defectos | **15 pts** |

| PUNTAJE TOTAL DE LA ETAPA | 100 pts |
| ----: | :---: |

# **Etapa 4: Pruebas de Sistema: Bus TCP Completo con pthreads (Sem 7–8)**

Entregable: bus\_server.c \+ bus\_client.c \+ pruebas funcionales end-to-end \+ pruebas de protocolo \+ rendimiento \+ matriz de trazabilidad actualizada

| Criterio de Evaluación | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0%) | Pts. |
| ----- | ----- | ----- | ----- | ----- | :---: |
| **Cobertura de requisitos (matriz de trazabilidad)** | 100% de los RF verificados con al menos un caso de prueba ejecutado. Matriz de Etapa 1 actualizada: Verificado / Fallido / No probado (justificado) | 80-99% de RF verificados en la matriz | 50-79% de RF cubiertos | \<50% o sin actualizar la matriz | **20 pts** |
| **Pruebas funcionales end-to-end (≥4 flujos)** | Flujos completos: List (create→insert×5→get×5→remove→size), Stack LIFO (push×3→pop×3 verifica orden), Tree BST (insert×5→search→inorder), Multi-instancia (2 listas con valores aislados) | 3 flujos completos ejecutados correctamente | 1-2 flujos completos | Sin pruebas end-to-end o no conectan al servidor | **25 pts** |
| **Pruebas de protocolo y seguridad básica** | Verifica respuesta ERROR ante: mensaje malformado, objeto inválido, ID inexistente, estructura vacía, índice fuera de rango. El servidor nunca crashea ante estas entradas | Verifica 4 de los 5 casos de error | Verifica 2-3 casos de error | Sin pruebas de protocolo o servidor crashea | **20 pts** |
| **Pruebas de rendimiento y concurrencia en sistema** | Benchmark mide latencia round-trip con 1, 5 y 10 clientes simultáneos. Reporta mínimo/máximo/promedio. Analiza degradación bajo carga concurrente | Benchmark con 1 cliente, análisis parcial | Solo tiempo total sin análisis | Sin pruebas de rendimiento | **20 pts** |
| **Reporte de resultados y defectos** | Reporte con % pruebas exitosas/fallidas, densidad de defectos por módulo y plan de corrección priorizado. Defectos en GitHub Issues | Reporte con resultados parciales y lista básica de defectos | Solo resultados globales sin análisis | Sin reporte o vacío | **15 pts** |

| PUNTAJE TOTAL DE LA ETAPA | 100 pts |
| ----: | :---: |

# **Etapa 5: Regresión y Automatización (Sem 9–10)**

Entregable: Suite de regresión \+ Pipeline CI/CD completo \+ Demostración de detección \+ Criterios de selección documentados

| Criterio de Evaluación | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0%) | Pts. |
| ----- | ----- | ----- | ----- | ----- | :---: |
| **Suite de pruebas de regresión automatizada** | Cubre ≥80% de funcionalidades críticas (List, Stack, Tree, Serializer, Dispatcher, concurrencia básica). make regresion ejecuta todo sin intervención. Imprime resumen de resultados | 60-79% de funcionalidades, ejecutable automáticamente | \<60%, ejecución manual | Suite ausente o no ejecutable | **30 pts** |
| **Pipeline CI/CD completo** | Compila con \-Werror, ejecuta regresión, test\_concurrency, genera cobertura y ejecuta Valgrind. Falla correctamente en cada paso ante error. Badge de estado en README | Compila y ejecuta regresión, sin cobertura ni Valgrind | Solo compilación en CI/CD | Sin pipeline configurado | **25 pts** |
| **Demostración de detección de regresión** | Introduce cambio deliberado (mutex eliminado, serializer roto o stack\_pop devuelve basura), hace push, captura fallo del pipeline con evidencia, revierte y documenta todo el ciclo completo | Introduce cambio y documenta fallo, capturas básicas | Describe el cambio sin demostración real | Sin demostración | **25 pts** |
| **Criterios de selección de pruebas a automatizar** | Documenta para cada componente: frecuencia de ejecución, estabilidad (determinismo), costo-beneficio y justificación de pruebas excluidas. Incluye análisis de qué pruebas de red son no determinísticas | Criterios documentados para mayoría de componentes | Lista de pruebas sin criterios explícitos | Sin criterios documentados | **20 pts** |

| PUNTAJE TOTAL DE LA ETAPA | 100 pts |
| ----: | :---: |

# **Etapa 6: Pruebas de Aceptación y Cierre (Sem 11–12)**

Entregable: Plan UAT \+ Acta con usuarios simulados \+ Informe final de calidad \+ Presentación oral con demo en vivo

| Criterio de Evaluación | Excelente (100%) | Bueno (75%) | Suficiente (50%) | Insuficiente (0%) | Pts. |
| ----- | ----- | ----- | ----- | ----- | :---: |
| **Plan de pruebas de aceptación (UAT)** | Criterios binarios (pasa/no pasa) para todas las operaciones remotas \+ criterios de concurrencia (2 clientes simultáneos). Guión detallado para usuarios simulados. Datos precargados | Criterios para mayoría de operaciones, 1 criterio de concurrencia, guión básico | Criterios genéricos sin guión ni datos de prueba | Sin plan UAT | **20 pts** |
| **Ejecución UAT con usuarios simulados** | ≥2 usuarios externos al equipo ejecutan test\_client interactivo con el guión. Acta firmada con resultado por criterio y feedback libre documentado | 1 usuario externo, acta básica | Pruebas ejecutadas por el propio equipo | Sin UAT ejecutado | **20 pts** |
| **Informe final de calidad** | Densidad de defectos por módulo, cobertura total alcanzada, % defectos resueltos por etapa, resultados UAT, análisis del diseño concurrente (¿las secciones críticas identificadas en Etapa 1 eran correctas?), tendencia de defectos | Mayoría de métricas con análisis parcial de concurrencia | Resumen de defectos sin métricas de calidad | Sin informe o vacío | **25 pts** |
| **Lecciones aprendidas** | ≥5 lecciones concretas y accionables sobre el proceso de pruebas en sistemas distribuidos concurrentes, con reflexión sobre errores cometidos | 3-4 lecciones con reflexión parcial | 1-2 lecciones genéricas | Sin lecciones aprendidas | **15 pts** |
| **Presentación oral con demo en vivo** | Demo: ≥2 clientes simultáneos conectados al servidor. Ejecución del pipeline. Métricas de calidad. Responde preguntas técnicas sobre mutex, protocolo y pruebas. Tiempo respetado | Demo con 1 cliente, pipeline ejecutado, algunas dudas al responder | Presentación básica sin concurrencia visible en demo | Sin demo en vivo o sistema no corre | **20 pts** |

| PUNTAJE TOTAL DE LA ETAPA | 100 pts |
| ----: | :---: |

# **Escala de Notas**

| Puntaje obtenido | Porcentaje | Nota |
| ----- | ----- | ----- |
| 90–100 pts | 90-100% | 7.0 |
| 80–89 pts | 80-89% | 6.0 |
| 70–79 pts | 70-79% | 5.0 |
| 60–69 pts | 60-69% | 4.0 |
| 50–59 pts | 50-59% | 3.5 |
| 0–49 pts | 0-49% | 2.0 (Reprobado) |

