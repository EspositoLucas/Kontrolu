# import numpy as np
# import control
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from sympy import sympify, Symbol, expand, Poly
# from sympy.parsing.latex import parse_latex
# from back.topologia.topologia_serie import *

# class Simulacion:
#     def __init__(self, controlador, actuador, proceso, medidor):
#         self.controlador = controlador
#         self.actuador = actuador
#         self.proceso = proceso
#         self.medidor = medidor
#         self.sistema = None
#         self.fig, self.ax = plt.subplots()
#         self.line, = self.ax.plot([], [])
#         self.setup_plot()

#     def setup_plot(self):
#         self.ax.set_xlim(0, 10)  # Ajusta según tus necesidades
#         self.ax.set_ylim(0, 2)   # Ajusta según tus necesidades
#         self.ax.set_xlabel('Tiempo')
#         self.ax.set_ylabel('Salida')
#         self.ax.set_title('Respuesta del sistema en tiempo real')
#         self.ax.grid(True)

#     @staticmethod
#     def latex_to_tf(latex_expr):
#         expr = parse_latex(latex_expr) # captura el latex y lo procesa
#         s = Symbol('s') # define la variable matematica principal a tener en cuenta
#         num, den = expr.as_numer_denom() # separa numerador y denominador
#         print("numerador: ", num, type(num))
#         print("denominador: ", den, type(den))
#         num_expanded = expand(num) # la funcion "expand" resuelve la expresión (por ejemplo: si tiene 2*(s+1), lo que hace es devolver: 2s+2)
#         den_expanded = expand(den) # lo mismo hace para denominador
#         print("numerador expandido: ", num_expanded, type(num_expanded))
#         print("denominador expandido: ", den_expanded, type(den_expanded))
        
#         def get_coeffs(expr):
#             if expr.is_constant():
#                 return [float(expr)]
#             else:
#                 """
#                 Lo de abajo hace lo siguiente:
#                 1) calcula el grado del polinomio (ya sea num_exapnded (numerador) o  den_expanded (denominador)) --> esto lo hace con variable.degree y le pasa la variable principal del polinomio
#                 2) luego itera tantas veces sea ese grado del polinomio y va armando una lista de float(variable.coeff(s,i))
#                 3) esto significa lo siguiente: calcula el float del coeficiente que acompaña a la variable "s" en el grado "i"
#                 por ejemplo: si tengo el polinomio 5 * s^2 - s + 2 * s^2 - 7 y hago pol.coeff(s, 2), esto me devuelve 7 (porque, para el grado 2 y la variable "s", el coeficiente que la acompaña es 5 + 2 = 7)
#                 4) [::-1] --> esto en Python invierte la lista --> esto lo hace para que adelante queden los coeficientes asociados al mayor grado (exponente)
#                 """
#                 degree = Poly(expr, s).degree()
#                 return [float(expr.coeff(s, i)) for i in range(degree + 1)][::-1]
        
#         num_coeffs = get_coeffs(num_expanded)
#         den_coeffs = get_coeffs(den_expanded)
#         return control.tf(num_coeffs, den_coeffs)

#     @staticmethod
#     def crear_funcion_transferencia(latex_expr):
#         return Simulacion.latex_to_tf(latex_expr)

#     @staticmethod
#     def combinar_serie(tf1, tf2):
#         return tf1 * tf2

#     @staticmethod
#     def combinar_paralelo(tf1, tf2):
#         return tf1 + tf2

#     def procesar_topologia(self, topologia):
#         # Convierte la topología en una función de transferencia
#         if topologia is None:
#             return control.tf(1, 1)  # Retorna una función de transferencia unitaria si la topología es None
        
#         # Procesa diferentes tipos de topologías (MicroBloque, TopologiaSerie, TopologiaParalelo)
        
#         if isinstance(topologia, MicroBloque):
#             return self.crear_funcion_transferencia(topologia.funcion_transferencia)
#         elif isinstance(topologia, TopologiaSerie):
#             tf_total = control.tf(1, 1)  # Función de transferencia unitaria
#             for hijo in topologia.hijos:
#                 tf_hijo = self.procesar_topologia(hijo)
#                 if tf_hijo is not None:
#                     tf_total = self.combinar_serie(tf_total, tf_hijo)
#             return tf_total
#         elif isinstance(topologia, TopologiaParalelo):
#             tf_total = control.tf(0, 1)  # Función de transferencia cero
#             for hijo in topologia.hijos:
#                 tf_hijo = self.procesar_topologia(hijo)
#                 if tf_hijo is not None:
#                     tf_total = self.combinar_paralelo(tf_total, tf_hijo)
#             return tf_total
#         else:
#             print(f"Tipo de topología desconocido: {type(topologia)}")
#             return control.tf(1, 1) 
        
    
#     def preparar_sistema(self):
#         # Procesa cada componente del sistema
#         tf_controlador = self.procesar_topologia(self.controlador.topologia)
#         tf_actuador = self.procesar_topologia(self.actuador.topologia)
#         tf_proceso = self.procesar_topologia(self.proceso.topologia)
#         tf_medidor = self.procesar_topologia(self.medidor.topologia)
        
#         # Imprime las funciones de transferencia para depuración
#         print(f"TF Controlador: {tf_controlador}")
#         print(f"TF Actuador: {tf_actuador}")
#         print(f"TF Proceso: {tf_proceso}")
#         print(f"TF Medidor: {tf_medidor}")
        
#         # Combina las funciones de transferencia para crear el sistema completo
#         tf_directa = tf_controlador * tf_actuador * tf_proceso
#         """
#         G: funcion de transferencia del lazo directo
#         H: funcion de transferencia del lazo de realimentacion
#         La funcion feedback usa esta fórmula que estudiamos en clase: G / (1 + G * H)
#         self.sistema = G / (1 + G * H)
#         """
#         self.sistema = control.feedback(tf_directa, tf_medidor)
#         print(f"Sistema completo: {self.sistema}")
        
#     def simular_paso(self, t, dt, u, x0):
#         result = control.forced_response(self.sistema, T=[t, t+dt], U=[u, u], X0=x0)
        
#         if len(result) == 3:
#             y, _, x = result
#             return y[-1], x
#         elif len(result) == 2:
#             y, _ = result
#             # En este caso, no tenemos acceso directo al nuevo estado x
#             # Podemos intentar estimarlo o simplemente devolver el x0 original
#             return y[-1], x0
#         else:
#             raise ValueError(f"forced_response devolvió un número inesperado de valores: {len(result)}")

#     def simular_sistema_tiempo_real(self, entrada, t_total, dt, setpoint):
#         if self.sistema is None:
#             self.preparar_sistema()
        
#         if self.sistema is None:
#             print("Error: No se pudo preparar el sistema")
#             return
        
#         # Genera el vector de tiempo
#         t = np.arange(0, t_total, dt)
        
#         # Inicializa los arrays para almacenar los resultados
#         y = np.zeros_like(t)
#         u = np.zeros_like(t)
        
#         # Condiciones iniciales
#         x0 = np.zeros(self.sistema.nstates) # asume que el sistema comienza en el origen

#         # Simula paso a paso
#         for i, ti in enumerate(t):
#             # Calcula la entrada en este paso
#             if callable(entrada):
#                 u[i] = entrada(ti) * setpoint
#             else:
#                 u[i] = entrada * setpoint
#             """
#             # Calcula el error
#             error = setpoint - (y[i-1] if i > 0 else 0)
            
#             # Calcula la entrada usando un controlador (por ejemplo, un PID simple)
#             u[i] = self.calcular_control(error, dt)
            
#             # Simula un paso
#             y[i], x0 = self.simular_paso(ti, dt, u[i], x0)
#             """
#             # Simula un paso
#             y[i], x0 = self.simular_paso(ti, dt, u[i], x0)
#             print(f"paso numero {i}: salida: {y[i]}, {x0}")
        
#         self.ax.clear()
#         self.ax.plot(t, y, label='Salida')
#         self.ax.plot(t, u, label='Entrada')
#         self.ax.plot(t, [setpoint]*len(t), '--', label='Setpoint')
#         self.ax.set_xlabel('Tiempo')
#         self.ax.set_ylabel('Amplitud')
#         self.ax.set_title('Respuesta del sistema')
#         self.ax.legend()
#         self.ax.grid(True)
#         plt.show()
        
#     def init_animation(self):
#         self.line.set_data([], [])
#         return self.line,

#     def update_animation(self, frame):
#         t, y = frame
#         self.line.set_data(t, y)
#         self.ax.relim()
#         self.ax.autoscale_view()
#         return self.line,

#     def ejecutar_simulacion(self, entrada, t_total=10, dt=0.01, interval=50):
#         anim = FuncAnimation(self.fig, self.update_animation,
#                              frames=self.simular_sistema_tiempo_real(entrada, t_total, dt),
#                              init_func=self.init_animation, blit=True, interval=interval)
#         plt.show()



import numpy as np
import control
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import sympify, Symbol, expand, Poly
from sympy.parsing.latex import parse_latex
from back.topologia.topologia_serie import *

class Simulacion:
    def __init__(self, controlador, actuador, proceso, medidor):
        self.controlador = controlador
        self.actuador = actuador
        self.proceso = proceso
        self.medidor = medidor
        self.sistema = None
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        self.setup_plot()

    def setup_plot(self):
        self.ax.set_xlim(0, 10)  # Ajusta según tus necesidades
        self.ax.set_ylim(0, 2)   # Ajusta según tus necesidades
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Salida')
        self.ax.set_title('Respuesta del sistema en tiempo real')
        self.ax.grid(True)

    @staticmethod
    def latex_to_tf(latex_expr):
        expr = parse_latex(latex_expr) # captura el latex y lo procesa
        s = Symbol('s') # define la variable matematica principal a tener en cuenta
        num, den = expr.as_numer_denom() # separa numerador y denominador
        print("numerador: ", num, type(num))
        print("denominador: ", den, type(den))
        num_expanded = expand(num) # la funcion "expand" resuelve la expresión (por ejemplo: si tiene 2*(s+1), lo que hace es devolver: 2s+2)
        den_expanded = expand(den) # lo mismo hace para denominador
        print("numerador expandido: ", num_expanded, type(num_expanded))
        print("denominador expandido: ", den_expanded, type(den_expanded))
        
        def get_coeffs(expr):
            if expr.is_constant():
                return [float(expr)]
            else:
                """
                Lo de abajo hace lo siguiente:
                1) calcula el grado del polinomio (ya sea num_exapnded (numerador) o  den_expanded (denominador)) --> esto lo hace con variable.degree y le pasa la variable principal del polinomio
                2) luego itera tantas veces sea ese grado del polinomio y va armando una lista de float(variable.coeff(s,i))
                3) esto significa lo siguiente: calcula el float del coeficiente que acompaña a la variable "s" en el grado "i"
                por ejemplo: si tengo el polinomio 5 * s^2 - s + 2 * s^2 - 7 y hago pol.coeff(s, 2), esto me devuelve 7 (porque, para el grado 2 y la variable "s", el coeficiente que la acompaña es 5 + 2 = 7)
                4) [::-1] --> esto en Python invierte la lista --> esto lo hace para que adelante queden los coeficientes asociados al mayor grado (exponente)
                """
                degree = Poly(expr, s).degree()
                return [float(expr.coeff(s, i)) for i in range(degree + 1)][::-1]
        
        num_coeffs = get_coeffs(num_expanded)
        den_coeffs = get_coeffs(den_expanded)
        return control.tf(num_coeffs, den_coeffs)

    @staticmethod
    def crear_funcion_transferencia(latex_expr):
        return Simulacion.latex_to_tf(latex_expr)

    @staticmethod
    def combinar_serie(tf1, tf2):
        return tf1 * tf2

    @staticmethod
    def combinar_paralelo(tf1, tf2):
        return tf1 + tf2

    def procesar_topologia(self, topologia):
        # Convierte la topología en una función de transferencia
        if topologia is None:
            return control.tf(1, 1)  # Retorna una función de transferencia unitaria si la topología es None
        
        # Procesa diferentes tipos de topologías (MicroBloque, TopologiaSerie, TopologiaParalelo)
        
        if isinstance(topologia, MicroBloque):
            return self.crear_funcion_transferencia(topologia.funcion_transferencia)
        elif isinstance(topologia, TopologiaSerie):
            tf_total = control.tf(1, 1)  # Función de transferencia unitaria
            for hijo in topologia.hijos:
                tf_hijo = self.procesar_topologia(hijo)
                if tf_hijo is not None:
                    tf_total = self.combinar_serie(tf_total, tf_hijo)
            return tf_total
        elif isinstance(topologia, TopologiaParalelo):
            tf_total = control.tf(0, 1)  # Función de transferencia cero
            for hijo in topologia.hijos:
                tf_hijo = self.procesar_topologia(hijo)
                if tf_hijo is not None:
                    tf_total = self.combinar_paralelo(tf_total, tf_hijo)
            return tf_total
        else:
            print(f"Tipo de topología desconocido: {type(topologia)}")
            return control.tf(1, 1) 
        
    
    def preparar_sistema(self):
        # Procesa cada componente del sistema
        tf_controlador = self.procesar_topologia(self.controlador.topologia)
        tf_actuador = self.procesar_topologia(self.actuador.topologia)
        tf_proceso = self.procesar_topologia(self.proceso.topologia)
        tf_medidor = self.procesar_topologia(self.medidor.topologia)
        
        # Imprime las funciones de transferencia para depuración
        print(f"TF Controlador: {tf_controlador}")
        print(f"TF Actuador: {tf_actuador}")
        print(f"TF Proceso: {tf_proceso}")
        print(f"TF Medidor: {tf_medidor}")
        
        # Combina las funciones de transferencia para crear el sistema completo
        tf_directa = tf_controlador * tf_actuador * tf_proceso
        """
        G: funcion de transferencia del lazo directo
        H: funcion de transferencia del lazo de realimentacion
        La funcion feedback usa esta fórmula que estudiamos en clase: G / (1 + G * H)
        self.sistema = G / (1 + G * H)
        """
        self.sistema = control.feedback(tf_directa, tf_medidor)
        print(f"Sistema completo: {self.sistema}")
        
    def simular_paso(self, t, dt, u, x0):
        result = control.forced_response(self.sistema, T=[t, t+dt], U=[u, u], X0=x0)
        
        if len(result) == 3:
            y, _, x = result
            return y[-1], x
        elif len(result) == 2:
            y, _ = result
            # En este caso, no tenemos acceso directo al nuevo estado x
            # Podemos intentar estimarlo o simplemente devolver el x0 original
            return y[-1], x0
        else:
            raise ValueError(f"forced_response devolvió un número inesperado de valores: {len(result)}")

    def simular_sistema_tiempo_real(self, entrada, t_total, dt, setpoint):
        if self.sistema is None:
            self.preparar_sistema()
        
        t = np.arange(0, t_total, dt)
        
        if entrada == "impulso":
            u = np.zeros_like(t)
            u[0] = 1 / dt  # Aproximación del impulso
        elif callable(entrada):
            u = np.array([entrada(ti) for ti in t])
        else:
            u = np.full_like(t, entrada)
        
        # Manejo flexible de la respuesta de forced_response
        response = control.forced_response(self.sistema, T=t, U=u)
        
        if len(response) == 3:
            t_out, y, _ = response
        elif len(response) == 2:
            t_out, y = response
        else:
            raise ValueError(f"Unexpected number of return values from forced_response: {len(response)}")
        
        # Asegurarse de que t_out y t tienen la misma longitud
        if len(t_out) != len(t):
            # Interpolar y si es necesario
            y = np.interp(t, t_out, y)
        
        return t, y, u

        
    def init_animation(self):
        self.line.set_data([], [])
        return self.line,

    def update_animation(self, frame):
        t, y = frame
        self.line.set_data(t, y)
        self.ax.relim()
        self.ax.autoscale_view()
        return self.line,

    def ejecutar_simulacion(self, entrada, t_total, dt, setpoint, velocidad):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.line, = self.ax.plot([], [], 'b-', label='Salida')
        self.line_entrada, = self.ax.plot([], [], 'r-', label='Entrada')
        
        try:
            t, y, u = self.simular_sistema_tiempo_real(entrada, t_total, dt, setpoint)
        except Exception as e:
            print(f"Error durante la simulación: {e}")
            # Manejar el error apropiadamente, tal vez mostrando un mensaje al usuario
            return
        
        self.ax.set_xlim(0, t_total)
        self.ax.set_ylim(min(min(y), min(u)) * 0.9, max(max(y), max(u)) * 1.1)
        self.ax.set_xlabel('Tiempo (Segundos)')
        self.ax.set_ylabel('Amplitud')
        self.ax.set_title('Respuesta del Sistema')
        self.ax.legend()
        self.ax.grid(True)

        if velocidad == 'rapida':
            interval = 1
        elif velocidad == 'lenta':
            interval = 50
        else:
            interval = 10

        def update(frame):
            i = frame
            self.line.set_data(t[:i], y[:i])
            self.line_entrada.set_data(t[:i], u[:i])
            return self.line, self.line_entrada

        self.anim = FuncAnimation(self.fig, update, frames=len(t), interval=interval, blit=True)
        plt.show()
