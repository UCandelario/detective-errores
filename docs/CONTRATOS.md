# Contratos compartidos

Qué recibe y qué devuelve cada pieza, con **resultados esperados exactos**, para que cada carril escriba sus pruebas **sin esperar al otro** y sin tocar AWS. Si una prueba tuya contradice esta página, cambia la prueba o abre un PR para discutir el contrato; no cambies el comportamiento en silencio.

> Las decisiones marcadas con **(decisión)** son del equipo y se pueden cambiar con un PR. Mientras no cambien, son la regla.

## 1. Estados de un sitio
Hay exactamente tres, escritos así (minúsculas y sin acento): `"sano"`, `"degradado"`, `"caido"`.

## 2. Resultado de una revisión
Es lo que produce el revisor y lo que guarda la tabla:

| Campo | Tipo | Cuándo está |
|---|---|---|
| `sitio` | texto | siempre |
| `estado` | uno de los tres estados | siempre |
| `momento` | texto, hora UTC en formato ISO, por ejemplo `2026-10-24T15:00:00Z` | siempre |
| `codigo` | entero (200, 404...) | **solo si el sitio respondió** |
| `latencia_ms` | número (0 o más) | **solo si el sitio respondió** |

**Regla de datos:** `0` es un valor medido (un sitio que responde en 0 ms es un dato válido); "no hubo respuesta" es **campo ausente**, no `0` ni `None` guardado como `0`. Un timeout no tiene ni `codigo` ni `latencia_ms`.

## 3. `evaluar_respuesta(codigo, latencia_ms, umbral_ms=2000)` (carril A, tarea T4.2)
Vive en `functions/revisor/app.py`. Devuelve el estado de un sitio según lo que respondió.

Reglas, en este orden:
1. `codigo` es `None` (no hubo respuesta) → `"caido"`.
2. `codigo` debe ser un entero entre 100 y 599 y `latencia_ms` un número de 0 o más; si no, lanza `ValueError`.
3. Código 200 a 299: si `latencia_ms` es **mayor** que `umbral_ms` → `"degradado"`; si no → `"sano"` (justo en el umbral es `"sano"`).
4. Código 300 a 399 → `"degradado"` **(decisión)**: el sitio responde, pero redirige o no sirve lo esperado.
5. Cualquier otro código (100 a 199, 400 a 599) → `"caido"`.

| Entrada `(codigo, latencia_ms[, umbral_ms])` | Resultado |
|---|---|
| `(200, 150)` | `"sano"` |
| `(200, 0)` | `"sano"` (0 ms es un dato válido) |
| `(200, 2000)` | `"sano"` (igual al umbral) |
| `(200, 2001)` | `"degradado"` |
| `(204, 100)` | `"sano"` |
| `(299, 100)` | `"sano"` |
| `(301, 100)` | `"degradado"` |
| `(399, 100)` | `"degradado"` |
| `(404, 100)` | `"caido"` |
| `(500, 100)` | `"caido"` |
| `(503, 5000)` | `"caido"` |
| `(100, 10)` | `"caido"` |
| `(None, None)` | `"caido"` |
| `(200, 3000, 5000)` | `"sano"` (umbral personalizado) |

Deben lanzar `ValueError`: `(200, None)`, `(200, -1)`, `(99, 10)`, `(600, 10)`, `("200", 10)`, `(True, 10)`.

## 4. `detectar_cambio(estado_anterior, estado_nuevo)` (carril A, tarea T4.4)
Vive en `functions/revisor/app.py`. Devuelve el **tipo de cambio** como texto, o `None` si no hay nada que avisar.

Reglas:
1. Si `estado_nuevo` no es uno de los tres estados, o `estado_anterior` no es uno de los tres ni `None` → `ValueError`.
2. Primera revisión (`estado_anterior` es `None`): devuelve `"cae"` solo si el estado nuevo es `"caido"`; en otro caso `None` **(decisión)**: no se avisa de algo que nace sano, pero sí de algo que nace caído.
3. Mismo estado → `None`.
4. Si el nuevo es `"caido"` → `"cae"`.
5. Si el anterior era `"caido"` y el nuevo no → `"se_recupera"`.
6. `"sano"` → `"degradado"` es `"se_degrada"`; `"degradado"` → `"sano"` es `"mejora"`.

| `(anterior, nuevo)` | Resultado |
|---|---|
| `("sano", "sano")` | `None` |
| `("sano", "caido")` | `"cae"` |
| `("caido", "sano")` | `"se_recupera"` |
| `("caido", "degradado")` | `"se_recupera"` |
| `("sano", "degradado")` | `"se_degrada"` |
| `("degradado", "sano")` | `"mejora"` |
| `("degradado", "caido")` | `"cae"` |
| `("caido", "caido")` | `None` |
| `("degradado", "degradado")` | `None` |
| `(None, "sano")` | `None` |
| `(None, "degradado")` | `None` |
| `(None, "caido")` | `"cae"` |

Deben lanzar `ValueError`: `("roto", "sano")`, `("sano", None)`, `("sano", "otro")`.

Más adelante (tarea T4.5), el avisador decide qué tipos de cambio mandan mensaje a Slack; esta función solo clasifica.

## 5. `armar_saludo(nombre)` y `handler(event, context)` (carril B, tareas T2.1 y T2.2)
Viven en `functions/api/app.py`.

### `armar_saludo(nombre)`
Devuelve `{"mensaje": "Hola, <nombre>"}`. Se le quitan los espacios de los extremos; si queda vacío, o es `None`, el nombre es `"mundo"`.

| Entrada | Resultado |
|---|---|
| `None` | `{"mensaje": "Hola, mundo"}` |
| `""` | `{"mensaje": "Hola, mundo"}` |
| `"   "` | `{"mensaje": "Hola, mundo"}` |
| `"Ana"` | `{"mensaje": "Hola, Ana"}` |
| `"  Ana  "` | `{"mensaje": "Hola, Ana"}` |
| `"José"` | `{"mensaje": "Hola, José"}` |

`armar_saludo` **no** comprueba la longitud; eso lo hace el handler.

### Evento que recibe el handler
Una Lambda con Function URL recibe un evento con formato de carga 2.0 (según la [documentación de AWS](https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html); esa página es antigua, así que se confirma al desplegar). Para las pruebas usa este ejemplo, escrito dentro del propio test:

```python
EVENTO_ANA = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/",
    "rawQueryString": "nombre=Ana",
    "queryStringParameters": {"nombre": "Ana"},
    "requestContext": {"http": {"method": "GET", "path": "/"}},
    "isBase64Encoded": False,
}
```
Cuando **no hay** parámetros en la URL, `queryStringParameters` puede venir como `None` o faltar del todo: el handler debe tolerar las dos cosas y que el evento sea `{}` o `None`.

### Respuesta del handler
Un diccionario con `statusCode`, `headers` y `body` (texto JSON; las pruebas lo leen con `json.loads`). Siempre lleva el encabezado `"Content-Type": "application/json; charset=utf-8"`.

| Evento | `statusCode` | `body` (ya convertido con `json.loads`) |
|---|---|---|
| `nombre=Ana` | 200 | `{"mensaje": "Hola, Ana"}` |
| sin `queryStringParameters` (`None`) | 200 | `{"mensaje": "Hola, mundo"}` |
| `queryStringParameters` igual a `{}` | 200 | `{"mensaje": "Hola, mundo"}` |
| `nombre=` (vacío) | 200 | `{"mensaje": "Hola, mundo"}` |
| evento `{}` o `None` | 200 | `{"mensaje": "Hola, mundo"}` |
| `nombre` de 50 letras | 200 | saluda con ese nombre |
| `nombre` de 51 letras | 400 | `{"error": "El nombre no puede pasar de 50 caracteres."}` |
| `nombre` con 2 espacios a cada lado y 50 letras | 200 | los espacios se quitan **antes** de contar la longitud |

El mensaje de error nunca incluye el detalle interno de una excepción.

## 6. Cómo usar este documento al probar
- Cada fila de una tabla es **una prueba**. Conviene un `subTest` por fila o un método por grupo.
- Los datos de prueba van **dentro del archivo de pruebas**, no en archivos aparte.
- Una prueba de `ValueError` usa `with self.assertRaises(ValueError):`.
- Si una fila te parece mal, no la ignores: abre un comentario en tu PR o un PR contra este archivo.
