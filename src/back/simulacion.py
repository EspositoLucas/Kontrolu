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

        datos_paso = {}

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
        

        datos_paso['tiempo'] = tiempo
        datos_paso['controlador'] = y_controlador
        datos_paso['actuador'] = y_actuador
        datos_paso['proceso'] = y_proceso
        datos_paso['medidor'] = y_medidor
        datos_paso['entrada'] = y_entrada
        datos_paso['error'] = error
        datos_paso['salida'] = y_actual
        datos_paso['carga'] = estado

        #self.graficadora.agregar_datos(datos_paso)

        return y_actual

    

    def simular_sistema_tiempo_real(self,velocidad=5):

        y_salida = self.salida_cero

        # Simulación paso a paso
        for i in range(1, self.ciclos+1):
            y_salida = self.simular_paso(y_salida,i)
            sleep(velocidad)
        
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
    
    def ejecutar_simulacion(self,velocidad=5):
        global ESTA_SIMULANDO
        ESTA_SIMULANDO = True
        self.simular_sistema_tiempo_real(velocidad=velocidad)
        ESTA_SIMULANDO = False

