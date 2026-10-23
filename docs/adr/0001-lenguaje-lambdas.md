# ADR 0001: Python para las Lambdas

- **Estado:** aceptada (2026-10-23)
- **Decide:** dueño de la cuenta

## Contexto
Hay que elegir un lenguaje para las tres Lambdas (revisor, avisador y API) antes de escribir código. El equipo son tres personas que están aprendiendo, y el objetivo es poder probar cada cambio rápido y en local.

## Decisión
Python para todas las funciones. Las pruebas usan `unittest` de la biblioteca estándar, sin dependencias externas.

## Por qué
- Ya está instalado en la máquina del dueño (3.14) y es sencillo de leer para quien aprende.
- `boto3` (el SDK de AWS) viene incluido en el runtime de Lambda, así que no hace falta empaquetar dependencias para las primeras etapas.
- `unittest` evita instalar nada: cualquiera con Python corre las pruebas con un comando.

## Alternativas consideradas
- **Node.js:** también instalado y con runner de pruebas integrado, pero el SDK v3 se empaqueta aparte y no aporta ventaja para este proyecto.
- **Mixto (Python y JavaScript en la web):** la página lleva JavaScript de todos modos, pero tener dos conjuntos de pruebas suma complejidad. La web se prueba a mano con una lista de verificación.

## Consecuencias
- Cada función vive en `functions/<nombre>/` con `app.py` y `test_app.py`.
- Todas las pruebas se corren con `python scripts/probar.py` (ver `docs/LOCAL.md`).
- El **runtime exacto de Lambda** (por ejemplo, Python 3.12 o 3.13) se fija al crear la primera función; el Python local puede ser más nuevo. Hay que verificar qué versiones soporta Lambda en ese momento y evitar sintaxis que solo exista en versiones muy nuevas.
- Si en el futuro hay dependencias externas, se empaquetan por función y se acuerdan antes (ver `CONTRIBUIR.md`).
