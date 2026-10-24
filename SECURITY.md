# Política de seguridad

Este es un proyecto de práctica, pero se toma en serio no exponer credenciales ni datos.

## Cómo reportar un problema de seguridad
**No abras un issue público.** Usa el reporte privado de GitHub: pestaña **Security** del repositorio → **Report a vulnerability**. Solo lo verán quienes mantienen el repo.

Sirve para, por ejemplo:
- Una credencial, token o webhook que se haya colado en el código o en el historial.
- Una forma de abusar de la API o de la página (peticiones masivas, entradas que rompen validaciones).
- Un permiso demasiado amplio en la infraestructura.

Si encuentras un secreto expuesto, **no lo uses ni lo copies**: repórtalo y se rotará.

## Qué versiones se atienden
Solo la rama `main`.

## Cómo se protege el repositorio
- `main` solo recibe cambios por pull request con revisión; ver [`docs/CONTRIBUIR.md`](docs/CONTRIBUIR.md).
- Cada PR pasa por pruebas, revisión de secretos, ESLint, revisión de sintaxis y análisis de CodeQL.
- GitHub escanea secretos y bloquea los push que los contengan.
- Reglas internas para el equipo: [`docs/SEGURIDAD.md`](docs/SEGURIDAD.md).
