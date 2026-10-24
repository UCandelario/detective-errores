import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import revisar_secretos as rs

# Los valores falsos se arman por partes para que ESTE archivo no se detecte a sí mismo.
CLAVE_FALSA = "AKIA" + "A" * 16
WEBHOOK_FALSO = "https://hooks.slack.com/services/" + "T0000000/B0000000/" + "x" * 24
TOKEN_SLACK_FALSO = "xoxb-" + "1" * 12 + "-" + "a" * 12
TOKEN_GITHUB_FALSO = "ghp_" + "a" * 36
LLAVE_FALSA = "-----BEGIN " + "RSA PRIVATE KEY-----"


class PruebaBuscarEnTexto(unittest.TestCase):
    def test_detecta_cada_tipo(self):
        casos = {
            CLAVE_FALSA: "clave de acceso de AWS",
            "aws_secret_access_key = abc123": "clave secreta de AWS",
            WEBHOOK_FALSO: "webhook de Slack",
            TOKEN_SLACK_FALSO: "token de Slack",
            TOKEN_GITHUB_FALSO: "token de GitHub",
            LLAVE_FALSA: "llave privada",
        }
        for texto, esperado in casos.items():
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, rs.buscar_en_texto(f"valor = {texto}"))

    def test_texto_normal_no_se_marca(self):
        for texto in ["print('hola')", "AKIA...", "hooks.slack.com", "token = None", ""]:
            with self.subTest(texto=texto):
                self.assertEqual(rs.buscar_en_texto(texto), [])

    def test_la_marca_de_ignorar_salta_la_linea(self):
        linea = f"{CLAVE_FALSA}  # {rs.MARCA_IGNORAR}"
        self.assertEqual(rs.buscar_en_texto(linea), [])


class PruebaNombresProhibidos(unittest.TestCase):
    def test_nombres_prohibidos(self):
        for ruta in [".env", ".env.local", "a/b/clave.pem", "x.key", "terraform.tfstate",
                     "terraform.tfstate.backup", "credentials", "secrets.tfvars",
                     "prod.auto.tfvars", "infra/.terraform/providers/x"]:
            with self.subTest(ruta=ruta):
                self.assertTrue(rs.nombre_prohibido(ruta))

    def test_nombres_permitidos(self):
        for ruta in [".env.example", "README.md", "infra/main.tf", "config/sitios.json"]:
            with self.subTest(ruta=ruta):
                self.assertFalse(rs.nombre_prohibido(ruta))


class PruebaDiff(unittest.TestCase):
    DIFF = (
        "diff --git a/uno.py b/uno.py\n"
        "--- a/uno.py\n"
        "+++ b/uno.py\n"
        "@@ -1,0 +5,2 @@\n"
        "+primera\n"
        "+segunda\n"
        "@@ -9 +20 @@\n"
        "-vieja\n"
        "+nueva\n"
        "diff --git a/borrado.py b/borrado.py\n"
        "--- a/borrado.py\n"
        "+++ /dev/null\n"
        "@@ -1 +0,0 @@\n"
        "-adios\n"
    )

    def test_devuelve_solo_lineas_anadidas_con_su_numero(self):
        self.assertEqual(
            list(rs.lineas_anadidas(self.DIFF)),
            [("uno.py", 5, "primera"), ("uno.py", 6, "segunda"), ("uno.py", 20, "nueva")],
        )

    def test_revisar_lineas_encuentra_el_secreto_en_la_linea_correcta(self):
        diff = f"+++ b/x.py\n@@ -0,0 +3 @@\n+k = {CLAVE_FALSA}\n"
        self.assertEqual(
            rs.revisar_lineas(rs.lineas_anadidas(diff)),
            [("x.py", 3, "clave de acceso de AWS")],
        )


class PruebaSalida(unittest.TestCase):
    def test_no_imprime_el_valor_del_secreto(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "config.txt"
            archivo.write_text(f"clave = {CLAVE_FALSA}\n", encoding="utf-8")
            salida = io.StringIO()
            with contextlib.redirect_stdout(salida):
                codigo = rs.main(["--rutas", str(archivo)])
        texto = salida.getvalue()
        self.assertEqual(codigo, 1)
        self.assertIn("clave de acceso de AWS", texto)
        self.assertNotIn(CLAVE_FALSA, texto)

    def test_archivo_limpio_termina_en_cero(self):
        with tempfile.TemporaryDirectory() as carpeta:
            archivo = Path(carpeta) / "limpio.txt"
            archivo.write_text("nada sensible\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(rs.main(["--rutas", str(archivo)]), 0)


if __name__ == "__main__":
    unittest.main()
