from back.topologia.topologia_serie import *
from back.macros.macro_controlador import MacroControlador
from back.macros.macro_actuador import MacroActuador
from back.macros.macro_proceso import MacroProceso
from back.macros.macro_medidor import MacroMedidor
from back.topologia.carga import Carga
from time import sleep
from globals import ESTA_SIMULANDO

class Simulacion:
    def __init__(self, controlador :MacroControlador= None, actuador:MacroActuador = None, proceso:MacroProceso =None, medidor:MacroMedidor =None, delta =1, ciclos=10, entrada:MicroBloque=None,salida_cero=10,carga:MicroBloque= None):
        
        self.controlador : MacroControlador = controlador
        self.actuador : MacroActuador = actuador
        self.proceso : MacroProceso = proceso
        self.medidor : MacroMedidor = medidor
        self.delta = delta
        self.ciclos = ciclos
        self.entrada : MicroBloque = entrada
        self.salida_cero = salida_cero
        self.carga :Carga = carga
        self.datos = {'tiempo': [], 'controlador': [], 'actuador': [], 'proceso': [], 'medidor': [], 'entrada': [], 'error': [], 'salida': [], 'carga': []}
            
    def simular_paso(self, y_actual, ciclo):

        tiempo = ciclo * self.delta

        y_medidor = self.medidor.simular(tiempo, y_actual)
        print(f"Paso {ciclo}: Salida del medidor: {y_medidor}")
        self.datos['medidor'].append(y_medidor)

        y_entrada =  self.entrada.simular(tiempo)
        print(f"Mi entrada es {self.entrada}")
        print(f"Paso {ciclo}: Salida de la entrada: {y_entrada}")
        self.datos['entrada'].append(y_entrada)

        # Calcula el error actual
        error = y_entrada - y_medidor        
        print(f"Paso {ciclo}: Error obtenido: {error}")
        self.datos['error'].append(error)
        
        # Simula cada componente del sistema en secuencia
        # Cada componente recibe el mismo vector de tiempo
        y_controlador = self.controlador.simular(tiempo, error)
        print(f"Paso {ciclo}: Salida del controlador: {y_controlador}")
        self.datos['controlador'].append(y_controlador)
        
        y_actuador = self.actuador.simular(tiempo, y_controlador)
        print(f"Paso {ciclo}: Salida del actuador: {y_actuador}")
        self.datos['actuador'].append(y_actuador)

        y_proceso = self.proceso.simular(tiempo, y_actuador)
        print(f"Paso {ciclo}: Salida del proceso (SALIDA DEL SISTEMA): {y_proceso}")
        self.datos['proceso'].append(y_proceso)

        y_actual += y_proceso
        self.datos['salida'].append(y_actual)

        estado = self.carga.simular(tiempo, y_actual)
        print(f"Paso {ciclo}: Estado de la carga: {estado}")
        self.datos['carga'].append(estado)

        return y_actual

    

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
        global ESTA_SIMULANDO
        ESTA_SIMULANDO = True
        self.simular_sistema_tiempo_real()
        ESTA_SIMULANDO = False
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


