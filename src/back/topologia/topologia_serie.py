from src.back.topologia.topologia_paralelo import TopologiaParalelo
from src.back.topologia.interfaz_topologia import InterfazTopologia
from src.back.macros.macro_bloque import MacroBloque
from __future__ import annotations
class TopologiaSerie(InterfazTopologia):
    
    def __init__(self,micro=None,lista_micros: list=None,padre: TopologiaSerie | MacroBloque = None):
        self.padre = padre
        self.hijos: list(InterfazTopologia) = []
        if not micro:
            self.hijos.append(micro)
        if not lista_micros:
            self.hijos.extend(lista_micros)

    def agregar_elemento(self,micro,indice):
        self.hijos.insert(indice,micro)

    def hacer_paralelo(self,posicion,microbloque):
        elemento = self.hijos[posicion]
        paralelo = TopologiaParalelo(elemento,microbloque)
        self.hijos[posicion] = paralelo

    def borrar_elemento(self,elemento):
        super().borrar_elemento(elemento)
        if(not len(self.hijos)): self.padre.borrar_elemento(self)

    def __str__(self):
        return f"{self.nombre}"
    