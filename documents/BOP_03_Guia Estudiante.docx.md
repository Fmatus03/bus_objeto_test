**GUÍA DEL ESTUDIANTE**

**Proyecto Semestral — Bus de Objetos en C**

Curso: Pruebas de Software

| Bienvenido al proyecto semestral Este documento contiene todo lo que necesitas saber para desarrollar el proyecto exitosamente: descripción general, calendario de entregas, herramientas, normas de trabajo en equipo y criterios de evaluación resumidos. Léelo completamente antes de comenzar.  El objetivo principal del proyecto NO es solo construir el Bus de Objetos, es aprender a aplicar los tipos de pruebas de software sobre un sistema distribuido y concurrente. El sistema es el vehículo; las pruebas son el aprendizaje. |
| :---- |

# **1\. Descripción General**

A lo largo del semestre construirás, junto a tu equipo, un Bus de Objetos en C con una arquitectura cliente-servidor donde un cliente invoca operaciones remotas sobre listas enlazadas, pilas y árboles binarios que residen en un servidor TCP. El servidor atiende múltiples clientes simultáneamente usando pthreads (POSIX Threads): biblioteca estándar (IEEE POSIX 1003.1c) para C/C++ que permite la programación paralela mediante hilos (threads) en sistemas tipo UNIX (Linux, macOS, etc.) y ejecutar múltiples flujos de trabajo simultáneos en memoria compartida, utilizando funciones como pthread\_create (crear hilo) y pthread\_join sincronizar). La comunicación sigue un protocolo de texto estructurado diseñado por el equipo en la Etapa 1\.

El desarrollo será en C/C++, porque ofrece las mejores características para escribir código que requiere mucha prueba para considerarlo *done*. C/C++ es un lenguaje permisivo por lo que se debe poner especial atención en la codificación. Los ambientes serán algún sabor de Linux

El proyecto se divide en 6 etapas de 2 semanas. En cada etapa agregarás nuevos componentes al sistema y aplicarás el tipo de prueba correspondiente a ese nivel. Al final del semestre tendrás un sistema funcionando, una suite completa de pruebas automatizadas, un pipeline CI/CD activo y un informe de calidad profesional.

## **1.1 Relación entre componentes y tipos de prueba**

| Etapa | Tipo de Prueba | Componente desarrollado | ¿Qué se aprende a probar? |
| ----- | ----- | ----- | ----- |
| 1 | Estáticas | (Solo documentación) | Revisión de requisitos, inspección de protocolo, identificación de secciones críticas |
| 2 | Unitarias | List, Stack, Serializer | Partición de equivalencia, valores límite, cobertura de código, TDD |
| 3 | Integración | Tree, Dispatcher, Object Server | Estrategias Top-Down/Bottom-Up, stubs, drivers, interfaces entre módulos |
| 4 | Sistema | Bus Server, Bus Client | Pruebas end-to-end, protocolo, seguridad básica, rendimiento bajo carga |
| 5 | Regresión | Suite consolidada \+ CI/CD | Automatización, criterios de selección, detección de cambios |
| 6 | Aceptación | UAT con usuarios simulados | Criterios de aceptación, métricas de calidad, lecciones aprendidas |

## **1.2 Roles del equipo (rotación obligatoria cada etapa)**

| Rol | Responsabilidades | Rotación |
| ----- | ----- | ----- |
| Tester Líder | Diseña el plan y casos de pruebas. Supervisa la ejecución | Cambia c/etapa |
| Desarrollador | Implementa el código. Corrige defectos detectados | Cambia c/etapa |
| Documentador | Registra defectos en Issues. Redacta entregables | Cambia c/etapa |
| Integrador/DevOps | Gestiona Git, Makefile y pipeline CI/CD | Cambia c/etapa |

| Importante En cada entregable debes registrar quién ocupó cada rol.  El docente verificará que todos los integrantes hayan ejercido cada rol al menos una vez durante el semestre. |
| :---- |

# **2\. Calendario de Entregas**

Todas las entregas se realizan a través del repositorio GitHub del equipo. El plazo de cada etapa corresponde al último commit antes de las 23:59 del día indicado por el docente.

| Etapa | Semana | Tipo Prueba | Entregable principal | Peso |
| :---: | :---: | :---: | ----- | :---: |
| 1 | 1–2 | Estáticas | Requisitos \+ protocolo \+ secciones críticas \+ walkthrough | 10% |
| 2 | 3–4 | Unitarias | list.c \+ stack.c \+ serializer.c \+ suite Unity+cobertura ≥90% | 20% |
| 3 | 5–6 | Integración | tree.c \+ dispatcher \+ object\_server \+ plan integración \+ defectos | 20% |
| 4 | 7–8 | Sistema | bus\_server.c \+ bus\_client.c \+ 4 flujos end-to-end \+ rendimiento | 20% |
| 5 | 9–10 | Regresión | Suite regresión \+ pipeline CI/CD \+ demostración de regresión | 20% |
| 6 | 11–12 | Aceptación | Acta UAT \+ informe final calidad \+ presentación con demo en vivo | 10% |

| Política de atrasos Hasta 48h de atraso: penalización del 20% del puntaje de la etapa. Más de 48h: nota mínima (2.0). En casos de fuerza mayor, contacta al docente ANTES del plazo, no después. |
| :---- |

# **3\. Herramientas e Instalación**

| Herramienta | Propósito | Costo |
| ----- | ----- | ----- |
| VirtualBox \+ Linux (algún sabor) | SO para el desarrollo | Gratis |
| GCC (MinGW en Windows) | Compilador C con soporte \-pthread y \--coverage | Gratis |
| VS Code \+ extensión C/C++ | Editor de código | Gratis |
| Unity Test Framework | Pruebas unitarias en C (solo 3 archivos) | Open Source |
| gcov \+ lcov | Cobertura de código | Incluido con GCC |
| Valgrind \+ Helgrind | Fugas de memoria y condiciones de carrera | Gratis (Linux/Mac) |
| Netcat (nc) | Probar el servidor manualmente con el protocolo | Incluido en Linux/Mac |
| Git \+ GitHub \+ GitHub Actions | Control de versiones y CI/CD | Gratis |
| Google Docs / Sheets | Documentación | Gratis |

**Instalación de VirtualVox y Linux**

En la estación con Windows 10 u 11 instalar VBox y luego descargar la imagen ISO del Linux de preferencia.

**Instalación en Linux (Ubuntu/Debian)**

sudo apt update && sudo apt install \-y gcc make lcov valgrind netcat-openbsd git

**Instalar Unity Test Framework**

* git clone https://github.com/ThrowTheSwitch/Unity.git

* Copia unity.c, unity.h y unity\_internals.h a la carpeta tests/unity/ de tu proyecto

| Tip: prueba el servidor con netcat ANTES de escribir el cliente C \# Terminal 1: iniciar el servidor ./build/bus\_server 8080  \# Terminal 2: conectar y probar el protocolo manualmente nc 127.0.0.1 8080 LIST|CREATE|0|          → Servidor responde: OK|1 LIST|INSERT|1|42        → Servidor responde: OK| LIST|GET|1|0            → Servidor responde: OK|42 QUEUE|CREATE|0|         → Servidor responde: ERROR|INVALID\_OBJECT  Esto es exactamente lo que harás en las pruebas de protocolo de la Etapa 4\. |
| :---- |

# **4\. Flujo de Trabajo en Equipo**

## **4.1 Proceso recomendado para cada etapa**

| Semana de la etapa | Actividad recomendada |
| ----- | ----- |
| Semana 1 | Leer el enunciado, distribuir tareas, diseñar los casos de prueba ANTES de codificar |
| Semana 2 | Desarrollar el código y las pruebas en paralelo, ejecutar y corregir defectos Revisar cobertura, completar documentación, commit final antes del plazo |

## **4.2 Convenciones de Git**

* \[etapa-2\] test: agrega test\_list\_get\_fuera\_de\_rango — ROJO (TDD)

* \[etapa-2\] feat: implementa list\_get con validación de rango — VERDE

* \[etapa-3\] fix:  corrige deadlock en dispatcher al ID no existir

* \[etapa-4\] test: agrega prueba de protocolo con mensaje malformado

* \[etapa-5\] ci:   agrega step de Helgrind al pipeline

## **4.3 Gestión de Defectos en GitHub Issues**

Todo defecto encontrado desde la Etapa 2 se registra con:

* Labels obligatorios: bug, etapa-N, severidad-alta/media/baja, tipo-unitaria/integración/sistema

* Para bugs de concurrencia: agrega también el label concurrency

* Cuerpo: pasos para reproducir (exactos), resultado esperado y resultado obtenido

* Estado: Open al detectar, Closed al verificar que la corrección funciona

# **5\. Evaluación y Nota Final**

## **5.1 Fórmula de la nota final del proyecto**

Nota Final=(E1×0.10)+(E2×0.20)+(E3×0.20)+(E4×0.20)+(E5×0.20)+(E6×0.10)

## **5.2 Lo que el profe revisará en cada entregable**

* Repositorio GitHub con código fuente y pruebas actualizado

* Pipeline CI/CD ejecutándose sin errores (desde Etapa 2\)

* Reporte de cobertura de código (desde Etapa 2\)

* Defectos registrados en GitHub Issues con formato correcto

* Documento de entrega con el contenido del enunciado de la etapa

* Rotación de roles documentada en el encabezado del entregable

| Criterios de aprobación del proyecto Promedio ponderado ≥ 4.0 en las 6 etapas. Ninguna etapa puede tener nota inferior a 2.0 (refleja entregable no realizado). El plagio o copia entre equipos implica nota mínima en la etapa para todos los involucrados. |
| :---- |

# **6\. Glosario de Términos Esenciales**

| Término | Definición |
| ----- | ----- |
| Bus de Objetos | Middleware que permite a un cliente invocar operaciones sobre objetos que residen en otro proceso. El cliente no accede directamente a la memoria del servidor |
| Serialización | Convertir datos en memoria (struct C) en una cadena de texto para transmitir por el socket. La deserialización hace el proceso inverso |
| Sección crítica | Fragmento de código que accede a datos compartidos entre hilos. Debe estar protegido por un mutex para evitar condiciones de carrera |
| Condición de carrera | Error cuando dos hilos acceden simultáneamente a los mismos datos sin protección, produciendo resultados impredecibles |
| Mutex | Mecanismo de sincronización que garantiza que solo un hilo ejecuta una sección crítica a la vez |
| Stub | Componente de prueba que simula el comportamiento de un módulo no disponible. En este proyecto: simula el socket TCP para probar el dispatcher sin red |
| Driver | Componente de prueba que invoca al módulo bajo prueba cuando el módulo que lo llama normalmente aún no está disponible |
| Partición de equivalencia | Técnica de diseño de pruebas que divide las entradas en clases donde el comportamiento se espera similar, reduciendo el número de casos necesarios |
| Valores límite | Técnica complementaria que prueba los valores exactos en el borde de las clases de equivalencia (0, 1, MAX-1, MAX, \-1) |
| Cobertura de código | Porcentaje de líneas o ramas del código ejecutadas por la suite de pruebas. Mide qué parte del código está siendo probada |
| TDD | Test-Driven Development: escribir la prueba ANTES que el código que la satisface, siguiendo el ciclo Rojo-Verde-Refactorizar |

