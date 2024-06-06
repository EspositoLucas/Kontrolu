#tests/tests_back/tests_macros/tests_macro_medidor.py

import unittest
from src.back.macros.macro_proceso import MacroProceso
from src.back.macros.macro_bloque import MacroBloque


class TestMacroProceso(unittest.TestCase):
    def setUp(self):
        self.macro_proceso = MacroProceso()

    def test_nombre(self):
        self.assertEqual(self.macro_proceso.nombre, "Proceso")

    def test_superclass(self):
        self.assertIsInstance(self.macro_proceso, MacroBloque)

    # Add more tests here

if __name__ == "__main__":
    unittest.main()