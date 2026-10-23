# Etapa 5: el panel completo

**Carril C.** **Meta:** la página muestra el estado real de los sitios y su historial, y se mantiene sana aunque la API falle.

Las pruebas de la web son **manuales** (lista de verificación) y se anotan en el PR. Se abren en local con `python -m http.server 8080 --directory web`.

---

### T5.1 Leer el estado desde la API
- **Depende de:** T3.7, T1.2 · **Tiempo:** 1 h · **Costo:** 0
- **Pasos:** reemplaza los datos de ejemplo por una llamada a `GET /sitios`. La URL de la API vive en un archivo de configuración de la web (no es un secreto, pero sí cambia por entorno).
- **Prueba rápida:** abrir en local contra la API desplegada; se ven los sitios reales.
- **Hecho cuando:** las tarjetas muestran datos reales y no queda ningún dato de ejemplo en el código final.

### T5.2 Sin dato no es cero
- **Depende de:** T5.1 · **Tiempo:** 30 min · **Costo:** 0
- **Pasos:** si un sitio no tiene latencia (timeout), la tarjeta muestra "sin dato" y no "0 ms".
- **Hecho cuando:** se comprueba con un sitio caído: aparece "sin dato", y una latencia real de 0 ms (si ocurriera) sí se muestra como 0.

### T5.3 Historial de un sitio
- **Depende de:** T5.1 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Pasos:** al elegir un sitio, pide `GET /sitios/{id}/historial?limite=20` y lo muestra como lista con hora, estado y latencia, el más reciente primero.
- **Hecho cuando:** el historial se ve ordenado, y un sitio sin historial muestra "Todavía no hay revisiones".

### T5.4 Manejo de errores y API caída
- **Depende de:** T5.1 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** si la API no responde o devuelve error, muestra un mensaje claro y conserva los datos anteriores.
- **Prueba rápida:** con una URL de API incorrecta, la página no se rompe y avisa del error.
- **Hecho cuando:** la página sobrevive a una API apagada.

### T5.5 Actualización automática moderada
- **Depende de:** T5.1 · **Tiempo:** 30 min · **Costo:** 0
- **Pasos:** vuelve a pedir el estado cada **60 segundos** y solo mientras la pestaña está visible. No menos de 60 s: cada petición cuenta en el uso de Lambda.
- **Hecho cuando:** el estado se refresca solo y se detiene en una pestaña en segundo plano.

### T5.6 Accesibilidad básica
- **Depende de:** T5.1 · **Tiempo:** 45 min · **Costo:** 0
- **Pasos:** el estado no depende solo del color (texto o ícono), contraste suficiente, y navegación con teclado.
- **Hecho cuando:** se entiende la página con los colores desactivados.

### T5.7 Publicar la versión final
- **Depende de:** T5.1 a T5.6, T1.10 · **Tiempo:** 30 min · **Costo:** 0
- **Hecho cuando:** el cambio llega a la URL de CloudFront con el procedimiento de `docs/DESPLIEGUE.md` y se registra en el PR qué se verificó.
