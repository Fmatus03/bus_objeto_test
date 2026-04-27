"""
test_harness.py — Arnés de Pruebas Unitarias a Medida (sin frameworks externos)
Proyecto: Bus de Objetos en Python — Etapa 2

Descripción:
    Arnés de pruebas 100% nativo construido desde cero.
    NO usa pytest, unittest, nose ni ninguna librería de pruebas.
    Usa únicamente: assert nativo de Python, try/except, print, sys, time.

Uso:
    from test_harness import TestSuite, assert_equal, assert_none, assert_not_none

    suite = TestSuite("Nombre del módulo")
    suite.run(nombre_del_test, funcion_de_test)
    suite.report()
"""

import sys
import time
import traceback

# ─── Colores ANSI para terminal ───────────────────────────────
_GREEN  = "\033[92m"
_RED    = "\033[91m"
_YELLOW = "\033[93m"
_RESET  = "\033[0m"
_BOLD   = "\033[1m"


# ─── Clase principal del arnés ─────────────────────────────────

class TestSuite:
    """
    Gestiona la ejecución y reporte de una suite de pruebas unitarias.
    Cada prueba es una función sin argumentos que usa assert* helpers o
    assert nativo de Python.
    """

    def __init__(self, name: str):
        self.name   = name
        self._tests: list[tuple[str, str, bool, str, float]] = []
        # Cada entrada: (id_caso, descripcion, passed, mensaje_error, duracion_ms)

    def run(self, test_id: str, description: str, test_fn) -> bool:
        """
        Ejecuta una función de prueba y registra el resultado.

        Args:
            test_id:     ID único del caso (ej. "TC-LIST-001")
            description: Descripción breve del caso
            test_fn:     Función callable sin argumentos

        Retorna:
            True si la prueba pasó, False si falló.
        """
        start = time.perf_counter()
        try:
            test_fn()
            elapsed = (time.perf_counter() - start) * 1000
            self._tests.append((test_id, description, True, "", elapsed))
            print(f"  {_GREEN}✔ PASS{_RESET} [{test_id}] {description} ({elapsed:.2f}ms)")
            return True
        except AssertionError as e:
            elapsed = (time.perf_counter() - start) * 1000
            msg = str(e) if str(e) else "Aserción fallida sin mensaje"
            self._tests.append((test_id, description, False, msg, elapsed))
            print(f"  {_RED}✘ FAIL{_RESET} [{test_id}] {description}")
            print(f"         {_RED}→ {msg}{_RESET}")
            return False
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            tb = traceback.format_exc().strip().split("\n")[-1]
            self._tests.append((test_id, description, False, f"EXCEPCIÓN: {tb}", elapsed))
            print(f"  {_RED}✘ ERROR{_RESET} [{test_id}] {description}")
            print(f"         {_RED}→ {tb}{_RESET}")
            return False

    def report(self) -> int:
        """
        Imprime el resumen de la suite y retorna el número de pruebas fallidas.
        """
        total   = len(self._tests)
        passed  = sum(1 for _, _, ok, _, _ in self._tests if ok)
        failed  = total - passed
        avg_ms  = (sum(d for _, _, _, _, d in self._tests) / total) if total else 0

        print()
        print(f"{_BOLD}{'═'*60}{_RESET}")
        print(f"{_BOLD}  SUITE: {self.name}{_RESET}")
        print(f"  Total:  {total} pruebas | "
              f"{_GREEN}PASS: {passed}{_RESET} | "
              f"{_RED}FAIL: {failed}{_RESET} | "
              f"Tiempo promedio: {avg_ms:.2f}ms")
        if failed > 0:
            print(f"\n  {_RED}{_BOLD}Pruebas fallidas:{_RESET}")
            for tid, desc, ok, msg, _ in self._tests:
                if not ok:
                    print(f"    • [{tid}] {desc}: {msg}")
        print(f"{_BOLD}{'═'*60}{_RESET}")
        return failed


# ─── Helpers de aserción con mensajes descriptivos ─────────────

def assert_equal(actual, expected, msg: str = "") -> None:
    """assert actual == expected"""
    if actual != expected:
        label = f" ({msg})" if msg else ""
        raise AssertionError(
            f"Esperado {expected!r}, obtenido {actual!r}{label}"
        )

def assert_not_equal(actual, expected, msg: str = "") -> None:
    """assert actual != expected"""
    if actual == expected:
        label = f" ({msg})" if msg else ""
        raise AssertionError(f"Valores iguales: {actual!r}{label}")

def assert_true(expr, msg: str = "") -> None:
    """assert expr is truthy"""
    if not expr:
        raise AssertionError(msg or f"Se esperaba True, obtenido {expr!r}")

def assert_false(expr, msg: str = "") -> None:
    """assert expr is falsy"""
    if expr:
        raise AssertionError(msg or f"Se esperaba False, obtenido {expr!r}")

def assert_none(obj, msg: str = "") -> None:
    """assert obj is None"""
    if obj is not None:
        raise AssertionError(msg or f"Se esperaba None, obtenido {obj!r}")

def assert_not_none(obj, msg: str = "") -> None:
    """assert obj is not None"""
    if obj is None:
        raise AssertionError(msg or "Se esperaba valor no-None, obtenido None")

def assert_greater(a, b, msg: str = "") -> None:
    """assert a > b"""
    if not (a > b):
        raise AssertionError(msg or f"Se esperaba {a!r} > {b!r}")

def assert_in_range(value, lo, hi, msg: str = "") -> None:
    """assert lo <= value <= hi"""
    if not (lo <= value <= hi):
        raise AssertionError(
            msg or f"Se esperaba {lo} <= {value!r} <= {hi}"
        )
