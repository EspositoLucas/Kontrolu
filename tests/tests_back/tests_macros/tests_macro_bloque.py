#tests/tests_back/tests_macros/tests_macro_bloque.py

import unittest
from src.back.macros.macro_bloque import MacroBloque
from src.back.topologia.topologia_serie import MicroBloque

class TestMacroBloque(unittest.TestCase):

    def test_init(self):
        macro = MacroBloque()
        self.assertIsInstance(macro, MacroBloque)

    def test_str(self):
        macro = MacroBloque()
        self.assertEqual(str(macro), "MacroBloque: SERIE: []")

    def test_add_serie(self):
        micro = MicroBloque("microSerie1")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro)
        print(str(macro))

    def test_agregar_serie_despues_y_antes(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microSerie1")
        micro2 = MicroBloque("microSerie2")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro1,5)

        macro.topologia.agregar_elemento(micro0,0)

        macro.topologia.agregar_elemento(micro2,2)

        print(str(macro))
    
    def test_agregar_paralelo(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microParalelo1")
        micro2 = MicroBloque("microParalelo2")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro1,5)

        macro.topologia.agregar_elemento(micro0,0)

        macro.topologia.agregar_elemento(micro2,2)

        print(str(macro))

if __name__ == '__main__':
    unittest.main()