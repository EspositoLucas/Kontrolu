import sympy as sp
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo
from back.topologia.microbloque import MicroBloque
from back.topologia.perturbacion import Perturbacion
from back.topologia.hoja import Hoja
from latex2sympy2 import latex2sympy
from tbcontrol.symbolic import routh
import numpy as np
import math

class Estabilidad:
    def __init__(self, sesion):
        self.sesion = sesion

    def obtener_funcion_transferencia(self):
        ft_controlador = self.calcular_ft_macrobloque(self.sesion.controlador)
        ft_actuador = self.calcular_ft_macrobloque(self.sesion.actuador)
        ft_proceso = self.calcular_ft_macrobloque(self.sesion.proceso)
        ft_medidor = self.calcular_ft_macrobloque(self.sesion.medidor)

        # Calcula la función de transferencia de lazo directo considerando las perturbaciones
        ft_lazo_directo = self.calcular_ft_con_perturbaciones_lazo_directo(ft_controlador * ft_actuador * ft_proceso)
        ft_retroalimentacion = self.calcular_ft_con_perturbaciones_retroalimentacion(ft_medidor)

        ft_global = ft_lazo_directo / (1 + (ft_lazo_directo * ft_retroalimentacion))

        ft_global_simplificada = sp.simplify(ft_global)
        return sp.latex(ft_global_simplificada)
    
    def calcular_ft_con_perturbaciones_lazo_directo(self, ft_base):
        ft_total = ft_base
        for macrobloque in [self.sesion.controlador, self.sesion.actuador, self.sesion.proceso]:
            ft_total += self.obtener_perturbaciones(macrobloque)
        return ft_total
    
    def calcular_ft_con_perturbaciones_retroalimentacion(self, ft_base):
        ft_total = ft_base
        for macrobloque in [self.sesion.medidor]:
            ft_total += self.obtener_perturbaciones(macrobloque)
        return ft_total

    def obtener_perturbaciones(self, macrobloque):
        ft_perturbaciones = 0
        for elemento in macrobloque.topologia.obtener_micros():
            if isinstance(elemento, Perturbacion):
                ft_perturbaciones += self.parse_latex_to_sympy(elemento.funcion_transferencia)
        return ft_perturbaciones

    def calcular_ft_macrobloque(self, macrobloque):
        return self.calcular_ft_topologia(macrobloque.topologia)
        
    def calcular_ft_topologia(self, topologia):
        if isinstance(topologia, TopologiaSerie):
            return self.calcular_ft_serie(topologia)
        elif isinstance(topologia, TopologiaParalelo):
            return self.calcular_ft_paralelo(topologia)
        elif isinstance(topologia, MicroBloque):
            return self.parse_latex_to_sympy(topologia.funcion_transferencia)
        elif isinstance(topologia, Hoja):
            if isinstance(topologia, Perturbacion):
                return 0  # Las perturbaciones se manejan por separado
            return self.parse_latex_to_sympy(topologia.funcion_transferencia)
        else:
            raise ValueError(f"Tipo de topología no reconocido: {type(topologia)}")

    def calcular_ft_serie(self, serie):
        ft = 1
        for hijo in serie.hijos:
            if not isinstance(hijo, Perturbacion):
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

    def get_expr(self, raw_expr: str) -> sp.Expr:
        """
        Convert string to SymPy expression.
        """
        return sp.simplify(sp.parse_expr(raw_expr))

    def calcular_estabilidad(self):
        G_cl_latex = self.obtener_funcion_transferencia()
        G_cl = self.parse_latex_to_sympy(G_cl_latex)
        
        s = sp.Symbol('s')
        den = sp.fraction(G_cl)[1]
        coeficientes = sp.Poly(den, s).all_coeffs()
        
        # Manejar el caso de función de transferencia constante
        if len(coeficientes) == 1:
            es_estable = sp.sympify(coeficientes[0]).is_positive
            return [[coeficientes[0]]], es_estable

        coeficientes_str = list(map(str, coeficientes))
        grado = len(coeficientes_str) - 1
        filas = grado + 1
        columnas = math.ceil((grado + 1) / 2)
        matriz_routh = np.full((filas, columnas), self.get_expr('0'), dtype=object)
        
        # Rellenar la primera y segunda fila de la matriz de Routh
        for i in range(0, columnas):
            if 2 * i <= grado:
                matriz_routh[0, i] = self.get_expr(coeficientes_str[2 * i])
            if 2 * i + 1 <= grado:
                matriz_routh[1, i] = self.get_expr(coeficientes_str[2 * i + 1])
        
        # Calcular las filas restantes de la matriz de Routh
        for fila in range(2, filas):
            for columna in range(columnas - 1):
                a = matriz_routh[fila - 1, 0]
                b = matriz_routh[fila - 2, columna + 1]
                c = matriz_routh[fila - 2, 0]
                d = matriz_routh[fila - 1, columna + 1]

                # Verificar si hay una fila completa de ceros y tratar el caso especial
                if all(matriz_routh[fila - 1, j] == self.get_expr('0') for j in range(columnas)):
                    # Rellenar fila con derivada de los coeficientes anteriores
                    for k in range(columnas):
                        matriz_routh[fila, k] = self.get_expr(str((grado - fila + 1 - 2 * k) * sp.sympify(coeficientes_str[k])))
                    break
                else:
                    matriz_routh[fila, columna] = sp.simplify((b * a - c * d) / a if a != 0 else self.get_expr('0'))
        
        # Verificar si todos los elementos de la primera columna son positivos
        es_estable = all(sp.sympify(element).is_positive for element in matriz_routh[:, 0])

        return matriz_routh, es_estable
    
    def calcular_routh_con_libreria(self):
        den_poly = self.polinomio_caracteristico()
        coeficientes = den_poly.all_coeffs()

        if len(coeficientes) == 1:
            es_estable = sp.sympify(coeficientes[0]).is_positive
            if es_estable:
                es_estable = "ESTABLE"
            else:
                es_estable = "INESTABLE"
            return sp.Matrix([[coeficientes[0]]]), es_estable

        matriz_routh = routh(den_poly)
        
        primera_columna = [matriz_routh[i, 0] for i in range(matriz_routh.rows)]
        
        if all(valor > 0 for valor in primera_columna):
            estabilidad = "ESTABLE"
        elif any(valor == 0 for valor in primera_columna):
            estabilidad = "CRITICAMENTE_ESTABLE"
        elif any(valor < 0 for valor in primera_columna):
            estabilidad = "INESTABLE"
        else:
            estabilidad = "No se puede determinar la estabilidad"

        return matriz_routh, estabilidad

    def polinomio_caracteristico(self):
        G_cl_latex = self.obtener_funcion_transferencia()
        G_cl = self.parse_latex_to_sympy(G_cl_latex)
        s = sp.Symbol('s')
        den = sp.fraction(G_cl)[1]
        den_poly = sp.Poly(den, s)
        return den_poly

    def calcular_polos_y_ceros(self):
        G_cl_latex = self.obtener_funcion_transferencia()
        G_cl = self.parse_latex_to_sympy(G_cl_latex)
        s = sp.Symbol('s')
        
        num, den = sp.fraction(G_cl)
        
        den_poly = sp.Poly(den, s)
        polos = sp.roots(den_poly)
        
        num_poly = sp.Poly(num, s)
        ceros = sp.roots(num_poly)
        
        return polos, ceros

    def calcular_error_estado_estable(self):
        """
        Calcula el error en estado estable basándose en la entrada configurada
        usando el teorema del valor final.
        """
        s = sp.Symbol('s')
        G_ol = self.parse_latex_to_sympy(self.obtener_funcion_transferencia_lazo_abierto())
        
        # Obtenemos la entrada del sistema
        entrada_ft = self.parse_latex_to_sympy(self.sesion.entrada.funcion_transferencia)
        
        # Calculamos el error usando la fórmula E(s) = θi(s)[1/(1+G₀(s))]
        error_funcion = entrada_ft * (1 / (1 + G_ol))
        
        # Aplicamos el teorema del valor final: e_ss = lim[s->0] s·E(s)
        error_estado_estable = sp.limit(s * error_funcion, s, 0)
        
        return sp.simplify(error_estado_estable)

    def obtener_funcion_transferencia_lazo_abierto(self):
        ft_controlador = self.calcular_ft_macrobloque(self.sesion.controlador)
        ft_actuador = self.calcular_ft_macrobloque(self.sesion.actuador)
        ft_proceso = self.calcular_ft_macrobloque(self.sesion.proceso)
        ft_medidor = self.calcular_ft_macrobloque(self.sesion.medidor)

        ft_lazo_abierto = ft_controlador * ft_actuador * ft_proceso * ft_medidor

        ft_lazo_abierto_simplificada = sp.simplify(ft_lazo_abierto)
        return sp.latex(ft_lazo_abierto_simplificada)