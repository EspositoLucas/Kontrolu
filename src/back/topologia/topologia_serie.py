from __future__ import annotations
from src.back.topologia.interfaz_topologia import InterfazTopologia
from src.back.topologia.micro_bloque import MicroBloque
from src.back.macros.macro_bloque import MacroBloque

from src.back.topologia.topologia_paralelo import TopologiaParalelo

class TopologiaSerie(InterfazTopologia):
    
    def __init__(self,micro: TopologiaParalelo | MicroBloque = None,lista_micros: list=None,padre: TopologiaSerie | MacroBloque = None):
        self.padre = padre
        self.hijos: list[InterfazTopologia] = []
        if micro:
            micro.cambiar_padre(self)
            self.hijos.append(micro)
        if lista_micros:
            for micro in lista_micros:
                micro.cambiar_padre(self)
            self.hijos.extend(lista_micros)

    def agregar_elemento(self,microbloque: InterfazTopologia, posicion: int = 0):
        microbloque.cambiar_padre(self)
        self.hijos.insert(posicion,microbloque)

    def hacer_paralelo(self,microbloque: InterfazTopologia,posicion:int=0):
        elemento = self.hijos[posicion]
        paralelo = TopologiaParalelo(elemento,microbloque,padre=self)
        self.hijos[posicion] = paralelo

    def borrar_elemento(self,elemento):
        super().borrar_elemento(elemento)
        if(not len(self.hijos)):self.padre.borrar_elemento(self)

    def agregar_elementos(self,reemplazar:TopologiaParalelo,lista_micros: list):
        posicion = self.hijos.index(reemplazar)
        for micro in lista_micros:
            micro.cambiar_padre(self)
        self.hijos[posicion:posicion] = lista_micros

    def alto(self) -> int:
        return max(map(lambda x: x.alto(),self.hijos))
    
    def ancho(self) -> int:
        return sum(map(lambda x: x.ancho(),self.hijos))


    def __str__(self):
        return "SERIE: " + list(map(lambda hijo: hijo.__str__(),self.hijos))


