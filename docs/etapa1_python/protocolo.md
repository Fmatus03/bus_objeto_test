# Especificación Formal del Protocolo — Bus de Objetos en C
**Etapa 1 — Pruebas Estáticas y Especificación del Protocolo**  
Curso: Pruebas de Software | Proyecto: Bus de Objetos (C99 + TCP/IP + pthreads)

---

## 1. Gramática EBNF del Formato de Mensaje

```ebnf
<Message>       ::= <Request> | <Response>

<Request>       ::= <ObjectType> "|" <Operation> "|" <InstanceID> "|" <Data> "\n"
<Response>      ::= <OKResponse> | <ErrorResponse>
<OKResponse>    ::= "OK|" <ResponseData> "\n"
<ErrorResponse> ::= "ERROR|" <ErrorCode> "\n"

<ObjectType>    ::= "LIST" | "STACK" | "TREE"

<Operation>     ::= "CREATE" | "INSERT" | "GET" | "REMOVE" | "SIZE"
                  | "CONTAINS" | "CLEAR"
                  | "PUSH" | "POP" | "PEEK" | "IS_EMPTY"
                  | "SEARCH" | "DELETE" | "INORDER"

<InstanceID>    ::= <Digit> { <Digit> }

<Data>          ::= { <Char> }
<Char>          ::= <Letter> | <Digit> | " " | "-"

<ResponseData>  ::= <Value> { "," <Value> } | ""
<Value>         ::= "TRUE" | "FALSE" | <IntegerLiteral> | ""
<IntegerLiteral>::= [ "-" ] <Digit> { <Digit> }

<ErrorCode>     ::= <Letter> { <Letter> | "_" }

<Digit>         ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<Letter>        ::= "A" | "B" | ... | "Z" | "a" | "b" | ... | "z"
```

**Restricciones semánticas no expresadas en EBNF:**
- El campo `<InstanceID>` en mensajes `CREATE` es ignorado por el servidor (por convención se envía `0`).
- El campo `<Data>` debe ser un entero decimal válido en el rango `[INT_MIN, INT_MAX]` cuando la operación lo requiera.
- El terminador `\n` (0x0A) es **obligatorio**. Mensajes sin él provocan bloqueo del `recv()` o respuesta `ERROR|INVALID_MESSAGE` si se implementa timeout.
- El separador `|` (0x7C) no puede aparecer dentro del campo `<Data>`.

---

## 2. Tabla Completa de Operaciones

Cubre los tres objetos soportados: **LIST**, **STACK** y **TREE**.

| Objeto | Operación | Dato Enviado (`<Data>`) | Respuesta OK (`OK\|<dato>`) | Respuestas ERROR posibles |
|:---|:---|:---|:---|:---|
| **LIST** | CREATE | (vacío) | ID asignado (entero ≥ 0) | `SERVER_ERROR` |
| **LIST** | INSERT | valor entero | (vacío) → `OK\|` | `INSTANCE_NOT_FOUND`, `INVALID_MESSAGE` |
| **LIST** | GET | posición (entero ≥ 0) | valor en la posición | `OUT_OF_BOUNDS`, `INSTANCE_NOT_FOUND` |
| **LIST** | REMOVE | posición (entero ≥ 0) | (vacío) → `OK\|` | `OUT_OF_BOUNDS`, `INSTANCE_NOT_FOUND` |
| **LIST** | SIZE | (vacío) | Número de elementos (entero ≥ 0) | `INSTANCE_NOT_FOUND` |
| **LIST** | CONTAINS | valor entero | `TRUE` o `FALSE` | `INSTANCE_NOT_FOUND` |
| **LIST** | CLEAR | (vacío) | (vacío) → `OK\|` | `INSTANCE_NOT_FOUND` |
| **STACK** | CREATE | (vacío) | ID asignado (entero ≥ 0) | `SERVER_ERROR` |
| **STACK** | PUSH | valor entero | (vacío) → `OK\|` | `INSTANCE_NOT_FOUND`, `INVALID_MESSAGE` |
| **STACK** | POP | (vacío) | valor extraído del tope | `EMPTY_STRUCTURE`, `INSTANCE_NOT_FOUND` |
| **STACK** | PEEK | (vacío) | valor del tope (sin extraer) | `EMPTY_STRUCTURE`, `INSTANCE_NOT_FOUND` |
| **STACK** | IS_EMPTY | (vacío) | `TRUE` o `FALSE` | `INSTANCE_NOT_FOUND` |
| **TREE** | CREATE | (vacío) | ID asignado (entero ≥ 0) | `SERVER_ERROR` |
| **TREE** | INSERT | valor entero | (vacío) → `OK\|` | `DUPLICATE_VALUE`, `INSTANCE_NOT_FOUND` |
| **TREE** | SEARCH | valor entero | `TRUE` o `FALSE` | `INSTANCE_NOT_FOUND` |
| **TREE** | DELETE | valor entero | (vacío) → `OK\|` | `NOT_FOUND`, `INSTANCE_NOT_FOUND` |
| **TREE** | INORDER | (vacío) | valores CSV ascendentes (`v1,v2,...`) o vacío | `INSTANCE_NOT_FOUND` |

---

## 3. Tabla de Códigos de Error

| Código de Error | Condición que lo activa | Módulo que lo genera |
|:---|:---|:---|
| `INSTANCE_NOT_FOUND` | El campo `<InstanceID>` no corresponde a ningún slot activo en `object_server`. | `dispatcher.c` → `object_server_get()` retorna -1 |
| `EMPTY_STRUCTURE` | Se invoca `POP` o `PEEK` sobre una pila con `size == 0`, o `GET` sobre una lista vacía. | `dispatcher.c` → `stack_pop()` / `stack_peek()` retornan `STACK_EMPTY` |
| `OUT_OF_BOUNDS` | El índice `<pos>` enviado en `GET` o `REMOVE` satisface `pos < 0` o `pos >= size`. | `dispatcher.c` → `list_get()` / `list_remove()` retornan `LIST_OUT_OF_BOUNDS` |
| `DUPLICATE_VALUE` | Se intenta insertar en el BST un entero que ya existe en un nodo del árbol. | `dispatcher.c` → `tree_insert()` retorna `TREE_DUPLICATE` |
| `NOT_FOUND` | Se intenta eliminar (`DELETE`) del BST un entero que no existe en ningún nodo. | `dispatcher.c` → `tree_delete()` retorna -1 |
| `INVALID_OBJECT` | El campo `<ObjectType>` no es `LIST`, `STACK` ni `TREE` (ej. `QUEUE`, `MAP`, `DICT`). | `dispatcher.c` → `switch(msg->obj_type)` rama `default` |
| `INVALID_OPERATION` | La operación existe en el protocolo pero no está definida para el tipo de objeto indicado (ej. `LIST\|SEARCH`, `TREE\|POP`). | `dispatcher.c` → `dispatch_list/stack/tree()` rama `default` del switch de operación |
| `INVALID_MESSAGE` | El mensaje no tiene el número correcto de separadores `\|`, le falta el terminador `\n`, o un campo numérico obligatorio contiene caracteres no numéricos. | `serializer.c` → `deserialize_message()` retorna -1 |
| `SERVER_ERROR` | `malloc()` falla al crear una nueva instancia, o no hay slots libres en `slots[MAX_INSTANCES]`, u otro error interno irrecuperable. | `object_server.c` → `object_server_create()` retorna -1 |

---

## 4. Ejemplos de Intercambio Cliente / Servidor

Se muestran ≥12 casos comentados, cubriendo flujos estándar y todos los códigos de error.

| N° | Tipo | Descripción del Caso | Request (C → S) | Response (S → C) | Código de Error Activado |
|:---:|:---|:---|:---|:---|:---|
| **1** | ESTÁNDAR | Crear lista vacía. El servidor asigna ID=1 al primer slot libre. | `LIST\|CREATE\|0\|\n` | `OK\|1\n` | — |
| **2** | ESTÁNDAR | Insertar el entero 42 en la lista ID=1 (primer elemento). | `LIST\|INSERT\|1\|42\n` | `OK\|\n` | — |
| **3** | ESTÁNDAR | Obtener el elemento en posición 0 de la lista ID=1 (valor: 42). | `LIST\|GET\|1\|0\n` | `OK\|42\n` | — |
| **4** | ESTÁNDAR | Crear pila; el servidor asigna ID=2. | `STACK\|CREATE\|0\|\n` | `OK\|2\n` | — |
| **5** | ESTÁNDAR | Push del valor 99 en la pila ID=2. | `STACK\|PUSH\|2\|99\n` | `OK\|\n` | — |
| **6** | ESTÁNDAR | Pop de la pila ID=2: extrae y retorna 99. | `STACK\|POP\|2\|\n` | `OK\|99\n` | — |
| **7** | ESTÁNDAR | Crear árbol BST; servidor asigna ID=3. Insertar 5, luego verificar con SEARCH. | `TREE\|CREATE\|0\|\n` → `TREE\|INSERT\|3\|5\n` → `TREE\|SEARCH\|3\|5\n` | `OK\|3\n` → `OK\|\n` → `OK\|TRUE\n` | — |
| **8** | ESTÁNDAR | INORDER del árbol ID=3 con nodos {1, 3, 5, 7, 9} ya insertados. | `TREE\|INORDER\|3\|\n` | `OK\|1,3,5,7,9\n` | — |
| **9** | ESTÁNDAR | CLEAR de la lista ID=1: todos los nodos son liberados. | `LIST\|CLEAR\|1\|\n` | `OK\|\n` | — |
| **10** | ERROR: FORMATO | Mensaje sin separadores (falta el `\|`). `deserialize_message()` no puede tokenizar. | `LISTINSERT1\|42\n` | `ERROR\|INVALID_MESSAGE\n` | `INVALID_MESSAGE` |
| **11** | ERROR: BOUNDS | GET en lista ID=1 con solo 3 elementos, solicitando posición 312. | `LIST\|GET\|1\|312\n` | `ERROR\|OUT_OF_BOUNDS\n` | `OUT_OF_BOUNDS` |
| **12** | ERROR: INSTANCE | INORDER de un árbol con ID=999, que no existe en el servidor. | `TREE\|INORDER\|999\|\n` | `ERROR\|INSTANCE_NOT_FOUND\n` | `INSTANCE_NOT_FOUND` |
| **13** | ERROR: EMPTY | POP en pila ID=2 que fue vaciada previamente con pops anteriores. | `STACK\|POP\|2\|\n` | `ERROR\|EMPTY_STRUCTURE\n` | `EMPTY_STRUCTURE` |
| **14** | ERROR: DUPLICADO | INSERT de valor 5 en árbol ID=3 donde 5 ya existe. | `TREE\|INSERT\|3\|5\n` | `ERROR\|DUPLICATE_VALUE\n` | `DUPLICATE_VALUE` |
| **15** | ERROR: NOT FOUND | DELETE de valor 99 en árbol ID=3 donde 99 nunca fue insertado. | `TREE\|DELETE\|3\|99\n` | `ERROR\|NOT_FOUND\n` | `NOT_FOUND` |
| **16** | ERROR: OBJ INVÁLIDO | Tipo de objeto `QUEUE` no existe en el protocolo. | `QUEUE\|CREATE\|0\|\n` | `ERROR\|INVALID_OBJECT\n` | `INVALID_OBJECT` |
| **17** | ERROR: OP INVÁLIDA | `LIST\|SEARCH` no existe: SEARCH pertenece solo a TREE. | `LIST\|SEARCH\|1\|5\n` | `ERROR\|INVALID_OPERATION\n` | `INVALID_OPERATION` |
| **18** | ERROR: SERVER | El slot 256 está ocupado; no hay slots libres para crear una instancia más. | `LIST\|CREATE\|0\|\n` | `ERROR\|SERVER_ERROR\n` | `SERVER_ERROR` |
