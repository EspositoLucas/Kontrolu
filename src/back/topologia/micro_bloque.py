from __future__ import annotations
from src.back.topologia.interfaz_topologia import InterfazTopologia
from src.back.topologia.topologia_serie import TopologiaSerie

class MicroBloque(InterfazTopologia):
    def __init__(self,nombre: str,padre: TopologiaSerie=None) -> None:
        self.padre = padre
        self.nombre = nombre

    def borrar_elemento(self):
        self.padre.borrar_elemento(self)
        self.padre = None

    def agregar_arriba(self,microbloque:MicroBloque):
        self.padre.hacer_paralelo(microbloque,self.padre.hijos.index(self))
    
    def agregar_abajo(self,microbloque:MicroBloque):
        self.padre.hacer_paralelo(microbloque,self.padre.hijos.index(self)+1)
    
    def agregar_antes(self,microbloque:MicroBloque):
        self.padre.agregar_elemento(microbloque,self.padre.hijos.index(self))
    
    def agregar_despues(self,microbloque:MicroBloque):
        self.padre.agregar_elemento(microbloque,self.padre.hijos.index(self)+1)
    
    def alto(self) -> int:
        return 1
    
    def ancho(self) -> int:
        return 1
    
    def __str__(self) -> str:
        return self.nombre
