import sympy as sp

class FuncionTransferencia:
    def __init__(self, numerador, denominador=None):
        # Definimos 's' como un símbolo para usar en las expresiones
        self.s = sp.Symbol('s')
        
        if denominador is None:
            # Si solo se proporciona un argumento, asumimos que es la función completa
            try:
                # Intentamos convertir la cadena de entrada en una expresión simbólica
                self.funcion = sp.sympify(numerador)
                # Separamos la función en numerador y denominador
                self.numerador, self.denominador = self.funcion.as_numer_denom()
            except:
                # Si hay un error al procesar la función, lanzamos una excepción
                raise ValueError("Función de transferencia inválida")
        else:
            # Si se proporcionan numerador y denominador por separado
            self.numerador = sp.sympify(numerador)
            self.denominador = sp.sympify(denominador)
            self.funcion = self.numerador / self.denominador

    def validar(self):
        # Verificar que el denominador no sea cero
        if self.denominador == 0:
            return False
        # Verificar que el grado del numerador no sea mayor que el del denominador
        if sp.degree(self.numerador, self.s) > sp.degree(self.denominador, self.s):
            return False
        return True

    def to_latex(self):
        # Convertir la función de transferencia a formato LaTeX
        return sp.latex(self.funcion)

    def multiplicar(self, otra_funcion):
        nuevo_numerador = self.numerador * otra_funcion.numerador
        nuevo_denominador = self.denominador * otra_funcion.denominador
        return FuncionTransferencia(nuevo_numerador, nuevo_denominador)

    def sumar(self, otra_funcion):
        nuevo_numerador = (self.numerador * otra_funcion.denominador + 
                           otra_funcion.numerador * self.denominador)
        nuevo_denominador = self.denominador * otra_funcion.denominador
        return FuncionTransferencia(nuevo_numerador, nuevo_denominador)

    def multiplicar_constante(self, constante):
        nuevo_numerador = self.numerador * constante
        return FuncionTransferencia(nuevo_numerador, self.denominador)
