from latex2sympy2 import latex2sympy
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from .interfaz_topologia import InterfazTopologia

class Perturbacion(InterfazTopologia):

    def __init__(self,funcion_transferencia:str="1",ciclos=0,estado=False):
        self.funcion_transferencia = funcion_transferencia
        self.ciclos = ciclos
        self.estado = estado
        self.datos = {'tiempo': [], 'valor_original': [], 'perturbacion': [], 'resultado': []}
    
    
    def simular(self,entrada,tiempo):
        
        if not self.estado: return entrada

        s,t = symbols('s t')

        self.ciclos -= 1
        
        if self.ciclos <= 0: self.estado = False

        perturbacion_laplace = latex2sympy(self.funcion_transferencia)

        perturbacion_tiempo = inverse_laplace_transform(perturbacion_laplace,s,t)

        perturbado = perturbacion_tiempo.subs(t,tiempo)



        nuevo_valor = perturbado + entrada

        self.datos['tiempo'].append(tiempo)
        self.datos['valor_original'].append(entrada)
        self.datos['perturbacion'].append(perturbado)
        self.datos['resultado'].append(nuevo_valor)

        return nuevo_valor
    
    def activa(self):
        return self.estado

    def generar_perturbacion(self,ft,ciclos):
        self.funcion_transferencia = ft
        self.ciclos = ciclos
        self.estado = True
    
    def cancelar_perturbacion(self):
        self.estado = False
        self.ciclos = 0
        self.funcion_transferencia = "0"
    
    def radio(self) -> int:
        return 20

    def borrar_elemento(self):
        self.padre.borrar_elemento(self)
        self.padre = None


    def agregar_antes(self,microbloque:MicroBloque|Perturbacion):
        self.padre.agregar_antes_de(microbloque,self)
    
    def agregar_despues(self,microbloque:MicroBloque|Perturbacion):
        self.padre.agregar_despues_de(microbloque,self)
    
    def obtener_micros(self):
        return [self]
    
    def set_funcion_transferencia(self, funcion):
        self.funcion_transferencia = funcion

    def agregar_en_serie_fuera_de_paralela_antes(self,microbloque:MicroBloque|Perturbacion):
        self.padre.agregar_en_serie_fuera_de_paralela_antes(microbloque)
        
    def agregar_en_serie_fuera_de_paralela_despues(self,microbloque:MicroBloque|Perturbacion):
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
    
    
    def validar_entrada(self):
        return self.padre.validar_entrada(self,self.unidad_entrada())
    
    def validar_salida(self):
        return self.padre.validar_salida(self,self.unidad_salida())

    def unidad_entrada(self):
        return self.padre.unidad_entrante(self)
    
    def unidad_salida(self):
        return self.padre.unidad_saliente(self)

    