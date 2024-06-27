from __future__ import annotations
from src.back.topologia.interfaz_topologia import InterfazTopologia
class TopologiaSerie(InterfazTopologia):
    
    def __init__(self,micro: TopologiaParalelo | MicroBloque = None,lista_micros: list=None,padre = None):
        self.padre = padre
        self.hijos: list[InterfazTopologia] = []
        print("creo serie")
        if micro:
            print("Entra micro")
            micro.cambiar_padre(self)
            self.hijos.append(micro)
        if lista_micros:
            print("Entra lista")
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
        return "SERIE: " + str(list(map(lambda hijo: str(hijo),self.hijos)))



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