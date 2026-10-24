# Seguridad

## Regla de oro
**Nunca** pongas credenciales en el repo, en el chat, en un issue, en un PR ni en una captura de pantalla. Eso incluye: claves de acceso de AWS, tokens de GitHub, URLs de webhook de Slack, contraseñas, archivos `.pem`/`.key` y contenido de `.env`.

## Qué cuenta como secreto
| Es secreto | No es secreto |
|---|---|
| Claves de acceso de AWS (`AKIA...` y su clave secreta) | ID de cuenta, nombre de región |
| URL del webhook de Slack | Nombres de recursos y de buckets |
| Tokens de GitHub, contraseñas | Código y documentación del proyecto |
| Archivos `.env`, `*.pem`, `*.key` | Diagramas y ADR |

En caso de duda, trátalo como secreto y pregunta.

## Cómo se manejan los secretos
- **En local:** variables de entorno o archivos ignorados por git (`.env`, ya cubiertos en `.gitignore`). Nunca se commitean.
- **En AWS:** el webhook de Slack se guarda en SSM Parameter Store y la Lambda lo lee al ejecutarse.
- **En el pipeline:** autenticación con OIDC, sin claves de larga duración guardadas en GitHub.
- Los colaboradores **no tienen acceso a la cuenta AWS**. Si alguien necesita ver algo de AWS, se pide al dueño y se le da el acceso mínimo posible, con MFA.

## Mínimo privilegio
Cada Lambda y cada rol tiene solo los permisos que necesita, sobre los recursos concretos. Nada de `*` en acciones o recursos si se puede evitar.

## Qué hacer si se filtra algo
1. **Avisa de inmediato** al dueño de la cuenta. No lo borres a escondidas.
2. **Revoca o rota** el secreto (cambiar la clave, regenerar el webhook). Borrar el commit no basta: el historial lo conserva.
3. El dueño revisa si hubo uso indebido y limpia el historial si hace falta.
4. Se anota qué pasó y cómo evitarlo.

## Revisiones
- Antes de volver público el repo se revisa el historial completo en busca de secretos.
- Se revisa que `.gitignore` cubra secretos, estados de Terraform y dependencias.
- Las acciones de terceros en el pipeline se acuerdan antes de usarlas.

## Sitios vigilados
Solo sitios propios o de práctica, con lista fija en configuración. No se acepta una URL arbitraria de un usuario.

## Repositorio público: qué lo protege
El repo es **público**: cualquiera puede leer el código y el historial, así que **todo lo que se suba es público para siempre** (borrar un commit no lo retira de las copias ni de los PR).

| Capa | Qué hace | Dónde |
|---|---|---|
| Ruleset "Proteger main" | Exige PR con 1 aprobación, checks en verde y squash; nadie queda exento | Settings → Rules |
| Escaneo de secretos de GitHub | Detecta claves conocidas en el repo | Settings → Code security |
| Protección de push de GitHub | **Rechaza el push** si contiene un secreto reconocido | Settings → Code security |
| `Secretos en el cambio` | Nuestro escáner (`scripts/revisar_secretos.py`) sobre las líneas del PR | Workflow `secretos.yml` |
| `ESLint` y `Sintaxis de Python` | Calidad del código, con reglas que prohíben `eval` y similares | Workflow `calidad.yml` |
| `CodeQL` | Análisis de seguridad de Python y JavaScript | Workflow `codeql.yml` |
| `guardia-main` | Avisa si un commit llega a `main` sin PR | Workflow `guardia-main.yml` |
| Reporte privado de vulnerabilidades | Canal para avisar de un problema sin hacerlo público | Pestaña Security (ver `SECURITY.md`) |

Ninguna de estas capas es perfecta: ayudan, pero no reemplazan la regla de oro de arriba. Si un push es rechazado por la protección de secretos, **no lo fuerces ni lo saltes**: quita el secreto del cambio y avisa al dueño.

## Qué NUNCA debe ir a un repo público
Credenciales, webhooks, tokens, claves, el contenido de `.env` o de `*.tfstate`, URLs con firmas o tokens, datos personales de otras personas (correos, nombres) y datos de prueba reales. El ID de cuenta de AWS no es un secreto, pero tampoco hace falta publicarlo.

Las **URLs públicas de la página y de la API sí son públicas** (la página las necesita). Por eso lo que protege el costo y el abuso son los límites en AWS (concurrencia reservada, validación de entradas, lista fija de sitios y alertas de presupuesto), no esconder la URL.

## Workflows y pull requests de personas externas
- Solo quienes tienen permiso de escritura pueden subir ramas del repo. Cualquier otra persona solo puede proponer cambios desde un fork.
- Los workflows usan `pull_request` y **nunca** `pull_request_target`, que daría a código externo acceso a permisos y secretos.
- Los workflows no usan secretos y tienen permisos mínimos (`contents: read`); solo CodeQL puede escribir resultados de seguridad.
- Todas las acciones son oficiales de GitHub y van fijadas por hash de commit.
- Antes de añadir un workflow o una acción nueva, se revisa quién puede dispararlo y con qué permisos.
