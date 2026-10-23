import unittest

import app


class PruebaBase(unittest.TestCase):
    def test_el_modulo_se_importa(self):
        # Prueba de humo: confirma que el entorno de pruebas funciona.
        self.assertTrue(app.__doc__)


if __name__ == "__main__":
    unittest.main()
