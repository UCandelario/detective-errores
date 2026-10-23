# Montaje y pruebas en local

Todo cambio se prueba en tu máquina **antes** de abrir un pull request. No necesitas acceso a AWS para hacerlo.

## Principios
- Las pruebas **no llaman a AWS ni a Slack**. Usan dobles de prueba (funciones o clases falsas en memoria) definidos dentro del propio código de pruebas.
- Los datos de prueba grandes, semillas (seeds) y mocks personales viven **fuera del repo**, en tu carpeta local de pruebas, y nunca se commitean. Si necesitas datos de ejemplo, se documenta su **formato** aquí o en `docs/`, y cada quien genera los suyos.
- Nunca pruebes contra la cuenta AWS de producción desde tu máquina.

## Qué necesitas instalado
| Herramienta | Para qué | Estado |
|---|---|---|
| Git | Control de versiones | requerido |
| Lenguaje de las Lambdas | Correr código y pruebas | por decidir (ADR en la etapa 0) |
| Terraform | Validar infraestructura (`terraform validate`, `fmt`) | se instala cuando haya código en `infra/` |

Cualquier herramienta nueva se acuerda antes y se explica (para qué, costo, licencia).

## Flujo local
1. Clona el repo y crea tu rama (ver [`CONTRIBUIR.md`](CONTRIBUIR.md)).
2. Escribe o ajusta la prueba primero cuando sea posible.
3. Corre las pruebas de tu carpeta.
4. Para la página: ábrela con un servidor estático local y verifica que se vea bien y que maneje errores de la API (por ejemplo, la API caída).
5. Para Terraform: `terraform fmt -check` y `terraform validate` en `infra/`. El `plan` contra la cuenta real lo corre el dueño.
6. Revisa `git status` antes de commitear: nada de `.env`, claves ni estados de Terraform.

## Qué probar según el carril
- **A (revisor y avisador):** respuesta 200, error 500, tiempo de espera agotado, sitio que cae y se recupera, y que el aviso se manda solo en cambios de estado.
- **B (API y datos):** entradas inválidas, sitio inexistente, historial vacío (que sea "sin dato", no `0`), TTL y orden de resultados.
- **C (panel e infra):** que la página funcione con la API caída, que el bucket siga privado y que el `validate` pase.

## Lo que no se prueba en local
Permisos reales de IAM, el comportamiento de EventBridge y la entrega a Slack se validan **después del despliegue**, con la aprobación del dueño, y se anotan en el PR.
