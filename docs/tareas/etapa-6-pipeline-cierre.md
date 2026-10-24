# Etapa 6: pipeline y cierre

**Carril C, con apoyo de todos.** **Meta:** que los cambios se prueben solos (T6.1 a T6.3) y, **si se decide**, que se desplieguen con aprobación del dueño, sin guardar claves de AWS en GitHub (T6.4 y T6.5).

> **T6.4 y T6.5 son opcionales.** AWS no depende de GitHub: el dueño puede desplegar siempre a mano desde su PC o CloudShell (`aws s3 sync`, `terraform apply`), como describe [`DESPLIEGUE.md`](../DESPLIEGUE.md). El despliegue automático solo ahorra pasos y es un buen ejercicio de CI/CD, pero no hace falta para que el proyecto funcione ni para quedarse dentro del plan gratuito. Se hacen solo si el equipo quiere practicarlos, y siempre con OK del dueño.

**Antes de empezar:** el repo es privado y el plan gratuito de GitHub incluye 2.000 minutos de Actions al mes. Revisa en *Settings → Billing → Spending limit* que el límite de gasto esté en **0 USD**.

---

### T6.1 Pruebas automáticas en cada pull request (sin AWS) ✅ (`.github/workflows/ci.yml`)
- **Depende de:** T0.2 · **Tiempo:** 1 h · **Costo:** 0 (minutos gratuitos)
- **Pasos:** workflow en `.github/workflows/` que corre `python scripts/probar.py` en cada PR. **No usa credenciales ni acciones de terceros**: solo acciones oficiales de GitHub (`actions/checkout`, `actions/setup-python`), previo OK del dueño.
- **Prueba rápida:** abrir un PR con una prueba que falla a propósito y comprobar que el workflow la marca en rojo.
- **Hecho cuando:** el check aparece en los PR y falla ante una prueba rota.

### T6.2 Revisión de secretos antes de fusionar ✅ (`.github/workflows/secretos.yml` y `scripts/revisar_secretos.py`)
- **Depende de:** T6.1 · **Tiempo:** 1 h · **Costo:** 0
- **Pasos:** añade un paso que busca patrones obvios de credenciales (`AKIA`, `hooks.slack.com`, `-----BEGIN`) en el cambio, con un script propio. **No uses herramientas ni acciones de terceros sin acuerdo.**
- **Hecho cuando:** un commit de prueba con un patrón falso (en una rama descartable) hace fallar el check.

### T6.3 Validación de Terraform en el PR
- **Depende de:** T1.7, T6.1 · **Tiempo:** 1 h · **Costo:** 0
- **Pasos:** el workflow corre `terraform fmt -check` y `terraform validate` **sin** `plan` ni credenciales.
- **Hecho cuando:** un archivo `.tf` mal formado hace fallar el check.

### T6.4 Rol de AWS para GitHub (OIDC) con permisos mínimos (opcional)
- **Depende de:** T6.1, OK del dueño · **Tiempo:** 2 h · **Costo:** 0
- **Cuándo hacerla:** solo si se quiere desplegar desde GitHub. Sin ella, el despliegue manual del dueño sigue valiendo.
- **Aprendes:** confianza federada: GitHub se identifica ante AWS sin claves guardadas.
- **Pasos:** crear el proveedor OIDC y un rol que **solo** el repo y la rama `main` pueden asumir, con permisos limitados a lo que el despliegue necesita. Todo en Terraform y revisado por otra persona.
- **Cuidado:** la condición de confianza debe fijar el repo y la rama; un rol demasiado abierto permitiría que otros repos lo asuman.
- **Hecho cuando:** un workflow de prueba asume el rol y ejecuta `aws sts get-caller-identity` correctamente; desde otra rama o repo, no puede.

### T6.5 Despliegue con aprobación manual (opcional)
- **Depende de:** T6.4 · **Tiempo:** 2 h · **Costo:** 0
- **Cuándo hacerla:** igual que T6.4; si se omite, el despliegue lo ejecuta el dueño a mano.
- **Pasos:** workflow de despliegue que se dispara a mano o al fusionar en `main` y **espera la aprobación del dueño**. En repos privados con plan gratuito, "Environments" con revisores requeridos puede no estar disponible (**no verificado**); si no lo está, el despliegue se dispara solo manualmente (`workflow_dispatch`) y lo ejecuta el dueño.
- **Hecho cuando:** un cambio llega a producción sin que nadie tenga claves guardadas y sin despliegue automático sin aprobar.

### T6.6 Revisión de seguridad y del historial
- **Depende de:** T4.12 · **Tiempo:** 2 h · **Costo:** 0
- **Pasos:** revisar `docs/SEGURIDAD.md` punto por punto: secretos en el historial completo, permisos IAM sin comodines, bucket privado, tope de concurrencia, capacidad de DynamoDB, correo de los commits.
- **Hecho cuando:** hay un informe corto con lo encontrado y lo corregido.

### T6.7 README reproducible y recursos al día
- **Depende de:** T4.12, T5.7 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Prueba rápida:** una persona que no escribió el código sigue el README desde cero y llega al mismo resultado (en local, sin AWS).
- **Hecho cuando:** `docs/RECURSOS.md` lista cada recurso con costo y cómo borrarlo, y el README tiene los comandos reales.

### T6.8 Decidir el futuro cuando venza el plan de AWS
- **Depende de:** T6.7 · **Tiempo:** 1 h · **Costo:** 0
- **Contexto:** los créditos vencen el **2027-04-23** y después se pierde el acceso a los servicios.
- **Pasos:** decidir y anotar en un ADR si se pasa a plan de pago, o si la página estática se mueve a otro hosting gratuito. **GitHub Pages en repo privado requiere plan de pago; en repo público es gratis.** Cloudflare Pages se evalúa si el repo sigue privado (**no verificado**).
- **Antes de hacer público el repo:** revisión completa del historial (T6.6) y del correo de los commits.
- **Hecho cuando:** hay un ADR con la decisión y el plan de migración.
