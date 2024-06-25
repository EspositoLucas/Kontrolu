from src.back.topologia.interfaz_topologia import InterfazTopologia
from src.back.topologia.topologia_serie import TopologiaSerie
from __future__ import annotations

class MicroBloque(InterfazTopologia):
    def __init__(self,padre: TopologiaSerie) -> None:
        self.padre = padre
    def borrar_elemento(self):
        self.padre.borrar_elemento(self)
    def agregar_arriba(self,microbloque:MicroBloque):
        self.padre.agregar_elemento(self,self.padre.hijos.index(self))