## Tarea y carril
<!-- ID de la tarea (por ejemplo T4.2) y carril (A, B o C). Sin tarea no hay PR. -->

## Qué cambia y por qué
<!-- Una o dos frases. Enlaza la tarea de docs/TAREAS.md -->

## Cómo lo probé
<!-- Comandos y resultado real en local. Lo que no pude probar, dilo: "no verificado". -->

## Uso de asistentes de IA
- [ ] No usé un asistente de IA
- [ ] Usé un asistente de IA y **leí cada línea** del cambio
- [ ] Puedo explicar cada línea de este cambio con mis palabras

## Checklist
- [ ] Probé en local y las pruebas pasan
- [ ] El cambio toca **solo** los archivos de mi tarea y de mi carril
- [ ] Corrí `python scripts/auditar_codigo.py functions/<mi-carpeta>` y no queda nada pendiente
- [ ] No hay credenciales, tokens, webhooks ni datos de prueba en el cambio
- [ ] No añadí dependencias nuevas
- [ ] Actualicé la documentación y marqué la tarea en `docs/TAREAS.md`
- [ ] Si toca AWS: anoté el costo esperado y actualicé `docs/RECURSOS.md`
- [ ] Si toca infraestructura: incluí el `terraform plan` (sin datos sensibles)
- [ ] El PR es pequeño (unas 300 líneas como máximo) y hace una sola cosa
