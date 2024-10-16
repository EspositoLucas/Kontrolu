from back.topologia.microbloque import MicroBloque
from back.macros.macro_controlador import MacroControlador
from back.macros.macro_actuador import MacroActuador
from back.macros.macro_proceso import MacroProceso
from back.macros.macro_medidor import MacroMedidor
from back.topologia.carga import Carga
from time import sleep
from globals import ESTA_SIMULANDO
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtGui
import os
from PyQt5.QtWidgets import QApplication

class Simulacion(QObject):
    
    def __init__(self, controlador :MacroControlador= None, actuador:MacroActuador = None, proceso:MacroProceso =None, medidor:MacroMedidor =None, delta =1, ciclos=10, entrada:MicroBloque=None,salida_cero=10,carga:MicroBloque= None,graficadora =None):
        
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
        self.graficadora = graficadora
        self.continuar_simulacion = True
        
        if self.graficadora:
            self.graficadora.closeEvent = self.confirmar_cierre  # Reemplaza el evento de cierre
        self.cerrando = False  # Nueva variable para controlar el cierre

            
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

        estado_carga = self.carga.simular(tiempo, y_actual)
        print(f"Paso {ciclo}: Estado de la carga: {estado_carga}")
        self.datos['carga'].append(estado_carga)

        datos_paso = {
            'tiempo': tiempo,
            'controlador': y_controlador,
            'actuador': y_actuador,
            'proceso': y_proceso,
            'medidor': y_medidor,
            'entrada': y_entrada,
            'error': error,
            'salida': y_actual,
            'carga': estado_carga  # Añadimos el estado de la carga
        }

        if self.graficadora:
            self.graficadora.agregar_datos(datos_paso)
            self.graficadora.procesar_eventos()
            
        # Añadir impresión detallada de los valores
        print(f"\nCiclo {ciclo}:")
        print(f"Tiempo: {tiempo}")
        print(f"Entrada: {y_entrada}")
        print(f"Medidor: {y_medidor}")
        print(f"Error: {error}")
        print(f"Controlador: {y_controlador}")
        print(f"Actuador: {y_actuador}")
        print(f"Proceso: {y_proceso}")
        print(f"Salida actual: {y_actual}")
        print(f"Estado de la carga: {estado_carga}")
        print("-" * 30)

        return y_actual
    
    def confirmar_cierre(self, event):
        if self.cerrando:  # Si ya estamos en proceso de cierre, aceptar el evento
            event.accept()
            return

        dialog = QMessageBox(self.graficadora)
        dialog.setWindowTitle('Confirmar cierre')
        dialog.setText('¿Desea terminar la simulación?')
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        
        # Establecer el estilo de la ventana
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #333;
                color: white;
            }
            
            QMessageBox QLabel {
                color: white;
                background-color: black;
                padding: 10px;
            }
        """)
        
        # Cambiar el texto del botón "Yes" a "Si"
        yes_button = dialog.button(QMessageBox.Yes)
        if yes_button:
            yes_button.setText("Si")

        # Aplicar estilo a los botones específicos
        for button in dialog.buttons():
            button.setStyleSheet("""
                background-color: black;
                color: white;
                min-width: 80px;
                min-height: 30px;
                border: none;
            """)

        reply = dialog.exec_()

        if reply == QMessageBox.Yes:
            self.continuar_simulacion = False
            self.cerrando = True  # Marcamos que estamos en proceso de cierre
            self.graficadora.close()  # Cerramos la ventana del gráfico
        else:
            event.ignore()

    def simular_sistema_tiempo_real(self, velocidad=5000):
        y_salida = self.salida_cero

        for i in range(1, self.ciclos+1):
            if not self.continuar_simulacion or (self.graficadora and self.graficadora.is_paused):
                while self.graficadora and self.graficadora.is_paused: # esto provoca que cuando se pausa la simulacion, se termina y se quiere salir de la aplcacion, en la terminal se sigue igual ejecutando por el multihilo
                    self.graficadora.procesar_eventos()   # esto provoca que cuando se pausa la simulacion, se termina y se quiere salir de la aplcacion, en la terminal se sigue igual ejecutando por el multihilo
                    sleep(0.1)
            if not self.continuar_simulacion:
                break
            y_salida = self.simular_paso(y_salida, i)
            sleep(velocidad / 1000)  # Convierte la velocidad a segundos
            
        if self.continuar_simulacion and self.graficadora and not self.cerrando:
            self.graficadora.show()  # Asegura que la gráfica sea visible al final
        
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
    
    def ejecutar_simulacion(self, velocidad=5):
        global ESTA_SIMULANDO
        ESTA_SIMULANDO = True
        self.simular_sistema_tiempo_real(velocidad=velocidad)
        ESTA_SIMULANDO = False
        if self.graficadora and not self.graficadora.isHidden():
            self.graficadora.close()
    

