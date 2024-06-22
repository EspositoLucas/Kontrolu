from src.back.topologia.topologia_paralelo import TopologiaParalelo

class TopologiaSerie():
    
    def __init__(self,micro=None,lista_micros: list=None):
        self.elementos = []
        if not micro:
            self.elementos.append(micro)
        if not lista_micros:
            self.elementos.extend(lista_micros)

    def agregar_elemento(self,micro,indice):
        self.elementos.insert(indice,micro)

    def hacer_paralelo(self,posicion,microbloque):
        elemento = self.elementos[posicion]
        paralelo = TopologiaParalelo(elemento,microbloque)
        self.elementos[posicion] = paralelo

    def __str__(self):
        return f"{self.nombre}"
    