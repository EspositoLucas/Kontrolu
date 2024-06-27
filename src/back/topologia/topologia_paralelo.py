
from src.back.topologia.interfaz_topologia import InterfazTopologia

from src.back.topologia.topologia_serie import TopologiaSerie

class TopologiaParalelo(InterfazTopologia):
    
    
    def __init__(self,microbloque,microbloque2,padre:TopologiaSerie=None):
        self.padre = padre
        serie = TopologiaSerie(micro=microbloque,padre=self)
        serie2 = TopologiaSerie(micro=microbloque2,padre=self)
        self.hijos = [serie,serie2]
    
    def agregar_paralela(self,microbloque,indice):
        serie = TopologiaSerie(micro=microbloque)
        self.hijos.insert(indice,serie)

    def borrar_paralela(self):
        self.padre.agregar_elementos(self,self.hijos[0])
    
    def borrar_elemento(self,elemento):
        super().borrar_elemento(elemento)
        if(len(self.hijos) == 1): self.borrar_paralela()

    def alto(self) -> int:
        return sum(map(lambda x: x.alto(),self.hijos))
    
    def ancho(self) -> int:
        return max(map(lambda x: x.ancho(),self.hijos))

    def __str__(self):
        return "PARALELO: " + list(map(lambda hijo: hijo.__str__(),self.hijos))

