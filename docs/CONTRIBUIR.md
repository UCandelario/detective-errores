# Cómo contribuir

## Flujo de trabajo
1. `main` siempre debe estar sano y desplegable. **No se trabaja directamente en `main`.**
2. Crea una rama por tarea: `a/revisor-http`, `b/tabla-dynamodb`, `c/bucket-s3` (letra del carril + tema corto).
3. Haz **commits pequeños**, cada uno con un solo propósito y un mensaje claro en español ("Agrega validación de URL en el revisor").
4. Súbela y abre un **pull request** hacia `main` con la plantilla que aparece.
5. **Otra persona** lo revisa. El PR no se fusiona sin al menos una aprobación.
6. Se fusiona con "Squash and merge" para mantener un historial limpio.

> **`main` está protegida por GitHub** (ruleset "Proteger main", el repo es público): no se puede empujar directo, hay que abrir un pull request con **1 aprobación** de otra persona (quien subió el último commit no cuenta), pasar los checks `Pruebas` y `Secretos en el cambio`, resolver los comentarios abiertos y fusionar con *squash*. Nadie queda exento, tampoco el dueño del repo. Solo las personas con permiso de escritura (los colaboradores) pueden subir ramas; cualquier otra persona solo puede proponer cambios desde un fork.
>
> Red de seguridad extra: el workflow `guardia-main` falla en rojo (y GitHub avisa por correo) si un commit llega a `main` sin pull request.

## Reglas de código
- Nombres explícitos: `revisarSitio`, no `chk`. Funciones pequeñas con una sola responsabilidad.
- Cada función Lambda tiene pruebas unitarias que no llaman a AWS (ver [`LOCAL.md`](LOCAL.md)).
- Valida las entradas. Nunca confíes en datos que vengan de fuera.
- Un valor `0` es un dato medido; "sin dato" es otra cosa y no se guarda como `0`. Usa `null` o ausencia, y documenta cuál.
- Sin dependencias nuevas sin hablarlo antes: cada una se explica (para qué, alternativa más simple, costo, licencia).
- Los comentarios explican el *por qué*, no repiten lo que hace el código.

## Reglas de seguridad (resumen)
Lee [`SEGURIDAD.md`](SEGURIDAD.md). Lo esencial: **cero credenciales, tokens, webhooks o IDs sensibles** en commits, issues, PR o capturas.

## Infraestructura
- Todo recurso se crea con Terraform en `infra/`. Lo que se pruebe a mano en la consola se anota en `docs/RECURSOS.md` y luego se pasa a código.
- Un PR de infraestructura debe incluir el resultado de `terraform plan` (sin datos sensibles) en la descripción.
- **Nadie ejecuta `apply` ni `destroy` salvo el dueño de la cuenta.** Ver [`DESPLIEGUE.md`](DESPLIEGUE.md).

## Antes de abrir un PR
- [ ] Probé en local y las pruebas pasan.
- [ ] No hay credenciales ni datos de prueba en el cambio.
- [ ] Actualicé la documentación y marqué la tarea en `TAREAS.md`.
- [ ] Si toca AWS, anoté el costo esperado.
- [ ] El PR es pequeño y hace una sola cosa.

## Decisiones
Si el cambio toma una decisión de arquitectura (lenguaje, servicio, estructura de datos), añade un ADR corto en `docs/adr/` con: contexto, decisión, alternativas y consecuencias.
