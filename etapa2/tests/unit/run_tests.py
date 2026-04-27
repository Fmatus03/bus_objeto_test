"""
run_tests.py — Runner Maestro de Pruebas Unitarias — Etapa 2
Bus de Objetos en Python

Ejecuta todas las suites y retorna código 0 (todo OK) o 1 (hay fallos).
Uso:
    python run_tests.py
"""
import sys, os, time, importlib

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _ROOT)

_GREEN = "\033[92m"; _RED = "\033[91m"; _RESET = "\033[0m"; _BOLD = "\033[1m"

SUITES = [
    ("tests.unit.test_list",       "TC-LIST (List Enlazada)"),
    ("tests.unit.test_stack",      "TC-STACK (Pila LIFO)"),
    ("tests.unit.test_serializer", "TC-SER (Serializer — TDD)"),
]

def main():
    print(f"\n{_BOLD}{'═'*60}")
    print("  RUNNER MAESTRO — Etapa 2: Pruebas Unitarias")
    print(f"{'═'*60}{_RESET}\n")

    total_failed = 0
    start_global = time.perf_counter()

    for module_path, label in SUITES:
        print(f"\n{_BOLD}▶ {label}{_RESET}")
        try:
            mod = importlib.import_module(module_path)
            # Cada módulo tiene un objeto 'suite' de tipo TestSuite
            suite = getattr(mod, "suite", None)
            if suite is None:
                print(f"  {_RED}ERROR: módulo '{module_path}' no tiene atributo 'suite'{_RESET}")
                total_failed += 1
                continue
            failed = suite.report()
            total_failed += failed
        except Exception as e:
            print(f"  {_RED}ERROR importando {module_path}: {e}{_RESET}")
            total_failed += 1

    elapsed = (time.perf_counter() - start_global) * 1000

    print(f"\n{_BOLD}{'═'*60}")
    if total_failed == 0:
        print(f"  {_GREEN}✔ TODAS LAS PRUEBAS PASARON{_RESET}{_BOLD}")
    else:
        print(f"  {_RED}✘ {total_failed} PRUEBA(S) FALLARON{_RESET}{_BOLD}")
    print(f"  Tiempo total de ejecución: {elapsed:.2f}ms")
    print(f"{'═'*60}{_RESET}\n")

    return 1 if total_failed > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
