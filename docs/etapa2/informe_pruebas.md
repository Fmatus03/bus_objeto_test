# Informe de Pruebas Unitarias - Etapa 2
**Proyecto:** Bus de Objetos (Implementación Python Vanilla)

## 1. Diseño basado en Clases de Equivalencia y Valores Límite
Para asegurar la robustez de los módulos sin depender de frameworks externos, las pruebas en `unittest` fueron construidas definiendo las siguientes clases por función:

| Módulo / Función | Clases Válidas | Clases Inválidas | Valores Límite Evaluados |
| :--- | :--- | :--- | :--- |
| `list_get(lst, pos)` | `pos` dentro de [0, size-1] | `lst` = None, `pos` no numérico | `pos=0` (Inf), `pos=size-1` (Sup), `pos=size` (Fuera de rango) |
| `stack_pop(stk)` | Pila con N elementos | `stk` = None | Pop a pila vacía `size=0` -> Retorna `STACK_EMPTY` |
| `deserialize_message()` | Cadena con 4 campos y `\n` final | Falta separador `|`, Falta terminador `\n` | String al borde de `MAX_MSG_LEN`, Operaciones int con dato en blanco |

## 2. Análisis de Cobertura (Reporte equivalente a LCOV/GCOV)
Tras ejecutar `coverage run` y analizar el reporte HTML generado, obtuvimos un **97% de cobertura total**.

**¿Qué líneas o ramas no están cubiertas?**
* **`list_obj.py` y `stack_obj.py`**: Tienen **100% de cobertura**. Todas las ramas de inserción, extracción, límites y validación de nulos (`None`) fueron visitadas.
* **`serializer.py`**: Tiene **81% de cobertura**. Las líneas no cubiertas (99, 104, 109, 112-113, 115, 122, 127, 134-139) corresponden a ramas defensivas profundas del método `deserialize_message()`, específicamente las bifurcaciones `except ValueError` ocultas y validaciones anidadas del `<ID_INSTANCIA>`.

**¿Qué casos de prueba agregarías para mejorar la cobertura?**
Para alcanzar el 100% en el serializador agregaría 3 casos específicos:
1. Una trama con objeto válido pero ID de instancia negativo explícito (`LIST|INSERT|-10|42`).
2. Una trama con ID que excede los límites manejables por int.
3. Un caso donde la operación NO requiera un entero (ej. `POP`), pero `<DATO>` sea un número válido, forzando a que entre por la rama condicional de auto-casteo de enteros.

**¿Hay código muerto?**
**No hay código muerto real**. El 100% de las funciones escritas se invocan. Sin embargo, en `serializer.py`, la rama `except ValueError` tras el `isdigit()` se comporta de forma casi redundante, ya que la comprobación previa bloquea el paso de strings puros; se podría considerar "código inalcanzable" por diseño defensivo.

## 3. Ausencia de Fugas de Memoria (Estrategia sin Valgrind)
Al programar en Python, el Garbage Collector (GC) actúa como un Valgrind automático. Sin embargo, para prevenir *Memory Leaks* a nivel de estructura de datos, nuestras funciones destructoras (`list_destroy`, `list_clear`) desvinculan activamente los nodos (seteando `_head` y `_tail` a `None`). Las pruebas validan que el estado interno quede estricto en cero referencias, asegurando que el GC libere la memoria RAM predeciblemente.
