# Etapa 0: base del proyecto

**Responsable:** dueño de la cuenta. **Meta:** que los tres puedan trabajar y probar en local sin tocar AWS.

Formato de cada tarea: carril, dependencias, tiempo estimado, costo, qué se aprende, pasos, **prueba rápida** y **hecho cuando**.

---

### T0.1 Repo, documentación y presupuesto ✅
- **Carril:** C · **Depende de:** nada · **Tiempo:** hecho · **Costo:** 0
- **Aprendes:** repo privado, alertas de presupuesto.
- **Hecho cuando:** el repo existe en GitHub y los dos presupuestos de AWS están en estado OK.

### T0.2 Base de código y lenguaje ✅
- **Carril:** C · **Depende de:** T0.1 · **Tiempo:** hecho en la rama `c/base-proyecto` · **Costo:** 0
- **Aprendes:** estructura por funciones, ADR, pruebas sin dependencias.
- **Prueba rápida:** `python scripts/probar.py` termina con "Probadas: 3. Fallidas: 0."
- **Hecho cuando:** el pull request de la base está fusionado en `main`.

### T0.3 Invitar a los colaboradores
- **Carril:** C · **Depende de:** T0.1 · **Tiempo:** 5 min · **Costo:** 0
- **Pasos:** GitHub → repo → Settings → Collaborators → Add people, con permiso de escritura. Cada persona acepta la invitación por correo.
- **Prueba rápida:** cada colaborador corre `git clone` del repo y ve los archivos.
- **Hecho cuando:** las dos personas clonaron el repo y corrieron `python scripts/probar.py` con éxito.

### T0.4 Cada quien deja su equipo listo
- **Carril:** todos · **Depende de:** T0.3 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** configurar git y Python, y correr pruebas en local.
- **Pasos:** instalar Git y Python 3.12 o superior; configurar `git config user.name` y `user.email` (ojo: ese correo queda en los commits; elige el que quieras mostrar); clonar el repo; correr las pruebas.
- **Prueba rápida:** `python --version` y `python scripts/probar.py`.
- **Hecho cuando:** las pruebas pasan en la máquina de cada quien.

### T0.5 Primer pull request de práctica
- **Carril:** todos · **Depende de:** T0.4 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** el flujo rama → commit → pull request → revisión → fusión.
- **Pasos:** cada colaborador crea una rama (`a/practica-flujo` o `b/practica-flujo`), añade su nombre y el carril a `docs/EQUIPO.md` (archivo nuevo), abre un PR y otra persona lo revisa y lo fusiona.
- **Prueba rápida:** el PR aparece en GitHub con la plantilla y la lista de verificación.
- **Hecho cuando:** los dos PR de práctica están fusionados por una persona distinta de su autor.

### T0.6 Perfil de AWS CLI local (solo dueño)
- **Carril:** C · **Depende de:** nada · **Tiempo:** 30 min · **Costo:** 0
- **Aprendes:** autenticación sin claves largas en archivos.
- **Nota:** el CLI ya está instalado. Falta decidir **cómo** autenticar sin guardar claves de larga duración (opciones a evaluar: inicio de sesión desde la consola con `aws login`, o IAM Identity Center). Esto se decide con el dueño antes de hacerlo; las credenciales nunca se pegan en el chat ni en el repo.
- **Prueba rápida:** `aws sts get-caller-identity --profile personal` muestra la cuenta personal.
- **Hecho cuando:** el comando anterior responde con la cuenta correcta. Los colaboradores no necesitan esto.
