# Etapa 2: la primera Lambda

**Carril B (con apoyo de C).** **Meta:** una función "hola" que devuelve JSON, probada en local, desplegada y consumida desde la página.

---

### T2.1 La función pura `armar_saludo`
- **Depende de:** T0.2 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** separar la lógica pura del handler, primera prueba unitaria.
- **Pasos:** en `functions/api/app.py`, escribe `armar_saludo(nombre)` que devuelve un diccionario `{"mensaje": "Hola, <nombre>"}`; sin nombre usa "mundo". Escribe primero la prueba en `test_app.py`.
- **Prueba rápida:** `python scripts/probar.py api`.
- **Hecho cuando:** hay pruebas para con nombre, sin nombre y nombre vacío o solo espacios, y pasan.

### T2.2 El handler para Function URL
- **Depende de:** T2.1 · **Tiempo:** 45 min · **Costo:** 0
- **Aprendes:** la forma del evento de una Function URL y de la respuesta (`statusCode`, `headers`, `body`).
- **Pasos:** crea `handler(event, context)` que lee `queryStringParameters.nombre`, llama a `armar_saludo` y devuelve `{"statusCode": 200, "headers": {...}, "body": "<json>"}`. Una entrada inválida devuelve 400, no una excepción.
- **Prueba rápida:** pruebas con un evento de ejemplo escrito en el propio test (sin AWS).
- **Hecho cuando:** hay pruebas para 200, parámetro ausente y parámetro demasiado largo (límite de 50 caracteres).

### T2.3 Empaquetar la función
- **Depende de:** T2.2 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** qué es el `.zip` de una Lambda y qué lleva dentro.
- **Pasos:** añade `scripts/empaquetar.py <funcion>` que crea un `.zip` con solo `app.py` (los `.zip` ya están ignorados por git).
- **Prueba rápida:** el zip se crea y `python -m zipfile -l <zip>` lista solo los archivos esperados.
- **Hecho cuando:** el zip no contiene pruebas, `.git` ni archivos de configuración sensibles.

### T2.4 Crear la Lambda en la consola
- **Depende de:** T2.3, OK del dueño · **Tiempo:** 45 min · **Costo:** 0 (a confirmar)
- **Aprendes:** runtime, handler, memoria, tiempo de espera y el rol de ejecución.
- **Pasos:** crear la función `detective-api`, **runtime de Python soportado** (verificar la lista vigente en la consola; ver ADR 0001), memoria 128 MB, tiempo de espera 5 s, rol con solo permisos de logs. Subir el zip. Handler `app.handler`.
- **Prueba rápida:** botón "Test" con un evento de ejemplo; responde 200 con el saludo.
- **Hecho cuando:** la prueba en consola da 200. Registrado en `docs/RECURSOS.md`.

### T2.5 Function URL y CORS
- **Depende de:** T2.4 · **Tiempo:** 45 min · **Costo:** 0
- **Aprendes:** autenticación de la URL (pública o con IAM), CORS y qué expone cada opción.
- **Decisión del dueño:** una Function URL pública permite que **cualquiera** invoque la función. Para `/hola` el riesgo es bajo, pero se pone un tope de **concurrencia reservada** pequeño para limitar abuso y costo.
- **Pasos:** crear la URL, restringir el origen CORS a la URL de CloudFront y poner el tope de concurrencia.
- **Prueba rápida:** `curl "<url>?nombre=Ana"` devuelve el JSON; una petición con otro origen no tiene permiso CORS.
- **Hecho cuando:** el `curl` responde y el tope de concurrencia está puesto.

### T2.6 Ver los logs
- **Depende de:** T2.4 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** CloudWatch Logs, duración y memoria usadas por invocación.
- **Prueba rápida:** tras invocar la función, aparece un registro con `REPORT` en CloudWatch.
- **Hecho cuando:** sabes cuánto duró y cuánta memoria usó una invocación. **No imprimas datos sensibles en los logs.**

### T2.7 La página llama a la API
- **Depende de:** T2.5, T1.1 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** en `web/app.js`, llama con `fetch` a la Function URL y muestra el saludo. Maneja el error si la API no responde (mensaje claro, sin romper la página).
- **Prueba rápida:** con la API apagada o la URL mal puesta, la página muestra el aviso de error.
- **Hecho cuando:** funciona con la API arriba y falla con elegancia con la API caída.

### T2.8 La Lambda en Terraform
- **Depende de:** T2.5, T1.7 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Prueba rápida:** `terraform validate` y `plan` sin cambios inesperados.
- **Hecho cuando:** el recurso coincide con el creado a mano y el dueño lo aplica.
