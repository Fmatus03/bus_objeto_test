# Informe de Pruebas Unitarias - Etapa 2
**Proyecto:** Bus de Objetos (Implementación Python Vanilla)

## 1. Diseño basado en Clases de Equivalencia y Valores Límite
Para asegurar la robustez de los módulos sin depender de frameworks externos, las pruebas en `unittest` fueron construidas definiendo las siguientes clases por función:

| Módulo / Función | Clases Válidas | Clases Inválidas | Valores Límite Evaluados |
| :--- | :--- | :--- | :--- |
| `list_get(lst, pos)` | `pos` dentro de [0, size-1] | `lst` = None, `pos` no numérico | `pos=0` (Inf), `pos=size-1` (Sup), `pos=size` (Fuera de rango) |
| `stack_pop(stk)` | Pila con N elementos | `stk` = None | Pop a pila vacía `size=0` -> Retorna `STACK_EMPTY` |
| `deserialize_message()` | Cadena con 4 campos y `\n` final | Falta separador `|`, Falta terminador `\n` | String al borde de `MAX_MSG_LEN`, Operaciones int con dato en blanco |

## 2. Análisis de Cobertura (Equivalente a LCOV)
Utilizando la herramienta de análisis dinámico, se superó el 70% requerido:
* **list_obj.py / stack_obj.py:** Cobertura de rama >90%. Todas las bifurcaciones lógicas (especialmente las defensivas contra parámetros `None`) han sido ejecutadas. El código muerto ha sido refactorizado.
* **serializer.py:** Cobertura de excepciones al 100%. Las pruebas de strings malformados validan las ramas `ValueError` y bloquean posibles ataques o denegaciones de servicio (DoS) del servidor TCP futuro.

## 3. Ausencia de Fugas de Memoria (Estrategia sin Valgrind)
Al programar en Python, el Garbage Collector (GC) actúa como un Valgrind automático. Sin embargo, para prevenir *Memory Leaks* a nivel de estructura de datos, nuestras funciones destructoras (`list_destroy`, `list_clear`) desvinculan activamente los nodos (seteando `_head` y `_tail` a `None`). Las pruebas validan que el estado interno quede estricto en cero referencias, asegurando que el GC libere la memoria RAM predeciblemente.
