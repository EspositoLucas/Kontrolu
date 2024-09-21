from latex2sympy2 import latex2sympy
from sympy import  inverse_laplace_transform, symbols,laplace_transform
from back.topologia.interfaz_topologia import InterfazTopologia

class Perturbacion(InterfazTopologia):

    def __init__(self,responsable=None,ft="0",ciclos=0,estado=False):
        super().__init__()
        self.responsable = responsable
        self.funcion_transferencia = ft
        self.ciclos = ciclos
        self.estado = estado
        self.datos = {'tiempo': [], 'valor_original': [], 'perturbacion': [], 'resultado': []}
    
    def matar(self):
        self.ciclos = 0
    
    def alterar(self,entrada,tiempo):
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
