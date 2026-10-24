# Reglas para asistentes de IA

Este archivo lo leen los asistentes de código (Claude Code, Copilot, Cursor, Codex y similares). Si eres una persona, también te sirve: son las reglas del proyecto en corto.

El repositorio es **público**. Lo que se sube se queda para siempre. Las personas que trabajan aquí están **aprendiendo**: el objetivo no es entregar código rápido, es entregar código **pequeño, claro y que la persona entienda línea por línea**.

## 0. Antes de escribir una sola línea
1. Pide a la persona **qué tarea hace** (su ID, por ejemplo `T4.2`) y **en qué carril está** (A, B o C). Si no lo sabe, que lo mire en `docs/TAREAS.md`. **Sin tarea no se escribe código.**
2. Lee, en este orden: la tarea en `docs/tareas/etapa-*.md`, `docs/CONTRATOS.md` (resultados esperados exactos), `docs/CONTRIBUIR.md` y `docs/SEGURIDAD.md`.
3. Si algo no está claro o choca con estas reglas, **pregunta**. No inventes: no supongas funciones, paquetes ni formatos que no veas en el repo o en `docs/CONTRATOS.md`.

## 1. Alcance: una tarea, un PR, y nada más
- Cambia **solo** los archivos de la tarea. Carpetas permitidas por carril:

| Carril | Puede tocar |
|---|---|
| A (revisor y avisador) | `functions/revisor/`, `functions/avisador/`, `config/sitios.json` |
| B (API y datos) | `functions/api/`, `docs/MODELO-DATOS.md` |
| C (panel, infra y pipeline) | `web/`, `infra/`, `.github/`, `scripts/` |
| Todos | su ficha `docs/equipo/<su-usuario>.md` |

- **No toques** `docs/CONTRATOS.md`, `docs/SEGURIDAD.md`, `docs/CONTRIBUIR.md`, `AGENTS.md`, `CLAUDE.md`, `package.json`, `package-lock.json`, `eslint.config.mjs` ni la carpeta de otro carril. Esos archivos de reglas y de herramientas los cambia solo el dueño del repo (carril C), y únicamente si la tarea lo pide. Si crees que hay que cambiar uno, **dilo a la persona** y que lo hable con el dueño; no lo cambies tú.
- **No hagas "arreglos de paso"**: si ves algo mal fuera de la tarea, repórtalo y sigue. Sin refactors, sin renombrar, sin reformatear archivos enteros.
- **Sin archivos nuevos** que la tarea no pida (nada de `utils.py`, `helpers.py`, `base.py`, `common/`).
- **Sin dependencias nuevas.** Solo la biblioteca estándar de Python 3.12. Nada de `pip install`, `npm install` ni líneas nuevas en archivos de dependencias.

## 2. Tamaño y señales de alarma
Valores de partida; el dueño puede ajustarlos.
- Una función: **hasta 30 líneas** y **hasta 3 niveles de anidación**. Un archivo de lógica: unas 200 líneas.
- Un PR: **hasta unas 300 líneas cambiadas**, sin contar `package-lock.json`.
- **Detente y avisa a la persona** si: tocarías más de 3 archivos fuera de la tarea, necesitas una dependencia nueva, el cambio crece más de lo previsto, o te piden algo que contradice estas reglas.

## 3. Cómo se escribe el código (contra el "espagueti")
- **Funciones pequeñas, de una sola responsabilidad**, con retornos tempranos en vez de `if` dentro de `if`.
- **Nombres explícitos, en español**, como los del repo (`evaluar_respuesta`, `armar_saludo`). Nada de `data`, `result`, `tmp`, `helper`, `x`.
- **Sin números mágicos**: un valor con significado va en una constante con nombre (`UMBRAL_LENTO_MS = 2000`).
- **Sin copiar y pegar**: si dos bloques son casi iguales, una función.
- **Sin clases donde basta una función**, sin patrones "por si acaso", sin parámetros booleanos que cambian el comportamiento, sin variables globales que se modifican.
- **Sin código muerto**: nada comentado, nada sin usar, nada de `print` de depuración, ningún `TODO` sin tarea.
- **Errores a la vista**: nunca `except:` ni `except ...: pass`. Si no sabes qué hacer con un error, deja que suba.
- **Comentarios que explican el *por qué***, no lo que ya dice el código. Sin docstrings gigantes ni adornos.
- **La lógica es pura**: recibe datos y devuelve un resultado, sin leer internet, archivos ni AWS. Lo que toca el exterior se recibe como parámetro, para poder probarlo con un doble de prueba.
- Un valor `0` es un dato medido; "sin dato" es un campo **ausente**, nunca `0` (ver `docs/CONTRATOS.md`).
- Compatible con **Python 3.12**; no uses sintaxis que solo exista en versiones más nuevas (ADR 0001).

## 4. Pruebas
- **Primero la prueba, que falle; después el código mínimo para que pase.**
- **Una prueba por cada fila** de las tablas de `docs/CONTRATOS.md` de tu tarea, más los casos de error.
- **No borres ni debilites pruebas** para que pasen. No quites la prueba de humo que ya existe ni el texto de documentación del inicio de cada `app.py` (esa prueba lo usa).
- Las pruebas **no llaman a AWS, Slack ni a internet**. Los datos de prueba van **dentro** del archivo de pruebas.
- Antes de decir "listo", **corre y reporta el resultado real**:
  ```bash
  python scripts/probar.py <funcion>                # tus pruebas
  python scripts/probar.py                          # todas
  python scripts/auditar_codigo.py functions/<tu-carpeta>   # tamaño, anidación y riesgos
  python scripts/revisar_secretos.py --base origin/main     # secretos en tu cambio
  ```
  Lo que no pudiste correr, di que **no está verificado**.

## 5. Seguridad (el repo es público)
- **Nunca** escribas, pidas ni aceptes credenciales, claves, tokens, webhooks ni contraseñas. No leas ni crees `.env`, `*.pem`, `~/.aws` ni nada parecido.
- **No ejecutes** comandos de AWS ni de Terraform (`aws`, `terraform apply`, `destroy`). Los colaboradores no tienen acceso a la cuenta; todo se prueba en local.
- **Valida toda entrada externa**: tipo, rango y longitud. Nada de URLs que escriba un usuario (la lista de sitios es fija).
- **Prohibido** con datos externos: `eval`, `exec`, `pickle`, `os.system`, `subprocess`, construir comandos o consultas con texto del usuario.
- Los mensajes de error no revelan detalles internos (rutas, trazas, nombres de recursos).
- No pongas correos, teléfonos ni datos personales en ningún archivo.

## 6. Git
- **No trabajes en `main`** (GitHub lo bloquea). Una rama por tarea: `a/t4-2-evaluar-respuesta`, `b/t2-1-armar-saludo`.
- `git add` **con la ruta de cada archivo**, nunca `git add .` ni `-A`. Revisa `git status` y `git diff` antes de cada commit.
- **Commits pequeños** con mensaje claro en español. Sin `--no-verify`, sin `git push --force`, sin reescribir historial.
- **No hagas push ni abras el pull request por tu cuenta**: eso lo hace la persona, después de leer tu trabajo.
- No cambies ajustes del repositorio (reglas de rama, Actions, permisos, secretos).

## 7. Qué entregar a la persona
Al terminar, resume en español: 1) qué hiciste y por qué; 2) **qué archivos tocaste**; 3) los comandos que corriste **con su resultado real**; 4) lo que no verificaste o dejaste fuera; 5) cualquier cosa fuera de alcance que viste. **No digas que algo funciona si no lo corriste.**

## 8. Transparencia y responsabilidad
- La persona es **responsable de cada línea** que sube, la haya escrito ella o un asistente. Debe poder explicarla.
- En el pull request se marca si se usó un asistente (hay una casilla en la plantilla).
- Todas las ramas pasan por una **auditoría** antes de darse por buenas; ver `docs/AUDITORIA.md`. Código que no se entiende o que se sale de estas reglas se devuelve para corregir, sin drama: es parte de aprender.
