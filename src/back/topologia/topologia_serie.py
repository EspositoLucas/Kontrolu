from __future__ import annotations
from back.topologia.interfaz_topologia import InterfazTopologia
from back.topologia.perturbacion import Perturbacion
from .perturbacion import Perturbacion
from .hoja import Hoja

ANCHO = 150
ALTO = 80

class TopologiaSerie(InterfazTopologia):
    
    def __init__(self,micro: InterfazTopologia = None,lista_micros: list=None,padre: InterfazTopologia = None,from_json=None):
        if from_json:
            self.from_json(from_json)
            self.padre = padre
            return
        self.hijos: list[InterfazTopologia] = []
        if micro:
            micro.cambiar_padre(self)
            self.hijos.append(micro)
        if lista_micros:
            for micro in lista_micros:
                micro.cambiar_padre(self)
            self.hijos.extend(lista_micros)
        super().__init__(padre)

    def agregar_serie_arriba(self,microbloque:Hoja):
        self.padre.agregar_arriba_de(microbloque,self)

    def agregar_serie_abajo(self,microbloque:Hoja):
        self.padre.agregar_abajo_de(microbloque,self)

    def agregar_elemento(self,microbloque: InterfazTopologia, posicion: int = 0):
        microbloque.cambiar_padre(self)
        self.hijos.insert(posicion,microbloque)


    def crear_paralela_respecto_de_serie_arriba(self,microbloque:Hoja):
        self.hijos = [TopologiaParalelo(microbloqueNuevo=microbloque,serie=TopologiaSerie(lista_micros=self.hijos),arriba=True,padre=self)]
    

    def crear_paralela_respecto_de_serie_abajo(self,microbloque:Hoja):
        self.hijos = [TopologiaParalelo(microbloqueNuevo=microbloque,serie=TopologiaSerie(lista_micros=self.hijos),arriba=False,padre=self)]
    


    def agregar_arriba_de(self,microbloque:Hoja,actual:Hoja):
        indice = self.hijos.index(actual)
        paralelo = TopologiaParalelo(microbloqueNuevo=microbloque,microbloque2=actual,arriba=True,padre=self)
        self.hijos[indice] = paralelo
        
    def agregar_abajo_de(self,microbloque:Hoja,actual:Hoja):
        indice = self.hijos.index(actual)
        paralelo = TopologiaParalelo(microbloqueNuevo=microbloque,microbloque2=actual,arriba=False,padre=self)
        self.hijos[indice] = paralelo

    def agregar_despues_de(self,microbloque:Hoja,actual:InterfazTopologia):
        indice = self.hijos.index(actual)
        self.agregar_elemento(microbloque,indice+1)

    def agregar_antes_de(self,microbloque:Hoja,actual:InterfazTopologia):
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

    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:Hoja):
        self.padre.agregar_en_serie_fuera_de_paralela_antes(microbloque)
        
    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:Hoja):
        self.padre.agregar_en_serie_fuera_de_paralela_despues(microbloque)       

    def agregar_perturbacion_antes(self, actual: Hoja, perturbacion: Perturbacion):
        indice = self.hijos.index(actual)
        perturbacion.cambiar_padre(self)
        self.hijos.insert(indice, perturbacion)

    def agregar_perturbacion_despues(self, actual: Hoja, perturbacion: Perturbacion):
        indice = self.hijos.index(actual)
        perturbacion.cambiar_padre(self)
        self.hijos.insert(indice + 1, perturbacion)


    def alto(self) -> int:
        if len(self.hijos) == 0:
            return 0
        return max(map(lambda x: x.alto(),self.hijos))
    
    def ancho(self) -> int:
        if len(self.hijos) == 0:
            return 0
        return sum(map(lambda x: x.ancho(),self.hijos))


    def __str__(self):
        return "SERIE: " + str(list(map(lambda hijo: str(hijo),self.hijos)))
    
    def simular(self, tiempo, entrada=None):

        for hijo in self.hijos:
                entrada = hijo.simular(tiempo, entrada)
    
        return entrada
    

    def validar_entrada(self, hijo: InterfazTopologia, unidad: str)-> bool:
        return self.unidad_entrante(hijo) == unidad
        
    def validar_salida(self, hijo: InterfazTopologia, unidad: str)-> bool:
        return self.unidad_saliente(hijo) == unidad
        
    def unidad_entrante(self, hijo: InterfazTopologia)-> str:
        pos = self.hijos.index(hijo)
        if pos == 0:
            return self.padre.unidad_entrante()
        else:
            return self.hijos[pos-1].unidad_salida()
        
    def unidad_saliente(self, hijo: InterfazTopologia)-> str:
        pos = self.hijos.index(hijo)
        if pos == len(self.hijos) - 1:
            return self.padre.unidad_saliente()
        else:
            return self.hijos[pos+1].unidad_entrada()


    def unidad_entrada(self):
        if len(self.hijos) == 0:
            return self.padre.unidad_saliente()
        return self.hijos[0].unidad_entrada()
    
    def unidad_salida(self):
        if len(self.hijos) == 0:
            return self.padre.unidad_entrante()
        return self.hijos[-1].unidad_salida()
    
    def to_json(self):
        return {
            "tipo": "serie",
            "hijos": [hijo.to_json() for hijo in self.hijos]
        }
    
    def from_json(self, json):
        self.hijos = []
        for hijo in json['hijos']:
            if hijo['tipo'] == 'paralelo':
                self.hijos.append(TopologiaParalelo(from_json=hijo,padre=self))
            elif hijo['tipo'] == 'hoja':
                self.hijos.append(Hoja(from_json=hijo,padre=self))
            elif hijo['tipo'] == 'perturbacion':
                self.hijos.append(Perturbacion(from_json=hijo,padre=self))
        return self


    


    

class TopologiaParalelo(InterfazTopologia):
    
    
    def __init__(self,microbloqueNuevo=None,microbloque2:Hoja=None,serie:TopologiaSerie=None,arriba=True,padre:TopologiaSerie=None,from_json=None):
        if from_json:
            self.from_json(from_json)
            self.padre = padre
            return
        nuevaSerie = TopologiaSerie(micro=microbloqueNuevo,padre=self)
        if(serie):  nuevo = serie
        if(microbloque2): nuevo = TopologiaSerie(micro=microbloque2,padre=self)
        nuevo.cambiar_padre(self)
        if(arriba): self.hijos = [nuevaSerie,nuevo]
        else: self.hijos :list[InterfazTopologia] = [nuevo,nuevaSerie]
        super().__init__(padre)
    
    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:Hoja):
        self.padre.agregar_antes_de(microbloque,self)

    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:Hoja):
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
    
    def simular(self, tiempo, entrada=None):

        # Simula todos los hijos con la misma entrada
        salidas = [hijo.simular(tiempo, entrada) for hijo in self.hijos]
        # Suma las salidas de todos los hijos
        salida =  sum(salidas)
        
        return salida
    
    
    def validar_entrada(self, unidad) -> bool:
        return self.padre.validar_entrada(self, unidad)
    
    def validar_salida(self, unidad) -> bool:
        return self.padre.validar_salida(self, unidad)
    
    def unidad_entrada(self)-> str:
        return self.hijos[0].unidad_entrada()

    def unidad_salida(self)-> str:
        return self.hijos[-1].unidad_salida()
    
    def unidad_entrante(self)-> str:
        return self.padre.unidad_entrante(self)
    
    def unidad_saliente(self)-> str:
        return self.padre.unidad_saliente(self)
    
    def to_json(self):
        return {
            "tipo": "paralelo",
            "hijos": [hijo.to_json() for hijo in self.hijos]
        }
    
    def from_json(self, json):
        self.hijos = []
        for hijo in json['hijos']:
            self.hijos.append(TopologiaSerie(from_json=hijo,padre=self))
        return self