import unittest

import app


class PruebaBase(unittest.TestCase):
    def test_el_modulo_se_importa(self):
        # Prueba de humo: confirma que el entorno de pruebas funciona.
        self.assertTrue(app.__doc__)


class PruebaEvaluarRespuesta(unittest.TestCase):
    def test_tabla_de_casos(self):
        casos = [
            # (codigo, latencia, umbral, esperado_esperado)
            (200, 150, 2000, "sano"),
            (200, 0, 2000, "sano"),
            (200, 2000, 2000, "sano"),
            (200, 2500, 2000, "degradado"),
            (301, 100, 2000, "degradado"),
            (404, 50, 2000, "caido"),
            (None, None, 2000, "caido"),
        ]
        for codigo, latencia, umbral, esperado in casos:
            with self.subTest(codigo=codigo, latencia=latencia):
                self.assertEqual(app.evaluar_respuesta(codigo, latencia, umbral), esperado)

# class PruebaEvaluarRespuesta(unittest.TestCase):
#     def test_sitio_rapido_esta_sano(self):
#         self.assertEqual(app.evaluar_respuesta(399, 100), "degradado")

#     def test_sin_respuesta_esta_caido(self):
#         self.assertEqual(app.evaluar_respuesta(None, None), "caido")

#     def test_codigo_invalido_lanza_error(self):
#         with self.assertRaises(ValueError):
#             app.evaluar_respuesta(600, 10)

if __name__ == "__main__":
    unittest.main()
