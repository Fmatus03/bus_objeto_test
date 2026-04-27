"""
test_stack.py — Pruebas Unitarias: stack_obj.py
Bus de Objetos — Etapa 2 | Arnés 100% nativo

Clases de equivalencia:
  CE-S1 [Válida]   stk válido, pila con elementos
  CE-S2 [Inválida] stk es None → STACK_NULL_PTR
  CE-S3 [Límite]   pila vacía (size=0) → STACK_EMPTY en pop/peek
  CE-S4 [Límite]   pila de un elemento (size=1)
  CE-S5 [Especial] valores INT_MIN e INT_MAX
  CE-S6 [LIFO]     orden de extracción inverso al de inserción
"""
import sys, os
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _ROOT)

from src.objects.stack_obj import (
    stack_create, stack_destroy, stack_push, stack_pop,
    stack_peek, stack_is_empty, stack_size,
    STACK_OK, STACK_NULL_PTR, STACK_EMPTY,
)
from tests.unit.test_harness import TestSuite, assert_equal, assert_not_none, assert_true

INT_MIN = -(2**31)
INT_MAX =  (2**31) - 1
suite   = TestSuite("stack_obj.py")

# ── stack_create / stack_destroy ────────────────────────────
suite.run("TC-S-001","create: retorna objeto no-None",
    lambda: assert_not_none(stack_create()))

suite.run("TC-S-002","create: size inicial == 0",
    lambda: assert_equal(stack_size(stack_create()), 0))

suite.run("TC-S-003","create: is_empty inicialmente TRUE",
    lambda: assert_equal(stack_is_empty(stack_create()), 1))

suite.run("TC-S-004","destroy: None → STACK_NULL_PTR",
    lambda: assert_equal(stack_destroy(None), STACK_NULL_PTR))

suite.run("TC-S-005","destroy: pila vacía → STACK_OK",
    lambda: assert_equal(stack_destroy(stack_create()), STACK_OK))

def _t_destroy_with_elems():
    s = stack_create(); stack_push(s, 1); stack_push(s, 2)
    assert_equal(stack_destroy(s), STACK_OK)
suite.run("TC-S-006","destroy: pila con elementos → STACK_OK", _t_destroy_with_elems)

# ── stack_push ───────────────────────────────────────────────
def _t_push_ok():
    s = stack_create()
    assert_equal(stack_push(s, 42), STACK_OK)
    assert_equal(stack_size(s), 1)
suite.run("TC-S-007","push: size se incrementa a 1", _t_push_ok)

suite.run("TC-S-008","push: None → STACK_NULL_PTR",
    lambda: assert_equal(stack_push(None, 5), STACK_NULL_PTR))

def _t_push_multiple():
    s = stack_create()
    for v in [10,20,30]: stack_push(s,v)
    assert_equal(stack_size(s), 3)
suite.run("TC-S-009","push múltiple: size correcto", _t_push_multiple)

def _t_push_intmin():
    s = stack_create(); stack_push(s, INT_MIN)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, INT_MIN)
suite.run("TC-S-010","push: INT_MIN almacenado y recuperado", _t_push_intmin)

def _t_push_intmax():
    s = stack_create(); stack_push(s, INT_MAX)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, INT_MAX)
suite.run("TC-S-011","push: INT_MAX almacenado y recuperado", _t_push_intmax)

def _t_push_zero():
    s = stack_create(); stack_push(s, 0)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, 0)
suite.run("TC-S-012","push: valor 0 (límite inferior)", _t_push_zero)

# ── stack_pop ────────────────────────────────────────────────
def _t_pop_ok():
    s = stack_create(); stack_push(s, 5)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, 5)
    assert_equal(stack_size(s), 0)
suite.run("TC-S-013","pop: retorna tope y decrementa size", _t_pop_ok)

def _t_pop_lifo():
    s = stack_create()
    for v in [1,2,3]: stack_push(s,v)
    results = []
    for _ in range(3):
        _, v = stack_pop(s); results.append(v)
    assert_equal(results, [3,2,1])
suite.run("TC-S-014","pop: orden LIFO (push 1,2,3 → pop 3,2,1)", _t_pop_lifo)

def _t_pop_empty():
    s = stack_create()
    code, val = stack_pop(s)
    assert_equal(code, STACK_EMPTY); assert_true(val is None)
suite.run("TC-S-015","pop: pila vacía → STACK_EMPTY", _t_pop_empty)

suite.run("TC-S-016","pop: None → STACK_NULL_PTR",
    lambda: assert_equal(stack_pop(None)[0], STACK_NULL_PTR))

def _t_pop_single():
    s = stack_create(); stack_push(s,99)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, 99)
    assert_equal(stack_size(s), 0)
suite.run("TC-S-017","pop: único elemento → pila vacía tras pop", _t_pop_single)

def _t_pop_negative():
    s = stack_create(); stack_push(s,-7)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, -7)
suite.run("TC-S-018","pop: valor negativo recuperado correctamente", _t_pop_negative)

# ── stack_peek ───────────────────────────────────────────────
def _t_peek_ok():
    s = stack_create(); stack_push(s, 99)
    code, val = stack_peek(s)
    assert_equal(code, STACK_OK); assert_equal(val, 99)
    assert_equal(stack_size(s), 1)
suite.run("TC-S-019","peek: retorna tope SIN modificar size", _t_peek_ok)

def _t_peek_empty():
    s = stack_create()
    code, val = stack_peek(s)
    assert_equal(code, STACK_EMPTY); assert_true(val is None)
suite.run("TC-S-020","peek: pila vacía → STACK_EMPTY", _t_peek_empty)

suite.run("TC-S-021","peek: None → STACK_NULL_PTR",
    lambda: assert_equal(stack_peek(None)[0], STACK_NULL_PTR))

def _t_peek_lifo():
    s = stack_create()
    for v in [1,2,3]: stack_push(s,v)
    _, val = stack_peek(s)
    assert_equal(val, 3)
suite.run("TC-S-022","peek: tras 3 pushes retorna el último", _t_peek_lifo)

def _t_peek_no_alter():
    s = stack_create(); stack_push(s,7)
    stack_peek(s)
    code, val = stack_pop(s)
    assert_equal(code, STACK_OK); assert_equal(val, 7)
suite.run("TC-S-023","peek: no altera estado (pop posterior retorna mismo valor)", _t_peek_no_alter)

# ── stack_is_empty ───────────────────────────────────────────
suite.run("TC-S-024","is_empty: pila nueva → 1 (TRUE)",
    lambda: assert_equal(stack_is_empty(stack_create()), 1))

def _t_isempty_false():
    s = stack_create(); stack_push(s,1)
    assert_equal(stack_is_empty(s), 0)
suite.run("TC-S-025","is_empty: tras push → 0 (FALSE)", _t_isempty_false)

def _t_isempty_after_pop():
    s = stack_create(); stack_push(s,1); stack_pop(s)
    assert_equal(stack_is_empty(s), 1)
suite.run("TC-S-026","is_empty: tras push+pop → 1 (TRUE)", _t_isempty_after_pop)

suite.run("TC-S-027","is_empty: None → STACK_NULL_PTR",
    lambda: assert_equal(stack_is_empty(None), STACK_NULL_PTR))

def _t_isempty_multi():
    s = stack_create()
    for v in [1,2,3]: stack_push(s,v)
    assert_equal(stack_is_empty(s), 0)
    for _ in range(3): stack_pop(s)
    assert_equal(stack_is_empty(s), 1)
suite.run("TC-S-028","is_empty: ciclo completo push×3 → pop×3 → TRUE", _t_isempty_multi)

# ── stack_size ───────────────────────────────────────────────
suite.run("TC-S-029","size: pila nueva == 0",
    lambda: assert_equal(stack_size(stack_create()), 0))

def _t_size_5():
    s = stack_create()
    for i in range(5): stack_push(s,i)
    assert_equal(stack_size(s), 5)
suite.run("TC-S-030","size: tras 5 pushes == 5", _t_size_5)

def _t_size_after_pop():
    s = stack_create()
    for v in [1,2,3]: stack_push(s,v)
    stack_pop(s)
    assert_equal(stack_size(s), 2)
suite.run("TC-S-031","size: tras push×3 + pop×1 == 2", _t_size_after_pop)

suite.run("TC-S-032","size: None → STACK_NULL_PTR",
    lambda: assert_equal(stack_size(None), STACK_NULL_PTR))

def _t_size_zero_after_all_pops():
    s = stack_create()
    for v in [10,20]: stack_push(s,v)
    stack_pop(s); stack_pop(s)
    assert_equal(stack_size(s), 0)
suite.run("TC-S-033","size: tras vaciar completamente == 0", _t_size_zero_after_all_pops)

# ── Reporte ──────────────────────────────────────────────────
if __name__ == "__main__":
    sys.exit(1 if suite.report() > 0 else 0)
