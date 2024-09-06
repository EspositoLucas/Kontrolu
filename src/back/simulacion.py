import numpy as np
import control
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import sympify, Symbol, expand, Poly
from scipy import signal
from sympy.parsing.latex import parse_latex
from back.topologia.topologia_serie import *
from back.macros.macro_controlador import MacroControlador

class Simulacion:
    def __init__(self, controlador, actuador, proceso, medidor):
        self.controlador = controlador
        self.actuador = actuador
        self.proceso = proceso
        self.medidor = medidor

    def latex_to_tf(self, latex_expr):
        # Captura el latex y lo procesa
        expr = parse_latex(latex_expr)
        
        # Define la variable matemática principal
        s = Symbol('s')
        
        # Separa numerador y denominador
        num, den = expr.as_numer_denom()
        
        # Expande numerador y denominador
        num_expanded = expand(num)
        den_expanded = expand(den)
        
        # Convierte a polinomios en función de 's'
        num_poly = Poly(num_expanded, s)
        den_poly = Poly(den_expanded, s)
        
        # Obtiene los coeficientes en forma de lista
        num_coeffs = [float(coeff.evalf()) for coeff in num_poly.all_coeffs()]
        den_coeffs = [float(coeff.evalf()) for coeff in den_poly.all_coeffs()]
        
        # Imprime los coeficientes obtenidos
        print("Coeficientes del numerador: ", num_coeffs)
        print("Coeficientes del denominador: ", den_coeffs)
        
        return num_coeffs, den_coeffs
            
    def simular_paso(self, t, dt, setpoint, y_actual, u_actual):
        # Calcula el error
        error = setpoint - y_actual
        
        # Simula cada componente del sistema
        y_proceso = self.simular_arbol(self.controlador.topologia, error)
        y_proceso = self.simular_arbol(self.actuador.topologia, y_proceso)
        y_proceso = self.simular_arbol(self.proceso.topologia, y_proceso)
        
        # Aplica el medidor
        medicion = self.medidor.medir(y_proceso)
        
        return y_proceso, medicion

    def simular_arbol(self, nodo, entrada):
        # Caso base: MicroBloque
        if isinstance(nodo, MicroBloque):
            return self.aplicar_tf(nodo.funcion_transferencia, entrada)
        
        # Caso recursivo: TopologiaSerie o MacroControlador
        elif isinstance(nodo, (TopologiaSerie, MacroControlador)):
            for hijo in nodo.hijos:
                entrada = self.simular_arbol(hijo, entrada)
            return entrada
        
        # Caso recursivo: TopologiaParalelo
        elif isinstance(nodo, TopologiaParalelo):
            salidas = [self.simular_arbol(hijo, entrada) for hijo in nodo.hijos]
            return sum(salidas)
        
        # Caso de error
        else:
            raise ValueError(f"Tipo de nodo desconocido: {type(nodo)}")

    def aplicar_tf(self, tf, entrada):
        # Extrae numerador y denominador de la función de transferencia 
        num, den = self.latex_to_tf(tf)
        num = np.asarray(num, dtype=np.float64)
        den = np.asarray(den, dtype=np.float64)
        
        # Crea el sistema de función de transferencia
        sys = control.TransferFunction(num, den)
        
        # Crea un pequeño intervalo de tiempo para la simulación
        t = np.linspace(0, 0.1, 10)
        
        # Simula la respuesta del sistema usando control.forced_response
        T, yout = control.forced_response(sys, T=t, U=entrada * np.ones_like(t))
        
        # Retorna el último valor de la salida
        return yout[-1]

    def generar_entrada(self, entrada, t):
        if entrada == "impulso":
            # Genera una señal de impulso
            u = np.zeros_like(t)
            u[0] = 1 / (t[1] - t[0])  # Aproximación del impulso
        elif callable(entrada):
            # Si la entrada es una función, la aplica a cada punto de tiempo
            u = np.array([entrada(ti) for ti in t])
        else:
            # Si es un valor constante, crea un array con ese valor
            u = np.full_like(t, entrada)
        return u
    
    def simular_sistema_tiempo_real(self, entrada, t_total, dt, setpoint):
        
        # Genera un array de tiempos
        t = np.arange(0, t_total, dt)
        
        # Genera la señal de entrada
        u = self.generar_entrada(entrada, t)
        
        # Inicializa arrays para almacenar las salidas
        y = np.zeros_like(t)
        y_medido = np.zeros_like(t)
        
        # Simulación paso a paso
        for i in range(1, len(t)):
            y[i], y_medido[i] = self.simular_paso(t[i], dt, setpoint, y_medido[i-1], u[i])
        
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
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  # Aumentamos el tamaño de la figura
        self.line, = self.ax.plot([], [], 'b-', label='Salida del sistema')
        self.line_setpoint, = self.ax.plot([], [], 'r--', label='Valor esperado')
        
        try:
            t, y, _ = self.simular_sistema_tiempo_real(entrada, t_total, dt, setpoint)
        except Exception as e:
            print(f"Error durante la simulación: {e}")
            return
        
        # Calculamos los límites del eje y
        y_min, y_max = min(y), max(y)
        y_range = y_max - y_min
        
        # Ajustamos los límites para que la gráfica ocupe el 80% del espacio vertical
        margin = y_range * 0.1
        y_bottom = min(y_min, setpoint) - margin
        y_top = max(y_max, setpoint) + margin
        
        self.ax.set_xlim(0, t_total)
        self.ax.set_ylim(y_bottom, y_top)
        
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
            self.line_setpoint.set_data([0, t[i-1]], [setpoint, setpoint])
            
            # Ajuste dinámico de la escala
            if i > 1:
                y_min, y_max = min(y[:i]), max(y[:i])
                y_range = y_max - y_min
                margin = y_range * 0.1
                self.ax.set_ylim(min(y_min, setpoint) - margin, max(y_max, setpoint) + margin)
            
            return self.line, self.line_setpoint

        self.anim = FuncAnimation(self.fig, update, frames=len(t), interval=interval, blit=True)
        plt.tight_layout()
        plt.show()


