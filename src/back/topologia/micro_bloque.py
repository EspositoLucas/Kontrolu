from src.back.topologia.interfaz_topologia import InterfazTopologia
from src.back.topologia.topologia_serie import TopologiaSerie
from __future__ import annotations

class MicroBloque(InterfazTopologia):
    def __init__(self,padre: TopologiaSerie) -> None:
        self.padre = padre

    def borrar_elemento(self):
        self.padre.borrar_elemento(self)
        self.padre = None

    def agregar_arriba(self,microbloque:MicroBloque):
        self.padre.hacer_paralelo(self.padre.hijos.index(self),microbloque)
    
    def agregar_abajo(self,microbloque:MicroBloque):
        self.padre.hacer_paralelo(self.padre.hijos.index(self)+1,microbloque)
    
    def agregar_antes(self,microbloque:MicroBloque):
        self.padre.agregar_elemento(self.padre.hijos.index(self),microbloque)
    
    def agregar_despues(self,microbloque:MicroBloque):
        self.padre.agregar_elemento(self.padre.hijos.index(self)+1,microbloque)