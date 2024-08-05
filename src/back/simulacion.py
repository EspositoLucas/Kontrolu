import numpy as np
import control
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import sympify, Symbol, expand
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
        expr = parse_latex(latex_expr)
        s = Symbol('s')
        num, den = expr.as_numer_denom()
        num_expanded = expand(num)
        den_expanded = expand(den)
        num_coeffs = [float(num_expanded.coeff(s, i)) for i in range(num_expanded.degree(s) + 1)][::-1]
        den_coeffs = [float(den_expanded.coeff(s, i)) for i in range(den_expanded.degree(s) + 1)][::-1]
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
        tf_controlador = self.procesar_topologia(self.controlador)
        tf_actuador = self.procesar_topologia(self.actuador)
        tf_proceso = self.procesar_topologia(self.proceso)
        tf_medidor = self.procesar_topologia(self.medidor)
        
        # Imprime las funciones de transferencia para depuración
        print(f"TF Controlador: {tf_controlador}")
        print(f"TF Actuador: {tf_actuador}")
        print(f"TF Proceso: {tf_proceso}")
        print(f"TF Medidor: {tf_medidor}")
        
        # Combina las funciones de transferencia para crear el sistema completo
        tf_directa = tf_controlador * tf_actuador * tf_proceso
        self.sistema = control.feedback(tf_directa, tf_medidor)
        print(f"Sistema completo: {self.sistema}")
        
    def simular_paso(self, t, dt, u, x0):
        y, _, x0 = control.forced_response(self.sistema, T=[t, t+dt], U=[u, u], X0=x0)
        return y[-1], x0

    def simular_sistema_tiempo_real(self, entrada, t_total, dt):
        if self.sistema is None:
            self.preparar_sistema()
        
        if self.sistema is None:
            print("Error: No se pudo preparar el sistema")
            return
        
        # Genera el vector de tiempo y la señal de entrada
        t = np.arange(0, t_total, dt)
        u = np.array([entrada(ti) for ti in t])
        
        # Simula la respuesta del sistema
        result = control.forced_response(self.sistema, T=t, U=u)
        
        # Maneja diferentes formatos de salida de forced_response
        if len(result) == 3:
            t, y, _ = result
        elif len(result) == 2:
            t, y = result
        else:
            print(f"Error: forced_response devolvió un número inesperado de valores: {len(result)}")
            return

        # Grafica los resultados
        self.ax.clear()
        self.ax.plot(t, y)
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Salida')
        self.ax.set_title('Respuesta del sistema')
        self.ax.grid(True)
        plt.show()
        
    def init_animation(self):
        self.line.set_data([], [])
        return self.line,

    def update_animation(self, frame):
        t, y = frame
        self.line.set_data(t, y)
        self.ax.relim()
        self.ax.autoscale_view()
        return self.line,

    def ejecutar_simulacion(self, entrada, t_total=10, dt=0.01, interval=50):
        anim = FuncAnimation(self.fig, self.update_animation,
                             frames=self.simular_sistema_tiempo_real(entrada, t_total, dt),
                             init_func=self.init_animation, blit=True, interval=interval)
        plt.show()