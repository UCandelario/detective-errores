"""Corre las pruebas de todas las funciones, o solo las de una.

Uso:
    python scripts/probar.py              # todas las funciones
    python scripts/probar.py revisor      # solo functions/revisor

Cada función se prueba en un proceso aparte, porque todas usan un módulo
llamado `app` y no deben mezclarse. No usa dependencias externas ni AWS.
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUNCIONES = RAIZ / "functions"


def listar_funciones(nombre=None):
    """Devuelve las carpetas de funciones a probar; falla si el nombre no existe."""
    carpetas = sorted(p for p in FUNCIONES.iterdir() if p.is_dir())
    if nombre is None:
        return carpetas
    elegidas = [p for p in carpetas if p.name == nombre]
    if not elegidas:
        disponibles = ", ".join(p.name for p in carpetas)
        raise SystemExit(f"No existe la función '{nombre}'. Disponibles: {disponibles}")
    return elegidas


def probar(carpeta):
    """Corre unittest dentro de una carpeta y devuelve el código de salida."""
    print(f"\n=== {carpeta.name} ===", flush=True)
    resultado = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(carpeta), "-p", "test_*.py"],
    )
    return resultado.returncode


def main():
    nombre = sys.argv[1] if len(sys.argv) > 1 else None
    carpetas = listar_funciones(nombre)
    fallidas = [c.name for c in carpetas if probar(c) != 0]
    print("\n--- Resumen ---")
    print(f"Probadas: {len(carpetas)}. Fallidas: {len(fallidas)}.")
    if fallidas:
        print("Fallaron: " + ", ".join(fallidas))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
