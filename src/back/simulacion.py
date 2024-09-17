import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sympy import  Symbol, expand, Poly,inverse_laplace_transform, symbols,laplace_transform
from sympy.parsing.latex import parse_latex
from back.topologia.topologia_serie import *
from back.macros.macro_controlador import MacroControlador
from latex2sympy2 import latex2sympy
from time import sleep

class Simulacion:
    def __init__(self, controlador = None, actuador = None, proceso =None, medidor =None, delta =1, ciclos=10, entrada="",salida_cero=10):
        # crear dataframe con las columnas tiempo, controlador, actuador, proceso, medidor, entrada
        self.controlador = controlador
        self.actuador = actuador
        self.proceso = proceso
        self.medidor = medidor
        self.delta = delta
        self.ciclos = ciclos
        self.entrada = entrada
        self.salida_cero = salida_cero
        self.datos = {'tiempo': [], 'controlador': [], 'actuador': [], 'proceso': [], 'medidor': [], 'entrada': [], 'error': [], 'salida': []}
            
    def simular_paso(self, y_actual, ciclo):

        tiempo = ciclo * self.delta

        y_medidor = self.simular_arbol(self.medidor.topologia, tiempo, y_actual)
        print(f"Paso {ciclo}: Salida del medidor: {y_medidor}")
        self.datos['medidor'].append(y_medidor)

        y_entrada =  self.aplicar_tf(self.entrada, tiempo)
        print(f"Mi entrada es {self.entrada}")
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

    def aplicar_tf(self, tf, tiempo, entrada=None):

        s,t = symbols('s t')

        tf_sympy = latex2sympy(tf)
        print(f"La función de transferencia es: {tf_sympy}")

        operacion_laplace = tf_sympy

        if entrada:
            entrada_micro_bloque = laplace_transform(entrada,t,s)[0]
            print(f"La entrada es: {entrada_micro_bloque}")
            operacion_laplace = entrada_micro_bloque * tf_sympy
            print(f"La operación de Laplace es: {operacion_laplace}")
        
        operacion_tiempo = inverse_laplace_transform(operacion_laplace,s,t)
        print(f"La operación en tiempo es: {operacion_tiempo}")
        salida_micro_bloque = operacion_tiempo.subs(t,tiempo)
        print(f"La salida en tiempo es: {salida_micro_bloque}")

        
        return salida_micro_bloque
    
    

    def simular_sistema_tiempo_real(self):

        y_salida = self.salida_cero

        # Simulación paso a paso
        for i in range(1, self.ciclos+1):
            y_salida = self.simular_paso(y_salida,i)
            sleep(2)
        
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
    
    def ejecutar_simulacion(self):
        self.simular_sistema_tiempo_real()
        # self.fig, self.ax = plt.subplots(figsize=(12, 8))
        # self.line, = self.ax.plot([], [], 'b-', label='Salida del sistema')
        # self.line_setpoint, = self.ax.plot([], [], 'r--', label='Setpoint')
        # self.line_entrada, = self.ax.plot([], [], 'g-', label='Entrada')
        
        # t = np.arange(0, t_total, dt)
        # y = np.zeros_like(t)
        # y_medido = np.zeros_like(t)
        
        # # Calcular el valor máximo de la entrada para el rango de tiempo
        # entrada_valores = [entrada(ti) for ti in t]
        # y_max = max(max(entrada_valores), setpoint) * 1.2
        
        # # Ajustar la escala inicial
        # self.ax.set_xlim(0, t_total)
        # self.ax.set_ylim(0, y_max)
        
        # # Ajustar las marcas del eje x
        # self.ax.set_xticks(np.linspace(0, t_total, 11))
        
        # # Ajustar las marcas del eje y
        # y_ticks = np.linspace(0, y_max, 11)
        # self.ax.set_yticks(y_ticks)
        # self.ax.set_yticklabels([f"{tick:.1f}" for tick in y_ticks])

        # def update(frame):
        #     i = frame
        #     if i > 0:
        #         # Modificar esta línea
        #         y_actual = self.simular_paso(y_medido[i-1], i)
        #         y[i] = y_actual
        #         y_medido[i] = y_actual  # Asumimos que y_medido es igual a y en este caso
        #     self.line.set_data(t[:i+1], y_medido[:i+1])
        #     self.line_setpoint.set_data(t[:i+1], [setpoint] * (i+1))
        #     self.line_entrada.set_data(t[:i+1], [entrada(ti) for ti in t[:i+1]])
            
        #     # Ajuste dinámico de la escala solo si es necesario
        #     current_y_max = self.ax.get_ylim()[1]
        #     new_y_max = max(max(y_medido[:i+1]), max([entrada(ti) for ti in t[:i+1]]), setpoint) * 1.2
        #     if new_y_max > current_y_max:
        #         self.ax.set_ylim(0, new_y_max)
        #         y_ticks = np.linspace(0, new_y_max, 11)
        #         self.ax.set_yticks(y_ticks)
        #         self.ax.set_yticklabels([f"{tick:.1f}" for tick in y_ticks])
            
        #     return self.line, self.line_setpoint, self.line_entrada

        # velocidad = velocidad.lower().strip()
        # if 'rap' in velocidad:
        #     interval = 1
        # elif 'lent' in velocidad:
        #     interval = 50
        # else:
        #     interval = 10  # velocidad normal por defecto

        # self.anim = FuncAnimation(self.fig, update, frames=len(t), interval=interval, blit=True, repeat=False)
        
        # self.ax.set_xlabel('Tiempo (Segundos)')
        # self.ax.set_ylabel('Amplitud')
        # self.ax.set_title('Respuesta del Sistema')
        # self.ax.legend()
        # self.ax.grid(True)
        
        # plt.tight_layout()
        # plt.show()


