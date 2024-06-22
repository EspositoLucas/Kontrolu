from src.back.topologia.topologia_serie import TopologiaSerie


class TopologiaParalelo():
    
    def __init__(self,microbloque,microbloque2):
        serie = TopologiaSerie(micro=microbloque)
        serie2 = TopologiaSerie(micro=microbloque2)
        self.elementos = [serie,serie2]
    
    def agregar_paralela(self,microbloque,indice):
        serie = TopologiaSerie(micro=microbloque)
        self.elementos.insert(indice,serie)

    def borrar_paralela(self,indice):
        self.elementos.pop(indice)
        if(len(self.elementos)==1): return self.elementos[0]
        return self

    def __str__(self):
        return f"{self.nombre}"
    