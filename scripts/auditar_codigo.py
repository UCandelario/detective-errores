"""Revisión rápida de calidad y de riesgos obvios en archivos Python.

Uso:
    python scripts/auditar_codigo.py functions/revisor
    python scripts/auditar_codigo.py functions/api/app.py --max-lineas 25 --max-anidacion 2

Marca, sin ejecutar nada del código revisado:
  - funciones demasiado largas o con demasiada anidación;
  - `except` que se traga el error (desnudo, o con `pass`);
  - llamadas riesgosas: eval, exec, compile, __import__, os.system, pickle, subprocess;
  - pendientes (TODO, FIXME) sin tarea.

Termina con código 1 si encuentra algo. Es una ayuda para la revisión humana, no la
reemplaza: puede dar falsos positivos y no detecta todo.
"""
import argparse
import ast
import re
import sys
from pathlib import Path

MAX_LINEAS_POR_DEFECTO = 30
MAX_ANIDACION_POR_DEFECTO = 3

LLAMADAS_PELIGROSAS = {"eval", "exec", "compile", "__import__"}
ATRIBUTOS_PELIGROSOS = {
    ("os", "system"), ("os", "popen"),
    ("pickle", "load"), ("pickle", "loads"), ("marshal", "loads"),
}
BLOQUES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith, ast.Match)
PENDIENTES = re.compile(r"#.*\b(TODO|FIXME|XXX)\b")


def anidacion_maxima(nodo, nivel=0):
    """Profundidad máxima de bloques (if, for, while, try, with) dentro de un nodo.

    Un `elif` no cuenta como un nivel más: es la misma decisión, no una anidada.
    """
    maximo = nivel
    for campo, valor in ast.iter_fields(nodo):
        hijos = valor if isinstance(valor, list) else [valor]
        for hijo in hijos:
            if not isinstance(hijo, ast.AST):
                continue
            es_elif = (
                isinstance(nodo, ast.If) and campo == "orelse"
                and len(valor) == 1 and isinstance(hijo, ast.If)
            )
            sube = isinstance(hijo, BLOQUES) and not es_elif
            maximo = max(maximo, anidacion_maxima(hijo, nivel + (1 if sube else 0)))
    return maximo


def _nombre_llamada(llamada):
    """Devuelve ('eval', None) o ('os', 'system') según cómo se llame; None si no aplica."""
    func = llamada.func
    if isinstance(func, ast.Name):
        return func.id, None
    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
        return func.value.id, func.attr
    return None


def _cuerpo_solo_pass(manejador):
    return all(isinstance(n, ast.Pass) for n in manejador.body)


def revisar_codigo(codigo, ruta="<texto>", max_lineas=MAX_LINEAS_POR_DEFECTO,
                   max_anidacion=MAX_ANIDACION_POR_DEFECTO):
    """Devuelve una lista de (ruta, linea, mensaje) con lo que merece una segunda mirada."""
    hallazgos = []
    arbol = ast.parse(codigo)

    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            largo = nodo.end_lineno - nodo.lineno + 1
            if largo > max_lineas:
                hallazgos.append((ruta, nodo.lineno,
                                  f"la función {nodo.name} tiene {largo} líneas (máximo {max_lineas}): conviene partirla"))
            nivel = anidacion_maxima(nodo)
            if nivel > max_anidacion:
                hallazgos.append((ruta, nodo.lineno,
                                  f"la función {nodo.name} anida {nivel} niveles (máximo {max_anidacion}): usa retornos tempranos o funciones auxiliares"))
        elif isinstance(nodo, ast.ExceptHandler):
            if nodo.type is None:
                hallazgos.append((ruta, nodo.lineno, "except desnudo: captura todo, incluso errores que no esperabas"))
            elif _cuerpo_solo_pass(nodo):
                hallazgos.append((ruta, nodo.lineno, "except que ignora el error con pass: el fallo desaparece sin dejar rastro"))
        elif isinstance(nodo, ast.Call):
            nombre = _nombre_llamada(nodo)
            if nombre is None:
                continue
            principal, atributo = nombre
            if atributo is None and principal in LLAMADAS_PELIGROSAS:
                hallazgos.append((ruta, nodo.lineno, f"llamada riesgosa: {principal}()"))
            elif (principal, atributo) in ATRIBUTOS_PELIGROSOS:
                hallazgos.append((ruta, nodo.lineno, f"llamada riesgosa: {principal}.{atributo}()"))
            elif principal == "subprocess":
                hallazgos.append((ruta, nodo.lineno, f"ejecuta procesos externos: subprocess.{atributo}()"))
        elif isinstance(nodo, ast.Import) and any(a.name.split(".")[0] == "subprocess" for a in nodo.names):
            hallazgos.append((ruta, nodo.lineno, "importa subprocess: ¿de verdad hace falta ejecutar procesos?"))
        elif isinstance(nodo, ast.ImportFrom) and (nodo.module or "").split(".")[0] == "subprocess":
            hallazgos.append((ruta, nodo.lineno, "importa subprocess: ¿de verdad hace falta ejecutar procesos?"))

    for numero, linea in enumerate(codigo.splitlines(), start=1):
        if PENDIENTES.search(linea):
            hallazgos.append((ruta, numero, "pendiente (TODO/FIXME) sin tarea asociada"))

    return sorted(hallazgos, key=lambda h: (h[0], h[1]))


def archivos_python(rutas):
    """Expande carpetas a sus archivos .py, sin __pycache__ ni node_modules."""
    for texto in rutas:
        ruta = Path(texto)
        if ruta.is_dir():
            for archivo in sorted(ruta.rglob("*.py")):
                if not {"__pycache__", "node_modules", ".venv"} & set(archivo.parts):
                    yield archivo
        else:
            yield ruta


def main(argv=None):
    analizador = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    analizador.add_argument("rutas", nargs="+", help="archivos o carpetas con código Python")
    analizador.add_argument("--max-lineas", type=int, default=MAX_LINEAS_POR_DEFECTO)
    analizador.add_argument("--max-anidacion", type=int, default=MAX_ANIDACION_POR_DEFECTO)
    args = analizador.parse_args(argv)

    hallazgos, revisados = [], 0
    for archivo in archivos_python(args.rutas):
        revisados += 1
        try:
            codigo = archivo.read_text(encoding="utf-8")
            hallazgos += revisar_codigo(codigo, str(archivo), args.max_lineas, args.max_anidacion)
        except (OSError, UnicodeDecodeError, SyntaxError) as error:
            hallazgos.append((str(archivo), 0, f"no se pudo revisar: {type(error).__name__}"))

    if not hallazgos:
        print(f"Sin hallazgos en {revisados} archivo(s).")
        return 0
    print(f"{len(hallazgos)} hallazgo(s) en {revisados} archivo(s):")
    for ruta, linea, mensaje in hallazgos:
        donde = f"{ruta}:{linea}" if linea else ruta
        print(f"  - {donde}: {mensaje}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
