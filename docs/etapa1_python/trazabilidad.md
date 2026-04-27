# Matriz de Trazabilidad RF → Casos de Prueba
**Etapa 1 — Bus de Objetos en C**

Cobertura: 100% de los RF. Mínimo 5 casos de prueba por requisito.  
Tipos: **U**=Unitaria · **I**=Integración · **S**=Sistema · **A**=Aceptación

---

## RF-001 — Crear Lista

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-001-1 | CREATE exitoso: servidor retorna ID entero ≥ 0 | I | Enviar `LIST\|CREATE\|0\|` al dispatcher con mock de object_server; verificar que la respuesta es `OK\|<n>` con n entero. |
| TC-001-2 | IDs únicos: dos CREATE consecutivos retornan IDs distintos | I | Dos llamadas a `object_server_create(OBJ_LIST)`; assert(id1 != id2). |
| TC-001-3 | Límite máximo: CREATE cuando ya hay 256 instancias retorna SERVER_ERROR | S | Pre-crear 256 instancias, luego enviar CREATE vía TCP; verificar `ERROR\|SERVER_ERROR`. |
| TC-001-4 | Slot marcado activo: tras CREATE, `slots[id].active == 1` | U | Llamar `object_server_create(OBJ_LIST)`, luego inspeccionar el arreglo interno con función de test. |
| TC-001-5 | Puntero no nulo: `slots[id].ptr != NULL` tras CREATE | U | Misma ejecución que TC-001-4; assert(slots[id].ptr != NULL). |
| TC-001-6 | CREATE concurrente: 10 hilos simultáneos obtienen IDs distintos | S | `test_concurrency.c`: 10 pthread crean listas simultáneamente; verificar que los 10 IDs son únicos. |

---

## RF-002 — Insertar en Lista

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-002-1 | INSERT válido: valor agregado al final, size se incrementa | U | `list_insert(list, 42)`; assert(list->size == 1 && list_get retorna 42 en pos 0). |
| TC-002-2 | INSERT múltiple: orden de inserción preservado (FIFO) | U | Insertar 10, 20, 30; GET en pos 0,1,2 retorna 10,20,30 respectivamente. |
| TC-002-3 | INSERT con ID inexistente: retorna INSTANCE_NOT_FOUND | I | Enviar `LIST\|INSERT\|999\|5\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-002-4 | INSERT con dato no numérico: retorna INVALID_MESSAGE | I | Enviar `LIST\|INSERT\|1\|abc\n`; el deserializer detecta el error; verificar `ERROR\|INVALID_MESSAGE`. |
| TC-002-5 | INSERT en lista recién creada (size=0, primera inserción) | U | `list_create()` seguido de `list_insert(list, 0)`; assert(list->size == 1). |
| TC-002-6 | INSERT valor negativo válido (-2147483648) | U | `list_insert(list, INT_MIN)`; `list_get(list, 0, &out)`; assert(out == INT_MIN). |

---

## RF-003 — Obtener Elemento de Lista

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-003-1 | GET en posición 0 (primer elemento) | U | Insertar 77; `list_get(list, 0, &out)`; assert(out == 77). |
| TC-003-2 | GET en posición size-1 (último elemento) | U | Insertar {1,2,3}; `list_get(list, 2, &out)`; assert(out == 3). |
| TC-003-3 | GET con índice == size: retorna OUT_OF_BOUNDS | U | Lista de 3 elementos; `list_get(list, 3, &out)`; assert retorno == LIST_OUT_OF_BOUNDS. |
| TC-003-4 | GET con índice negativo (-1): retorna OUT_OF_BOUNDS | U | `list_get(list, -1, &out)`; assert retorno == LIST_OUT_OF_BOUNDS. |
| TC-003-5 | GET con ID inexistente vía protocolo: retorna INSTANCE_NOT_FOUND | I | Enviar `LIST\|GET\|999\|0\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-003-6 | GET end-to-end vía TCP: valor correcto recibido por cliente | S | Flujo completo: CREATE → INSERT(42) → GET(0); cliente verifica `OK\|42\n`. |

---

## RF-004 — Remover Elemento de Lista

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-004-1 | REMOVE en posición 0: head actualizado correctamente | U | {10,20,30}; `list_remove(list,0)`; GET(0) retorna 20, size==2. |
| TC-004-2 | REMOVE en posición size-1: tail actualizado correctamente | U | {10,20,30}; `list_remove(list,2)`; GET(1) retorna 20, size==2. |
| TC-004-3 | REMOVE en posición media: reenlace correcto | U | {10,20,30}; `list_remove(list,1)`; GET(0)=10, GET(1)=30, size==2. |
| TC-004-4 | REMOVE con índice == size: retorna OUT_OF_BOUNDS | U | `list_remove(list, 3)` en lista de 3; assert retorno == LIST_OUT_OF_BOUNDS. |
| TC-004-5 | REMOVE con ID inexistente: retorna INSTANCE_NOT_FOUND | I | Enviar `LIST\|REMOVE\|999\|0\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-004-6 | REMOVE libera memoria: Valgrind no reporta leak tras remove | U | `list_remove` + `list_destroy`; ejecutar con Valgrind `--leak-check=full`; 0 bytes perdidos. |

---

## RF-005 — Tamaño de Lista

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-005-1 | SIZE de lista vacía recién creada: retorna 0 | U | `list_create()`; `list_size(list)` == 0. |
| TC-005-2 | SIZE tras 5 inserciones: retorna 5 | U | 5 × `list_insert`; `list_size(list)` == 5. |
| TC-005-3 | SIZE consistente tras INSERT+REMOVE: retorna n correcto | U | 3 inserts, 1 remove; `list_size` == 2. |
| TC-005-4 | SIZE con ID inexistente: retorna INSTANCE_NOT_FOUND | I | Enviar `LIST\|SIZE\|999\|\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-005-5 | SIZE end-to-end vía TCP | S | CREATE → 3×INSERT → SIZE vía socket; cliente verifica `OK\|3\n`. |

---

## RF-006 — Contiene Elemento en Lista

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-006-1 | CONTAINS con valor presente: retorna TRUE | U | {10,20,30}; `list_contains(list, 20)` == 1 (TRUE). |
| TC-006-2 | CONTAINS con valor ausente: retorna FALSE | U | {10,20,30}; `list_contains(list, 99)` == 0 (FALSE). |
| TC-006-3 | CONTAINS en lista vacía: retorna FALSE (no es error) | U | `list_create()`; `list_contains(list, 5)` == 0; size permanece 0. |
| TC-006-4 | CONTAINS con ID inexistente: retorna INSTANCE_NOT_FOUND | I | Enviar `LIST\|CONTAINS\|999\|5\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-006-5 | CONTAINS end-to-end vía TCP | S | CREATE → INSERT(42) → CONTAINS(42); cliente verifica `OK\|TRUE\n`. |

---

## RF-007 — Limpiar Lista (CLEAR)

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-007-1 | CLEAR en lista con 5 elementos: size queda en 0 | U | 5×insert; `list_clear(list)`; `list_size(list)` == 0. |
| TC-007-2 | CLEAR libera todos los nodos: Valgrind sin leaks | U | 5×insert; `list_clear(list)`; `list_destroy(list)`; Valgrind 0 bytes perdidos. |
| TC-007-3 | CLEAR es idempotente en lista vacía | U | `list_create()`; `list_clear(list)` dos veces; sin crash, size == 0. |
| TC-007-4 | CLEAR con ID inexistente: retorna INSTANCE_NOT_FOUND | I | Enviar `LIST\|CLEAR\|999\|\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-007-5 | POST-CLEAR: lista usable para nuevas inserciones | U | CLEAR; luego `list_insert(list,1)`; size == 1. |
| TC-007-6 | CLEAR end-to-end vía TCP | S | CREATE→3×INSERT→CLEAR→SIZE; cliente verifica `OK\|0\n`. |

---

## RF-008 — Crear Pila

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-008-1 | CREATE Stack exitoso: retorna ID ≥ 0 | I | `object_server_create(OBJ_STACK)`; assert(id >= 0). |
| TC-008-2 | Stack creado con size=0 y top=NULL | U | `stack_create()`; assert(s->size==0 && s->top==NULL). |
| TC-008-3 | IDs únicos entre Stack y List en misma sesión | I | CREATE LIST → CREATE STACK; los IDs son distintos. |
| TC-008-4 | CREATE con slots llenos: retorna SERVER_ERROR | S | 256 instancias activas; enviar STACK CREATE; verificar `ERROR\|SERVER_ERROR`. |
| TC-008-5 | CREATE concurrente: 10 hilos crean stacks, IDs únicos | S | `test_concurrency.c`; 10 hilos; assert todos los IDs distintos. |

---

## RF-009 — Push en Pila

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-009-1 | PUSH válido: size se incrementa a 1 | U | `stack_push(s, 42)`; assert(s->size == 1). |
| TC-009-2 | PUSH múltiple: orden LIFO verificado con POP | U | push(10),push(20),push(30); pop retorna 30,20,10. |
| TC-009-3 | PUSH valor INT_MAX | U | `stack_push(s, INT_MAX)`; `stack_pop(s, &out)`; assert(out == INT_MAX). |
| TC-009-4 | PUSH con ID inexistente: INSTANCE_NOT_FOUND | I | `STACK\|PUSH\|999\|5\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-009-5 | PUSH dato no numérico: INVALID_MESSAGE | I | `STACK\|PUSH\|1\|xyz\n`; verificar `ERROR\|INVALID_MESSAGE`. |
| TC-009-6 | PUSH end-to-end vía TCP | S | CREATE→PUSH(7)→PEEK; cliente verifica `OK\|7\n`. |

---

## RF-010 — Pop en Pila

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-010-1 | POP retorna valor del tope y decrementa size | U | push(5); `stack_pop(s,&out)`; assert(out==5 && s->size==0). |
| TC-010-2 | POP LIFO: secuencia push(1,2,3) → pop retorna 3,2,1 | U | Tres pushes; tres pops; verificar orden inverso. |
| TC-010-3 | POP en pila vacía: retorna EMPTY_STRUCTURE | U | `stack_create()`; `stack_pop(s,&out)`; assert retorno == STACK_EMPTY. |
| TC-010-4 | POP con ID inexistente: INSTANCE_NOT_FOUND | I | `STACK\|POP\|999\|\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-010-5 | POP libera nodo: Valgrind sin leaks | U | push+pop+destroy; Valgrind 0 bytes perdidos. |
| TC-010-6 | POP end-to-end vía TCP | S | CREATE→PUSH(42)→POP; cliente verifica `OK\|42\n`. |

---

## RF-011 — Peek en Pila

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-011-1 | PEEK retorna valor sin modificar size | U | push(99); peek retorna 99; size sigue siendo 1. |
| TC-011-2 | PEEK tras múltiples pushes: retorna el último push | U | push(1,2,3); peek retorna 3. |
| TC-011-3 | PEEK en pila vacía: retorna EMPTY_STRUCTURE | U | `stack_create()`; `stack_peek(s,&out)`; assert == STACK_EMPTY. |
| TC-011-4 | PEEK con ID inexistente: INSTANCE_NOT_FOUND | I | `STACK\|PEEK\|999\|\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-011-5 | PEEK no altera estado: POP posterior retorna mismo valor | U | push(7); peek; pop retorna 7. |

---

## RF-012 — ¿Pila Vacía? (IS_EMPTY)

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-012-1 | IS_EMPTY en pila recién creada: retorna TRUE | U | `stack_create()`; `stack_is_empty(s)` == 1. |
| TC-012-2 | IS_EMPTY tras PUSH: retorna FALSE | U | push(1); `stack_is_empty(s)` == 0. |
| TC-012-3 | IS_EMPTY tras PUSH+POP completo: retorna TRUE | U | push(1); pop; `stack_is_empty(s)` == 1. |
| TC-012-4 | IS_EMPTY con ID inexistente: INSTANCE_NOT_FOUND | I | `STACK\|IS_EMPTY\|999\|\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-012-5 | IS_EMPTY end-to-end vía TCP | S | CREATE→IS_EMPTY; cliente verifica `OK\|TRUE\n`. |

---

## RF-013 — Crear Árbol BST

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-013-1 | CREATE Tree exitoso: retorna ID ≥ 0 | I | `object_server_create(OBJ_TREE)`; assert(id >= 0). |
| TC-013-2 | Tree creado con root=NULL y size=0 | U | `tree_create()`; assert(t->root==NULL && t->size==0). |
| TC-013-3 | IDs únicos entre Tree, Stack y List | I | CREATE LIST, CREATE STACK, CREATE TREE; los 3 IDs distintos. |
| TC-013-4 | CREATE con slots llenos: SERVER_ERROR | S | 256 instancias; TREE CREATE → `ERROR\|SERVER_ERROR`. |
| TC-013-5 | CREATE concurrente: 10 hilos crean trees, IDs únicos | S | `test_concurrency.c`; 10 hilos; IDs únicos verificados. |

---

## RF-014 — Insertar en Árbol

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-014-1 | INSERT mantiene propiedad BST: menor a izquierda, mayor a derecha | U | insert(5,3,7); verificar root=5, root->left->data=3, root->right->data=7. |
| TC-014-2 | INSERT valor duplicado: retorna DUPLICATE_VALUE | U | insert(5); insert(5); assert retorno == TREE_DUPLICATE. |
| TC-014-3 | INSERT con ID inexistente: INSTANCE_NOT_FOUND | I | `TREE\|INSERT\|999\|5\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-014-4 | INSERT valor mínimo (INT_MIN) y máximo (INT_MAX) en mismo árbol | U | insert(INT_MIN); insert(INT_MAX); SEARCH ambos retorna TRUE. |
| TC-014-5 | INSERT incrementa size correctamente | U | 5 inserts de valores distintos; assert(t->size == 5). |
| TC-014-6 | INSERT end-to-end vía TCP + SEARCH verifica inserción | S | CREATE→INSERT(10)→SEARCH(10); cliente verifica `OK\|TRUE\n`. |

---

## RF-015 — Buscar en Árbol

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-015-1 | SEARCH de valor existente: retorna TRUE | U | insert(5); `tree_search(t,5)` == 1. |
| TC-015-2 | SEARCH de valor inexistente: retorna FALSE | U | insert(5); `tree_search(t,9)` == 0. |
| TC-015-3 | SEARCH en árbol vacío: retorna FALSE (no error) | U | `tree_create()`; `tree_search(t,1)` == 0; sin crash. |
| TC-015-4 | SEARCH con ID inexistente: INSTANCE_NOT_FOUND | I | `TREE\|SEARCH\|999\|5\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-015-5 | SEARCH end-to-end vía TCP: valor no insertado → FALSE | S | CREATE→SEARCH(99); cliente verifica `OK\|FALSE\n`. |

---

## RF-016 — Eliminar Nodo de Árbol

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-016-1 | DELETE nodo hoja: BST válido tras eliminación | U | insert(5,3,7); delete(3); SEARCH(3)==FALSE; SEARCH(5)==TRUE. |
| TC-016-2 | DELETE nodo con un hijo: hijo adoptado por abuelo | U | insert(5,3,7,2); delete(3); SEARCH(2)==TRUE; SEARCH(3)==FALSE. |
| TC-016-3 | DELETE nodo con dos hijos: sucesor inorden correcto | U | insert(5,3,7,6,9); delete(7); INORDER retorna "3,5,6,9". |
| TC-016-4 | DELETE valor inexistente: retorna NOT_FOUND | U | insert(5); `tree_delete(t,99)`; assert retorno == -1. |
| TC-016-5 | DELETE con ID inexistente: INSTANCE_NOT_FOUND | I | `TREE\|DELETE\|999\|5\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-016-6 | DELETE libera memoria: Valgrind sin leaks | U | insert+delete+destroy; Valgrind 0 bytes perdidos. |

---

## RF-017 — Recorrido Inorden del Árbol

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-017-1 | INORDER retorna valores en orden ascendente | U | insert(5,3,8,1,4); `tree_inorder` retorna arr={1,3,4,5,8}. |
| TC-017-2 | INORDER en árbol vacío: retorna cadena vacía, sin crash | U | `tree_create()`; `tree_inorder(t,arr,&count)`; count==0. |
| TC-017-3 | INORDER de árbol con un solo nodo | U | insert(42); INORDER retorna "42". |
| TC-017-4 | INORDER con ID inexistente: INSTANCE_NOT_FOUND | I | `TREE\|INORDER\|999\|\n`; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-017-5 | INORDER end-to-end vía TCP: CSV correcto | S | CREATE→INSERT(5,3,8,1,4)→INORDER; cliente verifica `OK\|1,3,4,5,8\n`. |

---

## RF-018 — Objeto de Tipo Inválido

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-018-1 | Objeto "QUEUE": retorna INVALID_OBJECT | I | Enviar `QUEUE\|CREATE\|0\|\n`; verificar `ERROR\|INVALID_OBJECT`. |
| TC-018-2 | Objeto "MAP": retorna INVALID_OBJECT | I | Enviar `MAP\|GET\|1\|0\n`; verificar `ERROR\|INVALID_OBJECT`. |
| TC-018-3 | Objeto vacío "": retorna INVALID_MESSAGE | I | Enviar `\|INSERT\|1\|5\n`; verificar `ERROR\|INVALID_MESSAGE`. |
| TC-018-4 | Servidor no crashea ante objeto inválido | S | Enviar 100 mensajes con objetos inválidos vía TCP; servidor sigue respondiendo. |
| TC-018-5 | deserialize_message retorna -1 para objeto desconocido | U | `deserialize_message("QUEUE\|CREATE\|0\|\n", &msg)` retorna -1. |

---

## RF-019 — Operación No Soportada

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-019-1 | `LIST\|SEARCH`: LIST no tiene SEARCH → INVALID_OPERATION | I | Enviar `LIST\|SEARCH\|1\|5\n`; verificar `ERROR\|INVALID_OPERATION`. |
| TC-019-2 | `TREE\|POP`: TREE no tiene POP → INVALID_OPERATION | I | Enviar `TREE\|POP\|1\|\n`; verificar `ERROR\|INVALID_OPERATION`. |
| TC-019-3 | `STACK\|INORDER`: STACK no tiene INORDER → INVALID_OPERATION | I | Enviar `STACK\|INORDER\|1\|\n`; verificar `ERROR\|INVALID_OPERATION`. |
| TC-019-4 | Estado del objeto no modificado tras INVALID_OPERATION | I | LIST con 3 elementos; enviar LIST\|POP; SIZE sigue retornando 3. |
| TC-019-5 | Servidor no crashea ante operación inválida | S | 100 operaciones inválidas vía TCP; servidor continúa operativo. |

---

## RF-020 — Mensaje con Formato Inválido

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-020-1 | Sin separadores: `LISTINSERT142` → INVALID_MESSAGE | U | `deserialize_message("LISTINSERT142", &msg)` retorna -1. |
| TC-020-2 | Sin terminador `\n`: bloqueo o timeout | U | `deserialize_message("LIST\|INSERT\|1\|42", &msg)` retorna -1. |
| TC-020-3 | Campo ID no numérico: `LIST\|GET\|abc\|0\n` → INVALID_MESSAGE | U | `deserialize_message("LIST\|GET\|abc\|0\n", &msg)` retorna -1. |
| TC-020-4 | Solo 2 campos: `LIST\|INSERT\n` → INVALID_MESSAGE | U | `deserialize_message("LIST\|INSERT\n", &msg)` retorna -1. |
| TC-020-5 | Hilo cliente continúa activo tras INVALID_MESSAGE | S | Enviar mensaje inválido; luego enviar `LIST\|CREATE\|0\|\n`; servidor responde correctamente. |
| TC-020-6 | Buffer overflow: mensaje > MAX_MSG_LEN → INVALID_MESSAGE | S | Enviar cadena de 2048 chars; servidor responde `ERROR\|INVALID_MESSAGE` sin crash. |

---

## RF-021 — Destrucción de Instancia

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-021-1 | DESTROY: slot marcado inactivo tras destrucción | U | `object_server_create` + `object_server_destroy_instance(id)`; slots[id].active == 0. |
| TC-021-2 | DESTROY: GET posterior retorna INSTANCE_NOT_FOUND | I | Crear instancia, destruirla; enviar GET con el mismo ID; verificar `ERROR\|INSTANCE_NOT_FOUND`. |
| TC-021-3 | DESTROY libera toda la memoria (Valgrind) | U | Crear List con 10 nodos; destroy_instance; Valgrind 0 bytes perdidos. |
| TC-021-4 | DESTROY de ID inexistente retorna -1 | U | `object_server_destroy_instance(999)` retorna -1. |
| TC-021-5 | DESTROY concurrente: dos hilos intentan destruir el mismo ID | S | Hilo A y B llaman destroy_instance(id) simultáneamente; solo uno tiene éxito, no hay double-free. Helgrind limpio. |

---

## RF-022 — Concurrencia de Múltiples Clientes

| ID Caso | Descripción | Tipo | Estrategia de Verificación |
|---|---|:---:|---|
| TC-022-1 | 10 clientes simultáneos: cada uno recibe sus propias respuestas | S | `test_concurrency.c`: 10 pthread_t clientes; verificar que los IDs recibidos coinciden con los solicitados. |
| TC-022-2 | Helgrind: sin condiciones de carrera con 20 hilos | S | `valgrind --tool=helgrind ./build/test_concurrency`; 0 race conditions. |
| TC-022-3 | Desconexión abrupta de cliente: servidor continúa operativo | S | `kill -9` a proceso cliente; verificar que el servidor acepta y responde a nuevas conexiones. |
| TC-022-4 | pthread_create falla: socket del cliente cerrado, servidor no crashea | U | Mock de pthread_create retornando EAGAIN; assert servidor continúa en bucle accept(). |
| TC-022-5 | 50 clientes simultáneos: 0% de respuestas mezcladas | S | 50 hilos cliente; cada uno verifica que los valores retornados corresponden a sus propias inserciones (aislamiento de instancias). |
| TC-022-6 | Size correcto con writes concurrentes en misma instancia | S | 10 hilos hacen INSERT sobre la misma lista; SIZE final == número de insertos exitosos. |
