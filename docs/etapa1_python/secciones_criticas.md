# Análisis de Secciones Críticas — Concurrencia con pthreads
**Etapa 1 — Pruebas Estáticas y Especificación del Protocolo**  
Curso: Pruebas de Software | Proyecto: Bus de Objetos (C99 + TCP/IP + pthreads)

---

## Introducción

El Bus de Objetos implementa una arquitectura servidor TCP multihilo: por cada cliente aceptado con `accept()`, el servidor crea un hilo POSIX independiente mediante `pthread_create()`. Todos estos hilos comparten el mismo espacio de memoria del proceso, en particular el arreglo global `slots[MAX_INSTANCES]` de `object_server.c` y el `pthread_mutex_t server_mutex` que lo protege.

Este análisis estático identifica las regiones del código donde datos compartidos entre hilos pueden ser accedidos concurrentemente (secciones críticas), justifica por qué representan un riesgo de **race condition** o **data corruption**, y propone el mecanismo de sincronización concreto a implementar con la API POSIX de pthreads.

> **Restricción del proyecto:** No se utilizan frameworks externos. Todo el mecanismo de sincronización se construye con primitivas POSIX nativas: `pthread_mutex_t`, `pthread_mutex_lock()`, `pthread_mutex_unlock()`, `pthread_mutex_init()` y `pthread_mutex_destroy()`.

---

## Sección Crítica 1 — Asignación de Nuevo Slot en `object_server_create()`

### Datos compartidos
- Arreglo global `static ObjectSlot slots[MAX_INSTANCES]` en `object_server.c`.
- Iteración sobre `slots[i].active` para encontrar un slot libre.

### ¿Por qué es crítica?
Cuando dos hilos de cliente envían simultáneamente `LIST|CREATE` o `STACK|CREATE`, ambos ejecutan `object_server_create()` de manera concurrente. El patrón de acceso peligroso es:

```c
// Hilo A y Hilo B ejecutan simultáneamente:
for (int i = 0; i < MAX_INSTANCES; i++) {
    if (slots[i].active == 0) {   // ← Ambos leen slots[i].active == 0
        slots[i].active = 1;      // ← Ambos escriben active = 1 sobre el MISMO slot
        slots[i].ptr = list_create();
        id = i;
        break;
    }
}
```

**Escenario de corrupción:** El planificador del SO puede interrumpir al Hilo A justo después de la lectura `slots[i].active == 0` y antes de la escritura `slots[i].active = 1`. El Hilo B se ejecuta, también lee `slots[i].active == 0`, asigna el slot, y retorna el mismo ID al cliente B. Al reactivarse, el Hilo A sobreescribe el mismo slot, corrompiendo la instancia del cliente B. Ambos clientes creen tener IDs distintos pero manipulan el mismo objeto.

### Mecanismo de Sincronización Propuesto
```c
int object_server_create(ObjectType type) {
    int id = -1;
    pthread_mutex_lock(&server_mutex);   /* Adquiere el mutex: exclusión mutua garantizada */
    for (int i = 0; i < MAX_INSTANCES; i++) {
        if (slots[i].active == 0) {
            /* Solo UN hilo puede estar aquí a la vez */
            slots[i].ptr    = /* list_create() / stack_create() / tree_create() según type */;
            slots[i].type   = type;
            slots[i].active = 1;
            id = i;
            break;
        }
    }
    pthread_mutex_unlock(&server_mutex); /* Libera el mutex: otros hilos pueden continuar */
    return id;
}
```
El bloque completo de búsqueda + asignación es atómico. Con `server_mutex` inicializado en `object_server_init()` con `pthread_mutex_init(&server_mutex, NULL)`, se garantiza que solo un hilo a la vez puede modificar el arreglo `slots`.

---

## Sección Crítica 2 — Operaciones de Mutación sobre Estructuras Compartidas

### Datos compartidos
- Los campos internos de los objetos: `List->head`, `List->tail`, `List->size`; `Stack->top`, `Stack->size`; `Tree->root`, `Tree->size`.
- Cualquier instancia a la que dos clientes distintos tengan el mismo ID (posible si un cliente comparte el ID a otro).

### ¿Por qué es crítica?
Las operaciones `INSERT`, `REMOVE`, `PUSH`, `POP`, `DELETE` y `CLEAR` modifican múltiples campos de la estructura en secuencia. En C, estas operaciones **no son atómicas** incluso en arquitecturas modernas. Ejemplo con `list_insert()`:

```c
// Operación no protegida sobre la misma instancia List* desde dos hilos:
// Hilo A: list_insert(list, 10)
//   1. Aloja new_node = malloc(sizeof(ListNode))
//   2. new_node->data = 10
//   3. list->tail->next = new_node   ← Hilo B interrumpe aquí
// Hilo B: list_insert(list, 20)
//   3. list->tail->next = new_node_B  ← Sobreescribe el puntero de Hilo A
//   4. list->tail = new_node_B
//   5. list->size++
// Hilo A reanuda:
//   4. list->tail = new_node_A       ← new_node_B queda desvinculado → memory leak
//   5. list->size++                  ← size = 2, pero solo hay 1 nodo accesible
```

**Consecuencias:** nodos huérfanos (memory leak), `size` inconsistente, undefined behavior al acceder a memoria liberada.

### Mecanismo de Sincronización Propuesto
El `dispatcher.c` adquiere `server_mutex` **antes** de obtener el puntero al objeto y lo libera **después** de completar la operación. La función `object_server_lock()` / `object_server_unlock()` expone esta API al dispatcher:

```c
static void dispatch_list(const BusMessage *msg, BusResponse *resp) {
    List *list = NULL;
    void *ptr  = NULL;

    object_server_lock();                         /* pthread_mutex_lock(&server_mutex) */
    if (object_server_get(msg->instance_id, OBJ_LIST, &ptr) != 0) {
        snprintf(resp->payload, sizeof(resp->payload), "INSTANCE_NOT_FOUND");
        object_server_unlock();
        return;
    }
    list = (List *)ptr;

    switch (msg->operation) {
        case OP_INSERT: list_insert(list, msg->data_int); resp->success = 1; break;
        case OP_REMOVE: /* ... */ break;
        /* ... */
    }
    object_server_unlock();                       /* pthread_mutex_unlock(&server_mutex) */
}
```

> **Nota de diseño:** Se usa un **único mutex global** para simplificar la etapa de diseño estático y evitar deadlocks por orden incorrecto de adquisición de múltiples mutexes. Una mejora futura (Etapa 3) puede migrar a un mutex por instancia para mayor paralelismo.

---

## Sección Crítica 3 — Destrucción de Instancia con Acceso Concurrente

### Datos compartidos
- El slot `slots[id]` en `object_server.c`: su campo `active` y el puntero `ptr`.

### ¿Por qué es crítica?
Considera el siguiente escenario con dos hilos sobre el mismo ID:

| Tiempo | Hilo A (DESTROY ID=5) | Hilo B (GET ID=5) |
|:---:|:---|:---|
| t1 | Lee `slots[5].active == 1` | — |
| t2 | Llama `list_destroy(slots[5].ptr)` → libera todos los nodos | — |
| t3 | — | Lee `slots[5].active == 1` (aún no actualizado) |
| t4 | `slots[5].active = 0; slots[5].ptr = NULL` | — |
| t5 | — | Desreferencia `slots[5].ptr` → **USE-AFTER-FREE / SIGSEGV** |

El uso de memoria liberada (`use-after-free`) produce comportamiento indefinido: el proceso puede crashear (`SIGSEGV`) o, peor aún, retornar datos de otra instancia que reutilizó esa memoria.

### Mecanismo de Sincronización Propuesto
```c
int object_server_destroy_instance(int id) {
    int result = -1;
    pthread_mutex_lock(&server_mutex);    /* Sección crítica: ningún otro hilo puede acceder a slots */
    if (id >= 0 && id < MAX_INSTANCES && slots[id].active == 1) {
        /* Liberar los nodos según el tipo */
        switch (slots[id].type) {
            case OBJ_LIST:  list_destroy((List *)slots[id].ptr);   break;
            case OBJ_STACK: stack_destroy((Stack *)slots[id].ptr); break;
            case OBJ_TREE:  tree_destroy((Tree *)slots[id].ptr);   break;
        }
        slots[id].ptr    = NULL;  /* Evitar dangling pointer */
        slots[id].active = 0;
        result = 0;
    }
    pthread_mutex_unlock(&server_mutex);  /* Slot ya inactivo: lecturas posteriores retornan INSTANCE_NOT_FOUND */
    return result;
}
```
La atomicidad garantiza que, una vez liberada la memoria y marcado `active = 0`, cualquier hilo que intente `object_server_get(id, ...)` obtendrá -1 (INSTANCE_NOT_FOUND) de manera limpia.

---

## Sección Crítica 4 — Recorrido Inorden del Árbol con Modificación Concurrente

### Datos compartidos
- El árbol BST completo (`Tree->root` y toda la red de punteros `TreeNode->left`, `->right`).

### ¿Por qué es crítica?
`tree_inorder()` es una operación de **lectura secuencial** que visita todos los nodos en orden ascendente usando recursión (o una pila auxiliar). Si mientras se ejecuta el recorrido, otro hilo realiza `tree_delete()` o `tree_insert()` sobre el **mismo árbol**, pueden ocurrir:

- **Nodo eliminado durante el recorrido:** El puntero `current->right` apunta a un nodo que ya fue liberado con `free()`. Al dereferenciarlo, el comportamiento es indefinido.
- **Rotación parcial del árbol:** Un `tree_insert()` concurrente puede rebalancear punteros a mitad del recorrido, haciendo que el iterador siga un camino inválido o entre en un ciclo infinito.

```c
// Escenario peligroso sin sincronización:
// Hilo A: tree_inorder() visita nodo con valor 7, avanza a 7->right (nodo 9)
// Hilo B: tree_delete(tree, 9) → free(nodo_9); nodo_7->right = NULL o sucesor
// Hilo A: dereferencia nodo_9 (ya liberado) → use-after-free
```

### Mecanismo de Sincronización Propuesto
El `dispatch_tree()` ya mantiene `server_mutex` durante toda la operación `INORDER`, bloqueando cualquier `INSERT` o `DELETE` concurrente sobre el mismo o cualquier otro objeto del servidor. Esta política de mutex global garantiza la atomicidad del recorrido:

```c
case OP_INORDER: {
    /* server_mutex ya adquirido por dispatch_tree() */
    int arr[MAX_INSTANCES];
    int count = 0;
    tree_inorder(tree, arr, &count);  /* Recorrido seguro: ningún DELETE puede interrumpir */
    /* Construir string CSV en resp->payload */
    /* ... */
    resp->success = 1;
    break;
}
/* server_mutex liberado al salir de dispatch_tree() */
```

---

## Resumen de Secciones Críticas

| ID | Sección Crítica | Datos Compartidos | Riesgo sin Sincronización | Mecanismo POSIX |
|:---:|:---|:---|:---|:---|
| SC-1 | Asignación de nuevo slot (`CREATE`) | `slots[]`, iteración sobre `active` | IDs duplicados; dos clientes con el mismo objeto | `pthread_mutex_lock/unlock(&server_mutex)` en `object_server_create()` |
| SC-2 | Mutación de estructuras (`INSERT/REMOVE/PUSH/POP/DELETE/CLEAR`) | Campos internos de `List*`, `Stack*`, `Tree*` | Corrupción de punteros, memory leak, `size` incorrecto | `object_server_lock/unlock()` en cada `dispatch_*()` |
| SC-3 | Destrucción de instancia (`DESTROY`) | `slots[id].active`, `slots[id].ptr` | Use-after-free, SIGSEGV, corrupción de heap | `pthread_mutex_lock/unlock(&server_mutex)` en `object_server_destroy_instance()` |
| SC-4 | Recorrido inorden (`INORDER`) | Red de punteros `TreeNode*` del BST | Use-after-free durante el recorrido, ciclo infinito | `server_mutex` mantenido durante toda la operación `INORDER` en `dispatch_tree()` |

### Inicialización y Destrucción del Mutex

```c
/* object_server_init() — llamado una sola vez al arrancar el servidor */
int object_server_init(void) {
    if (initialized) return -1;
    if (pthread_mutex_init(&server_mutex, NULL) != 0) return -1;
    memset(slots, 0, sizeof(slots));
    initialized = 1;
    return 0;
}

/* object_server_destroy() — llamado al apagar el servidor */
void object_server_destroy(void) {
    pthread_mutex_lock(&server_mutex);
    for (int i = 0; i < MAX_INSTANCES; i++) {
        if (slots[i].active) {
            /* liberar según type... */
            slots[i].active = 0;
            slots[i].ptr = NULL;
        }
    }
    pthread_mutex_unlock(&server_mutex);
    pthread_mutex_destroy(&server_mutex);
    initialized = 0;
}
```
