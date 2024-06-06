#tests/tests_back/tests_macros/tests_macro_bloque.py

import unittest
from src.back.macros.macro_bloque import MacroBloque

class TestMacroBloque(unittest.TestCase):

    def test_init(self):
        macro = MacroBloque()
        self.assertIsInstance(macro, MacroBloque)

    def test_str(self):
        macro = MacroBloque()
        self.assertEqual(str(macro), "MacroBloque")

if __name__ == '__main__':
    unittest.main()