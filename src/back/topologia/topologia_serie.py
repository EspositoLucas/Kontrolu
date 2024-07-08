from __future__ import annotations
from back.topologia.interfaz_topologia import InterfazTopologia
from PyQt5.QtGui import QColor

ANCHO = 150
ALTO = 80

class TopologiaSerie(InterfazTopologia):
    
    def __init__(self,micro: TopologiaParalelo | MicroBloque = None,lista_micros: list=None,padre: InterfazTopologia = None):
        self.padre = padre
        self.hijos: list[InterfazTopologia] = []
        if micro:
            micro.cambiar_padre(self)
            self.hijos.append(micro)
        if lista_micros:
            for micro in lista_micros:
                micro.cambiar_padre(self)
            self.hijos.extend(lista_micros)

    def agregar_serie_arriba(self,microbloque:MicroBloque):
        self.padre.agregar_arriba_de(microbloque,self)

    def agregar_serie_abajo(self,microbloque:MicroBloque):
        self.padre.agregar_abajo_de(microbloque,self)

    def agregar_elemento(self,microbloque: InterfazTopologia, posicion: int = 0):
        microbloque.cambiar_padre(self)
        self.hijos.insert(posicion,microbloque)


    def crear_paralela_respecto_de_serie_arriba(self,microbloque:MicroBloque):
        self.hijos = [TopologiaParalelo(microbloqueNuevo=microbloque,serie=TopologiaSerie(lista_micros=self.hijos),arriba=True,padre=self)]
    

    def crear_paralela_respecto_de_serie_abajo(self,microbloque:MicroBloque):
        self.hijos = [TopologiaParalelo(microbloqueNuevo=microbloque,serie=TopologiaSerie(lista_micros=self.hijos),arriba=False,padre=self)]
    


    def agregar_arriba_de(self,microbloque:MicroBloque,actual:MicroBloque):
        indice = self.hijos.index(actual)
        paralelo = TopologiaParalelo(microbloqueNuevo=microbloque,microbloque2=actual,arriba=True,padre=self)
        self.hijos[indice] = paralelo
        
    def agregar_abajo_de(self,microbloque:MicroBloque,actual:MicroBloque):
        indice = self.hijos.index(actual)
        paralelo = TopologiaParalelo(microbloqueNuevo=microbloque,microbloque2=actual,arriba=False,padre=self)
        self.hijos[indice] = paralelo

    def agregar_despues_de(self,microbloque:MicroBloque,actual:InterfazTopologia):
        indice = self.hijos.index(actual)
        self.agregar_elemento(microbloque,indice+1)

    def agregar_antes_de(self,microbloque:MicroBloque,actual:InterfazTopologia):
        indice = self.hijos.index(actual)
        self.agregar_elemento(microbloque,indice)

    def borrar_elemento(self,elemento):
        super().borrar_elemento(elemento)
        if(not len(self.hijos)):self.padre.borrar_elemento(self)
    
    def disolver_paralela(self,paralela:TopologiaParalelo):
        posicion = self.hijos.index(paralela)
        del self.hijos[posicion]

        nuevos_hijos = paralela.obtener_micros()

        for micro in reversed(nuevos_hijos):
            micro.cambiar_padre(self)
            self.hijos.insert(posicion,micro)

    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:MicroBloque):
        self.padre.agregar_en_serie_fuera_de_paralela_antes(microbloque)
        
    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:MicroBloque):
        self.padre.agregar_en_serie_fuera_de_paralela_despues(microbloque)

    def alto(self) -> int:
        return max(map(lambda x: x.alto(),self.hijos))
    
    def ancho(self) -> int:
        return sum(map(lambda x: x.ancho(),self.hijos))


    def __str__(self):
        return "SERIE: " + str(list(map(lambda hijo: str(hijo),self.hijos)))

class MicroBloque(InterfazTopologia):
    def __init__(self, nombre: str, color: QColor=None, funcion_transferencia: str=None, opciones_adicionales: dict=None, padre: TopologiaSerie=None) -> None:
        self.padre = padre
        self.nombre = nombre
        self.color = color
        self.funcion_transferencia = funcion_transferencia
        self.opciones_adicionales = opciones_adicionales

    def borrar_elemento(self):
        self.padre.borrar_elemento(self)
        self.padre = None

    def agregar_arriba(self,microbloque:MicroBloque):
        self.padre.agregar_arriba_de(microbloque,self)
    
    def agregar_abajo(self,microbloque:MicroBloque):
        self.padre.agregar_abajo_de(microbloque,self)
    
    def agregar_antes(self,microbloque:MicroBloque):
        self.padre.agregar_antes_de(microbloque,self)
    
    def agregar_despues(self,microbloque:MicroBloque):
        self.padre.agregar_despues_de(microbloque,self)
    
    def alto(self) -> int:
        return 80
    
    def ancho(self) -> int:
        return 150
    
    def __str__(self) -> str:
        return self.nombre
    
    def obtener_micros(self):
        return [self]
    
    def set_funcion_transferencia(self, funcion):
        self.funcion_transferencia = funcion

    def set_opcion_adicional(self, clave, valor):
        self.opciones_adicionales[clave] = valor

    def get_opcion_adicional(self, clave):
        return self.opciones_adicionales.get(clave)
    
    def agregar_en_paralela_en_padre_arriba(self,microbloque:MicroBloque):
        self.padre.agregar_serie_arriba(microbloque)
        
    def agregar_en_paralela_en_padre_abajo(self,microbloque:MicroBloque):
        self.padre.agregar_serie_abajo(microbloque)

    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:MicroBloque):
        self.padre.agregar_en_serie_fuera_de_paralela_antes(microbloque)
        
    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:MicroBloque):
        self.padre.agregar_en_serie_fuera_de_paralela_despues(microbloque)
    
    def get_parent_structures(self):
        parents = []
        actual = self.padre
        nivel = 0
        while actual and "Macro" not in actual.__class__.__name__: # "Macro" not in actual.__class__.__name__ esta condicion es para que no se incluya el macrobloque en la lista de padres 
            # seguir hasta llegar al macrobloque --> esto porque el padre de la serie principal es el macrobloque
            parents.append([actual, nivel])
            actual = actual.padre
            nivel += 1
        return parents

    




class TopologiaParalelo(InterfazTopologia):
    
    
    def __init__(self,microbloqueNuevo,microbloque2:MicroBloque=None,serie:TopologiaSerie=None,arriba=True,padre:TopologiaSerie=None):
        self.padre = padre
        nuevaSerie = TopologiaSerie(micro=microbloqueNuevo,padre=self)
        if(serie):  nuevo = serie
        if(microbloque2): nuevo = TopologiaSerie(micro=microbloque2,padre=self)
        nuevo.cambiar_padre(self)
        if(arriba): self.hijos = [nuevaSerie,nuevo]
        else: self.hijos = [nuevo,nuevaSerie]
    
    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:MicroBloque):
        self.padre.agregar_antes_de(microbloque,self)

    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:MicroBloque):
        self.padre.agregar_despues_de(microbloque,self)

    def agregar_abajo_de(self,microbloque,actual):
        indice = self.hijos.index(actual)
        self.agregar_paralela(microbloque,indice+1)
    
    def agregar_arriba_de(self,microbloque,actual):
        indice = self.hijos.index(actual)
        self.agregar_paralela(microbloque,indice)

    def agregar_paralela(self,microbloque,indice):
        serie = TopologiaSerie(micro=microbloque,padre=self)
        self.hijos.insert(indice,serie)

    def borrar_paralela(self):
        self.padre.disolver_paralela(self)
    
    def borrar_elemento(self,elemento):
        super().borrar_elemento(elemento)
        if(len(self.hijos) == 1): self.borrar_paralela()

    def alto(self) -> int:
        return sum(map(lambda x: x.alto(),self.hijos))
    
    def ancho(self) -> int:
        return max(map(lambda x: x.ancho(),self.hijos))

    def __str__(self):
        return "PARALELO: " + str(list(map(lambda hijo: hijo.__str__(),self.hijos)))