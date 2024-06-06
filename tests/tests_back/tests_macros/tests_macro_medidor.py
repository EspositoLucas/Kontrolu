#tests/tests_back/tests_macros/tests_macro_medidor.py

import unittest
from src.back.macros.macro_bloque import MacroBloque
from src.back.macros.macro_medidor import MacroMedidor

class TestMacroMedidor(unittest.TestCase):
    def setUp(self):
        self.macro_medidor = MacroMedidor()

    def test_nombre(self):
        self.assertEqual(self.macro_medidor.nombre, "Medidor")

    def test_herencia(self):
        self.assertIsInstance(self.macro_medidor, MacroBloque)

    # Add more tests here

if __name__ == "__main__":
    unittest.main()