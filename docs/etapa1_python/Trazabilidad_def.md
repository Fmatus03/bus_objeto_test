# Documentación Complementaria Etapa 1: Matriz de Trazabilidad (Entorno Python)

Este documento complementa a los Requisitos Funcionales y No Funcionales, aportando el artefacto de trazabilidad exigido por la rúbrica (adaptada a Python).

## Matriz de Trazabilidad (RF → Casos de Prueba)

Cobertura del 100% de los Requisitos Funcionales, detallando arneses de pruebas adaptados para un entorno de Python usando librerías como `pytest`, `socket` nativo y `threading`/`concurrent.futures`.

| ID RF | Descripción Corta | ID Caso de Prueba | Descripción del Caso de Prueba | Nivel de Prueba |
| :--- | :--- | :--- | :--- | :--- |
| **RF-001** | Crear Lista | CP-U-001 | Usar `pytest` para instanciar `object_server` y ejecutar `create("LIST")`, validando ID retornado con `assert` | Unitaria |
| **RF-001** | Crear Lista | CP-I-001 | Simular llamada en `dispatcher.py` con mensaje `LIST|CREATE`, verificando el registro en el diccionario de instancias | Integración |
| **RF-001** | Crear Lista | CP-S-001 | Cliente TCP (usando `socket`) envía trama `b"LIST|CREATE|0|\n"` y valida recepción de `b"OK|X\n"` | Sistema |
| **RF-002** | Insertar Lista | CP-U-002 | `test_list_insert()` validando que `len(list.elements) == 1` | Unitaria |
| **RF-002** | Insertar Lista | CP-S-002 | Cliente envía `b"LIST|INSERT|X|42\n"` y valida persistencia en servidor | Sistema |
| **RF-003** | Obtener Elemento | CP-U-003 | Prueba `test_list_get()` en una lista poblada usando un mock | Unitaria |
| **RF-004** | Remover Elemento | CP-U-004 | Ejecución de método `remove()` asertando reducción en propiedad `size` y estado interno | Unitaria |
| **RF-005** | Tamaño Lista | CP-U-005 | Asertar que el llamado a `get_size()` corresponde a `len(self.elements)` | Unitaria |
| **RF-006** | Contiene Elemento| CP-U-006 | Búsqueda booleana con operador `in` o recorrido de nodos, verificando `True`/`False` | Unitaria |
| **RF-007** | Limpiar Lista | CP-U-007 | Uso de `clear()`, verificando `size == 0` y validando liberación de memoria con `tracemalloc` | Unitaria |
| **RF-008** | Crear Pila | CP-U-008 | Instanciación comprobando tipado correcto (`isinstance(obj, Stack)`) en servidor | Unitaria |
| **RF-009** | Push Pila | CP-U-009 | Inserciones en pila seguidas de validación del último valor en `self.elements[-1]` | Unitaria |
| **RF-010** | Pop Pila | CP-U-010 | Asertar extracción y control de excepciones (ej: `IndexError` mapeado a `EMPTY_STRUCTURE`) | Unitaria |
| **RF-011** | Peek Pila | CP-U-011 | `test_stack_peek()` verificando retorno de valor al tope sin modificar longitud | Unitaria |
| **RF-012** | Pila Vacía | CP-U-012 | `test_stack_is_empty()` iterando estados de vaciado en bucle | Unitaria |
| **RF-013** | Crear Árbol | CP-U-013 | Instanciación de `Tree()` asertando raíz en `None` | Unitaria |
| **RF-014** | Insertar Árbol | CP-U-014 | `test_tree_insert()` validando referencias cruzadas en el árbol izquierdo/derecho | Unitaria |
| **RF-015** | Buscar Árbol | CP-I-002 | Inyección de buffer `TREE|SEARCH` al dispatcher simulado, verificando retorno booleano | Integración |
| **RF-016** | Eliminar Árbol | CP-U-015 | Validar la lógica de reasignación del nodo sucesor en eliminaciones complejas (2 hijos) | Unitaria |
| **RF-017** | Inorden Árbol | CP-S-003 | Cliente inserta múltiples ramas y evalúa retorno de strings separados por comas | Sistema |
| **RF-018** | Límite Instancia | CP-S-004 | Script con `asyncio` o *threads* saturando `MAX_INSTANCES` para comprobar rechazo seguro | Sistema |
| **RF-019** | Eliminar Inst. | CP-I-003 | Llamado de destrucción asertando `KeyError` o respuesta `INSTANCE_NOT_FOUND` tras la purga | Integración |
| **RF-020** | Bloqueo (Mutex) | CP-I-004 | `ThreadPoolExecutor` lanzando inserciones asíncronas y verificando integridad protegida por `threading.Lock` | Integración |
