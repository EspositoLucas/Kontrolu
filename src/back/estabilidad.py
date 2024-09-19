# import numpy as np
# import sympy as sp
# from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque
# from latex2sympy2 import latex2sympy

# class Estabilidad:
#     def __init__(self, sesion):
#         self.sesion = sesion

#     def obtener_funcion_transferencia(self):
#         ft_controlador = self.calcular_ft_macrobloque(self.sesion.controlador)
#         ft_actuador = self.calcular_ft_macrobloque(self.sesion.actuador)
#         ft_proceso = self.calcular_ft_macrobloque(self.sesion.proceso)
#         ft_medidor = self.calcular_ft_macrobloque(self.sesion.medidor)

#         ft_lazo_directo = ft_controlador * ft_actuador * ft_proceso
#         ft_global = ft_lazo_directo / (1 + ft_lazo_directo * ft_medidor)

#         ft_global_simplificada = sp.simplify(ft_global)
#         # Convertir la expresión simbólica a LaTeX
#         return sp.latex(ft_global_simplificada)

#     def calcular_ft_macrobloque(self, macrobloque):
#         return self.calcular_ft_topologia(macrobloque.topologia)

#     def calcular_ft_topologia(self, topologia):
#         if isinstance(topologia, TopologiaSerie):
#             return self.calcular_ft_serie(topologia)
#         elif isinstance(topologia, TopologiaParalelo):
#             return self.calcular_ft_paralelo(topologia)
#         elif isinstance(topologia, MicroBloque):
#             return self.parse_latex_to_sympy(topologia.funcion_transferencia)
#         else:
#             raise ValueError(f"Tipo de topología no reconocido: {type(topologia)}")

#     def calcular_ft_serie(self, serie):
#         ft = 1
#         for hijo in serie.hijos:
#             ft *= self.calcular_ft_topologia(hijo)
#         return ft

#     def calcular_ft_paralelo(self, paralelo):
#         ft = 0
#         for hijo in paralelo.hijos:
#             ft += self.calcular_ft_topologia(hijo)
#         return ft

#     def parse_latex_to_sympy(self, latex_str):
#         try:
#             return latex2sympy(latex_str)
#         except Exception as e:
#             print(f"Error parsing LaTeX: {e}")
#             # As a fallback, try to create a simple fraction if the latex represents a basic fraction
#             if '\\frac' in latex_str:
#                 num, den = latex_str.split('}{')
#                 num = num.split('{')[1]
#                 den = den.split('}')[0]
#                 return sp.sympify(f"({num})/({den})")
#             else:
#                 # If it's not a fraction, return the string as a symbol
#                 return sp.Symbol(latex_str)

#     def calcular_estabilidad(self):
#         G_cl_latex = self.obtener_funcion_transferencia()
#         G_cl = self.parse_latex_to_sympy(G_cl_latex)
        
#         # Obtener el denominador de la función de transferencia
#         s = sp.Symbol('s')
#         den = sp.fraction(G_cl)[1]
#         print("el denominador es: ", den)
#         coeficientes = sp.Poly(den, s).all_coeffs()
        
#         # Implementar el criterio de Routh-Hurwitz
#         n = len(coeficientes) - 1
#         matriz_routh = [[0 for j in range((n+1)//2)] for i in range(n+1)]
        
#         # Llenar las dos primeras filas
#         for i in range(0, n+1, 2):
#             matriz_routh[0][i//2] = coeficientes[i]
#         for i in range(1, n+1, 2):
#             matriz_routh[1][i//2] = coeficientes[i]
        
#         # Calcular el resto de la matriz
#         for i in range(2, n+1):
#             for j in range((n+1)//2):
#                 if i-2 < len(matriz_routh) and j+1 < len(matriz_routh[i-2]):
#                     if matriz_routh[i-1][0] == 0:
#                         # Manejo de caso especial cuando el primer elemento de la fila anterior es cero
#                         epsilon = sp.Symbol('ε')
#                         matriz_routh[i-1][0] = epsilon
#                     matriz_routh[i][j] = (matriz_routh[i-1][0] * matriz_routh[i-2][j+1] - 
#                                           matriz_routh[i-2][0] * matriz_routh[i-1][j+1]) / matriz_routh[i-1][0]
#                 else:
#                     matriz_routh[i][j] = 0
        
#         return matriz_routh


import numpy as np
import sympy as sp
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque
from latex2sympy2 import latex2sympy

class Estabilidad:
    def __init__(self, sesion):
        self.sesion = sesion

    def obtener_funcion_transferencia(self):
        ft_controlador = self.calcular_ft_macrobloque(self.sesion.controlador)
        ft_actuador = self.calcular_ft_macrobloque(self.sesion.actuador)
        ft_proceso = self.calcular_ft_macrobloque(self.sesion.proceso)
        ft_medidor = self.calcular_ft_macrobloque(self.sesion.medidor)

        ft_lazo_directo = ft_controlador * ft_actuador * ft_proceso
        ft_global = ft_lazo_directo / (1 + ft_lazo_directo * ft_medidor)

        ft_global_simplificada = sp.simplify(ft_global)
        # Convertir la expresión simbólica a LaTeX
        return sp.latex(ft_global_simplificada)

    def calcular_ft_macrobloque(self, macrobloque):
        return self.calcular_ft_topologia(macrobloque.topologia)

    def calcular_ft_topologia(self, topologia):
        if isinstance(topologia, TopologiaSerie):
            return self.calcular_ft_serie(topologia)
        elif isinstance(topologia, TopologiaParalelo):
            return self.calcular_ft_paralelo(topologia)
        elif isinstance(topologia, MicroBloque):
            return self.parse_latex_to_sympy(topologia.funcion_transferencia)
        else:
            raise ValueError(f"Tipo de topología no reconocido: {type(topologia)}")

    def calcular_ft_serie(self, serie):
        ft = 1
        for hijo in serie.hijos:
            ft *= self.calcular_ft_topologia(hijo)
        return ft

    def calcular_ft_paralelo(self, paralelo):
        ft = 0
        for hijo in paralelo.hijos:
            ft += self.calcular_ft_topologia(hijo)
        return ft

    def parse_latex_to_sympy(self, latex_str):
        try:
            return latex2sympy(latex_str)
        except Exception as e:
            print(f"Error parsing LaTeX: {e}")
            # As a fallback, try to create a simple fraction if the latex represents a basic fraction
            if '\\frac' in latex_str:
                num, den = latex_str.split('}{')
                num = num.split('{')[1]
                den = den.split('}')[0]
                return sp.sympify(f"({num})/({den})")
            else:
                # If it's not a fraction, return the string as a symbol
                return sp.Symbol(latex_str)

    import numpy as np
import sympy as sp
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque
from latex2sympy2 import latex2sympy

class Estabilidad:
    def __init__(self, sesion):
        self.sesion = sesion

    def obtener_funcion_transferencia(self):
        ft_controlador = self.calcular_ft_macrobloque(self.sesion.controlador)
        ft_actuador = self.calcular_ft_macrobloque(self.sesion.actuador)
        ft_proceso = self.calcular_ft_macrobloque(self.sesion.proceso)
        ft_medidor = self.calcular_ft_macrobloque(self.sesion.medidor)

        ft_lazo_directo = ft_controlador * ft_actuador * ft_proceso
        ft_global = ft_lazo_directo / (1 + ft_lazo_directo * ft_medidor)

        ft_global_simplificada = sp.simplify(ft_global)
        # Convertir la expresión simbólica a LaTeX
        return sp.latex(ft_global_simplificada)

    def calcular_ft_macrobloque(self, macrobloque):
        return self.calcular_ft_topologia(macrobloque.topologia)

    def calcular_ft_topologia(self, topologia):
        if isinstance(topologia, TopologiaSerie):
            return self.calcular_ft_serie(topologia)
        elif isinstance(topologia, TopologiaParalelo):
            return self.calcular_ft_paralelo(topologia)
        elif isinstance(topologia, MicroBloque):
            return self.parse_latex_to_sympy(topologia.funcion_transferencia)
        else:
            raise ValueError(f"Tipo de topología no reconocido: {type(topologia)}")

    def calcular_ft_serie(self, serie):
        ft = 1
        for hijo in serie.hijos:
            ft *= self.calcular_ft_topologia(hijo)
        return ft

    def calcular_ft_paralelo(self, paralelo):
        ft = 0
        for hijo in paralelo.hijos:
            ft += self.calcular_ft_topologia(hijo)
        return ft

    def parse_latex_to_sympy(self, latex_str):
        try:
            return latex2sympy(latex_str)
        except Exception as e:
            print(f"Error parsing LaTeX: {e}")
            # As a fallback, try to create a simple fraction if the latex represents a basic fraction
            if '\\frac' in latex_str:
                num, den = latex_str.split('}{')
                num = num.split('{')[1]
                den = den.split('}')[0]
                return sp.sympify(f"({num})/({den})")
            else:
                # If it's not a fraction, return the string as a symbol
                return sp.Symbol(latex_str)

    def calcular_estabilidad(self):
        G_cl_latex = self.obtener_funcion_transferencia()
        G_cl = self.parse_latex_to_sympy(G_cl_latex)
        
        s = sp.Symbol('s')
        den = sp.fraction(G_cl)[1]
        print("el denominador es: ", den)
        coeficientes = sp.Poly(den, s).all_coeffs()
        
        n = len(coeficientes) - 1
        matriz_routh = [[0 for j in range(2)] for i in range(n+1)]
        
        for i in range(n+1):
            if i < len(coeficientes):
                matriz_routh[i][0] = coeficientes[i]
            if i+1 < len(coeficientes):
                matriz_routh[i][1] = coeficientes[i+1]
        
        for i in range(2, n+1):
            if matriz_routh[i-1][0] == 0:
                epsilon = sp.Symbol('ε')
                matriz_routh[i-1][0] = epsilon
            matriz_routh[i][0] = (matriz_routh[i-1][0] * matriz_routh[i-2][1] - 
                                  matriz_routh[i-2][0] * matriz_routh[i-1][1]) / matriz_routh[i-1][0]
            matriz_routh[i][1] = 0  # La segunda columna siempre será 0 para filas calculadas
        
        return matriz_routh

    def calcular_error_estado_estable(self, tipo_entrada):
        G_ol_latex = self.obtener_funcion_transferencia_lazo_abierto()
        G_ol = self.parse_latex_to_sympy(G_ol_latex)
        
        s = sp.Symbol('s')
        
        if tipo_entrada == "escalon":
            Kp = sp.limit(G_ol, s, 0)
            error = 1 / (1 + Kp)
        elif tipo_entrada == "rampa":
            Kv = sp.limit(s * G_ol, s, 0)
            error = 1 / Kv if Kv != 0 else sp.oo
        elif tipo_entrada == "parabola":
            Ka = sp.limit(s**2 * G_ol, s, 0)
            error = 1 / Ka if Ka != 0 else sp.oo
        else:
            raise ValueError("Tipo de entrada no válido")
        
        return error

    def obtener_funcion_transferencia_lazo_abierto(self):
        ft_controlador = self.calcular_ft_macrobloque(self.sesion.controlador)
        ft_actuador = self.calcular_ft_macrobloque(self.sesion.actuador)
        ft_proceso = self.calcular_ft_macrobloque(self.sesion.proceso)
        ft_medidor = self.calcular_ft_macrobloque(self.sesion.medidor)

        ft_lazo_abierto = ft_controlador * ft_actuador * ft_proceso * ft_medidor

        ft_lazo_abierto_simplificada = sp.simplify(ft_lazo_abierto)
        return sp.latex(ft_lazo_abierto_simplificada)