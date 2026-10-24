# Auditoría de ramas y pull requests

Antes de dar por buena una rama (o al terminar una etapa) se **audita**. Sirve para comprobar que el código es pequeño, claro, seguro y que **se quedó dentro de la tarea**, sobre todo cuando se usó un asistente de IA. No es un examen: quien escribió el código aprende de lo que se encuentre, y lo que falle se corrige en el mismo PR.

Quién audita: el dueño del repo, otra persona del equipo, o un asistente de IA bajo las mismas reglas de [`AGENTS.md`](../AGENTS.md). Quien audita **no es quien escribió** la rama.

## 0. Preparar una copia desechable
Se audita en una copia aparte, para poder probar cosas sin ensuciar tu trabajo:
```bash
git fetch origin
git worktree add ../auditoria origin/<rama>
cd ../auditoria
```
Al terminar, vuelve a tu carpeta y elimina la copia: `git worktree remove --force ../auditoria`.

## 1. Alcance: ¿tocó solo lo que debía?
```bash
git diff --name-only origin/main...origin/<rama>
git diff --shortstat origin/main...origin/<rama>
```
| Pregunta | Debe ser |
|---|---|
| ¿Todos los archivos son de la tarea y del carril? (ver `AGENTS.md`, sección 1) | Sí. Archivos de otro carril, de reglas o de herramientas: **hallazgo** |
| ¿Hay archivos nuevos que la tarea no pedía (`utils`, `helpers`, `base`...)? | No |
| ¿Cambió `package.json`, `package-lock.json`, `.github/` o un archivo de dependencias? | No, salvo carril C con tarea que lo pida |
| ¿Cuántas líneas cambió? | Unas 300 como máximo, sin contar `package-lock.json`. Si pasa, **partir el PR** |
| ¿El PR hace una sola cosa? | Sí |

## 2. Pruebas
```bash
python scripts/probar.py
python -m unittest discover -s scripts -p "test_*.py"
```
- ¿Pasan todas? ¿Hay **una prueba por cada fila** de `docs/CONTRATOS.md` de la tarea, más los casos de error?
- ¿Se borró o debilitó alguna prueba existente (incluida la de humo)? Compara con `git diff origin/main...origin/<rama> -- '*test_*'`.
- ¿Las pruebas comprueban algo de verdad? Desconfía de `assertTrue(True)`, de pruebas que repiten la implementación y de pruebas sin `assert`.
- **Prueba de sensibilidad** (en la copia desechable): rompe el código a propósito, por ejemplo cambia un `>` por `>=` o borra una regla, y corre las pruebas. **Al menos una debe fallar.** Si todo sigue en verde, las pruebas no protegen esa regla: hallazgo.

## 3. Calidad: ¿es espagueti?
```bash
python scripts/auditar_codigo.py functions
```
Marca funciones de más de 30 líneas, anidación de más de 3 niveles, `except` que se traga el error, `eval`/`exec`/`pickle`/`subprocess` y pendientes sin tarea. Es una ayuda: puede dar falsos positivos, y no detecta todo. (Sobre `scripts/` no tiene sentido correrlo: esos scripts sí lanzan procesos a propósito.)

Lee además el código, con esta lista:
- [ ] Cada función hace una sola cosa y se entiende sin leer las demás.
- [ ] Los nombres dicen qué son; no hay `data`, `result`, `tmp`, `helper`, `x`.
- [ ] No hay números mágicos: los valores con significado tienen nombre.
- [ ] No hay código copiado y pegado, ni comentado, ni sin usar, ni `print` de depuración.
- [ ] No hay clases, capas ni parámetros "por si acaso" que nadie usa todavía.
- [ ] Los comentarios explican el *por qué*; no repiten el código.
- [ ] La lógica es pura (sin red, archivos ni AWS) y lo externo entra como parámetro.
- [ ] `0` y "sin dato" no se confunden (ver `docs/CONTRATOS.md`).

## 4. Seguridad
```bash
python scripts/revisar_secretos.py --base origin/main
```
- ¿Entradas externas validadas (tipo, rango, longitud)? ¿Algún mensaje de error revela detalles internos?
- ¿Aparece `eval`, `exec`, `pickle`, `os.system` o `subprocess` con datos de fuera? (El auditor de código lo marca.)
- ¿Hay correos, teléfonos, nombres de recursos reales o datos personales en archivos o comentarios?
- Recuerda: el repo es **público**. Un secreto que llegó a una rama ya está expuesto aunque el PR no se fusione; si pasa, **rotarlo**, no solo borrarlo.

## 5. Señales de código generado sin revisar
Una sola no prueba nada; varias juntas piden una conversación:
- Comentarios o docstrings que repiten lo que dice la línea de abajo, o enormes para una función de tres líneas.
- Funciones o parámetros que no se usan, o abstracciones con un solo uso.
- `try`/`except` amplios que ocultan errores, o validaciones que el contrato no pide.
- Estilo distinto al del resto del repo (nombres en inglés, comillas o sangrías diferentes).
- Archivos o carpetas que la tarea no mencionaba.
- Mensajes de commit genéricos ("update", "fix") o un solo commit enorme.
- Pruebas que parecen escritas a partir del código y no del contrato.
- La persona no puede explicar una función cuando se le pregunta.

## 6. Conversación con quien escribió la rama
Pide, con calma, que explique con sus palabras **dos funciones o dos pruebas** de su rama. Si las explica bien, el código es suyo, lo haya escrito quien lo haya escrito. Si no, no es una falta: es una señal de que esa parte hay que simplificar o repasar juntos antes de fusionar.

## 7. Veredicto
| Veredicto | Cuándo |
|---|---|
| **GO** | Sin hallazgos de alcance ni de seguridad, pruebas suficientes y código claro |
| **GO con cambios** | Hallazgos menores de estilo o pruebas que se corrigen en el mismo PR |
| **NO-GO** | Se salió del alcance, hay un riesgo de seguridad, faltan pruebas del contrato o no se entiende el código |

Plantilla de informe (se pega como comentario del PR):
```text
Auditoría de <rama> (commit <hash>) -- Veredicto: GO / GO con cambios / NO-GO

Alcance:    <archivos fuera de la tarea, o "ninguno">
Pruebas:    <n> pasan; faltan: <filas del contrato sin prueba, o "ninguna">; sensibilidad: <qué se rompió y qué prueba falló>
Calidad:    <salida de auditar_codigo.py y hallazgos de lectura>
Seguridad:  <secretos, entradas, llamadas riesgosas>
No verificado: <lo que no se pudo comprobar>
Pedido:     <qué debe corregirse antes de fusionar, con archivo:línea>
```
Cada hallazgo lleva `archivo:línea` y una propuesta concreta. Se separa lo **comprobado** de lo que es **opinión**.
