"""Busca patrones de secretos en un cambio, en todo el repo o en archivos concretos.

Uso:
    python scripts/revisar_secretos.py --base origin/main   # solo las líneas añadidas respecto a una rama
    python scripts/revisar_secretos.py --todo               # todos los archivos versionados
    python scripts/revisar_secretos.py --rutas a.txt b.txt  # archivos concretos

Termina con código 1 si encuentra algo. NUNCA imprime el valor encontrado
(solo archivo, línea y tipo), para que el secreto no acabe en los logs.

Es una red de seguridad básica, no un escáner completo: no detecta todo.
Una línea con el texto `revisar-secretos: ignorar` se salta (para ejemplos en documentación).
"""
import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

MARCA_IGNORAR = "revisar-secretos: ignorar"

PATRONES = {
    "clave de acceso de AWS": re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    "clave secreta de AWS": re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*\S+"),
    "webhook de Slack": re.compile(r"hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"),
    "token de Slack": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    "token de GitHub": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})"),
    "llave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

# Nombres de archivo que nunca deben versionarse (coinciden con el .gitignore).
NOMBRES_PROHIBIDOS = [
    ".env", ".env.*", "*.pem", "*.key", "credentials*",
    "secrets.tfvars", "*.auto.tfvars", "*.tfstate", "*.tfstate.*",
]
NOMBRES_PERMITIDOS = [".env.example"]


def buscar_en_texto(texto):
    """Devuelve la lista de tipos de secreto que aparecen en una línea."""
    if MARCA_IGNORAR in texto:
        return []
    return [tipo for tipo, patron in PATRONES.items() if patron.search(texto)]


def nombre_prohibido(ruta):
    """True si el archivo no debería estar en el repo por su nombre."""
    partes = Path(ruta).parts
    if ".terraform" in partes:
        return True
    nombre = Path(ruta).name
    if any(fnmatch.fnmatch(nombre, p) for p in NOMBRES_PERMITIDOS):
        return False
    return any(fnmatch.fnmatch(nombre, p) for p in NOMBRES_PROHIBIDOS)


def lineas_anadidas(diff):
    """Recorre un diff unificado (-U0) y devuelve (archivo, numero_de_linea, texto) de las líneas añadidas."""
    archivo, numero = None, 0
    for linea in diff.splitlines():
        if linea.startswith("+++ "):
            ruta = linea[4:]
            archivo = ruta[2:] if ruta.startswith("b/") else None
        elif linea.startswith("@@"):
            coincide = re.search(r"\+(\d+)", linea)
            numero = int(coincide.group(1)) if coincide else 0
        elif linea.startswith("+") and archivo:
            yield archivo, numero, linea[1:]
            numero += 1


def revisar_lineas(lineas):
    """Aplica los patrones a (archivo, numero, texto) y devuelve hallazgos sin el valor encontrado."""
    return [
        (archivo, numero, tipo)
        for archivo, numero, texto in lineas
        for tipo in buscar_en_texto(texto)
    ]


def revisar_archivo(ruta):
    """Lee un archivo de texto completo y devuelve sus hallazgos; ignora binarios ilegibles."""
    try:
        texto = Path(ruta).read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    lineas = ((str(ruta), n, t) for n, t in enumerate(texto.splitlines(), start=1))
    return revisar_lineas(lineas)


def git(*argumentos):
    return subprocess.run(
        ["git", *argumentos], capture_output=True, text=True, check=True, encoding="utf-8"
    ).stdout


def hallazgos_de_cambio(base):
    diff = git("diff", "-U0", "--no-color", "--diff-filter=ACMR", f"{base}...HEAD")
    nombres = git("diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD").splitlines()
    hallazgos = revisar_lineas(lineas_anadidas(diff))
    hallazgos += [(n, 0, "nombre de archivo prohibido") for n in nombres if nombre_prohibido(n)]
    return hallazgos


def hallazgos_de_archivos(rutas):
    hallazgos = []
    for ruta in rutas:
        hallazgos += revisar_archivo(ruta)
        if nombre_prohibido(ruta):
            hallazgos.append((str(ruta), 0, "nombre de archivo prohibido"))
    return hallazgos


def main(argv=None):
    analizador = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    grupo = analizador.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--base", help="rama contra la que comparar, por ejemplo origin/main")
    grupo.add_argument("--todo", action="store_true", help="todos los archivos versionados")
    grupo.add_argument("--rutas", nargs="+", help="archivos concretos")
    args = analizador.parse_args(argv)

    if args.base:
        hallazgos = hallazgos_de_cambio(args.base)
    elif args.todo:
        hallazgos = hallazgos_de_archivos(git("ls-files").splitlines())
    else:
        hallazgos = hallazgos_de_archivos(args.rutas)

    if not hallazgos:
        print("Sin hallazgos.")
        return 0
    print(f"Se encontraron {len(hallazgos)} posibles secretos (el valor no se muestra):")
    for archivo, numero, tipo in hallazgos:
        donde = f"{archivo}:{numero}" if numero else archivo
        print(f"  - {donde}: {tipo}")
    print("Si es un falso positivo en documentación, añade 'revisar-secretos: ignorar' en esa línea.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
