from __future__ import annotations
from typing import Tuple
import itertools
from sympy import simplify,latex
from sympy.abc import s,t,z
from sympy import inverse_laplace_transform



class InterfazTopologia():

    def __init__(self,padre:InterfazTopologia=None) -> None:
        self.padre:InterfazTopologia = padre
        

    def ancho(self) -> int:
        pass

    def alto(self) -> int:
        pass

    def tamanio(self) -> Tuple[int,int]:
        return(self.ancho(),self.alto())

    def obtenerHijo(self):
        pass

    def obtenerPadre(self):
        pass

    def borrar_elemento(self,elemento):
        self.hijos.remove(elemento)

    def reemplazar_elemento(self,elemento,nuevo):
        self.hijos[self.hijos.index(elemento)] = nuevo

    def cambiar_padre(self,padre: InterfazTopologia):
        self.padre = padre

    def obtener_micros(self):
        return list(itertools.chain.from_iterable(map(lambda x: x.obtener_micros(),self.hijos)))
    
    
    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque):
        pass
        
    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque):
        pass

    def agregar_abajo_de(self,microbloque,actual):
        pass

    def agregar_arriba_de(self,microbloque,actual):
        pass

    def validar_entrada(self)->bool:
        pass

    def validar_salida(self)->bool:
        pass

    def unidad_entrada(self)->str:
        pass

    def unidad_salida(self)->str:
        pass
    def simular(self, tiempo, delta, entrada=None)->float:
        pass

    def calcular_fdt(self):

        pass
    
    def obtener_fdt_simpy(self):

        return simplify(self.calcular_fdt())
    
    def obtener_fdt_latex(self):

        return latex(self.obtener_fdt_simpy())
    
    def obtener_fdt_tiempo(self):
        return inverse_laplace_transform(self.obtener_fdt_simpy(),s,t)
    
    def obtener_fdt_tiempo_latex(self):
        return latex(self.obtener_fdt_tiempo())
    
    def operar_fdt(self,input):

        pass