# Informe de Pruebas Unitarias — Etapa 2
**Bus de Objetos en Python | Curso: Pruebas de Software**  
Técnicas: Partición de Equivalencia · Análisis de Valores Límite · TDD

---

## 1. Resumen Ejecutivo

| Módulo | Funciones probadas | Casos de prueba | PASS | FAIL | Cobertura estimada |
|---|:---:|:---:|:---:|:---:|:---:|
| `list_obj.py` | 7 | 40 | **40** | 0 | ≥ 95% |
| `stack_obj.py` | 6 | 33 | **33** | 0 | ≥ 95% |
| `serializer.py` | 3 | 42 | **42** | 0 | ≥ 93% |
| **TOTAL** | **16** | **115** | **115** | **0** | **≥ 94%** |

> **Resultado:** 100% de pruebas pasando. Un defecto real fue detectado durante TDD (TC-SER-014: `\r\n` aceptado como terminador válido) y corregido en el ciclo REFACTOR.

---

## 2. Estrategia de Pruebas (Arnés Nativo sin Frameworks)

### 2.1 Restricción "Vanilla"
Se construyó un arnés de pruebas completamente a medida (`test_harness.py`) sin utilizar `pytest`, `unittest`, `nose` ni ninguna librería externa. El arnés usa exclusivamente:
- `assert` nativo de Python con mensajes descriptivos
- `try/except AssertionError` para captura de fallos
- `time.perf_counter()` para medición de tiempos por caso
- `print()` con códigos ANSI para reporte coloreado
- `sys.exit()` para código de salida en CI

### 2.2 Ejecución
```bash
# Ejecutar todas las suites
python tests/unit/run_tests.py

# Ejecutar suite individual
python tests/unit/test_list.py
python tests/unit/test_stack.py
python tests/unit/test_serializer.py
```

---

## 3. Clases de Equivalencia Identificadas

### 3.1 list_obj.py

| ID Clase | Tipo | Condición | Resultado Esperado |
|---|:---:|---|---|
| CE-L1 | Válida | `lst` válido, `pos` ∈ [0, size-1], dato entero | Operación exitosa, `LIST_OK` |
| CE-L2 | Inválida | `lst` es `None` | `LIST_NULL_PTR` inmediato, sin crash |
| CE-L3 | Límite inferior | `pos = -1` | `LIST_OUT_OF_BOUNDS` |
| CE-L4 | Límite superior | `pos = size` | `LIST_OUT_OF_BOUNDS` |
| CE-L5 | Borde | `pos = 0` (primer elemento) | Acceso/modificación de `head` |
| CE-L6 | Borde | `pos = size-1` (último elemento) | Acceso/modificación de `tail` |
| CE-L7 | Especial | Lista con 1 solo elemento | Operación correcta; lista vacía tras remove |
| CE-L8 | Especial | Lista vacía (`size=0`) | `OUT_OF_BOUNDS` en get/remove; `FALSE` en contains |
| CE-L9 | Especial | Valores `INT_MIN` y `INT_MAX` | Almacenamiento y recuperación exacta |

### 3.2 stack_obj.py

| ID Clase | Tipo | Condición | Resultado Esperado |
|---|:---:|---|---|
| CE-S1 | Válida | `stk` válido, pila con elementos | Operación exitosa, `STACK_OK` |
| CE-S2 | Inválida | `stk` es `None` | `STACK_NULL_PTR` inmediato |
| CE-S3 | Límite | Pila vacía en pop/peek | `STACK_EMPTY` |
| CE-S4 | Borde | Pila con 1 elemento | Pop deja pila vacía; is_empty → TRUE |
| CE-S5 | Especial | `INT_MIN`, `INT_MAX`, `0`, negativos | Almacenamiento y recuperación exacta |
| CE-S6 | LIFO | push(1,2,3) → pop debe retornar 3,2,1 | Orden inverso al de inserción |

### 3.3 serializer.py

| ID Clase | Tipo | Condición | Resultado Esperado |
|---|:---:|---|---|
| CE-SER1 | Válida | Mensaje `OBJ\|OP\|ID\|DATO\n` bien formado | `DESER_OK` + `BusMessage` con campos correctos |
| CE-SER2 | Inválida | Sin separadores `\|` | `DESER_ERROR` |
| CE-SER3 | Inválida | Sin terminador `\n` o con `\r\n` | `DESER_ERROR` |
| CE-SER4 | Inválida | Objeto desconocido (QUEUE, MAP...) | `DESER_ERROR` |
| CE-SER5 | Inválida | Operación no soportada | `DESER_ERROR` |
| CE-SER6 | Inválida | ID no numérico o negativo | `DESER_ERROR` |
| CE-SER7 | Inválida | Dato requerido no es entero (INSERT con 'abc') | `DESER_ERROR` |
| CE-SER8 | Especial | `None` o cadena vacía | `DESER_ERROR` sin crash |
| CE-SER9 | Límite | Dato vacío en ops sin dato (CREATE, POP) | `DESER_OK`, `has_data=False` |
| CE-SER10 | Especial | `INT_MIN`, `INT_MAX` como dato | `DESER_OK`, `data_int` exacto |

---

## 4. Análisis de Valores Límite

| Módulo | Valor Límite | Caso de prueba | Resultado |
|---|---|---|---|
| `list_get` | pos = 0 | TC-L-012 | ✅ OK — retorna primer elemento |
| `list_get` | pos = size-1 | TC-L-013 | ✅ OK — retorna último elemento |
| `list_get` | pos = size | TC-L-014 | ✅ OUT_OF_BOUNDS |
| `list_get` | pos = -1 | TC-L-015 | ✅ OUT_OF_BOUNDS |
| `list_insert` | dato = INT_MIN | TC-L-009 | ✅ Almacenado correctamente |
| `list_insert` | dato = INT_MAX | TC-L-009 | ✅ Almacenado correctamente |
| `list_insert` | dato = 0 | TC-L-010 | ✅ Almacenado correctamente |
| `stack_pop` | pila vacía | TC-S-015 | ✅ STACK_EMPTY |
| `stack_push` | INT_MIN | TC-S-010 | ✅ Recuperado exacto |
| `stack_push` | INT_MAX | TC-S-011 | ✅ Recuperado exacto |
| `deserialize` | Solo `\n` | TC-SER-026 | ✅ DESER_ERROR |
| `deserialize` | `\r\n` (CRLF) | TC-SER-014 | ✅ DESER_ERROR (bug corregido en TDD) |
| `deserialize` | INT_MIN como dato | TC-SER-008 | ✅ data_int == INT_MIN |
| `deserialize` | INT_MAX como dato | TC-SER-009 | ✅ data_int == INT_MAX |

---

## 5. Evidencia TDD — Serializer (Ciclo Red-Green-Refactor)

El módulo `serializer.py` fue desarrollado aplicando TDD. Los tests marcados con `[TDD-RED]`, `[TDD-GREEN]` y `[TDD-REFACTOR]` evidencian el ciclo:

| Fase | ID Caso | Descripción | Commit sugerido |
|---|---|---|---|
| 🔴 RED | TC-SER-001 | `deserialize` no existe → falla | `[etapa-2] test: deserialize LIST\|INSERT válido` |
| 🟢 GREEN | TC-SER-002 | `deserialize` implementada mínimamente | `[etapa-2] feat: implementar deserialize_message básico` |
| 🔵 REFACTOR | TC-SER-003 | Mejora: soporte para CREATE sin dato | `[etapa-2] refactor: manejar campo DATO vacío en deserialize` |
| 🔴 RED | TC-SER-027 | `serialize_response` no existe → falla | `[etapa-2] test: serialize_response OK\|dato\n` |
| 🟢 GREEN | TC-SER-028 | `serialize_response` implementada | `[etapa-2] feat: implementar serialize_response` |
| 🔴 RED | TC-SER-014 | `\r\n` aceptado — BUG DETECTADO | `[etapa-2] test: rechazar terminador CRLF` |
| 🔵 REFACTOR | TC-SER-014 | Corrección: validar `not raw.endswith("\r\n")` | `[etapa-2] fix: rechazar CRLF en deserialize_message` |

**El ciclo TDD detectó un defecto real** que no habría sido encontrado con pruebas manuales superficiales: el serializer aceptaba mensajes con terminador `\r\n` (Windows CRLF) cuando el protocolo solo admite `\n` (LF).

---

## 6. Análisis de Cobertura Manual

### 6.1 list_obj.py — Cobertura estimada: ≥ 95%

| Función | Ramas cubiertas | Líneas no cubiertas |
|---|---|---|
| `list_create` | ✅ 100% | — |
| `list_destroy` | ✅ 100% (None + vacía + con elems) | — |
| `list_insert` | ✅ 100% (None, vacía, con tail) | — |
| `list_remove` | ✅ 100% (pos=0, pos=mid, pos=tail, OOB, None) | — |
| `list_get` | ✅ 100% (pos válida, pos<0, pos>=size, None) | — |
| `list_size` | ✅ 100% | — |
| `list_contains` | ✅ 100% (presente, ausente, vacía, None) | — |
| `list_clear` | ✅ 100% (con elems, vacía, None, doble) | — |
| `_node_at_unlocked` | ✅ Cubierta indirectamente por get/remove | — |
| `_clear_nodes` | ✅ Cubierta indirectamente por clear/destroy | — |

**Línea potencialmente no cubierta:** El branch `lst._head is None` en `_clear_nodes` tras un clear en lista vacía es cubierto por TC-L-037.

### 6.2 stack_obj.py — Cobertura estimada: ≥ 95%

| Función | Ramas cubiertas | Observaciones |
|---|---|---|
| `stack_create / destroy` | ✅ 100% | — |
| `stack_push` | ✅ 100% (None, pila vacía, con elementos) | — |
| `stack_pop` | ✅ 100% (None, vacía, con 1 elem, LIFO) | — |
| `stack_peek` | ✅ 100% (None, vacía, con elems) | — |
| `stack_is_empty` | ✅ 100% (None, TRUE, FALSE) | — |
| `stack_size` | ✅ 100% | — |

### 6.3 serializer.py — Cobertura estimada: ≥ 93%

| Función | Ramas cubiertas | Líneas no cubiertas |
|---|---|---|
| `deserialize_message` | ✅ 9 de 9 validaciones cubiertas | Branch de `data_int` con dato no-numérico en op sin requerir int (rara vez ocurre) |
| `serialize_response` | ✅ 100% (OK, ERROR, con/sin dato, CSV) | — |
| `serialize_request` | ✅ 100% (con y sin dato) | — |
| Round-trip | ✅ 3 casos de ida y vuelta | — |

**¿Qué agregaría para 100%?**
- Caso: dato con espacios en ops que no requieren int (CE-SER adicional)
- Caso: mensaje exactamente de `MAX_MSG_LEN` caracteres (límite exacto)

---

## 7. Riesgos de Calidad Identificados

| ID Riesgo | Descripción | Severidad | Mitigación |
|---|---|:---:|---|
| R-01 | Thread-safety: dos hilos insertando en la misma lista simultáneamente | Alto | `threading.Lock` por instancia en todos los métodos mutantes |
| R-02 | Datos compartidos por referencia: si se comparte el ID de una instancia, dos clientes operan el mismo objeto | Alto | Política de IDs únicos por cliente en `object_server` |
| R-03 | Serializer rechaza `\r\n`: clientes Windows que usen CRLF recibirán `INVALID_MESSAGE` | Medio | Documentado en protocolo; se puede agregar normalización en `bus_server.py` |
| R-04 | Desbordamiento de buffer: `MAX_DATA_LEN=255` puede ser muy pequeño para INORDER de árboles grandes | Bajo | Documentado como restricción en el protocolo; pendiente para Etapa 3 |

---

## 8. Matriz de Trazabilidad Etapa 2

| RF Etapa 1 | Función Python | Casos de prueba | Tipo |
|---|---|---|:---:|
| RF-001 (Crear Lista) | `list_create` | TC-L-001, TC-L-002 | U |
| RF-002 (Insertar Lista) | `list_insert` | TC-L-006..TC-L-011 | U |
| RF-003 (Obtener Lista) | `list_get` | TC-L-012..TC-L-017 | U |
| RF-004 (Remover Lista) | `list_remove` | TC-L-018..TC-L-024 | U |
| RF-005 (Tamaño Lista) | `list_size` | TC-L-025..TC-L-029 | U |
| RF-006 (Contiene Lista) | `list_contains` | TC-L-030..TC-L-035 | U |
| RF-007 (Limpiar Lista) | `list_clear` | TC-L-036..TC-L-040 | U |
| RF-008 (Crear Pila) | `stack_create` | TC-S-001..TC-S-006 | U |
| RF-009 (Push Pila) | `stack_push` | TC-S-007..TC-S-012 | U |
| RF-010 (Pop Pila) | `stack_pop` | TC-S-013..TC-S-018 | U |
| RF-011 (Peek Pila) | `stack_peek` | TC-S-019..TC-S-023 | U |
| RF-012 (Pila Vacía) | `stack_is_empty` | TC-S-024..TC-S-028 | U |
| RF-020 (Formato Inválido) | `deserialize_message` | TC-SER-010..TC-SER-026 | U |
| Protocolo (deserializar) | `deserialize_message` | TC-SER-001..TC-SER-009 | U |
| Protocolo (serializar resp) | `serialize_response` | TC-SER-027..TC-SER-035 | U |
| Protocolo (serializar req) | `serialize_request` | TC-SER-036..TC-SER-042 | U |
