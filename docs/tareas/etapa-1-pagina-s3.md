# Etapa 1: la página en S3

**Carril C.** **Meta:** una página estática servida desde un bucket **privado**, primero a mano y luego en Terraform.

Cada tarea cabe en una sesión corta. Lo que toca AWS necesita el OK del dueño antes de crearse y se anota en `docs/RECURSOS.md`.

---

### T1.1 Esqueleto de la página
- **Depende de:** T0.2 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** HTML y CSS básicos, estructura de una página estática.
- **Pasos:** revisa `web/index.html`, `web/styles.css` y `web/app.js`; agrega un título, el nombre del proyecto y un pie con el enlace al repo.
- **Prueba rápida:** `python -m http.server 8080 --directory web` y abre `http://localhost:8080`; se ve la página sin errores en la consola del navegador.
- **Hecho cuando:** la página carga en local y muestra el mensaje de "sin sitios configurados".

### T1.2 La página pinta datos de ejemplo
- **Depende de:** T1.1 · **Tiempo:** 45 min · **Costo:** 0
- **Aprendes:** JavaScript sencillo, render a partir de datos.
- **Pasos:** dentro de `web/app.js`, define una lista de ejemplo (2 o 3 sitios con estado `sano`, `degradado`, `caido`, latencia y hora) y pinta una tarjeta por sitio con un color por estado.
- **Prueba rápida:** recargar la página local; aparecen las tarjetas con colores distintos. Cambia un estado en el código y comprueba que cambia el color.
- **Hecho cuando:** los tres estados se distinguen visualmente. **Los datos de ejemplo no salen del archivo y se reemplazan en la etapa 5.**

### T1.3 Crear el bucket privado (consola)
- **Depende de:** OK del dueño · **Tiempo:** 30 min · **Costo:** 0 (a confirmar; ver nota)
- **Aprendes:** qué es un bucket, "Block Public Access", cifrado por defecto.
- **Pasos:** en la consola de S3, región `us-east-2`, nombre único (por ejemplo `detective-errores-web-<id-de-cuenta>`), **mantener activado "Block all public access"** y el cifrado por defecto. Anotar el nombre en `docs/RECURSOS.md`.
- **Prueba rápida:** el bucket aparece en la lista con "Bucket and objects not public".
- **Hecho cuando:** el bucket existe, sigue privado y está registrado en `docs/RECURSOS.md`.
- **Nota de costo:** S3 con una página de pocos KB debería costar 0; el uso gratuito vigente se confirma en la consola antes de crear.

### T1.4 Subir la página y comprobar que NO es pública
- **Depende de:** T1.3 · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** subir objetos y por qué un bucket privado devuelve "Access Denied".
- **Pasos:** sube `index.html`, `styles.css` y `app.js` desde la consola. Copia la URL del objeto y ábrela en el navegador.
- **Prueba rápida:** la URL directa del objeto responde **Access Denied**. Eso es lo correcto.
- **Hecho cuando:** los archivos están en el bucket y el acceso directo está bloqueado.

### T1.5 Registrar la decisión de hosting (ADR)
- **Depende de:** T1.4 · **Tiempo:** 15 min · **Costo:** 0
- **Pasos:** crea `docs/adr/0002-hosting-s3-cloudfront.md` con contexto, decisión (bucket privado + CloudFront con OAC), alternativas (bucket público, GitHub Pages) y consecuencias.
- **Hecho cuando:** el ADR está en un PR revisado.

### T1.6 Instalar Terraform en local (con OK)
- **Depende de:** OK del dueño · **Tiempo:** 20 min · **Costo:** 0
- **Aprendes:** qué hace Terraform y por qué el estado no va al repo.
- **Pasos:** instalar Terraform (herramienta nueva en la PC: pedir OK y explicar para qué). Verificar versión.
- **Prueba rápida:** `terraform --version`.
- **Hecho cuando:** el comando muestra una versión.

### T1.7 El bucket en Terraform
- **Depende de:** T1.3, T1.6 · **Tiempo:** 1 h · **Costo:** 0
- **Aprendes:** `provider`, `resource`, `plan` y por qué importar un recurso existente.
- **Pasos:** en `infra/`, define el proveedor de AWS (`us-east-2`) y el bucket con bloqueo de acceso público. **Importa** el bucket creado a mano (`terraform import`) en vez de crear otro, o destruye el manual y deja que Terraform lo cree.
- **Prueba rápida:** `terraform fmt -check`, `terraform validate` y `terraform plan` sin diferencias inesperadas.
- **Hecho cuando:** `terraform plan` dice "No changes". `apply` y `destroy` solo con OK del dueño.
- **Cuidado:** `*.tfstate` está en `.gitignore`. Nunca se commitea.

### T1.8 CloudFront con acceso restringido al bucket (consola)
- **Depende de:** T1.4 · **Tiempo:** 1 h · **Costo:** 0 esperado (a confirmar con el plan gratuito)
- **Aprendes:** distribuciones, Origin Access Control (OAC) y políticas de bucket.
- **Pasos:** crear una distribución con el bucket como origen y **OAC**; aplicar la política de bucket que sugiere la consola; objeto raíz `index.html`.
- **Prueba rápida:** `https://<id>.cloudfront.net` muestra la página y el acceso directo al bucket sigue dando Access Denied.
- **Hecho cuando:** la página carga por HTTPS desde CloudFront. Registrado en `docs/RECURSOS.md`.

### T1.9 CloudFront en Terraform
- **Depende de:** T1.7, T1.8 · **Tiempo:** 1 h 30 min · **Costo:** 0
- **Prueba rápida:** `terraform validate` y `plan` sin cambios inesperados.
- **Hecho cuando:** el plan coincide con lo creado a mano y el dueño lo aplica.

### T1.10 Script de publicación de la página
- **Depende de:** T1.8 · **Tiempo:** 30 min · **Costo:** 0
- **Aprendes:** `aws s3 sync` y la invalidación de caché de CloudFront.
- **Pasos:** documenta en `docs/DESPLIEGUE.md` el comando para subir `web/` y qué hacer para ver cambios (la caché puede tardar). **Cuidado:** las invalidaciones de CloudFront no entran en el uso gratuito; evitar abusar.
- **Hecho cuando:** un cambio de texto en la página se ve en la URL de CloudFront.
