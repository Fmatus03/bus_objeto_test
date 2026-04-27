"""
test_serializer.py — Pruebas Unitarias (TDD): serializer.py
Bus de Objetos — Etapa 2 | Arnés 100% nativo

EVIDENCIA TDD: Este archivo fue escrito ANTES de la implementación.
Ciclo aplicado a cada función:
  RED   → test escrito, función no existe → falla
  GREEN → función implementada mínimamente → pasa
  REFACTOR → implementación mejorada → sigue pasando

Clases de equivalencia:
  CE-SER1 [Válida]    Mensaje bien formado con objetos y ops válidos
  CE-SER2 [Inválida]  Sin separadores '|'
  CE-SER3 [Inválida]  Sin terminador '\n'
  CE-SER4 [Inválida]  Objeto no reconocido (QUEUE, MAP...)
  CE-SER5 [Inválida]  Operación no válida
  CE-SER6 [Inválida]  ID no numérico
  CE-SER7 [Inválida]  Dato requerido no es entero (ej. INSERT con 'abc')
  CE-SER8 [Inválida]  None o cadena vacía
  CE-SER9 [Límite]    Dato vacío en ops que no lo requieren
  CE-SER10[Especial]  Valores límite: INT_MIN, INT_MAX
"""
import sys, os
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _ROOT)

from src.protocol.serializer import (
    deserialize_message, serialize_response, serialize_request,
    BusMessage, DESER_OK, DESER_ERROR,
)
from tests.unit.test_harness import TestSuite, assert_equal, assert_not_none, assert_true

INT_MIN = -(2**31)
INT_MAX =  (2**31) - 1
suite   = TestSuite("serializer.py (TDD)")

# ══════════════════════════════════════════════════════════════
# [RED→GREEN→REFACTOR] deserialize_message
# ══════════════════════════════════════════════════════════════

# ── CE-SER1: Mensajes válidos ────────────────────────────────
def _t_deser_list_insert():
    code, msg = deserialize_message("LIST|INSERT|1|42\n")
    assert_equal(code, DESER_OK)
    assert_not_none(msg)
    assert_equal(msg.obj_type, "LIST")
    assert_equal(msg.operation, "INSERT")
    assert_equal(msg.instance_id, 1)
    assert_equal(msg.data_int, 42)
    assert_equal(msg.has_data, True)
suite.run("TC-SER-001","[TDD-RED] deserialize: LIST|INSERT válido → DESER_OK + campos correctos", _t_deser_list_insert)

def _t_deser_stack_pop():
    code, msg = deserialize_message("STACK|POP|2|\n")
    assert_equal(code, DESER_OK)
    assert_equal(msg.obj_type, "STACK")
    assert_equal(msg.operation, "POP")
    assert_equal(msg.instance_id, 2)
    assert_equal(msg.has_data, False)
suite.run("TC-SER-002","[TDD-GREEN] deserialize: STACK|POP sin dato → has_data=False", _t_deser_stack_pop)

def _t_deser_tree_create():
    code, msg = deserialize_message("TREE|CREATE|0|\n")
    assert_equal(code, DESER_OK)
    assert_equal(msg.obj_type, "TREE")
    assert_equal(msg.operation, "CREATE")
    assert_equal(msg.instance_id, 0)
suite.run("TC-SER-003","[TDD-REFACTOR] deserialize: TREE|CREATE|0 → correcto", _t_deser_tree_create)

def _t_deser_list_get():
    code, msg = deserialize_message("LIST|GET|5|3\n")
    assert_equal(code, DESER_OK)
    assert_equal(msg.data_int, 3)
suite.run("TC-SER-004","deserialize: LIST|GET con pos numérica", _t_deser_list_get)

def _t_deser_tree_search():
    code, msg = deserialize_message("TREE|SEARCH|3|99\n")
    assert_equal(code, DESER_OK)
    assert_equal(msg.data_int, 99)
suite.run("TC-SER-005","deserialize: TREE|SEARCH con dato entero", _t_deser_tree_search)

def _t_deser_stack_isempty():
    code, msg = deserialize_message("STACK|IS_EMPTY|4|\n")
    assert_equal(code, DESER_OK)
    assert_equal(msg.operation, "IS_EMPTY")
suite.run("TC-SER-006","deserialize: STACK|IS_EMPTY → operación reconocida", _t_deser_stack_isempty)

def _t_deser_tree_inorder():
    code, msg = deserialize_message("TREE|INORDER|7|\n")
    assert_equal(code, DESER_OK)
    assert_equal(msg.operation, "INORDER")
    assert_equal(msg.has_data, False)
suite.run("TC-SER-007","deserialize: TREE|INORDER sin dato → has_data=False", _t_deser_tree_inorder)

# ── CE-SER10: Valores límite en dato ─────────────────────────
def _t_deser_intmin():
    raw = f"LIST|INSERT|1|{INT_MIN}\n"
    code, msg = deserialize_message(raw)
    assert_equal(code, DESER_OK)
    assert_equal(msg.data_int, INT_MIN)
suite.run("TC-SER-008","deserialize: dato INT_MIN válido", _t_deser_intmin)

def _t_deser_intmax():
    raw = f"STACK|PUSH|1|{INT_MAX}\n"
    code, msg = deserialize_message(raw)
    assert_equal(code, DESER_OK)
    assert_equal(msg.data_int, INT_MAX)
suite.run("TC-SER-009","deserialize: dato INT_MAX válido", _t_deser_intmax)

# ── CE-SER2: Sin separadores ──────────────────────────────────
suite.run("TC-SER-010","deserialize: sin separadores '|' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LISTINSERT142\n")[0], DESER_ERROR))

suite.run("TC-SER-011","deserialize: solo 2 campos → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|INSERT\n")[0], DESER_ERROR))

suite.run("TC-SER-012","deserialize: solo 3 campos → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|INSERT|1\n")[0], DESER_ERROR))

# ── CE-SER3: Sin terminador \n ────────────────────────────────
suite.run("TC-SER-013","deserialize: sin terminador '\\n' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|INSERT|1|42")[0], DESER_ERROR))

suite.run("TC-SER-014","deserialize: terminador '\\r\\n' no válido → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|INSERT|1|42\r\n")[0], DESER_ERROR))

# ── CE-SER4: Objeto inválido ──────────────────────────────────
suite.run("TC-SER-015","deserialize: objeto 'QUEUE' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("QUEUE|CREATE|0|\n")[0], DESER_ERROR))

suite.run("TC-SER-016","deserialize: objeto 'MAP' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("MAP|GET|1|0\n")[0], DESER_ERROR))

suite.run("TC-SER-017","deserialize: objeto vacío → DESER_ERROR",
    lambda: assert_equal(deserialize_message("|INSERT|1|5\n")[0], DESER_ERROR))

# ── CE-SER5: Operación inválida ───────────────────────────────
suite.run("TC-SER-018","deserialize: operación 'EXECUTE' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|EXECUTE|1|5\n")[0], DESER_ERROR))

suite.run("TC-SER-019","deserialize: operación vacía → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST||1|5\n")[0], DESER_ERROR))

# ── CE-SER6: ID no numérico ───────────────────────────────────
suite.run("TC-SER-020","deserialize: ID='abc' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|GET|abc|0\n")[0], DESER_ERROR))

suite.run("TC-SER-021","deserialize: ID negativo → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|GET|-1|0\n")[0], DESER_ERROR))

# ── CE-SER7: Dato no entero cuando se requiere ────────────────
suite.run("TC-SER-022","deserialize: INSERT con dato 'hola' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("LIST|INSERT|1|hola\n")[0], DESER_ERROR))

suite.run("TC-SER-023","deserialize: PUSH con dato flotante '3.14' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("STACK|PUSH|1|3.14\n")[0], DESER_ERROR))

# ── CE-SER8: None y cadena vacía ─────────────────────────────
suite.run("TC-SER-024","deserialize: None → DESER_ERROR",
    lambda: assert_equal(deserialize_message(None)[0], DESER_ERROR))

suite.run("TC-SER-025","deserialize: cadena vacía → DESER_ERROR",
    lambda: assert_equal(deserialize_message("")[0], DESER_ERROR))

suite.run("TC-SER-026","deserialize: solo '\\n' → DESER_ERROR",
    lambda: assert_equal(deserialize_message("\n")[0], DESER_ERROR))

# ══════════════════════════════════════════════════════════════
# [TDD] serialize_response
# ══════════════════════════════════════════════════════════════

suite.run("TC-SER-027","[TDD-RED] serialize_response: OK con dato → 'OK|42\\n'",
    lambda: assert_equal(serialize_response(True, "42"), "OK|42\n"))

suite.run("TC-SER-028","[TDD-GREEN] serialize_response: ERROR → 'ERROR|INSTANCE_NOT_FOUND\\n'",
    lambda: assert_equal(serialize_response(False, "INSTANCE_NOT_FOUND"), "ERROR|INSTANCE_NOT_FOUND\n"))

suite.run("TC-SER-029","serialize_response: OK sin dato → 'OK|\\n'",
    lambda: assert_equal(serialize_response(True, ""), "OK|\n"))

suite.run("TC-SER-030","serialize_response: ERROR sin dato → 'ERROR|\\n'",
    lambda: assert_equal(serialize_response(False, ""), "ERROR|\n"))

suite.run("TC-SER-031","serialize_response: OK con TRUE → 'OK|TRUE\\n'",
    lambda: assert_equal(serialize_response(True, "TRUE"), "OK|TRUE\n"))

suite.run("TC-SER-032","serialize_response: OK con FALSE → 'OK|FALSE\\n'",
    lambda: assert_equal(serialize_response(True, "FALSE"), "OK|FALSE\n"))

def _t_ser_resp_csv():
    result = serialize_response(True, "1,3,5,7,9")
    assert_equal(result, "OK|1,3,5,7,9\n")
suite.run("TC-SER-033","serialize_response: OK con CSV inorder", _t_ser_resp_csv)

suite.run("TC-SER-034","serialize_response: ERROR EMPTY_STRUCTURE",
    lambda: assert_equal(serialize_response(False, "EMPTY_STRUCTURE"), "ERROR|EMPTY_STRUCTURE\n"))

suite.run("TC-SER-035","serialize_response: ERROR OUT_OF_BOUNDS",
    lambda: assert_equal(serialize_response(False, "OUT_OF_BOUNDS"), "ERROR|OUT_OF_BOUNDS\n"))

# ══════════════════════════════════════════════════════════════
# [TDD] serialize_request
# ══════════════════════════════════════════════════════════════

suite.run("TC-SER-036","[TDD-RED] serialize_request: LIST|CREATE|0|",
    lambda: assert_equal(serialize_request("LIST","CREATE",0), "LIST|CREATE|0|\n"))

suite.run("TC-SER-037","[TDD-GREEN] serialize_request: LIST|INSERT|1|42",
    lambda: assert_equal(serialize_request("LIST","INSERT",1,"42"), "LIST|INSERT|1|42\n"))

suite.run("TC-SER-038","serialize_request: STACK|PUSH|2|99",
    lambda: assert_equal(serialize_request("STACK","PUSH",2,"99"), "STACK|PUSH|2|99\n"))

suite.run("TC-SER-039","serialize_request: TREE|INORDER|3|",
    lambda: assert_equal(serialize_request("TREE","INORDER",3), "TREE|INORDER|3|\n"))

# ── Round-trip: serializar → deserializar ────────────────────
def _t_roundtrip_insert():
    raw = serialize_request("LIST","INSERT",1,"42")
    code, msg = deserialize_message(raw)
    assert_equal(code, DESER_OK)
    assert_equal(msg.obj_type, "LIST")
    assert_equal(msg.data_int, 42)
suite.run("TC-SER-040","Round-trip: serialize_request → deserialize OK", _t_roundtrip_insert)

def _t_roundtrip_tree():
    raw = serialize_request("TREE","SEARCH",3,"7")
    code, msg = deserialize_message(raw)
    assert_equal(code, DESER_OK)
    assert_equal(msg.obj_type, "TREE")
    assert_equal(msg.data_int, 7)
suite.run("TC-SER-041","Round-trip: TREE|SEARCH → deserialize correcto", _t_roundtrip_tree)

def _t_roundtrip_stack():
    raw = serialize_request("STACK","POP",5)
    code, msg = deserialize_message(raw)
    assert_equal(code, DESER_OK)
    assert_equal(msg.operation, "POP")
    assert_equal(msg.has_data, False)
suite.run("TC-SER-042","Round-trip: STACK|POP sin dato → has_data=False", _t_roundtrip_stack)

# ── Reporte ──────────────────────────────────────────────────
if __name__ == "__main__":
    sys.exit(1 if suite.report() > 0 else 0)
