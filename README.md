# Detective de errores

Proyecto de **práctica entre tres personas** para aprender a construir y desplegar aplicaciones serverless en AWS (Lambda, S3, DynamoDB, EventBridge, Slack, Terraform y CI/CD). El resultado es una página web que vigila si unos sitios están vivos y avisa por Slack cuando uno cae o se recupera.

No es un proyecto de trabajo: usa una cuenta AWS **personal** y debe quedar **gratis**.

> Estado: en arranque (2026-10-23). El orden de trabajo está en [`docs/TAREAS.md`](docs/TAREAS.md).

## Qué hace
```text
EventBridge (cada 5 min) → Lambda "revisor" → DynamoDB
                                  │              ↑
                                  └→ Lambda "avisador" → Slack
Página en S3 → Lambda "API" → DynamoDB
```
1. Un reloj dispara la revisión cada pocos minutos.
2. El revisor consulta una **lista fija** de sitios y mide código de respuesta y latencia.
3. Los resultados se guardan en DynamoDB.
4. Si el estado de un sitio **cambia**, se avisa a Slack (no en cada revisión).
5. La página muestra el estado actual y el historial.

Detalle y alcance: [`docs/PROYECTO.md`](docs/PROYECTO.md).

## Estructura
| Carpeta | Para qué |
|---|---|
| `web/` | La página (estática) |
| `functions/` | Funciones Lambda (revisor, avisador, API) |
| `infra/` | Infraestructura como código (Terraform) |
| `docs/` | Documentación, decisiones (ADR) y lecciones aprendidas |

## Antes de tocar nada
Lee en este orden:
1. [`docs/CONTRIBUIR.md`](docs/CONTRIBUIR.md): ramas, commits y pull requests.
2. [`docs/SEGURIDAD.md`](docs/SEGURIDAD.md): **nunca** subas credenciales ni secretos.
3. [`docs/LOCAL.md`](docs/LOCAL.md): cómo probar en tu máquina sin tocar AWS.
4. [`docs/DESPLIEGUE.md`](docs/DESPLIEGUE.md): cómo llega un cambio a producción.

## Reglas resumidas
- Nada de credenciales, tokens, webhooks ni IDs sensibles en el repo, en issues ni en pull requests.
- Los colaboradores **no necesitan** acceso a AWS: se prueba en local y el despliegue lo aprueba y ejecuta la persona dueña de la cuenta.
- Todo cambio entra por pull request, pequeño y revisado por otra persona.
- Todo recurso en la nube existe en Terraform; no se crea nada "a mano" sin dejarlo documentado.
- Nada que pueda costar dinero sin acuerdo previo.

## Costo y cómo borrarlo
Objetivo: 0 USD. Los recursos creados, su costo esperado y cómo borrarlos se registran en [`docs/RECURSOS.md`](docs/RECURSOS.md).

## Cómo reproducirlo desde cero
Se completa a medida que se construye cada etapa. Cada etapa terminada actualiza esta sección.
