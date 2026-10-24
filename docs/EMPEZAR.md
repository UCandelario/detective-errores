# Empezar a trabajar (guía para colaboradores)

Esta guía te lleva de cero a tu primera prueba corriendo, **sin acceso a AWS y sin instalar dependencias**. Tiempo: unos 15 minutos.

## 1. Qué necesitas
| Herramienta | Versión | Cómo comprobarla |
|---|---|---|
| Git | cualquiera reciente | `git --version` |
| Python | **3.12 o superior** | `python --version` (en Mac o Linux, `python3 --version`) |
| Un navegador | cualquiera | — |
| Cuenta de GitHub | con la invitación al repo aceptada | — |

No necesitas Docker, Node, Terraform ni cuenta de AWS. Si una tarea pide algo más, la propia tarea lo dice y se acuerda antes.

## 2. Aceptar la invitación y clonar
1. Acepta la invitación que llegó a tu correo (o desde github.com → campana de notificaciones).
2. Clona el repo (es **privado**, así que GitHub te pedirá iniciar sesión en el navegador la primera vez):
   ```bash
   git clone https://github.com/UCandelario/detective-errores.git
   cd detective-errores
   ```
3. **Nunca pegues tokens ni contraseñas** en la terminal, en el chat ni en archivos del repo. Si git te pide autenticarte, usa la ventana del navegador.

## 3. Configurar tu identidad en git
El correo que pongas **queda en cada commit** (y es visible si el repo se hace público algún día). Elige uno que quieras mostrar.
```bash
git config user.name "Tu Nombre"
git config user.email "tu-correo@ejemplo.com"
```
Sin `--global`, esto aplica solo a este repo.

## 4. Comprobar que todo funciona
```bash
python scripts/probar.py
```
Debe terminar con:
```text
--- Resumen ---
Probadas: 3. Fallidas: 0.
```
Para ver la página:
```bash
python -m http.server 8080 --directory web
```
Abre `http://localhost:8080`. Debe decir "Todavía no hay sitios configurados." Detén el servidor con `Ctrl+C`.

## 5. Tu ciclo de trabajo (de una tarea pequeña)
1. Elige una tarea de [`docs/tareas/`](tareas/) de tu carril (ver [`TAREAS.md`](TAREAS.md)) que **no tenga dueño**. Avisa al equipo cuál tomas.
2. Crea tu rama desde `main` actualizado:
   ```bash
   git switch main
   git pull
   git switch -c a/t4-2-evaluar-respuesta     # letra de tu carril + tarea + tema
   ```
3. **Escribe primero la prueba** (debe fallar), luego el código mínimo para que pase.
4. Corre solo tu función mientras trabajas, y todas antes de subir:
   ```bash
   python scripts/probar.py revisor     # solo una función
   python scripts/probar.py             # todas
   ```
5. Revisa qué vas a commitear. **Nada de `.env`, claves ni datos de prueba:**
   ```bash
   git status
   git diff
   ```
6. Commits pequeños, con rutas explícitas (no uses `git add .`):
   ```bash
   git add functions/revisor/app.py functions/revisor/test_app.py
   git commit -m "Agrega evaluar_respuesta con pruebas"
   ```
7. Sube tu rama y abre un pull request hacia `main`:
   ```bash
   git push -u origin a/t4-2-evaluar-respuesta
   ```
   Llena la plantilla del PR. **Otra persona** lo revisa y lo fusiona; no fusiones el tuyo.

## 6. Ejemplo completo: una función con su prueba
Así se ve el patrón de todas las tareas de lógica. En `functions/api/test_app.py` agregas la prueba:
```python
import unittest

import app


class PruebaSaludo(unittest.TestCase):
    def test_sin_nombre_saluda_al_mundo(self):
        self.assertEqual(app.armar_saludo(None), {"mensaje": "Hola, mundo"})

    def test_con_nombre(self):
        self.assertEqual(app.armar_saludo("Ana"), {"mensaje": "Hola, Ana"})


if __name__ == "__main__":
    unittest.main()
```
`python scripts/probar.py api` falla (aún no existe `armar_saludo`). Luego en `functions/api/app.py` escribes:
```python
def armar_saludo(nombre):
    nombre = (nombre or "").strip() or "mundo"
    return {"mensaje": f"Hola, {nombre}"}
```
Y la prueba pasa. Ese es el ritmo: **prueba que falla → código mínimo → prueba que pasa → commit**.

Este ejemplo es la tarea T2.1; la tarea completa pide además el caso del nombre vacío o solo espacios.

## 7. Datos de prueba
- Las pruebas crean sus propios datos dentro del código de la prueba.
- Si necesitas datos de ejemplo más grandes, guárdalos **fuera del repo** (por ejemplo, en una carpeta tuya `~/detective-pruebas/`) y **nunca los commitees**.
- El formato de los datos de la tabla estará en `docs/MODELO-DATOS.md` cuando se complete la tarea T3.1.

## 8. Qué NO se prueba en tu máquina
Permisos reales de AWS, EventBridge y la entrega a Slack se verifican después del despliegue, con el dueño de la cuenta. Tú no necesitas credenciales de AWS para nada de esto.

## 9. Si algo falla
| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| `python: command not found` | En Mac o Linux el comando es `python3`; en Windows puede ser `py` | Prueba `python3 scripts/probar.py` o `py scripts/probar.py` |
| `No module named app` | Corriste la prueba a mano desde otra carpeta | Usa siempre `python scripts/probar.py <funcion>` desde la raíz del repo |
| `Address already in use` (puerto 8080) | Otro servidor ocupa el puerto | Usa otro: `--port 8081`, y abre ese puerto |
| `Permission denied` o `repository not found` al clonar | La invitación aún no está aceptada, o iniciaste sesión con otra cuenta | Acepta la invitación y verifica con qué cuenta entraste en GitHub |
| Avisos `LF will be replaced by CRLF` en Windows | Saltos de línea | Son normales; ignóralos |
| Una prueba falla en tu máquina pero no en la de otro | Versión de Python distinta | Compara con `python --version`; usa 3.12 o superior |
| Sospechas que subiste un secreto | — | **Avisa de inmediato** al dueño; ver [`SEGURIDAD.md`](SEGURIDAD.md). Borrar el commit no basta |

## 10. Si usas un asistente de IA
Puedes usarlo, con estas condiciones (las reglas completas están en [`AGENTS.md`](../AGENTS.md)):
1. **Dile que lea `AGENTS.md`** antes de empezar y dile **qué tarea haces** (por ejemplo `T4.2`). Los asistentes que leen archivos del repo (Claude Code, Copilot, Cursor y otros) lo toman solos, pero verifícalo.
2. **Tú eres responsable de cada línea** que subas. Léela completa y asegúrate de poder explicarla con tus palabras.
3. **Que no se salga de la tarea:** si toca archivos que no son de tu tarea y de tu carril, o añade archivos y dependencias nuevas, descártalo y vuelve a pedirlo más acotado.
4. **Antes de abrir el PR**, corre tú mismo `python scripts/probar.py` y `python scripts/auditar_codigo.py functions/<tu-carpeta>`.
5. **Marca la casilla de IA** en la plantilla del pull request. No es un castigo: ayuda a revisar mejor.
6. **Nunca le pegues a un asistente claves, tokens ni datos personales.**

Todas las ramas pasan por una auditoría ([`AUDITORIA.md`](AUDITORIA.md)). Código que no se entiende o que se sale de las reglas se devuelve para corregir; es parte de aprender.

## 11. Dónde seguir
- Reglas de ramas y PR: [`CONTRIBUIR.md`](CONTRIBUIR.md)
- Seguridad: [`SEGURIDAD.md`](SEGURIDAD.md)
- Qué probar según tu carril: [`LOCAL.md`](LOCAL.md)
- Tareas: [`TAREAS.md`](TAREAS.md)
