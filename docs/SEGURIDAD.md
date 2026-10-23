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
