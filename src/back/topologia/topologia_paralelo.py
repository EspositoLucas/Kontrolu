from src.back.topologia.topologia_serie import TopologiaSerie
from src.back.topologia.interfaz_topologia import InterfazTopologia

class TopologiaParalelo(InterfazTopologia):
    
    def __init__(self,microbloque,microbloque2,padre:TopologiaSerie=None):
        self.padre = padre
        serie = TopologiaSerie(micro=microbloque)
        serie2 = TopologiaSerie(micro=microbloque2)
        self.hijos = [serie,serie2]
    
    def agregar_paralela(self,microbloque,indice):
        serie = TopologiaSerie(micro=microbloque)
        self.hijos.insert(indice,serie)

    def borrar_paralela(self):
        self.padre.reemplazar_elemento(self,self.hijos[0])
    
    def borrar_elemento(self,elemento):
        super().borrar_elemento(elemento)
        if(len(self.hijos) == 1): self.borrar_paralela()

    def __str__(self):
        return f"{self.nombre}"
    