"""
test_list.py — Pruebas Unitarias: list_obj.py
Bus de Objetos — Etapa 2 | Arnés 100% nativo (sin frameworks externos)

Clases de equivalencia:
  CE-L1 [Válida]   lst válido, parámetros en rango
  CE-L2 [Inválida] lst es None → LIST_NULL_PTR
  CE-L3 [Límite-]  pos = -1 → OUT_OF_BOUNDS
  CE-L4 [Límite+]  pos = size → OUT_OF_BOUNDS
  CE-L5 [Borde]    pos = 0 (primer elemento)
  CE-L6 [Borde]    pos = size-1 (último elemento)
  CE-L7 [Especial] lista de un solo elemento
  CE-L8 [Especial] lista vacía
"""
import sys, os
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _ROOT)

from src.objects.list_obj import (
    list_create, list_destroy, list_insert, list_remove,
    list_get, list_size, list_contains, list_clear,
    LIST_OK, LIST_NULL_PTR, LIST_OUT_OF_BOUNDS,
)
from tests.unit.test_harness import TestSuite, assert_equal, assert_not_none, assert_true

INT_MIN = -(2**31)
INT_MAX =  (2**31) - 1
suite   = TestSuite("list_obj.py")

# ── list_create / list_destroy ──────────────────────────────
suite.run("TC-L-001","create: retorna objeto no-None con size=0",
    lambda: (assert_not_none(list_create()), assert_equal(list_size(list_create()), 0)))

suite.run("TC-L-002","create: dos instancias distintas",
    lambda: assert_true(list_create() is not list_create()))

suite.run("TC-L-003","destroy: OK en lista con elementos",
    lambda: assert_equal(list_destroy((lambda l: [list_insert(l,1), l][1])(list_create())), LIST_OK))

suite.run("TC-L-004","destroy: None → LIST_NULL_PTR",
    lambda: assert_equal(list_destroy(None), LIST_NULL_PTR))

suite.run("TC-L-005","destroy: lista vacía → LIST_OK",
    lambda: assert_equal(list_destroy(list_create()), LIST_OK))

# ── list_insert ─────────────────────────────────────────────
def _t_insert_ok():
    l = list_create(); list_insert(l, 42)
    assert_equal(list_size(l), 1)
suite.run("TC-L-006","insert: size se incrementa a 1", _t_insert_ok)

def _t_insert_fifo():
    l = list_create()
    for v in [10,20,30]: list_insert(l, v)
    for i,v in enumerate([10,20,30]):
        _, got = list_get(l, i); assert_equal(got, v)
suite.run("TC-L-007","insert múltiple: orden FIFO preservado", _t_insert_fifo)

suite.run("TC-L-008","insert: None → LIST_NULL_PTR",
    lambda: assert_equal(list_insert(None, 5), LIST_NULL_PTR))

def _t_insert_extremos():
    l = list_create()
    list_insert(l, INT_MIN); list_insert(l, INT_MAX)
    _, v0 = list_get(l,0); _, v1 = list_get(l,1)
    assert_equal(v0, INT_MIN); assert_equal(v1, INT_MAX)
suite.run("TC-L-009","insert: INT_MIN e INT_MAX", _t_insert_extremos)

def _t_insert_cero():
    l = list_create(); list_insert(l, 0)
    _, v = list_get(l,0); assert_equal(v, 0)
suite.run("TC-L-010","insert: valor 0 (límite inferior)", _t_insert_cero)

def _t_insert_negativo():
    l = list_create(); list_insert(l, -999)
    _, v = list_get(l,0); assert_equal(v, -999)
suite.run("TC-L-011","insert: valor negativo almacenado correctamente", _t_insert_negativo)

# ── list_get ────────────────────────────────────────────────
def _t_get_pos0():
    l = list_create(); list_insert(l, 77)
    code, val = list_get(l, 0)
    assert_equal(code, LIST_OK); assert_equal(val, 77)
suite.run("TC-L-012","get: pos=0 retorna valor correcto", _t_get_pos0)

def _t_get_last():
    l = list_create()
    for v in [1,2,3]: list_insert(l,v)
    code, val = list_get(l, 2)
    assert_equal(code, LIST_OK); assert_equal(val, 3)
suite.run("TC-L-013","get: pos=size-1 retorna último elemento", _t_get_last)

def _t_get_oob_over():
    l = list_create(); list_insert(l, 10)
    code, val = list_get(l, 1)
    assert_equal(code, LIST_OUT_OF_BOUNDS); assert_true(val is None)
suite.run("TC-L-014","get: pos==size → OUT_OF_BOUNDS", _t_get_oob_over)

def _t_get_oob_neg():
    l = list_create(); list_insert(l, 10)
    code, _ = list_get(l, -1)
    assert_equal(code, LIST_OUT_OF_BOUNDS)
suite.run("TC-L-015","get: pos==-1 → OUT_OF_BOUNDS", _t_get_oob_neg)

suite.run("TC-L-016","get: None → LIST_NULL_PTR",
    lambda: assert_equal(list_get(None, 0)[0], LIST_NULL_PTR))

def _t_get_empty():
    l = list_create(); code, _ = list_get(l, 0)
    assert_equal(code, LIST_OUT_OF_BOUNDS)
suite.run("TC-L-017","get: lista vacía → OUT_OF_BOUNDS", _t_get_empty)

# ── list_remove ─────────────────────────────────────────────
def _t_remove_head():
    l = list_create()
    for v in [10,20,30]: list_insert(l,v)
    assert_equal(list_remove(l,0), LIST_OK)
    assert_equal(list_size(l), 2)
    _, v0 = list_get(l,0); assert_equal(v0, 20)
suite.run("TC-L-018","remove: pos=0 actualiza head", _t_remove_head)

def _t_remove_tail():
    l = list_create()
    for v in [10,20,30]: list_insert(l,v)
    assert_equal(list_remove(l,2), LIST_OK)
    assert_equal(list_size(l), 2)
    _, v1 = list_get(l,1); assert_equal(v1, 20)
suite.run("TC-L-019","remove: pos=size-1 actualiza tail", _t_remove_tail)

def _t_remove_mid():
    l = list_create()
    for v in [10,20,30]: list_insert(l,v)
    list_remove(l,1)
    _, v0 = list_get(l,0); _, v1 = list_get(l,1)
    assert_equal(v0,10); assert_equal(v1,30)
suite.run("TC-L-020","remove: pos media reenlaza correctamente", _t_remove_mid)

suite.run("TC-L-021","remove: pos>=size → OUT_OF_BOUNDS",
    lambda: assert_equal(list_remove((lambda l:(list_insert(l,5),l)[1])(list_create()),1), LIST_OUT_OF_BOUNDS))

suite.run("TC-L-022","remove: pos<0 → OUT_OF_BOUNDS",
    lambda: assert_equal(list_remove((lambda l:(list_insert(l,5),l)[1])(list_create()),-1), LIST_OUT_OF_BOUNDS))

suite.run("TC-L-023","remove: None → LIST_NULL_PTR",
    lambda: assert_equal(list_remove(None,0), LIST_NULL_PTR))

def _t_remove_single():
    l = list_create(); list_insert(l,99)
    list_remove(l,0); assert_equal(list_size(l), 0)
suite.run("TC-L-024","remove: único elemento → lista vacía", _t_remove_single)

# ── list_size ────────────────────────────────────────────────
suite.run("TC-L-025","size: lista nueva == 0",
    lambda: assert_equal(list_size(list_create()), 0))

def _t_size_5():
    l = list_create()
    for i in range(5): list_insert(l,i)
    assert_equal(list_size(l), 5)
suite.run("TC-L-026","size: tras 5 inserts == 5", _t_size_5)

def _t_size_after_remove():
    l = list_create()
    for v in [1,2,3]: list_insert(l,v)
    list_remove(l,0); assert_equal(list_size(l), 2)
suite.run("TC-L-027","size: tras insert+remove consistente", _t_size_after_remove)

suite.run("TC-L-028","size: None → LIST_NULL_PTR",
    lambda: assert_equal(list_size(None), LIST_NULL_PTR))

def _t_size_after_clear():
    l = list_create()
    for i in range(3): list_insert(l,i)
    list_clear(l); assert_equal(list_size(l), 0)
suite.run("TC-L-029","size: tras clear == 0", _t_size_after_clear)

# ── list_contains ────────────────────────────────────────────
def _t_contains_true():
    l = list_create()
    for v in [10,20,30]: list_insert(l,v)
    assert_equal(list_contains(l,20), 1)
suite.run("TC-L-030","contains: valor presente → 1 (TRUE)", _t_contains_true)

def _t_contains_false():
    l = list_create()
    for v in [10,20,30]: list_insert(l,v)
    assert_equal(list_contains(l,99), 0)
suite.run("TC-L-031","contains: valor ausente → 0 (FALSE)", _t_contains_false)

def _t_contains_empty():
    l = list_create()
    assert_equal(list_contains(l,5), 0)
    assert_equal(list_size(l), 0)
suite.run("TC-L-032","contains: lista vacía → 0 (no error)", _t_contains_empty)

suite.run("TC-L-033","contains: None → LIST_NULL_PTR",
    lambda: assert_equal(list_contains(None,5), LIST_NULL_PTR))

def _t_contains_intmin():
    l = list_create(); list_insert(l, INT_MIN)
    assert_equal(list_contains(l, INT_MIN), 1)
suite.run("TC-L-034","contains: INT_MIN presente → TRUE", _t_contains_intmin)

def _t_contains_intmax_false():
    l = list_create(); list_insert(l, 0)
    assert_equal(list_contains(l, INT_MAX), 0)
suite.run("TC-L-035","contains: INT_MAX ausente → FALSE", _t_contains_intmax_false)

# ── list_clear ───────────────────────────────────────────────
def _t_clear_ok():
    l = list_create()
    for v in [1,2,3,4,5]: list_insert(l,v)
    assert_equal(list_clear(l), LIST_OK)
    assert_equal(list_size(l), 0)
suite.run("TC-L-036","clear: vacía la lista completamente", _t_clear_ok)

def _t_clear_empty():
    l = list_create()
    assert_equal(list_clear(l), LIST_OK)
    assert_equal(list_size(l), 0)
suite.run("TC-L-037","clear: lista ya vacía → LIST_OK (idempotente)", _t_clear_empty)

suite.run("TC-L-038","clear: None → LIST_NULL_PTR",
    lambda: assert_equal(list_clear(None), LIST_NULL_PTR))

def _t_clear_reuse():
    l = list_create()
    for v in [1,2,3]: list_insert(l,v)
    list_clear(l); list_insert(l,99)
    assert_equal(list_size(l),1)
    _, val = list_get(l,0); assert_equal(val,99)
suite.run("TC-L-039","clear + insert: lista reusable tras limpiar", _t_clear_reuse)

def _t_clear_twice():
    l = list_create(); list_insert(l,42)
    list_clear(l)
    assert_equal(list_clear(l), LIST_OK)
    assert_equal(list_size(l), 0)
suite.run("TC-L-040","clear doble: sin crash, size == 0", _t_clear_twice)

# ── Reporte ──────────────────────────────────────────────────
if __name__ == "__main__":
    sys.exit(1 if suite.report() > 0 else 0)
