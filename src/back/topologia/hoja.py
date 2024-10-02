from __future__ import annotations
from .interfaz_topologia import InterfazTopologia
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from latex2sympy2 import latex2sympy

class Hoja(InterfazTopologia):
    
    def __init__(self, nombre: str= "Hoja", funcion_transferencia: str="1", padre=None) -> None:
        self.nombre = nombre
        self.funcion_transferencia = funcion_transferencia
        self.padre = padre

    def agregar_perturbacion_antes(self, actual: Hoja, perturbacion):
        self.padre.agregar_perturbacion_antes(actual, perturbacion)

    def agregar_perturbacion_despues(self, actual: Hoja, perturbacion):
        self.padre.agregar_perturbacion_despues(actual, perturbacion)

    def borrar_elemento(self):
        self.padre.borrar_elemento(self)
        self.padre = None

    def agregar_arriba(self,microbloque:Hoja):
        self.padre.agregar_arriba_de(microbloque,self)
    
    def agregar_abajo(self,microbloque:Hoja):
        self.padre.agregar_abajo_de(microbloque,self)
    
    def agregar_antes(self,microbloque:Hoja):
        self.padre.agregar_antes_de(microbloque,self)
    
    def agregar_despues(self,microbloque:Hoja):
        self.padre.agregar_despues_de(microbloque,self)
    
    def __str__(self) -> str:
        return self.nombre
    
    def obtener_micros(self):
        return [self]
    
    def set_funcion_transferencia(self, funcion):
        self.funcion_transferencia = funcion
    
    def agregar_en_paralela_en_padre_arriba(self,microbloque:Hoja):
        self.padre.agregar_serie_arriba(microbloque)
        
    def agregar_en_paralela_en_padre_abajo(self,microbloque:Hoja):
        self.padre.agregar_serie_abajo(microbloque)

    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:Hoja):
        self.padre.agregar_en_serie_fuera_de_paralela_antes(microbloque)
        
    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:Hoja):
        self.padre.agregar_en_serie_fuera_de_paralela_despues(microbloque)
    


    def get_parent_structures(self):
        parents = []
        actual = self.padre
        nivel = 0
        while actual and "Macro" not in actual.__class__.__name__: # "Macro" not in actual.__class__.__name__ esta condicion es para que no se incluya el macrobloque en la lista de padres 
            # seguir hasta llegar al macrobloque --> esto porque el padre de la serie principal es el macrobloque
            parents.append([actual, nivel])
            actual = actual.padre
            nivel += 1
        return parents
    
    def simular(self, tiempo, entrada=None):
        pass

    def validar_entrada(self):
        return self.padre.validar_entrada(self,self.unidad_entrada())
    
    def validar_salida(self):
        return self.padre.validar_salida(self,self.unidad_salida())

    def unidad_entrada(self):
        pass
    
    def unidad_salida(self):
        pass