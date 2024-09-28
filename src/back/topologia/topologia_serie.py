from __future__ import annotations
from back.topologia.interfaz_topologia import InterfazTopologia
from back.topologia.perturbacion import Perturbacion
from back.configuracion.configuracion_microbloque import ConfiguracionMicrobloque
from PyQt5.QtGui import QColor
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from latex2sympy2 import latex2sympy
from back.topologia.configuraciones import Configuracion

ANCHO = 150
ALTO = 80

class TopologiaSerie(InterfazTopologia):
    
    def __init__(self,micro: TopologiaParalelo | MicroBloque = None,lista_micros: list=None,padre: InterfazTopologia = None):
        self.hijos: list[InterfazTopologia] = []
        if micro:
            micro.cambiar_padre(self)
            self.hijos.append(micro)
        if lista_micros:
            for micro in lista_micros:
                micro.cambiar_padre(self)
            self.hijos.extend(lista_micros)
        super().__init__(padre)

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

    def agregar_perturbacion_antes(self, actual: MicroBloque, perturbacion: Perturbacion):
        indice = self.hijos.index(actual)
        perturbacion.cambiar_padre(self)
        self.hijos.insert(indice, perturbacion)

    def agregar_perturbacion_despues(self, actual: MicroBloque, perturbacion: Perturbacion):
        indice = self.hijos.index(actual)
        perturbacion.cambiar_padre(self)
        self.hijos.insert(indice + 1, perturbacion)

    def alto(self) -> int:
        return max(map(lambda x: x.alto(),self.hijos))
    
    def ancho(self) -> int:
        return sum(map(lambda x: x.ancho(),self.hijos))


    def __str__(self):
        return "SERIE: " + str(list(map(lambda hijo: str(hijo),self.hijos)))
    
    def simular(self, tiempo, entrada=None):

        entrada_perturbada = self.alterar_entrada(entrada,tiempo)

        for hijo in self.hijos:
                entrada_perturbada = self.simular(hijo, tiempo, entrada_perturbada)
        
        salida_perturbada = self.alterar_salida(entrada_perturbada,tiempo)

        return salida_perturbada
    
    def agregar_perturbacion_antes_de_paralela(self,ft,ciclos):
        self.padre.generar_perturbacion_entrada(ft,ciclos)

    def agregar_perturbacion_despues_de_paralela(self,ft,ciclos):
        self.padre.generar_perturbacion_salida(ft,ciclos)
    

class MicroBloque(InterfazTopologia):
    def __init__(self, nombre: str="Entrada", color: QColor=None, funcion_transferencia: str=None, configuracion: ConfiguracionMicrobloque=None, padre: TopologiaSerie=None,configuracion_entrada=Configuracion(),configuracion_salida=Configuracion()) -> None:
        self.nombre = nombre
        self.color = color
        self.funcion_transferencia = funcion_transferencia
        self.configuracion = configuracion
        self.configuracion_entrada = configuracion_entrada
        self.configuracion_salida = configuracion_salida
        super().__init__(padre)

    def agregar_configuracion(self, nombre, tipo, valor_por_defecto, efecto):
        self.configuracion.agregar_configuracion(nombre, tipo, valor_por_defecto, efecto)
    
    def set_configuracion(self, nombre, valor):
        self.configuracion.set_configuracion(nombre, valor)

    def get_configuraciones(self):
        return self.configuracion.get_configuraciones()
    
    def get_configuracion(self, nombre):
        return self.configuracion.get_configuracion(nombre)

    def actualizar_configuracion(self, old_name, new_name, new_type, new_value, new_efecto):
        self.configuracion.actualizar_configuracion(old_name, new_name, new_type, new_value, new_efecto)

    def aplicar_efecto(self):
        self.configuracion.aplicar_efecto(self.funcion_transferencia)

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
    
    def agregar_perturbacion_antes_de_paralela(self,ft,ciclos):
        self.padre.agregar_perturbacion_antes_de_paralela(ft,ciclos)

    def agregar_perturbacion_despues_de_paralela(self,ft,ciclos):
        self.padre.agregar_perturbacion_despues_de_paralela(ft,ciclos)


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
    
    def simular(self, tiempo, entrada=None):

        s,t = symbols('s t')

        tf_sympy = latex2sympy(self.funcion_transferencia)
        print(f"La función de transferencia es: {tf_sympy}")

        operacion_laplace = tf_sympy

        if entrada:
            entrada_perturbada = self.alterar_entrada(entrada,tiempo)

            entrada_con_error = self.configuracion_entrada.actualizar(entrada_perturbada,tiempo)

            entrada_micro_bloque = laplace_transform(entrada_con_error,t,s)[0]
            print(f"La entrada es: {entrada_micro_bloque}")
            operacion_laplace = entrada_micro_bloque * tf_sympy
            print(f"La operación de Laplace es: {operacion_laplace}")
        
        operacion_tiempo = inverse_laplace_transform(operacion_laplace,s,t)
        print(f"La operación en tiempo es: {operacion_tiempo}")
        salida_micro_bloque = operacion_tiempo.subs(t,tiempo)
        print(f"La salida en tiempo es: {salida_micro_bloque}")

        salida_con_error = self.configuracion_salida.actualizar(salida_micro_bloque,tiempo)

        salida_perturbada = self.alterar_salida(salida_con_error,tiempo)

        return salida_perturbada
    

    




class TopologiaParalelo(InterfazTopologia):
    
    
    def __init__(self,microbloqueNuevo,microbloque2:MicroBloque=None,serie:TopologiaSerie=None,arriba=True,padre:TopologiaSerie=None):
        nuevaSerie = TopologiaSerie(micro=microbloqueNuevo,padre=self)
        if(serie):  nuevo = serie
        if(microbloque2): nuevo = TopologiaSerie(micro=microbloque2,padre=self)
        nuevo.cambiar_padre(self)
        if(arriba): self.hijos = [nuevaSerie,nuevo]
        else: self.hijos = [nuevo,nuevaSerie]
        super().__init__(padre)
    
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
    
    def simular(self, tiempo, entrada=None):

        self.alterar_entrada(entrada,tiempo)
        # Simula todos los hijos con la misma entrada
        salidas = [self.simular(hijo, tiempo, entrada) for hijo in self.hijos]
        # Suma las salidas de todos los hijos
        salida =  sum(salidas)

        salida_perturbada = self.alterar_salida(salida,tiempo)
        
        return salida_perturbada
    
    def agregar_perturbacion_antes_de_paralela(self,ft,ciclos):
        self.padre.agregar_perturbacion_antes_de_paralela(ft,ciclos)

    def agregar_perturbacion_despues_de_paralela(self,ft,ciclos):
        self.padre.agregar_perturbacion_despues_de_paralela(ft,ciclos)
    
    