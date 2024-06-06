#tests/tests_back/tests_macros/tests_macro_controlador.py

import unittest
from src.back.macros.macro_bloque import MacroBloque
from src.back.macros.macro_controlador import MacroControlador

class TestMacroControlador(unittest.TestCase):
    def setUp(self):
        self.macro_controlador = MacroControlador()

    def test_nombre(self):
        self.assertEqual(self.macro_controlador.nombre, "Controlador")

    def test_herencia(self):
        self.assertIsInstance(self.macro_controlador, MacroBloque)

    # Add more tests here

if __name__ == "__main__":
    unittest.main()