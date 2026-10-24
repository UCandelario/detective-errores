# Instrucciones para GitHub Copilot

Las reglas completas están en [`AGENTS.md`](../AGENTS.md) y son obligatorias. Lo esencial:

- Pregunta primero qué tarea se hace (ID y carril, ver `docs/TAREAS.md`). Sin tarea no se escribe código.
- Cambia solo los archivos de esa tarea y de su carril. Nada de refactors ni "arreglos de paso".
- Funciones pequeñas (hasta 30 líneas, hasta 3 niveles de anidación), nombres explícitos en español, sin código muerto ni `except` que se traguen errores.
- Escribe primero la prueba, una por cada fila de `docs/CONTRATOS.md`. No borres ni debilites pruebas. Solo biblioteca estándar de Python 3.12, sin dependencias nuevas.
- El repositorio es público: nunca credenciales, tokens, webhooks ni datos personales. No ejecutes comandos de AWS ni de Terraform.
- No hagas push ni abras pull requests por tu cuenta, y nunca trabajes en `main`.
- Reporta lo que corriste con su resultado real y lo que no verificaste.
