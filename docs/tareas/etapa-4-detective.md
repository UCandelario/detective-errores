# Etapa 4: el detective (revisor, avisador y programación)

**Carril A.** **Meta:** revisar sitios cada 5 minutos y avisar a Slack **solo cuando el estado cambia**.

La mayoría de las tareas son **funciones puras** que se prueban en segundos en local. Lo que toca AWS o Slack va al final.

**Reglas de esta etapa:**
- Solo sitios propios o de práctica, con **lista fija** en `config/sitios.json`.
- El webhook de Slack es un **secreto**: nunca en el repo, en un issue ni en una captura.
- Slack de **prueba**, propio.

---

### T4.1 Validar la configuración de sitios
- **Depende de:** T0.2 · **Tiempo:** 1 h · **Costo:** 0
- **Aprendes:** validar entradas y por qué una lista fija es más segura.
- **Pasos:** en `functions/revisor/app.py`, escribe `validar_sitios(config)` que acepte solo URLs `https`, rechace `localhost`, IPs privadas, esquemas distintos (`file://`, `http://`) y duplicados, y devuelva la lista limpia. Llena `config/sitios.json` con **tus propios** sitios (la página del proyecto cuando exista, por ejemplo).
- **Prueba rápida:** `python scripts/probar.py revisor`.
- **Hecho cuando:** hay pruebas para `https` válida, `http` rechazada, `localhost`, `127.0.0.1`, `10.x.x.x`, `169.254.169.254` (metadatos de AWS), URL vacía y duplicados.

### T4.2 Clasificar una respuesta: `evaluar_respuesta`
- **Depende de:** T0.2 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** función pura `evaluar_respuesta(codigo, latencia_ms, umbral_ms=2000)` que devuelve `"sano"`, `"degradado"` (2xx lento) o `"caido"` (5xx, 4xx inesperado o sin respuesta).
- **Hecho cuando:** hay pruebas para 200 rápido, 200 lento, 301, 404, 500, 503 y **sin respuesta (`None`)**, y `latencia 0` se trata como un valor medido válido.

### T4.3 Revisar un sitio con un cliente HTTP inyectado
- **Depende de:** T4.2 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Aprendes:** timeouts, no seguir redirecciones sin límite, inyección de dependencias.
- **Pasos:** `revisar_sitio(url, cliente)` mide el tiempo, aplica un **timeout de 5 s**, captura cualquier excepción y devuelve un resultado con `estado`, `codigo` y `latencia_ms` (ausentes si no hubo respuesta). El cliente real usa `urllib` de la biblioteca estándar; las pruebas usan uno falso.
- **Hecho cuando:** hay pruebas con cliente falso para éxito, error 500, timeout y excepción de conexión, sin salir a internet.

### T4.4 Detectar un cambio de estado
- **Depende de:** T4.2 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** función pura `detectar_cambio(estado_anterior, estado_nuevo)` que devuelve el tipo de transición o `None` si no cambió.
- **Hecho cuando:** hay pruebas para sano→caido, caido→sano, sano→sano (sin cambio) y **primera revisión sin estado anterior** (decisión documentada: no avisa, o avisa solo si ya está caído; el equipo decide y lo escribe en la prueba).

### T4.5 Armar el mensaje de Slack
- **Depende de:** T4.4 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** en `functions/avisador/app.py`, función pura `armar_mensaje(sitio, anterior, nuevo, momento)` con un texto claro y un emoji o color por estado.
- **Prueba rápida:** `python scripts/probar.py avisador`.
- **Hecho cuando:** hay pruebas para caída y recuperación, y el mensaje **no incluye datos sensibles**.

### T4.6 Orquestar la revisión completa en local
- **Depende de:** T4.1, T4.3, T4.4, T3.3 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Pasos:** `revisar_todos(sitios, cliente, repositorio, avisar)` recorre la lista, guarda cada resultado y llama a `avisar` solo en cambios. Un sitio que falla **no** detiene al resto.
- **Hecho cuando:** una prueba con 3 sitios falsos (uno cae a mitad) confirma que se guardan 3 resultados y se avisa una sola vez.

### T4.7 Guardar el webhook en SSM Parameter Store
- **Depende de:** OK del dueño · **Tiempo:** 30 min · **Costo:** 0 (parámetro estándar; a confirmar)
- **Aprendes:** secretos fuera del código.
- **Pasos:** crear un parámetro `SecureString` `/detective/slack-webhook` desde la consola o CloudShell. **Quien lo crea lo pega en su propia máquina; nunca en el chat ni en el repo.**
- **Prueba rápida:** `aws ssm get-parameter --name /detective/slack-webhook` confirma que existe (sin mostrar el valor en pantallas compartidas).
- **Hecho cuando:** el parámetro existe y el valor no aparece en ningún archivo del repo.

### T4.8 Enviar un mensaje de prueba a Slack
- **Depende de:** T4.5, T4.7 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** crea un canal en tu Slack **de prueba**, un webhook entrante y envía un mensaje de prueba. La función lee el webhook de SSM al ejecutarse.
- **Hecho cuando:** el mensaje llega al canal y el webhook no está en el código.

### T4.9 Desplegar el revisor y el avisador
- **Depende de:** T4.6, T4.8, T3.8, OK del dueño · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Pasos:** crear las dos Lambdas con roles de **permisos mínimos** (el revisor escribe en la tabla y lee solo ese parámetro; el avisador, solo ese parámetro). Probar con un evento manual.
- **Hecho cuando:** una invocación manual guarda un resultado real y registra el recurso en `docs/RECURSOS.md`.

### T4.10 Programar con EventBridge Scheduler
- **Depende de:** T4.9 · **Tiempo:** 45 min · **Costo:** 0 esperado (a confirmar)
- **Pasos:** crear la programación cada **5 minutos**, **creada desactivada**. El dueño la activa tras revisar la frecuencia. No bajar de 5 minutos.
- **Prueba rápida:** activar, esperar 15 minutos y confirmar 3 invocaciones en CloudWatch. Luego **desactivar** si se va a dejar de probar.
- **Hecho cuando:** se ven invocaciones periódicas sin errores.

### T4.11 Prueba de aceptación: provocar una caída
- **Depende de:** T4.10 · **Tiempo:** 1 h · **Costo:** 0
- **Pasos:** apunta a un sitio de práctica **propio** que puedas hacer caer y recuperar a voluntad (por ejemplo una Lambda que responde 500 con un interruptor).
- **Hecho cuando:** al caer llega **un** aviso, mientras sigue caído no llegan más, y al recuperarse llega **un** segundo aviso.

### T4.12 Todo en Terraform
- **Depende de:** T4.9, T4.10 · **Tiempo:** 2 h · **Costo:** 0
- **Hecho cuando:** `plan` coincide con lo creado a mano y el dueño lo aplica. El valor del webhook **no** aparece en el código ni en el estado de Terraform (se referencia el parámetro, no su valor).
