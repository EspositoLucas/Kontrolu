#tests/tests_back/tests_macros/tests_macro_actuador.py

import unittest
from src.back.macros.macro_bloque import MacroBloque
from src.back.topologia.micro_bloque import MicroBloque

class TestTopologia(unittest.TestCase):
    def setUp(self):
        self.macro_bloque = MacroBloque(None)

    def test_agregar_serie(self):
        bloque = MicroBloque("Bloque 1")
        self.macro_bloque.topologia.agregar_elemento(microbloque=bloque)
        print(1)
        

    

if __name__ == "__main__":
    unittest.main()