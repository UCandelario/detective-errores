import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import auditar_codigo as ac


def mensajes(codigo, **opciones):
    return [m for _, _, m in ac.revisar_codigo(codigo, **opciones)]


class PruebaFunciones(unittest.TestCase):
    def test_funcion_corta_y_plana_no_da_hallazgos(self):
        codigo = "def sumar(a, b):\n    return a + b\n"
        self.assertEqual(mensajes(codigo), [])

    def test_funcion_larga_se_marca(self):
        cuerpo = "".join(f"    x{i} = {i}\n" for i in range(40))
        resultado = mensajes("def larga():\n" + cuerpo + "    return 1\n")
        self.assertTrue(any("larga tiene 42 líneas" in m for m in resultado), resultado)

    def test_el_limite_de_lineas_se_puede_cambiar(self):
        codigo = "def f():\n    a = 1\n    b = 2\n    return a + b\n"
        self.assertEqual(mensajes(codigo, max_lineas=10), [])
        self.assertTrue(mensajes(codigo, max_lineas=3))

    def test_anidacion_profunda_se_marca(self):
        codigo = (
            "def f(xs):\n"
            "    for x in xs:\n"
            "        if x:\n"
            "            for y in x:\n"
            "                if y:\n"
            "                    return y\n"
        )
        self.assertTrue(any("anida 4 niveles" in m for m in mensajes(codigo)))

    def test_un_elif_no_cuenta_como_anidacion(self):
        codigo = (
            "def f(n):\n"
            "    if n == 1:\n        return 'a'\n"
            "    elif n == 2:\n        return 'b'\n"
            "    elif n == 3:\n        return 'c'\n"
            "    elif n == 4:\n        return 'd'\n"
            "    else:\n        return 'e'\n"
        )
        self.assertEqual(mensajes(codigo), [])


class PruebaErroresYLlamadas(unittest.TestCase):
    def test_except_desnudo_se_marca(self):
        codigo = "try:\n    x = 1\nexcept:\n    x = 2\n"
        self.assertTrue(any("except desnudo" in m for m in mensajes(codigo)))

    def test_except_con_pass_se_marca(self):
        codigo = "try:\n    x = 1\nexcept ValueError:\n    pass\n"
        self.assertTrue(any("ignora el error" in m for m in mensajes(codigo)))

    def test_except_que_maneja_el_error_no_se_marca(self):
        codigo = "try:\n    x = int('a')\nexcept ValueError:\n    x = 0\n"
        self.assertEqual(mensajes(codigo), [])

    def test_llamadas_riesgosas(self):
        casos = {
            "eval('1')": "eval()",
            "exec('x = 1')": "exec()",
            "__import__('os')": "__import__()",
            "os.system('ls')": "os.system()",
            "pickle.loads(b'')": "pickle.loads()",
            "subprocess.run(['ls'])": "subprocess.run()",
        }
        for codigo, esperado in casos.items():
            with self.subTest(codigo=codigo):
                self.assertTrue(any(esperado in m for m in mensajes(codigo)), mensajes(codigo))

    def test_importar_subprocess_se_marca(self):
        self.assertTrue(mensajes("import subprocess\n"))
        self.assertTrue(mensajes("from subprocess import run\n"))

    def test_un_metodo_con_el_mismo_nombre_no_se_marca(self):
        # `evaluar.eval` o `lista.compile` no son las funciones peligrosas.
        self.assertEqual(mensajes("resultado = objeto.eval(1)\n"), [])

    def test_pendientes_se_marcan(self):
        self.assertTrue(any("pendiente" in m for m in mensajes("x = 1  # TODO arreglar\n")))
        self.assertEqual(mensajes("x = 'TODO'\n"), [])


class PruebaLineaDelHallazgo(unittest.TestCase):
    def test_devuelve_ruta_y_linea(self):
        hallazgos = ac.revisar_codigo("a = 1\nb = eval('2')\n", ruta="x.py")
        self.assertEqual(hallazgos[0][:2], ("x.py", 2))


class PruebaEjecucion(unittest.TestCase):
    def correr(self, *argumentos):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = ac.main(list(argumentos))
        return codigo, salida.getvalue()

    def test_carpeta_limpia_termina_en_cero(self):
        with tempfile.TemporaryDirectory() as carpeta:
            Path(carpeta, "bien.py").write_text("def f():\n    return 1\n", encoding="utf-8")
            codigo, salida = self.correr(carpeta)
        self.assertEqual(codigo, 0)
        self.assertIn("Sin hallazgos en 1 archivo", salida)

    def test_carpeta_con_problema_termina_en_uno(self):
        with tempfile.TemporaryDirectory() as carpeta:
            Path(carpeta, "mal.py").write_text("x = eval('1')\n", encoding="utf-8")
            codigo, salida = self.correr(carpeta)
        self.assertEqual(codigo, 1)
        self.assertIn("eval()", salida)

    def test_un_archivo_con_error_de_sintaxis_se_reporta_sin_romper(self):
        with tempfile.TemporaryDirectory() as carpeta:
            Path(carpeta, "roto.py").write_text("def (:\n", encoding="utf-8")
            codigo, salida = self.correr(carpeta)
        self.assertEqual(codigo, 1)
        self.assertIn("no se pudo revisar", salida)

    def test_ignora_pycache(self):
        with tempfile.TemporaryDirectory() as carpeta:
            cache = Path(carpeta, "__pycache__")
            cache.mkdir()
            (cache / "x.py").write_text("x = eval('1')\n", encoding="utf-8")
            codigo, _ = self.correr(carpeta)
        self.assertEqual(codigo, 0)


if __name__ == "__main__":
    unittest.main()
