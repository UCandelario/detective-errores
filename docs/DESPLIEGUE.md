# Despliegue

## Quién y cuándo
- **Solo el dueño de la cuenta AWS** ejecuta `terraform apply` y `terraform destroy`, y siempre después de revisar el `plan`.
- Los colaboradores proponen cambios por pull request; no necesitan credenciales de AWS.
- Ningún cambio llega a producción sin: pruebas en local, PR revisado y aprobación explícita del dueño.

## Antes de desplegar (lista del dueño)
1. Verificar la cuenta y la región correctas:
   ```bash
   aws sts get-caller-identity --profile personal
   ```
   Debe ser la cuenta personal del proyecto, en `us-east-2`. Si no lo es, **parar**.
2. Correr `terraform plan` y leerlo completo: qué se crea, cambia o **destruye**.
3. Revisar el costo esperado de lo nuevo. Nada que pueda costar dinero sin acuerdo previo.
4. Confirmar que el PR está aprobado y fusionado en `main`.
5. Solo entonces `terraform apply`.

## Después de desplegar
- Verificar que el recurso funciona (la página carga, la Lambda responde, el aviso llega).
- Actualizar `docs/RECURSOS.md` con el recurso, su costo y cómo borrarlo.
- Anotar en el PR qué se verificó y qué quedó sin verificar.

## Reglas
- Infraestructura como código para todo lo desplegable. Lo hecho a mano en la consola se anota y luego se pasa a Terraform.
- Cada despliegue se hace en pasos pequeños, una cosa nueva por vez.
- Si algo sale mal, no se improvisa: se detiene, se anota y se revierte con un PR o con `destroy` del recurso afectado, con aprobación del dueño.

## Pipeline de despliegue (etapa 6, opcional)
**El camino por defecto es el despliegue manual del dueño**, descrito arriba; AWS no necesita GitHub para funcionar. El despliegue automático (tareas T6.4 y T6.5) es opcional.

Si se decide hacerlo: GitHub Actions con OIDC y un rol de permisos mínimos. El despliegue automático exige aprobación manual del dueño. Las acciones de terceros se acuerdan antes de usarlas. Los minutos gratuitos de Actions para repos privados están limitados (2.000 al mes en el plan gratuito); se vigilan.
