# Etapa 3: datos con DynamoDB

**Carril B.** **Meta:** una tabla provisionada con el historial, y una API que lista el estado actual y el historial de cada sitio. Se prueba en local con un repositorio falso en memoria.

**Regla de costo:** tabla en modo **provisionado**, clase **Standard**, 1 a 5 RCU y 1 a 5 WCU. **No on-demand.** El límite gratuito (25 RCU y 25 WCU) es de toda la cuenta, no por tabla.

---

### T3.1 Diseñar el modelo de la tabla
- **Depende de:** T0.2 · **Tiempo:** 45 min · **Costo:** 0
- **Aprendes:** clave de partición y de orden, patrones de acceso.
- **Pasos:** escribe `docs/MODELO-DATOS.md` con:
  - Clave de partición `sitio` y de orden `momento` (hora ISO en UTC).
  - Item de **estado actual** por sitio (clave de orden `ACTUAL`).
  - Atributos: `estado`, `codigo` (puede faltar), `latencia_ms` (puede faltar), `ttl` (epoch).
  - Regla de datos: **`0` es un valor medido; "sin dato" es atributo ausente.** Un timeout no tiene código ni latencia: se guarda sin esos atributos, no con `0`.
- **Hecho cuando:** el documento responde cómo se lee "estado actual" y "últimos N resultados" y lo revisa otra persona.

### T3.2 Función `construir_item`
- **Depende de:** T3.1 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** en `functions/api/` (o un módulo compartido acordado), escribe una función pura que recibe un resultado de revisión y devuelve el item listo para guardar, con `ttl` a 30 días.
- **Prueba rápida:** `python scripts/probar.py api`.
- **Hecho cuando:** hay pruebas para resultado normal, **timeout sin código ni latencia** (no aparece `0`), latencia `0` real (sí se guarda) y cálculo correcto del `ttl`.

### T3.3 Repositorio falso en memoria
- **Depende de:** T3.2 · **Tiempo:** 45 min · **Costo:** 0
- **Aprendes:** inyección de dependencias para probar sin AWS.
- **Pasos:** define la interfaz `guardar(item)`, `estado_actual(sitio)` y `ultimos(sitio, n)`, con una versión en memoria para las pruebas. La versión real con `boto3` viene en T3.6.
- **Hecho cuando:** hay pruebas que guardan y leen con el repositorio falso, incluidos orden descendente y límite `n`.

### T3.4 Crear la tabla en la consola
- **Depende de:** T3.1, OK del dueño · **Tiempo:** 30 min · **Costo:** 0 si se respetan los límites (a verificar en la consola)
- **Aprendes:** modos de capacidad y TTL.
- **Pasos:** crear la tabla `detective-resultados` en `us-east-2`, **provisionada**, **Standard**, 1 RCU y 1 WCU, **sin Auto Scaling**, y activar TTL sobre el atributo `ttl`.
- **Prueba rápida:** en el resumen de la tabla se ve "Provisioned" y la capacidad esperada.
- **Hecho cuando:** la tabla existe con esa capacidad. Registrada en `docs/RECURSOS.md`.

### T3.5 Escribir y leer un item a mano
- **Depende de:** T3.4 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** `put-item` y `query` desde CloudShell.
- **Prueba rápida:** un item guardado se recupera con el mismo contenido.
- **Hecho cuando:** guardaste y leíste un item de práctica y luego lo borraste.

### T3.6 Repositorio real con boto3
- **Depende de:** T3.3, T3.4 · **Tiempo:** 1 h · **Costo:** 0
- **Pasos:** implementa la versión real de la interfaz con `boto3`. Las pruebas unitarias no la llaman; se verifica a mano en T3.8.
- **Hecho cuando:** el código está revisado y las pruebas existentes siguen pasando.

### T3.7 Rutas de la API: `GET /sitios` y `GET /sitios/{id}/historial`
- **Depende de:** T3.3, T2.2 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Pasos:** el handler enruta por ruta, valida el `id` (solo caracteres permitidos y longitud acotada) y el parámetro `limite` (entre 1 y 100, por defecto 20), y devuelve JSON. Con el repositorio falso.
- **Prueba rápida:** `python scripts/probar.py api`.
- **Hecho cuando:** hay pruebas para sitio inexistente (404), `id` inválido (400), `limite` fuera de rango (400), historial vacío (lista vacía, no error) y orden más reciente primero.

### T3.8 Permisos mínimos y despliegue de la API
- **Depende de:** T3.6, T3.7, OK del dueño · **Tiempo:** 1 h · **Costo:** 0
- **Aprendes:** políticas IAM con acciones y recursos concretos.
- **Pasos:** el rol de la API solo puede `Query` y `GetItem` sobre **esa tabla** (no escribe). Subir el nuevo zip.
- **Prueba rápida:** con un item de práctica, `curl` a `/sitios` devuelve el estado. Intentar leer otra tabla desde la función debe fallar.
- **Hecho cuando:** la API responde con datos reales y el rol no tiene permisos de más.

### T3.9 Tabla y permisos en Terraform
- **Depende de:** T3.4, T3.8, T1.7 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Hecho cuando:** `plan` coincide con lo creado a mano y el dueño lo aplica.
