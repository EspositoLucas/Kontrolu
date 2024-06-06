#tests/tests_back/tests_macros/tests_macro_actuador.py

import unittest
from src.back.macros.macro_actuador import MacroActuador
from src.back.macros.macro_bloque import MacroBloque

class TestMacroActuador(unittest.TestCase):
    def setUp(self):
        self.macro_actuador = MacroActuador()

    def test_nombre(self):
        self.assertEqual(self.macro_actuador.nombre, "Actuador")

    def test_herencia(self):
        self.assertIsInstance(self.macro_actuador, MacroBloque)

    # Add more tests here...

if __name__ == "__main__":
    unittest.main()