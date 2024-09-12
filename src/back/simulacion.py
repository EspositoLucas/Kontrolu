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
        self.contador_paso = 0

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
        
        return num_coeffs, den_coeffs
            
    def simular_paso(self, t_inicio, t_fin, setpoint, y_actual):
        # Calcula el error actual
        error = setpoint - y_actual
        
        print(f"Paso {self.contador_paso}: Error obtenido: {error} de hacer: setpoint ({setpoint}) - y_actual ({y_actual})")

        # Crea un vector de tiempo para este paso
        t = np.array([t_inicio, t_fin])
        
        # Crea un vector de entrada constante para este paso
        # Usamos el error como entrada para el controlador
        u = np.array([error, error])
        
        # Simula cada componente del sistema en secuencia
        # Cada componente recibe el mismo vector de tiempo
        y_controlador = self.simular_arbol(self.controlador.topologia, t, u)
        print(f"Paso {self.contador_paso}: Salida del controlador: {y_controlador}")
        
        y_actuador = self.simular_arbol(self.actuador.topologia, t, y_controlador)
        print(f"Paso {self.contador_paso}: Salida del actuador: {y_actuador}")

        y_proceso = self.simular_arbol(self.proceso.topologia, t, y_actuador)
        print(f"Paso {self.contador_paso}: Salida del proceso (SALIDA DEL SISTEMA): {y_proceso}")
        
        # Aplica el medidor
        medicion = self.medidor.medir(setpoint, y_proceso)
        print(f"Paso {self.contador_paso}: Salida del medidor: {medicion}")
        
        return y_proceso[-1], medicion

    def simular_arbol(self, nodo, t, entrada):
        # Caso base: MicroBloque
        if isinstance(nodo, MicroBloque):
            return self.aplicar_tf(nodo.funcion_transferencia, t, entrada)
        
        # Caso recursivo: TopologiaSerie o MacroControlador
        elif isinstance(nodo, (TopologiaSerie, MacroControlador)):
            for hijo in nodo.hijos:
                # La salida de cada hijo es la entrada del siguiente
                entrada = self.simular_arbol(hijo, t, entrada)
            return entrada
        
        # Caso recursivo: TopologiaParalelo
        elif isinstance(nodo, TopologiaParalelo):
            # Simula todos los hijos con la misma entrada
            salidas = [self.simular_arbol(hijo, t, entrada) for hijo in nodo.hijos]
            # Suma las salidas de todos los hijos
            return sum(salidas)
        
        # Caso de error
        else:
            raise ValueError(f"Tipo de nodo desconocido: {type(nodo)}")

    def aplicar_tf(self, tf, t, entrada):
        # Convierte la función de transferencia de LaTeX a coeficientes
        num, den = self.latex_to_tf(tf)
        
        # Crea el sistema de función de transferencia
        sys = control.TransferFunction(num, den)
        
        # Simula la respuesta del sistema
        _, yout = control.forced_response(sys, T=t, U=entrada)
        
        # Retorna la salida del sistema
        return yout

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
    
    def simular_sistema_tiempo_real(self, t_total, dt, setpoint):
        # Crea un array de tiempos
        t = np.arange(0, t_total, dt)
        
        # Inicializa arrays para almacenar las salidas
        y = np.zeros_like(t)
        y_medido = np.zeros_like(t)
        
        # Simulación paso a paso
        for i in range(1, len(t)):
            # Simula un paso desde t[i-1] hasta t[i]
            y[i], y_medido[i] = self.simular_paso(t[i-1], t[i], setpoint, y_medido[i-1])
            self.contador_paso += 1
        
        # Retorna los arrays de tiempo, salida del proceso y salida medida
        return t, y, y_medido
        
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
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.line, = self.ax.plot([], [], 'b-', label='Salida del sistema')
        self.line_setpoint, = self.ax.plot([], [], 'r--', label='Setpoint')
        self.line_entrada, = self.ax.plot([], [], 'g-', label='Entrada')
        self.contador_paso = 0
        
        t = np.arange(0, t_total, dt)
        y = np.zeros_like(t)
        y_medido = np.zeros_like(t)
        u = self.generar_entrada(entrada, t)
        
        # Ajustar la escala inicial
        self.ax.set_xlim(0, t_total)
        y_max = max(setpoint * 1.2, max(u) * 1.2)  # 20% más que el setpoint o el máximo de la entrada
        self.ax.set_ylim(0, y_max)
        
        # Ajustar las marcas del eje x
        self.ax.set_xticks(np.linspace(0, t_total, 11))
        
        # Ajustar las marcas del eje y
        y_ticks = np.linspace(0, y_max, 11)
        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels([f"{tick:.1f}" for tick in y_ticks])

        def update(frame):
            i = frame
            if i > 0:
                y[i], y_medido[i] = self.simular_paso(t[i-1], t[i], setpoint, y_medido[i-1])
            self.line.set_data(t[:i+1], y_medido[:i+1])
            self.line_setpoint.set_data(t[:i+1], [setpoint] * (i+1))
            self.line_entrada.set_data(t[:i+1], u[:i+1])
            
            # Ajuste dinámico de la escala y solo si es necesario
            current_y_max = self.ax.get_ylim()[1]
            new_y_max = max(max(y_medido[:i+1]), max(u[:i+1]), setpoint) * 1.2
            if new_y_max > current_y_max:
                self.ax.set_ylim(0, new_y_max)
                y_ticks = np.linspace(0, new_y_max, 11)
                self.ax.set_yticks(y_ticks)
                self.ax.set_yticklabels([f"{tick:.1f}" for tick in y_ticks])
            
            return self.line, self.line_setpoint, self.line_entrada

        velocidad = velocidad.lower().strip()
        if 'rap' in velocidad:
            interval = 1
        elif 'lent' in velocidad:
            interval = 50
        else:
            interval = 10  # velocidad normal por defecto

        self.anim = FuncAnimation(self.fig, update, frames=len(t), interval=interval, blit=True, repeat=False)
        
        self.ax.set_xlabel('Tiempo (Segundos)')
        self.ax.set_ylabel('Amplitud')
        self.ax.set_title('Respuesta del Sistema')
        self.ax.legend()
        self.ax.grid(True)
        
        plt.tight_layout()
        plt.show()


