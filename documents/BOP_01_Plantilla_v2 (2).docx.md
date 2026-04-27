**PROYECTO SEMESTRAL**

**Bus de Objetos en C**

Base del Proyecto

Curso: Pruebas de Software  |  Lenguaje: C (C99/C11)

Objetos: List · Stack · Tree  |  Comunicación: Sockets TCP/IP \+ pthreads

Duración: 12 semanas  |  6 Etapas de 2 semanas

# **1\. Descripción General del Proyecto**

Este proyecto consiste en el desarrollo e implementación de pruebas de software sobre un Bus de Objetos: una arquitectura cliente-servidor donde un proceso Cliente invoca operaciones remotas sobre objetos (List, Stack, Tree) que residen en un proceso Servidor. La comunicación se realiza mediante sockets TCP/IP, el servidor atiende múltiples clientes simultáneamente con pthreads, y los mensajes siguen un protocolo de texto estructurado.

El objetivo principal del proyecto NO es solo construir el sistema, sino aprender a aplicar los diferentes tipos de pruebas de software sobre él. En cada etapa los estudiantes construirán nuevos componentes Y aplicarán el tipo de prueba correspondiente: estáticas, unitarias, integración, sistema, regresión y aceptación. Al final del semestre tendrán un sistema funcionando, una suite de pruebas completa y un informe de calidad profesional.

| Lo que hace especial este proyecto como plataforma de pruebas El Bus de Objetos es un sistema distribuido con tres capas de complejidad creciente: las estructuras de datos (List/Stack/Tree), el protocolo de comunicación (serializer \+ dispatcher) y la concurrencia (pthreads \+ mutex). Cada capa presenta desafíos de prueba distintos: pruebas de caja blanca para las estructuras, pruebas de protocolo para el serializer, pruebas de integración para el dispatcher y pruebas de concurrencia para el servidor. Este proyecto cubre el espectro completo de técnicas de prueba vistas en el curso. |
| :---- |

## **1.1 Estructura del Sistema y Relación con los Tipos de Prueba**

| Componente | Módulo | Tipo de prueba principal | Etapa |
| ----- | ----- | ----- | ----- |
| Lista enlazada doble | list.c / list.h | Unitaria — caja blanca y caja negra | 2 |
| Pila dinámica | stack.c / stack.h | Unitaria — partición equivalencia y valores límite | 2 |
| Serializer (protocolo) | serializer.c / serializer.h | Unitaria — pruebas de protocolo y mensajes malformados | 2 |
| Árbol BST | tree.c / tree.h | Unitaria \+ Integración | 3 |
| Object Server (thread-safe) | object\_server.c | Integración \+ Concurrencia | 3 |
| Dispatcher | dispatcher.c | Integración — interfaces entre módulos | 3 |
| Bus Server (pthreads) | bus\_server.c | Sistema — funcional, no funcional, concurrencia | 4 |
| Bus Client API | bus\_client.c / client\_api.h | Sistema — pruebas end-to-end | 4 |

## **1.2 Estructura de las 6 Etapas**

| Etapa | Semana | Tipo de Prueba | Componentes desarrollados | Ponder. |
| ----- | ----- | ----- | ----- | ----- |
| 1 | 1–2 | Pruebas Estáticas | Ninguno (solo documentación y revisión) | 10% |
| 2 | 3–4 | Pruebas Unitarias | list.c, stack.c, serializer.c | 20% |
| 3 | 5–6 | Pruebas de Integración | tree.c, dispatcher.c, object\_server.c | 20% |
| 4 | 7–8 | Pruebas de Sistema | bus\_server.c, bus\_client.c | 20% |
| 5 | 9–10 | Regresión y Automatización | Suite de regresión \+ CI/CD | 20% |
| 6 | 11–12 | Pruebas de Aceptación | UAT \+ Informe final de calidad | 10% |

## **1.3 Roles del Equipo (Rotación obligatoria cada etapa)**

| Rol | Responsabilidades |
| ----- | ----- |
| Tester Líder | Diseña el plan de pruebas y los casos de prueba de la etapa. Supervisa la ejecución y analiza los resultados |
| Desarrollador | Implementa el código fuente de los módulos de la etapa. Corrige los defectos detectados por las pruebas |
| Documentador | Registra todos los defectos en GitHub Issues. Redacta el documento de entregables de la etapa y mantiene la bitácora |
| Integrador / DevOps | Gestiona el repositorio Git, el Makefile y el pipeline de CI/CD. Verifica que el proyecto compila y las pruebas corren en CI |

# **2\. Protocolo de Mensajes**

El protocolo de comunicación entre cliente y servidor usa texto estructurado con el separador '|' y terminador '\\n'. Este diseño facilita enormemente las pruebas: cualquier herramienta de prueba puede enviar mensajes sin necesitar un cliente especial, y los mensajes son legibles por humanos para facilitar la depuración.

## **2.1 Formato General**

Solicitud (cliente → servidor):  OBJETO|OPERACION|ID\_INSTANCIA|DATO\\n  
Respuesta (servidor → cliente):  OK|DATO\\n   ó   ERROR|CODIGO\\n

## **2.2 Tabla Completa de Operaciones**

| Objeto | Operación | Dato enviado | Respuesta OK | Respuesta ERROR posible |
| ----- | ----- | ----- | ----- | ----- |
| LIST | CREATE | (vacío) | ID asignado | SERVER\_ERROR |
| LIST | INSERT | valor entero | (vacío) | INSTANCE\_NOT\_FOUND |
| LIST | GET | posición | valor en posición | OUT\_OF\_BOUNDS, INSTANCE\_NOT\_FOUND |
| LIST | REMOVE | posición | (vacío) | OUT\_OF\_BOUNDS, INSTANCE\_NOT\_FOUND |
| LIST | SIZE | (vacío) | Nro. de elementos | INSTANCE\_NOT\_FOUND |
| LIST | CONTAINS | valor | TRUE o FALSE | INSTANCE\_NOT\_FOUND |
| STACK | CREATE | (vacío) | ID asignado | SERVER\_ERROR |
| STACK | PUSH | valor entero | (vacío) | INSTANCE\_NOT\_FOUND |
| STACK | POP | (vacío) | valor extraído | EMPTY\_STRUCTURE |
| STACK | PEEK | (vacío) | valor del tope | EMPTY\_STRUCTURE |
| STACK | IS\_EMPTY | (vacío) | TRUE o FALSE | INSTANCE\_NOT\_FOUND |
| TREE | CREATE | (vacío) | ID asignado | SERVER\_ERROR |
| TREE | INSERT | valor entero | (vacío) | DUPLICATE\_VALUE |
| TREE | SEARCH | valor entero | TRUE o FALSE | INSTANCE\_NOT\_FOUND |
| TREE | DELETE | valor entero | (vacío) | NOT\_FOUND |
| TREE | INORDER | (vacío) | valores separados por coma | INSTANCE\_NOT\_FOUND |

## **2.3 Códigos de Error**

| Código | Condición que lo activa |
| ----- | ----- |
| INSTANCE\_NOT\_FOUND | El ID de instancia no existe en el servidor |
| EMPTY\_STRUCTURE | Operación sobre estructura vacía (pop/peek en pila vacía, get en lista vacía) |
| OUT\_OF\_BOUNDS | Índice fuera del rango válido \[0, size-1\] |
| DUPLICATE\_VALUE | Intento de insertar un valor ya existente en el árbol BST |
| NOT\_FOUND | Intento de eliminar un valor que no existe en el árbol |
| INVALID\_OBJECT | El tipo de objeto en el mensaje no es LIST, STACK ni TREE |
| INVALID\_OPERATION | La operación no está soportada por el tipo de objeto indicado |
| INVALID\_MESSAGE | El mensaje no tiene el formato correcto (campos faltantes, separadores incorrectos) |
| SERVER\_ERROR | Error interno del servidor (malloc fallido, mutex no inicializado, etc.) |

# **3\. Estructura del Proyecto**

## **3.1 Árbol de Carpetas**

bus-objetos/  
│  
├── src/  
│   ├── objects/                   \# Estructuras de datos (Etapa 2 y 3\)  
│   │   ├── list.c  / list.h  
│   │   ├── stack.c / stack.h  
│   │   └── tree.c  / tree.h  
│   ├── protocol/                  \# Capa de protocolo (Etapa 2\)  
│   │   ├── protocol.h             \# Constantes, enums y structs del protocolo  
│   │   └── serializer.c / serializer.h  
│   ├── server/                    \# Lógica del servidor (Etapa 3 y 4\)  
│   │   ├── dispatcher.c / dispatcher.h  
│   │   ├── object\_server.c / object\_server.h  \# Thread-safe con mutex  
│   │   └── bus\_server.c           \# Servidor TCP con pthreads  
│   └── client/                    \# API cliente (Etapa 4\)  
│       ├── bus\_client.c  
│       ├── client\_api.h  
│       └── test\_client.c          \# Cliente interactivo para UAT  
│  
├── tests/  
│   ├── unity/                     \# Framework Unity (3 archivos)  
│   ├── unit/                      \# Pruebas unitarias (Etapa 2\)  
│   │   ├── test\_list.c  
│   │   ├── test\_stack.c  
│   │   └── test\_serializer.c  
│   ├── integration/               \# Pruebas de integración (Etapa 3\)  
│   │   ├── test\_dispatcher.c  
│   │   ├── test\_object\_server.c  
│   │   └── test\_concurrency.c  
│   └── system/                    \# Pruebas de sistema (Etapa 4\)  
│       ├── test\_bus\_system.c  
│       ├── test\_protocol.c  
│       └── benchmark.c  
│  
├── build/                         \# Binarios compilados (ignorado por Git)  
├── reports/                       \# Reportes de cobertura lcov  
├── docs/                          \# Documentación por etapa  
│   ├── etapa1/ … etapa6/  
├── .github/workflows/ci.yml  
├── Makefile  
├── .gitignore  
└── README.md

## **3.2 Makefile**

CC     \= gcc  
CFLAGS \= \-Wall \-Wextra \-g \--coverage \-std=c99 \-pthread  
UNITY  \= tests/unity/unity.c  
OBJS   \= src/objects/list.c src/objects/stack.c src/objects/tree.c  
PROTO  \= src/protocol/serializer.c  
SRV    \= src/server/dispatcher.c src/server/object\_server.c

$(shell mkdir \-p build reports)

server:        ; $(CC) $(CFLAGS) $(OBJS) $(PROTO) $(SRV) src/server/bus\_server.c \-o build/bus\_server  
client:        ; $(CC) $(CFLAGS) $(PROTO) src/client/bus\_client.c src/client/test\_client.c \-o build/test\_client

test\_list:     ; $(CC) $(CFLAGS) $(UNITY) src/objects/list.c tests/unit/test\_list.c \-o build/test\_list && ./build/test\_list  
test\_stack:    ; $(CC) $(CFLAGS) $(UNITY) src/objects/stack.c tests/unit/test\_stack.c \-o build/test\_stack && ./build/test\_stack  
test\_serializer: ; $(CC) $(CFLAGS) $(UNITY) $(PROTO) tests/unit/test\_serializer.c \-o build/test\_serializer && ./build/test\_serializer  
test\_tree:     ; $(CC) $(CFLAGS) $(UNITY) src/objects/tree.c tests/unit/test\_tree.c \-o build/test\_tree && ./build/test\_tree  
test\_dispatcher: ; $(CC) $(CFLAGS) $(UNITY) $(OBJS) $(PROTO) $(SRV) tests/integration/test\_dispatcher.c \-o build/test\_dispatcher && ./build/test\_dispatcher  
test\_concurrency: ; $(CC) $(CFLAGS) $(UNITY) $(OBJS) $(PROTO) $(SRV) tests/integration/test\_concurrency.c \-o build/test\_concurrency \-pthread && ./build/test\_concurrency

test\_all: test\_list test\_stack test\_serializer test\_tree test\_dispatcher

regresion:  
	$(CC) $(CFLAGS) $(UNITY) $(OBJS) $(PROTO) $(SRV) \\  
	tests/unit/test\_list.c tests/unit/test\_stack.c \\  
	tests/unit/test\_serializer.c tests/unit/test\_tree.c \\  
	tests/integration/test\_dispatcher.c \\  
	\-o build/test\_regresion \-pthread && ./build/test\_regresion

coverage: test\_all  
	gcov src/objects/\*.c src/server/\*.c src/protocol/\*.c  
	lcov \--capture \--directory . \--output-file reports/coverage.info  
	genhtml reports/coverage.info \--output-directory reports/coverage\_html

valgrind\_check:  
	valgrind \--leak-check=full \--error-exitcode=1 ./build/test\_list  
	valgrind \--leak-check=full \--error-exitcode=1 ./build/test\_stack  
	valgrind \--leak-check=full \--error-exitcode=1 ./build/test\_serializer  
	valgrind \--leak-check=full \--error-exitcode=1 ./build/test\_tree  
	valgrind \--leak-check=full \--error-exitcode=1 ./build/test\_dispatcher

clean:  
	rm \-f build/\* \*.gcda \*.gcno \*.gcov  
	rm \-rf reports/coverage\_html reports/coverage.info

## **3.3 Pipeline CI/CD — GitHub Actions**

name: CI \- Bus de Objetos — Pruebas de Software  
on:  
  push:          { branches: \[main, develop\] }  
  pull\_request:  { branches: \[main\] }

jobs:  
  build-and-test:  
    runs-on: ubuntu-latest  
    steps:  
      \- uses: actions/checkout@v3  
      \- name: Instalar dependencias  
        run: sudo apt update && sudo apt install \-y gcc make lcov valgrind  
      \- name: Compilar servidor y cliente  
        run: make server && make client  
      \- name: Ejecutar pruebas unitarias e integración  
        run: make test\_all  
      \- name: Ejecutar pruebas de concurrencia  
        run: make test\_concurrency  
      \- name: Generar reporte de cobertura  
        run: make coverage  
      \- name: Publicar reporte de cobertura  
        uses: actions/upload-artifact@v3  
        with: { name: coverage-report, path: reports/coverage\_html/ }  
      \- name: Verificar fugas de memoria (Valgrind)  
        run: make valgrind\_check

# **4\. Interfaces Base del Sistema**

## **4.1 protocol.h — Tipos del Protocolo**

\#ifndef PROTOCOL\_H  
\#define PROTOCOL\_H  
\#define BUS\_PORT       8080  
\#define MAX\_MSG\_LEN    1024  
\#define MAX\_INSTANCES  256

typedef enum {OBJ\_LIST=1, OBJ\_STACK=2, OBJ\_TREE=3} ObjectType;  
typedef enum {  
    OP\_CREATE, OP\_INSERT, OP\_GET, OP\_REMOVE, OP\_SIZE, OP\_CONTAINS,  
    OP\_CLEAR, OP\_PUSH, OP\_POP, OP\_PEEK, OP\_IS\_EMPTY,  
    OP\_SEARCH, OP\_DELETE, OP\_INORDER, OP\_UNKNOWN  
} Operation;

typedef struct {  
    ObjectType obj\_type;  
    Operation  operation;  
    int        instance\_id;  
    char       data\[256\];  
    int        data\_int;  
    int        has\_data;  
} BusMessage;

typedef struct {  
    int  success;  
    char payload\[512\];  
} BusResponse;

\#endif

## **4.2 list.h, stack.h, tree.h — Interfaces de Objetos**

/\*   
list.h   
\*/  
typedef struct { ListNode \*head; ListNode \*tail; int size; } List;  
List \*list\_create(void);          void  list\_destroy(List \*l);  
int   list\_insert(List\*, int);    int   list\_get(List\*, int pos, int \*out);  
int   list\_remove(List\*, int);    int   list\_size(List\*);  
int   list\_contains(List\*, int);  void  list\_clear(List\*);  
\#define LIST\_OK 0  \#define LIST\_NULL\_PTR \-1  \#define LIST\_OUT\_OF\_BOUNDS \-2

/\*   
stack.h   
\*/  
typedef struct { StackNode \*top; int size; } Stack;  
Stack \*stack\_create(void);        void  stack\_destroy(Stack\*);  
int    stack\_push(Stack\*, int);   int   stack\_pop(Stack\*, int \*out);  
int    stack\_peek(Stack\*, int\*);  int   stack\_is\_empty(Stack\*);  
\#define STACK\_OK 0  \#define STACK\_EMPTY \-2

/\*   
tree.h   
\*/  
typedef struct { TreeNode \*root; int size; } Tree;  
Tree \*tree\_create(void);          void  tree\_destroy(Tree\*);  
int   tree\_insert(Tree\*, int);    int   tree\_search(Tree\*, int);  
int   tree\_delete(Tree\*, int);    int   tree\_height(Tree\*);  
void  tree\_inorder(Tree\*, int \*arr, int \*count);  
\#define TREE\_OK 0  \#define TREE\_DUPLICATE \-4

## **4.3 serializer.h — Serialización del Protocolo**

\#ifndef SERIALIZER\_H  
\#define SERIALIZER\_H  
\#include "protocol.h"

/\*  
   Deserializa un string del protocolo en BusMessage.  
   Retorna 0 en éxito, \-1 si el mensaje está mal armado.  
   USA strtok\_r (thread-safe), NO strtok.   
\*/  
int  deserialize\_message(const char \*raw, BusMessage \*msg);

/\*  
   Serializa una BusResponse en el formato del protocolo.  
   Escribe en buf (máx buf\_size bytes).   
\*/  
void serialize\_response(const BusResponse \*resp, char \*buf, int buf\_size);

/\*   
   Construye un mensaje de solicitud (usado por bus\_client.c)   
\*/  
void serialize\_request(ObjectType obj, Operation op,  
                       int id, const char \*data,  
                       char \*buf, int buf\_size);  
\#endif

# **5\. Ejemplo de Prueba Unitaria con Unity**

## **5.1 Prueba del Serializer — Técnica: Partición de Equivalencia**

El serializer es el componente más crítico del protocolo. Se aplica partición de equivalencia identificando las clases: mensajes válidos para cada objeto, mensajes con campo OBJETO inválido, mensajes con formato incorrecto y mensajes con campos vacíos incorrectos.

/\* tests/unit/test\_serializer.c \*/  
\#include "../unity/unity.h"  
\#include "../../src/protocol/serializer.h"

void setUp(void) {} void tearDown(void) {}

/\* Clase válida: mensajes bien formados \*/  
void test\_deserializar\_list\_insert\_valido(void) {  
    BusMessage msg;  
    TEST\_ASSERT\_EQUAL(0, deserialize\_message("LIST|INSERT|1|42\\n", \&msg));  
    TEST\_ASSERT\_EQUAL(OBJ\_LIST,   msg.obj\_type);  
    TEST\_ASSERT\_EQUAL(OP\_INSERT,  msg.operation);  
    TEST\_ASSERT\_EQUAL(1,          msg.instance\_id);  
    TEST\_ASSERT\_EQUAL(42,         msg.data\_int);  
}

void test\_deserializar\_stack\_pop\_sin\_dato(void) {  
    BusMessage msg;  
    TEST\_ASSERT\_EQUAL(0, deserialize\_message("STACK|POP|2|\\n", \&msg));  
    TEST\_ASSERT\_EQUAL(OBJ\_STACK, msg.obj\_type);  
    TEST\_ASSERT\_EQUAL(OP\_POP,    msg.operation);  
    TEST\_ASSERT\_EQUAL(0,         msg.has\_data);  
}

/\* Clase inválida: objeto desconocido \*/  
void test\_objeto\_invalido\_retorna\_error(void) {  
    BusMessage msg;  
    TEST\_ASSERT\_EQUAL(-1, deserialize\_message("QUEUE|PUSH|1|5\\n", \&msg));  
}

/\* Clase inválida: formato incorrecto \*/  
void test\_sin\_separadores\_retorna\_error(void) {  
    BusMessage msg;  
    TEST\_ASSERT\_EQUAL(-1, deserialize\_message("LISTINSERT142", \&msg));  
}

/\* Ida y vuelta: serializar respuesta \*/  
void test\_serialize\_ok\_con\_dato(void) {  
    BusResponse resp \= {1, "42"};  
    char buf\[64\];  
    serialize\_response(\&resp, buf, sizeof(buf));  
    TEST\_ASSERT\_EQUAL\_STRING("OK|42\\n", buf);  
}

void test\_serialize\_error(void) {  
    BusResponse resp \= {0, "EMPTY\_STRUCTURE"};  
    char buf\[64\];  
    serialize\_response(\&resp, buf, sizeof(buf));  
    TEST\_ASSERT\_EQUAL\_STRING("ERROR|EMPTY\_STRUCTURE\\n", buf);  
}

int main(void) {  
    UNITY\_BEGIN();  
    RUN\_TEST(test\_deserializar\_list\_insert\_valido);  
    RUN\_TEST(test\_deserializar\_stack\_pop\_sin\_dato);  
    RUN\_TEST(test\_objeto\_invalido\_retorna\_error);  
    RUN\_TEST(test\_sin\_separadores\_retorna\_error);  
    RUN\_TEST(test\_serialize\_ok\_con\_dato);  
    RUN\_TEST(test\_serialize\_error);  
    return UNITY\_END();  
}

# **6\. Plantilla de Registro de Defectos**

Desde la Etapa 2, todos los defectos encontrados se registran en GitHub Issues con el siguiente formato estándar:

| Campo | Descripción | Ejemplo |
| ----- | ----- | ----- |
| ID | Número correlativo | DEF-001 |
| Título | Descripción breve | deserialize\_message acepta mensaje sin terminador \\n |
| Módulo | Componente afectado | Serializer / Dispatcher / Object Server / Bus Server |
| Severidad | Crítico / Alto / Medio / Bajo | Alto |
| Etapa detectado | En qué etapa se encontró | Etapa 2 — Pruebas Unitarias |
| Tipo de prueba | Qué tipo de prueba lo detectó | Unitaria / Integración / Sistema / Regresión |
| Pasos para reproducir | Secuencia exacta | 1\. Llamar deserialize\_message("LIST|INSERT|1|42", \&msg) |
| Resultado esperado | Comportamiento correcto | Retornar \-1 (mensaje inválido por falta de \\n) |
| Resultado obtenido | Comportamiento real | Retornar 0 (acepta el mensaje sin terminador) |
| Estado | Abierto / Resuelto / Cerrado | Abierto |
| Asignado a | Integrante responsable | Ana González |

# **7\. Recursos y Referencias**

| Recurso | URL / Descripción |
| ----- | ----- |
| Unity Test Framework | https://github.com/ThrowTheSwitch/Unity |
| Beej's Guide to Network Programming | https://beej.us/guide/bgnet/; Referencia esencial para sockets en C |
| POSIX Threads Programming (LLNL) | [https://hpc-tutorials.llnl.gov/posix/](https://hpc-tutorials.llnl.gov/posix/); Tutorial completo de pthreads |
| gcov \+ lcov (cobertura) | https://gcc.gnu.org/onlinedocs/gcc/Gcov.html |
| Valgrind \+ Helgrind (data races) | https://valgrind.org/docs/manual/hg-manual.html |
| GitHub Actions | https://docs.github.com/en/actions |
| Netcat: probar el servidor manualmente | nc 127.0.0.1 8080 (disponible en Linux/Mac sin instalar) |

| 8\. Plantillas de C — Módulos del Servidor |
| :---- |

Esta sección provee las plantillas base (esqueletos) para los cuatro módulos del servidor que los estudiantes deben implementar en las Etapas 3 y 4\. Cada plantilla incluye los includes necesarios, la declaración de estructuras internas, las firmas de las funciones públicas y privadas, y comentarios guía que orientan la implementación sin revelarla.  
Nota: TODO \= To do.

| 8.1 object\_server.c — Repositorio Thread-Safe de Objetos |
| :---- |

Responsabilidad: mantener un arreglo de instancias de objetos (List, Stack, Tree) indexado por ID, protegido con mutex para acceso concurrente desde múltiples hilos. Proporciona las operaciones CRUD sobre instancias que el dispatcher consumirá.

| Etapa 3 — Pruebas de Integración. Probar la correcta inicialización del mutex, la creación y destrucción de instancias, y la seguridad en acceso concurrente con test\_concurrency.c. |
| :---- |

/\* \=============================================================  
 \* src/server/object\_server.c  
 \* Repositorio thread-safe de instancias de objetos.  
 \* Etapa 3 — Pruebas de Integración \+ Concurrencia  
 \* \============================================================= \*/

\#include "object\_server.h"  
\#include "../objects/list.h"  
\#include "../objects/stack.h"  
\#include "../objects/tree.h"  
\#include \<pthread.h\>  
\#include \<stdlib.h\>  
\#include \<string.h\>  
\#include \<stdio.h\>

/\* ── Estructura interna de una instancia ── \*/  
typedef struct {  
    ObjectType  type;       /\* OBJ\_LIST | OBJ\_STACK | OBJ\_TREE \*/  
    void       \*ptr;        /\* Puntero al objeto real           \*/  
    int         active;     /\* 1 \= en uso, 0 \= libre            \*/  
} ObjectSlot;

/\* ── Estado global del servidor de objetos ── \*/  
static ObjectSlot  slots\[MAX\_INSTANCES\];  
static pthread\_mutex\_t server\_mutex;  
static int         initialized \= 0;

/\* ─────────────────────────────────────────────────────────────  
 \* object\_server\_init()  
 \* Inicializa el arreglo de slots y el mutex.  
 \* Debe llamarse UNA sola vez antes de cualquier otra función.  
 \* Retorna: 0 en éxito, \-1 si ya fue inicializado o error mutex.  
 \* ───────────────────────────────────────────────────────────── \*/  
int object\_server\_init(void) {  
    /\* TODO: verificar que no esté ya inicializado \*/  
    /\* TODO: inicializar pthread\_mutex con pthread\_mutex\_init() \*/  
    /\* TODO: limpiar todos los slots (memset / bucle) \*/  
    /\* TODO: marcar initialized \= 1 \*/  
    return 0; /\* reemplazar con implementación \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* object\_server\_destroy()  
 \* Libera todos los objetos activos y destruye el mutex.  
 \* Debe llamarse al apagar el servidor.  
 \* ───────────────────────────────────────────────────────────── \*/  
void object\_server\_destroy(void) {  
    /\* TODO: adquirir el mutex \*/  
    /\* TODO: recorrer slots, llamar list/stack/tree\_destroy() según type \*/  
    /\* TODO: liberar el mutex \*/  
    /\* TODO: destruir el mutex con pthread\_mutex\_destroy() \*/  
    /\* TODO: marcar initialized \= 0 \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* object\_server\_create(type)  
 \* Crea una nueva instancia del tipo indicado y retorna su ID.  
 \* Retorna: ID \>= 0 en éxito, \-1 si no hay slots libres.  
 \* ───────────────────────────────────────────────────────────── \*/  
int object\_server\_create(ObjectType type) {  
    int id \= \-1;  
    /\* TODO: adquirir el mutex \*/  
    /\* TODO: buscar un slot con active \== 0 \*/  
    /\* TODO: según type, llamar list\_create() / stack\_create() / tree\_create() \*/  
    /\* TODO: asignar ptr, type, active=1 en el slot encontrado \*/  
    /\* TODO: liberar el mutex \*/  
    /\* TODO: retornar el índice del slot como ID \*/  
    return id;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* object\_server\_get(id, type, ptr\_out)  
 \* Retorna el puntero al objeto del slot indicado.  
 \* El llamador DEBE haber adquirido el mutex antes.  
 \* Retorna: 0 si el slot es válido y activo, \-1 si no existe.  
 \* ───────────────────────────────────────────────────────────── \*/  
int object\_server\_get(int id, ObjectType type, void \*\*ptr\_out) {  
    /\* TODO: validar rango de id \[0, MAX\_INSTANCES) \*/  
    /\* TODO: verificar slots\[id\].active \== 1 \*/  
    /\* TODO: verificar slots\[id\].type \== type \*/  
    /\* TODO: asignar \*ptr\_out \= slots\[id\].ptr \*/  
    return \-1; /\* reemplazar \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* object\_server\_destroy\_instance(id)  
 \* Destruye la instancia con el ID dado y libera su slot.  
 \* Retorna: 0 en éxito, \-1 si el ID no existe o no está activo.  
 \* ───────────────────────────────────────────────────────────── \*/  
int object\_server\_destroy\_instance(int id) {  
    /\* TODO: adquirir el mutex \*/  
    /\* TODO: validar el slot \*/  
    /\* TODO: llamar la función \_destroy() del tipo correspondiente \*/  
    /\* TODO: marcar active \= 0 y ptr \= NULL \*/  
    /\* TODO: liberar el mutex \*/  
    return \-1; /\* reemplazar \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* Funciones de conveniencia: lock / unlock del mutex global.  
 \* El dispatcher las usa para mantener el lock durante toda la  
 \* ejecución de una operación compuesta.  
 \* ───────────────────────────────────────────────────────────── \*/  
void object\_server\_lock(void)   { pthread\_mutex\_lock(\&server\_mutex);   }  
void object\_server\_unlock(void) { pthread\_mutex\_unlock(\&server\_mutex); }

| 8.2 dispatcher.c — Despachador de Operaciones |
| :---- |

Responsabilidad: recibir un BusMessage ya deserializado, resolver la operación sobre el objeto correcto a través de object\_server, y construir la BusResponse. Es la capa de integración entre el protocolo y las estructuras de datos.

| Etapa 3 — Pruebas de Integración. Las pruebas de test\_dispatcher.c verifican que cada combinación (objeto, operación) produzca la respuesta correcta, incluyendo todos los códigos de error del protocolo. |
| :---- |

/\* \=============================================================  
 \* src/server/dispatcher.c  
 \* Despacha operaciones del protocolo a los objetos del servidor.  
 \* Etapa 3 — Pruebas de Integración  
 \* \============================================================= \*/

\#include "dispatcher.h"  
\#include "object\_server.h"  
\#include "../objects/list.h"  
\#include "../objects/stack.h"  
\#include "../objects/tree.h"  
\#include "../protocol/protocol.h"  
\#include \<stdio.h\>  
\#include \<string.h\>  
\#include \<stdlib.h\>

/\* ── Prototipos de funciones internas (privadas) ── \*/  
static void dispatch\_list (const BusMessage \*msg, BusResponse \*resp);  
static void dispatch\_stack(const BusMessage \*msg, BusResponse \*resp);  
static void dispatch\_tree (const BusMessage \*msg, BusResponse \*resp);

/\* ─────────────────────────────────────────────────────────────  
 \* dispatch(msg, resp)  
 \* Punto de entrada principal. Redirige al despachador específico  
 \* según msg-\>obj\_type. Llena resp con OK|dato o ERROR|codigo.  
 \* ───────────────────────────────────────────────────────────── \*/  
void dispatch(const BusMessage \*msg, BusResponse \*resp) {  
    if (\!msg || \!resp) return;

    /\* TODO: inicializar resp-\>success \= 0 \*/  
    /\* TODO: switch sobre msg-\>obj\_type \*/  
    /\*       case OBJ\_LIST:  dispatch\_list(msg, resp);  break; \*/  
    /\*       case OBJ\_STACK: dispatch\_stack(msg, resp); break; \*/  
    /\*       case OBJ\_TREE:  dispatch\_tree(msg, resp);  break; \*/  
    /\*       default: snprintf resp-\>payload \= INVALID\_OBJECT   \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* dispatch\_list(msg, resp)  
 \* Despacha operaciones sobre objetos LIST.  
 \* ───────────────────────────────────────────────────────────── \*/  
static void dispatch\_list(const BusMessage \*msg, BusResponse \*resp) {  
    List \*list \= NULL;  
    void \*ptr  \= NULL;

    /\* TODO: adquirir lock con object\_server\_lock() \*/  
    /\* TODO: obtener la instancia con object\_server\_get() \*/  
    /\*       Si falla: resp payload \= INSTANCE\_NOT\_FOUND, unlock y return \*/  
    /\* TODO: switch sobre msg-\>operation \*/  
    /\*   OP\_CREATE:   id \= object\_server\_create(OBJ\_LIST)          \*/  
    /\*                snprintf(resp-\>payload, ..., "%d", id)       \*/  
    /\*   OP\_INSERT:   list\_insert(list, msg-\>data\_int)              \*/  
    /\*   OP\_GET:      list\_get(list, msg-\>data\_int, \&val)           \*/  
    /\*                manejar LIST\_OUT\_OF\_BOUNDS → OUT\_OF\_BOUNDS    \*/  
    /\*   OP\_REMOVE:   list\_remove(list, msg-\>data\_int)              \*/  
    /\*   OP\_SIZE:     snprintf(resp-\>payload, ..., "%d", size)     \*/  
    /\*   OP\_CONTAINS: result \= list\_contains(list, msg-\>data\_int)   \*/  
    /\*                snprintf(resp-\>payload, ..., result?"TRUE":"FALSE") \*/  
    /\*   default:     resp-\>payload \= INVALID\_OPERATION             \*/  
    /\* TODO: liberar lock con object\_server\_unlock() \*/  
    (void)list; (void)ptr;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* dispatch\_stack(msg, resp)  
 \* Despacha operaciones sobre objetos STACK.  
 \* ───────────────────────────────────────────────────────────── \*/  
static void dispatch\_stack(const BusMessage \*msg, BusResponse \*resp) {  
    Stack \*stack \= NULL;  
    void  \*ptr   \= NULL;

    /\* TODO: adquirir lock \*/  
    /\* TODO: obtener instancia; error → INSTANCE\_NOT\_FOUND \*/  
    /\* TODO: switch sobre msg-\>operation \*/  
    /\*   OP\_CREATE:   id \= object\_server\_create(OBJ\_STACK)         \*/  
    /\*   OP\_PUSH:     stack\_push(stack, msg-\>data\_int)              \*/  
    /\*   OP\_POP:      stack\_pop(stack, \&val)                        \*/  
    /\*                manejar STACK\_EMPTY → EMPTY\_STRUCTURE         \*/  
    /\*   OP\_PEEK:     stack\_peek(stack, \&val)                       \*/  
    /\*   OP\_IS\_EMPTY: result \= stack\_is\_empty(stack)               \*/  
    /\*                snprintf(resp-\>payload, ..., result?"TRUE":"FALSE") \*/  
    /\*   default:     INVALID\_OPERATION                             \*/  
    /\* TODO: liberar lock \*/  
    (void)stack; (void)ptr;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* dispatch\_tree(msg, resp)  
 \* Despacha operaciones sobre objetos TREE.  
 \* ───────────────────────────────────────────────────────────── \*/  
static void dispatch\_tree(const BusMessage \*msg, BusResponse \*resp) {  
    Tree \*tree \= NULL;  
    void \*ptr  \= NULL;

    /\* TODO: adquirir lock \*/  
    /\* TODO: obtener instancia; error → INSTANCE\_NOT\_FOUND \*/  
    /\* TODO: switch sobre msg-\>operation \*/  
    /\*   OP\_CREATE:   id \= object\_server\_create(OBJ\_TREE)          \*/  
    /\*   OP\_INSERT:   tree\_insert(tree, msg-\>data\_int)              \*/  
    /\*                manejar TREE\_DUPLICATE → DUPLICATE\_VALUE      \*/  
    /\*   OP\_SEARCH:   found \= tree\_search(tree, msg-\>data\_int)      \*/  
    /\*   OP\_DELETE:   tree\_delete(tree, msg-\>data\_int)              \*/  
    /\*   OP\_INORDER:  int arr\[MAX\_INSTANCES\]; int cnt=0;            \*/  
    /\*                tree\_inorder(tree, arr, \&cnt);                \*/  
    /\*                construir string "v1,v2,..." en resp-\>payload \*/  
    /\*   default:     INVALID\_OPERATION                             \*/  
    /\* TODO: liberar lock \*/  
    (void)tree; (void)ptr;  
}

| 8.3 bus\_server.c — Servidor TCP con pthreads |
| :---- |

Responsabilidad: abrir un socket TCP en BUS\_PORT, aceptar conexiones de clientes y crear un hilo por conexión. Cada hilo lee mensajes en un bucle, los deserializa, los despacha y envía la respuesta, hasta que el cliente cierra la conexión.

| Etapa 4 — Pruebas de Sistema. Las pruebas deben verificar: múltiples clientes simultáneos, comportamiento ante desconexión abrupta, límite de conexiones y rendimiento bajo carga (benchmark.c). |
| :---- |

/\* \=============================================================  
 \* src/server/bus\_server.c  
 \* Servidor TCP concurrente. Un hilo por cliente.  
 \* Etapa 4 — Pruebas de Sistema  
 \* \============================================================= \*/

\#include "../protocol/protocol.h"  
\#include "../protocol/serializer.h"  
\#include "dispatcher.h"  
\#include "object\_server.h"  
\#include \<stdio.h\>  
\#include \<stdlib.h\>  
\#include \<string.h\>  
\#include \<unistd.h\>  
\#include \<pthread.h\>  
\#include \<sys/socket.h\>  
\#include \<netinet/in.h\>  
\#include \<arpa/inet.h\>  
\#include \<signal.h\>

/\* ── Argumento que se pasa a cada hilo cliente ── \*/  
typedef struct {  
    int   client\_fd;  
    char  client\_ip\[INET\_ADDRSTRLEN\];  
    int   client\_port;  
} ClientArgs;

/\* ── Prototipo del hilo cliente ── \*/  
static void \*handle\_client(void \*arg);

/\* ─────────────────────────────────────────────────────────────  
 \* main()  
 \* Inicializa el servidor, entra en el bucle accept y lanza hilos.  
 \* ───────────────────────────────────────────────────────────── \*/  
int main(void) {  
    int server\_fd;  
    struct sockaddr\_in addr;

    /\* TODO: ignorar SIGPIPE para no morir si el cliente desconecta \*/  
    /\*       signal(SIGPIPE, SIG\_IGN);                              \*/  
    /\* TODO: inicializar object\_server con object\_server\_init() \*/  
    /\* TODO: crear socket TCP:                                      \*/  
    /\*       server\_fd \= socket(AF\_INET, SOCK\_STREAM, 0);           \*/  
    /\* TODO: configurar SO\_REUSEADDR para reutilizar el puerto      \*/  
    /\* TODO: bind() en 0.0.0.0:BUS\_PORT \*/  
    /\* TODO: listen() con backlog razonable (p.ej. 16\)             \*/  
    printf("Bus de Objetos escuchando en puerto %d...\\n", BUS\_PORT);  
    /\* ── Bucle principal de aceptación ── \*/  
    while (1) {  
        struct sockaddr\_in client\_addr;  
        socklen\_t          addr\_len \= sizeof(client\_addr);  
        int                client\_fd;  
        pthread\_t          tid;  
        ClientArgs        \*args;

        /\* TODO: client\_fd \= accept(server\_fd, ...)                \*/  
        /\*       manejar error con perror \+ continue               \*/  
        /\* TODO: asignar ClientArgs en el heap (malloc)            \*/  
        /\*       copiar client\_fd, ip (inet\_ntop), port            \*/  
        /\* TODO: crear hilo con pthread\_create(\&tid, NULL,         \*/  
        /\*        handle\_client, args)                             \*/  
        /\* TODO: pthread\_detach(tid) para liberar recursos auto.   \*/  
    }  
    /\* TODO: object\_server\_destroy() antes de salir \*/  
    close(server\_fd);  
    return 0;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* handle\_client(arg)  
 \* Hilo que atiende UN cliente: lee mensajes en bucle,  
 \* despacha y responde, hasta EOF o error.  
 \* ───────────────────────────────────────────────────────────── \*/  
static void \*handle\_client(void \*arg) {  
    ClientArgs \*ca \= (ClientArgs \*)arg;  
    char        raw\[MAX\_MSG\_LEN\];  
    char        resp\_buf\[MAX\_MSG\_LEN\];  
    BusMessage  msg;  
    BusResponse resp;  
    ssize\_t     n;

    printf("\[+\] Cliente conectado: %s:%d\\n",  
            ca-\>client\_ip, ca-\>client\_port);

    /\* TODO: bucle: recv(ca-\>client\_fd, raw, ...) \*/  
    /\*              Si n \<= 0: break (EOF o error) \*/  
    /\*              raw\[n\] \= '\\0'                  \*/  
    /\*              deserialize\_message(raw, \&msg) \*/  
    /\*              Si error: construir resp ERROR|INVALID\_MESSAGE \*/  
    /\*              Sino: dispatch(\&msg, \&resp)     \*/  
    /\*              serialize\_response(\&resp, resp\_buf, ...) \*/  
    /\*              send(ca-\>client\_fd, resp\_buf, strlen(resp\_buf), 0\) \*/

    printf("\[-\] Cliente desconectado: %s:%d\\n", ca-\>client\_ip, ca-\>client\_port);  
    close(ca-\>client\_fd);  
    free(ca);  
    return NULL;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* PISTAS DE IMPLEMENTACIÓN  
 \* \- Usar recv() en modo bloqueante; leer hasta encontrar '\\n'  
 \*   o buffer lleno para manejar mensajes fragmentados.  
 \* \- Considerar un helper read\_line(fd, buf, max) que acumule  
 \*   bytes hasta leer el terminador '\\n' del protocolo.  
 \* \- Helgrind (valgrind \--tool=helgrind) detectará data races  
 \*   si el mutex no se usa correctamente en object\_server.  
 \* ───────────────────────────────────────────────────────────── \*/

| 8.4 bus\_client.c — API Cliente del Bus |
| :---- |

Responsabilidad: proveer una API de alto nivel que encapsule la conexión TCP, la serialización del request y la deserialización de la respuesta. Es la biblioteca que usan las pruebas de sistema (test\_bus\_system.c) y el cliente interactivo (test\_client.c).

| Etapa 4 — Pruebas de Sistema end-to-end. La API debe ser robusta ante respuestas ERROR del servidor y ante desconexiones inesperadas. Las funciones retornan códigos de error semánticos, no mensajes crudos. |
| :---- |

/\* \=============================================================  
 \* src/client/bus\_client.c  
 \* API cliente del Bus de Objetos.  
 \* Etapa 4 — Pruebas de Sistema end-to-end  
 \* \============================================================= \*/

\#include "client\_api.h"  
\#include "../protocol/protocol.h"  
\#include "../protocol/serializer.h"  
\#include \<stdio.h\>  
\#include \<stdlib.h\>  
\#include \<string.h\>  
\#include \<unistd.h\>  
\#include \<sys/socket.h\>  
\#include \<netinet/in.h\>  
\#include \<arpa/inet.h\>

/\* ── Estructura opaca del handle de conexión ── \*/  
struct BusClient {  
    int  fd;              /\* descriptor del socket  \*/  
    char host\[64\];  
    int  port;  
    int  connected;  
};

/\* ─────────────────────────────────────────────────────────────  
 \* bus\_client\_connect(host, port)  
 \* Crea el socket y conecta al servidor.  
 \* Retorna: handle no-NULL en éxito, NULL si falla la conexión.  
 \* ───────────────────────────────────────────────────────────── \*/  
BusClient \*bus\_client\_connect(const char \*host, int port) {  
    BusClient          \*bc;  
    struct sockaddr\_in  addr;

    /\* TODO: malloc(sizeof(BusClient)); manejar NULL \*/  
    /\* TODO: socket(AF\_INET, SOCK\_STREAM, 0\) \*/  
    /\* TODO: rellenar addr: AF\_INET, port=htons(port), ip=inet\_pton() \*/  
    /\* TODO: connect(fd, \&addr, sizeof(addr)) \*/  
    /\*       Si falla: close(fd), free(bc), return NULL \*/  
    /\* TODO: bc-\>connected \= 1 \*/

    (void)host; (void)port;  
    bc \= NULL; /\* reemplazar \*/  
    return bc;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* bus\_client\_disconnect(bc)  
 \* Cierra el socket y libera el handle.  
 \* ───────────────────────────────────────────────────────────── \*/  
void bus\_client\_disconnect(BusClient \*bc) {  
    if (\!bc) return;  
    /\* TODO: close(bc-\>fd) si está conectado \*/  
    /\* TODO: free(bc) \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* bus\_send\_request(bc, obj, op, id, data, resp\_out)  
 \* Función interna: serializa, envía y recibe la respuesta.  
 \* Retorna: 0 en éxito de comunicación (la respuesta puede ser ERROR),  
 \*         \-1 si hay fallo de red.  
 \* ───────────────────────────────────────────────────────────── \*/  
static int bus\_send\_request(BusClient \*bc,  
                             ObjectType obj, Operation op,  
                             int id, const char \*data,  
                             BusResponse \*resp\_out) {  
    char req\_buf\[MAX\_MSG\_LEN\];  
    char rsp\_buf\[MAX\_MSG\_LEN\];

    /\* TODO: serialize\_request(obj, op, id, data, req\_buf, sizeof(req\_buf)) \*/  
    /\* TODO: send(bc-\>fd, req\_buf, strlen(req\_buf), 0\) \*/  
    /\* TODO: recv(bc-\>fd, rsp\_buf, sizeof(rsp\_buf)-1, 0\) \*/  
    /\*       Si n \<= 0: bc-\>connected \= 0; return \-1 \*/  
    /\* TODO: parsear respuesta manual:  
     \*       si empieza con "OK|"   → resp\_out-\>success=1, copiar payload  
     \*       si empieza con "ERROR|" → resp\_out-\>success=0, copiar codigo  
     \*/  
    (void)bc; (void)obj; (void)op; (void)id; (void)data; (void)resp\_out;  
    return \-1; /\* reemplazar \*/  
}

/\* ─────────────────────────────────────────────────────────────  
 \* API de alto nivel — List  
 \* Todas retornan 0 en éxito, código de error negativo si falla.  
 \* ───────────────────────────────────────────────────────────── \*/  
int bus\_list\_create(BusClient \*bc, int \*id\_out) {  
    BusResponse resp;  
    /\* TODO: bus\_send\_request(bc, OBJ\_LIST, OP\_CREATE, 0, "", \&resp) \*/  
    /\* TODO: si resp.success: \*id\_out \= atoi(resp.payload) \*/  
    (void)bc; (void)id\_out; (void)resp;  
    return \-1;  
}  
int bus\_list\_insert(BusClient \*bc, int id, int value) {  
    /\* TODO: formatear value como string, llamar bus\_send\_request \*/  
    (void)bc; (void)id; (void)value;  
    return \-1;  
}  
int bus\_list\_get(BusClient \*bc, int id, int pos, int \*val\_out) {  
    /\* TODO: formatear pos, llamar bus\_send\_request, parsear val\_out \*/  
    (void)bc; (void)id; (void)pos; (void)val\_out;  
    return \-1;  
}  
int bus\_list\_size(BusClient \*bc, int id, int \*size\_out) {  
    /\* TODO \*/  
    (void)bc; (void)id; (void)size\_out;  
    return \-1;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* API de alto nivel — Stack  
 \* ───────────────────────────────────────────────────────────── \*/  
int bus\_stack\_create(BusClient \*bc, int \*id\_out) {  
    /\* TODO \*/ (void)bc; (void)id\_out; return \-1;  
}  
int bus\_stack\_push(BusClient \*bc, int id, int value) {  
    /\* TODO \*/ (void)bc; (void)id; (void)value; return \-1;  
}  
int bus\_stack\_pop(BusClient \*bc, int id, int \*val\_out) {  
    /\* TODO \*/ (void)bc; (void)id; (void)val\_out; return \-1;  
}  
int bus\_stack\_peek(BusClient \*bc, int id, int \*val\_out) {  
    /\* TODO \*/ (void)bc; (void)id; (void)val\_out; return \-1;  
}

/\* ─────────────────────────────────────────────────────────────  
 \* API de alto nivel — Tree  
 \* ───────────────────────────────────────────────────────────── \*/  
int bus\_tree\_create(BusClient \*bc, int \*id\_out) {  
    /\* TODO \*/ (void)bc; (void)id\_out; return \-1;  
}  
int bus\_tree\_insert(BusClient \*bc, int id, int value) {  
    /\* TODO \*/ (void)bc; (void)id; (void)value; return \-1;  
}  
int bus\_tree\_search(BusClient \*bc, int id, int value, int \*found) {  
    /\* TODO \*/ (void)bc; (void)id; (void)value; (void)found; return \-1;  
}  
int bus\_tree\_inorder(BusClient \*bc, int id, int \*arr, int \*count) {  
    /\* TODO: recibir string "v1,v2,..." y parsear con strtok\_r \*/  
    (void)bc; (void)id; (void)arr; (void)count; return \-1;  
}

| 8.5 client\_api.h — Header Público de la API Cliente |
| :---- |

Este header es el contrato público de la API cliente. Las pruebas de sistema lo incluyen directamente. La estructura BusClient es opaca: sus campos internos solo son visibles en bus\_client.c.

/\* \=============================================================  
 \* src/client/client\_api.h  
 \* Interfaz pública de la API cliente del Bus de Objetos.  
 \* \============================================================= \*/

\#ifndef CLIENT\_API\_H  
\#define CLIENT\_API\_H

\#include "../protocol/protocol.h"

/\* Tipo opaco — definido en bus\_client.c \*/  
typedef struct BusClient BusClient;

/\* ── Conexión ── \*/  
BusClient \*bus\_client\_connect(const char \*host, int port);  
void       bus\_client\_disconnect(BusClient \*bc);  
int        bus\_client\_is\_connected(const BusClient \*bc);

/\* ── API List ── \*/  
int bus\_list\_create (BusClient \*bc, int \*id\_out);  
int bus\_list\_insert (BusClient \*bc, int id, int value);  
int bus\_list\_get    (BusClient \*bc, int id, int pos, int \*val\_out);  
int bus\_list\_remove (BusClient \*bc, int id, int pos);  
int bus\_list\_size   (BusClient \*bc, int id, int \*size\_out);  
int bus\_list\_contains(BusClient \*bc, int id, int value, int \*found);

/\* ── API Stack ── \*/  
int bus\_stack\_create  (BusClient \*bc, int \*id\_out);  
int bus\_stack\_push    (BusClient \*bc, int id, int value);  
int bus\_stack\_pop     (BusClient \*bc, int id, int \*val\_out);  
int bus\_stack\_peek    (BusClient \*bc, int id, int \*val\_out);  
int bus\_stack\_is\_empty(BusClient \*bc, int id, int \*empty\_out);

/\* ── API Tree ── \*/  
int bus\_tree\_create  (BusClient \*bc, int \*id\_out);  
int bus\_tree\_insert  (BusClient \*bc, int id, int value);  
int bus\_tree\_search  (BusClient \*bc, int id, int value, int \*found);  
int bus\_tree\_delete  (BusClient \*bc, int id, int value);  
int bus\_tree\_inorder (BusClient \*bc, int id, int \*arr, int \*count);

/\* ── Códigos de retorno de la API ── \*/  
\#define BUS\_OK               0  
\#define BUS\_ERR\_NETWORK     \-1   /\* falla de red o desconexión    \*/  
\#define BUS\_ERR\_NOT\_FOUND   \-2   /\* INSTANCE\_NOT\_FOUND del server \*/  
\#define BUS\_ERR\_EMPTY       \-3   /\* EMPTY\_STRUCTURE               \*/  
\#define BUS\_ERR\_BOUNDS      \-4   /\* OUT\_OF\_BOUNDS                 \*/  
\#define BUS\_ERR\_DUPLICATE   \-5   /\* DUPLICATE\_VALUE (árbol)       \*/  
\#define BUS\_ERR\_SERVER      \-9   /\* SERVER\_ERROR genérico         \*/

\#endif /\* CLIENT\_API\_H \*/

