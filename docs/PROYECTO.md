# Qué es el proyecto

## Objetivo
Aprender, construyendo algo real entre tres personas, a crear y operar servicios de AWS serverless y a desplegar cambios de forma segura y reproducible.

## Qué se construye
Un monitor de sitios web, el **Detective de errores**:

| Pieza | Servicio | Qué se practica |
|---|---|---|
| Reloj | EventBridge Scheduler | Tareas programadas |
| Revisor | Lambda | Peticiones HTTP, tiempos de espera, reintentos |
| Memoria | DynamoDB (modo provisionado) | Claves, consultas por sitio y fecha, TTL |
| Avisador | Lambda + webhook de Slack | Webhooks y manejo de secretos |
| API | Lambda (Function URL o API Gateway) | CORS, validación de entradas |
| Panel | S3 (y CloudFront después) | Hosting estático, permisos |
| Infra | Terraform | Infraestructura como código |
| Pipeline | GitHub Actions con OIDC | CI/CD sin claves guardadas |

## Reglas de diseño
- **Lista fija de sitios.** Solo se vigilan sitios propios o de práctica, definidos en configuración. Nunca una URL que escriba un usuario: sería una vía de abuso (peticiones a terceros o a direcciones internas).
- **Avisar solo en cambios de estado**, no en cada revisión.
- **Frecuencia moderada** (cada 5 minutos como máximo). Bajar de ahí multiplica las ejecuciones y el costo.
- **DynamoDB provisionado**, tabla Standard, capacidad mínima (1 a 5 RCU/WCU) y TTL de unos 30 días. No usar on-demand.
- **Bucket privado.** La página se sirve por CloudFront con acceso restringido, no con el bucket abierto.
- **Secretos fuera del repo.** El webhook de Slack vive en SSM Parameter Store.
- **Slack de prueba**, propio, nunca el de una empresa.

## Fuera de alcance
- Cuentas de usuario, pagos o datos personales.
- Monitoreo de sitios de terceros.
- Servicios que no tengan uso gratuito claro (por ejemplo RDS, Aurora, NAT Gateway).

## Costo y vencimiento
- Meta: **0 USD**. Los servicios elegidos tienen uso gratuito (a confirmar en la consola antes de crear cada recurso).
- La cuenta AWS está en plan gratuito con créditos que **vencen el 2027-04-23**; después se pierde el acceso a los servicios. Por eso todo debe quedar en Terraform y en este repo, y la página estática debe poder moverse a otro hosting.

## Éxito
- La página está en línea y muestra el estado real de los sitios vigilados.
- Cae un sitio de prueba y llega el aviso a Slack; se recupera y llega el segundo aviso.
- Todo se despliega desde el repo y se puede reproducir desde cero con el README.
- Costo real: 0 USD.
