# Tareas y reparto

Somos tres personas. El reparto es una propuesta y se puede ajustar de común acuerdo. Cada carril es dueño de su carpeta para no pisarse.

| Carril | Qué hace | Carpeta principal | Responsable |
|---|---|---|---|
| **A** | Revisor, EventBridge y avisador a Slack | `functions/revisor/`, `functions/avisador/` | por asignar |
| **B** | API, DynamoDB y pruebas | `functions/api/`, modelo de datos en `docs/` | por asignar |
| **C** | Panel web, Terraform y pipeline (coordina la infraestructura) | `web/`, `infra/`, `.github/` | dueño de la cuenta |

Decisión pendiente antes de empezar con funciones: **lenguaje de las Lambdas** (Python o Node). Se decide una vez y se anota como ADR en `docs/adr/`.

## Orden de trabajo
Una cosa nueva por vez. Cada etapa termina con: pruebas en local, pull request revisado, documentación actualizada y, si toca AWS, aprobación de despliegue.

### Etapa 0: base (dueño de la cuenta, ya hecho o en curso)
- [x] Cuenta AWS verificada y alerta de presupuesto creada.
- [ ] Repo privado con esta documentación y colaboradores invitados.
- [ ] Decidir lenguaje de las Lambdas (ADR).

### Etapa 1: la página en S3 (carril C)
- [ ] Página estática mínima en `web/`.
- [ ] Bucket S3 privado y subida manual de la página (se aprende en la consola).
- [ ] Repetir lo mismo en Terraform (`infra/`).
- [ ] CloudFront con acceso restringido al bucket.

### Etapa 2: primera Lambda (carril B, apoyo de C)
- [ ] Lambda "hola" que devuelve JSON, con prueba unitaria en local.
- [ ] Publicarla con Function URL y llamarla desde la página.

### Etapa 3: datos (carril B)
- [ ] Definir el modelo de la tabla (claves, TTL) y escribirlo en `docs/`.
- [ ] Tabla DynamoDB provisionada en Terraform.
- [ ] La API lista el estado actual y el historial de un sitio.

### Etapa 4: el detective (carril A)
- [ ] Revisor: lee la lista fija de sitios, mide código y latencia, guarda en DynamoDB.
- [ ] EventBridge Scheduler lo dispara cada 5 minutos.
- [ ] Avisador: detecta cambios de estado y manda el mensaje a Slack.
- [ ] Webhook de Slack en SSM Parameter Store (nunca en el repo).

### Etapa 5: panel completo (carril C)
- [ ] La página muestra estado actual, historial y colores por estado.

### Etapa 6: pipeline y cierre (carril C, con apoyo de todos)
- [ ] GitHub Actions con OIDC hacia AWS, con permisos mínimos.
- [ ] Despliegue con aprobación manual del dueño de la cuenta.
- [ ] Revisión de seguridad y de secretos en el historial.
- [ ] README reproducible, `docs/RECURSOS.md` al día y lecciones aprendidas.
- [ ] Decidir si el repo pasa a público y dónde vive la página cuando venza el plan de AWS.

## Dependencias
- La etapa 3 necesita el lenguaje decidido (etapa 0).
- La etapa 4 necesita el modelo de datos (etapa 3) y el bucket/API funcionando solo para el panel, no para el revisor.
- La etapa 6 necesita que las etapas 1 a 4 existan en Terraform.

## Cómo tomar una tarea
1. Elige una casilla sin dueño en tu carril, o acuerda con el equipo si es de otro.
2. Crea una rama (ver [`CONTRIBUIR.md`](CONTRIBUIR.md)).
3. Marca la casilla en el mismo pull request que la cierra.
