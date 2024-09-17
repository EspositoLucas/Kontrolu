import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import  Symbol, expand, Poly,inverse_laplace_transform, symbols,laplace_transform
from sympy.parsing.latex import parse_latex
from back.topologia.topologia_serie import *
from back.macros.macro_controlador import MacroControlador
from latex2sympy2 import latex2sympy

class Simulacion:
    def __init__(self, controlador, actuador, proceso, medidor, delta, ciclos, entrada = None):
        # crear dataframe con las columnas tiempo, controlador, actuador, proceso, medidor, entrada
        self.controlador = controlador
        self.actuador = actuador
        self.proceso = proceso
        self.medidor = medidor
        self.entrada = entrada
        self.delta = delta
        self.ciclos = ciclos
        self.datos = {'tiempo': [], 'controlador': [], 'actuador': [], 'proceso': [], 'medidor': [], 'entrada': [], 'error': [], 'salida': []}

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
            
    def simular_paso(self, y_actual, ciclo):

        tiempo = ciclo * self.delta

        y_medidor = self.simular_arbol(self.medidor.topologia, tiempo, y_actual)
        print(f"Paso {ciclo}: Salida del medidor: {y_medidor}")
        self.datos['medidor'].append(y_medidor)

        y_entrada =  self.simular_arbol(self.entrada.topologia, tiempo, 1)
        print(f"Paso {ciclo}: Salida de la entrada: {y_entrada}")
        self.datos['entrada'].append(y_entrada)

        # Calcula el error actual
        error = y_entrada - y_medidor        
        print(f"Paso {ciclo}: Error obtenido: {error}")
        self.datos['error'].append(error)
        
        # Simula cada componente del sistema en secuencia
        # Cada componente recibe el mismo vector de tiempo
        y_controlador = self.simular_arbol(self.controlador.topologia, tiempo, error)
        print(f"Paso {ciclo}: Salida del controlador: {y_controlador}")
        self.datos['controlador'].append(y_controlador)
        
        y_actuador = self.simular_arbol(self.actuador.topologia, tiempo, y_controlador)
        print(f"Paso {ciclo}: Salida del actuador: {y_actuador}")
        self.datos['actuador'].append(y_actuador)

        y_proceso = self.simular_arbol(self.proceso.topologia, tiempo, y_actuador)
        print(f"Paso {ciclo}: Salida del proceso (SALIDA DEL SISTEMA): {y_proceso}")
        self.datos['proceso'].append(y_proceso)

        y_actual += y_proceso
        self.datos['salida'].append(y_actual)

        return y_actual

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

    def aplicar_tf(self, tf, tiempo, entrada):

        s,t = symbols('s t')

        tf_sympy = latex2sympy(tf)

        entrada_micro_bloque = laplace_transform(entrada,t,s)[0]
        operacion_laplace = entrada_micro_bloque * tf_sympy
        operacion_tiempo = inverse_laplace_transform(operacion_laplace,s,t)
        salida_micro_bloque = operacion_tiempo.subs(t,tiempo)

        print(f"Entrada del microbloque: {entrada_micro_bloque}")
        print(f"Operación de Laplace: {operacion_laplace}")
        print(f"Operación de tiempo: {operacion_tiempo}")
        print(f"Salida del microbloque: {salida_micro_bloque}")
        
        
        return salida_micro_bloque
    


    def simular_sistema_tiempo_real(self):

        # Simulación paso a paso
        for i in range(1, len(self.ciclos+1)):
            y_salida = self.simular_paso(y_salida,i)
        
        # Retorna los arrays de tiempo, salida del proceso y salida medida
        return self.datos
        
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
        
        t = np.arange(0, t_total, dt)
        y = np.zeros_like(t)
        y_medido = np.zeros_like(t)
        # u = self.generar_entrada(entrada, t)
        
        # Ajustar la escala inicial
        self.ax.set_xlim(0, t_total)
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


