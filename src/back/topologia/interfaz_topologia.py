from __future__ import annotations
from typing import Tuple
import itertools
from back.perturbacion import Perturbacion
class InterfazTopologia():
    def __init__(self,padre=None) -> None:
        self.padre = padre
        self.perturbacion_entrada = Perturbacion(padre=self)
        self.perturbacion_salida = Perturbacion(padre=self)

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

    def alterar_entrada(self,entrada,tiempo):
        return self.perturbacion_entrada.alterar(entrada,tiempo)
    
    def alterar_salida(self,salida,tiempo):
        return self.perturbacion_salida.alterar(salida,tiempo)
    
    def generar_perturbacion_entrada(self,ft,ciclos):
        self.perturbacion_entrada.generar_perturbacion(ft,ciclos)
    
    def cancelar_perturbacion_entrada(self):
        self.perturbacion_entrada.cancelar_perturbacion()
    
    def generar_perturbacion_salida(self,ft,ciclos):
        self.perturbacion_salida.generar_perturbacion(ft,ciclos)
    
    def cancelar_perturbacion_salida(self):
        self.perturbacion_salida.cancelar_perturbacion()
        