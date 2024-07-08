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
        #print(str(macro))

    def test_agregar_serie_despues_y_antes(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microSerie1")
        micro2 = MicroBloque("microSerie2")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro1,5)

        
        micro1.agregar_antes(micro0)
        micro1.agregar_despues(micro2)

        self.assertEqual(str(macro), "MacroBloque: SERIE: ['microSerie0', 'microSerie1', 'microSerie2']")

    
    def test_crear_paralelo(self):
        micro0 = MicroBloque("microParalelo0")
        micro1 = MicroBloque("microParalelo1")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro1,5)
        micro1.agregar_arriba(micro0)


        #print(str(macro))

    def test_crear_paralelo_de_una_serie(self):
        micro0 = MicroBloque("microParalelo0")
        micro1 = MicroBloque("microParalelo1")
        micro2 = MicroBloque("microParalelo2")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro1,5)
        micro1.agregar_arriba(micro0)
        micro1.padre.agregar_serie_abajo(micro2)
        #print(str(macro))

    
    def test_eliminar_base(self):
        micro0 = MicroBloque("microSerie0")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro0)
        micro0.borrar_elemento()

        #print(str(macro))
    
    def test_eliminar_de_paralela_normal(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microSerie1")
        micro3 = MicroBloque("microSerie3")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro0)
        micro0.agregar_arriba(micro1)
        micro1.agregar_despues(micro3)

        micro1.borrar_elemento()

        #print(str(macro))

    def test_eliminar_de_paralela_borra_serie_no_paralela(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microSerie1")
        micro3 = MicroBloque("microSerie3")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro0)
        micro0.agregar_arriba(micro1)
        micro1.agregar_en_paralela_en_padre_abajo(micro3)

        micro1.borrar_elemento()

        #print(str(macro))

    def test_eliminar_de_paralela_borra_serie_y_paralela(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microSerie1")
        micro3 = MicroBloque("microSerie3")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro0)
        micro0.agregar_arriba(micro1)
        micro0.agregar_despues(micro3)

        micro1.borrar_elemento()
        

        #print(str(macro))

    def test_agregar_antes_de_paralela_microbloque(self):
        micro0 = MicroBloque("microSerie0")
        micro1 = MicroBloque("microSerie1")
        micro3 = MicroBloque("microParaleloAntes3")
        micro4 = MicroBloque("microParaleloDespues4")
        
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro0)
        micro0.agregar_arriba(micro1)
        micro0.agregar_en_serie_fuera_de_paralela_antes(micro3)
        micro0.agregar_en_serie_fuera_de_paralela_despues(micro4)

        #print(str(macro))

    

    def test_agregar_antes_de_paralela_microbloque(self):
        micro0 = MicroBloque("microArriba")
        micro1 = MicroBloque("microAbajo")
        macro = MacroBloque()
        macro.topologia.agregar_elemento(micro0)
        macro.topologia.agregar_serie_abajo(micro1)

        print(str(macro))


if __name__ == '__main__':
    unittest.main()