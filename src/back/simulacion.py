from back.topologia.microbloque import MicroBloque
from back.macros.macro_controlador import MacroControlador
from back.macros.macro_actuador import MacroActuador
from back.macros.macro_proceso import MacroProceso
from back.macros.macro_medidor import MacroMedidor
from back.topologia.carga import Carga
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtGui
import os
from PyQt5.QtCore import QTimer

class Simulacion(QObject):
    
    def __init__(self, controlador :MacroControlador= None, actuador:MacroActuador = None, proceso:MacroProceso =None, medidor:MacroMedidor =None, delta =1, ciclos=10, entrada:MicroBloque=None,salida_cero=10,carga:MicroBloque= None,graficadora =None,window = None):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simular_paso_timer)

        self.paso_actual = 0
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
        self.graficadora.add_simulacion(self)
        self.continuar_simulacion = True
        self.window = window
        
        if self.graficadora:
            self.graficadora.closeEvent = self.confirmar_cierre  # Reemplaza el evento de cierre
        self.cerrando = False  # Nueva variable para controlar el cierre



            
    def simular_paso(self, y_actual, ciclo):

        tiempo = ciclo * self.delta

        y_medidor = self.medidor.simular(tiempo, y_actual)
        self.datos['medidor'].append(y_medidor)

        y_entrada =  self.entrada.simular(tiempo)
        self.datos['entrada'].append(y_entrada)

        # Calcula el error actual
        error = y_entrada - y_medidor        
        self.datos['error'].append(error)
        
        # Simula cada componente del sistema en secuencia
        # Cada componente recibe el mismo vector de tiempo
        y_controlador = self.controlador.simular(tiempo, error)
        self.datos['controlador'].append(y_controlador)
        
        y_actuador = self.actuador.simular(tiempo, y_controlador)
        self.datos['actuador'].append(y_actuador)

        y_proceso = self.proceso.simular(tiempo, y_actuador)
        self.datos['proceso'].append(y_proceso)

        y_actual += y_proceso
        self.datos['salida'].append(y_actual)

        estado_carga = self.carga.simular(tiempo, y_actual)
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
        self.timer.stop()
        self.window.no_buttons()
        if self.cerrando:  # Si ya estamos en proceso de cierre, aceptar el evento
            self.window.deteniendo_buttons()
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
            self.window.deteniendo_buttons()
            self.timer.stop()
            self.continuar_simulacion = False
            self.cerrando = True  # Marcamos que estamos en proceso de cierre
            self.graficadora.close()  # Cerramos la ventana del gráfico
        else:
            self.window.reanudando_buttons()
            self.timer.start()
            event.ignore()
            

        
  
    def simular_paso_timer(self):
        # Simula un paso de la simulación
        if self.paso_actual <= self.ciclos:
            if not self.continuar_simulacion:
                while self.graficadora: # esto provoca que cuando se pausa la simulacion, se termina y se quiere salir de la aplcacion, en la terminal se sigue igual ejecutando por el multihilo
                    self.graficadora.procesar_eventos()   # esto provoca que cuando se pausa la simulacion, se termina y se quiere salir de la aplcacion, en la terminal se sigue igual ejecutando por el multihilo
            if not self.continuar_simulacion:
                self.timer.stop()
            self.y_salida = self.simular_paso(self.y_salida, self.paso_actual)
            self.paso_actual += 1
        else:
            self.timer.stop()  # Detener el temporizador cuando la simulación termine
            print("Simulación completada:", self.datos)
            return self.datos  # Retornar los datos al final
    
    def simular_sistema_tiempo_real(self,velocidad):
        self.paso_actual = 1  # Reiniciar el contador de pasos
        self.y_salida = self.salida_cero  # Reiniciar el valor de salida
        self.datos = {'tiempo': [], 'controlador': [], 'actuador': [], 'proceso': [], 'medidor': [], 'entrada': [], 'error': [], 'salida': [], 'carga': []}
        self.timer.setInterval(int(velocidad))
        self.timer.start()  # Iniciar el temporizador con el intervalo (milisegundos)

        #if self.continuar_simulacion and self.graficadora and not self.cerrando:
        #    self.graficadora.show()  # Asegura que la gráfica sea visible al final
        return self.datos
    

    
    def ejecutar_simulacion(self, velocidad=5):
        self.simular_sistema_tiempo_real(velocidad=velocidad)

    
    def detener_simulacion(self):
        self.graficadora.close()
        return self.datos
    
    def pausar_simulacion(self):
        self.timer.stop()
        self.graficadora.resume_button_change()
        return self.datos
    
    def reanudar_simulacion(self):
        self.timer.start()
        self.graficadora.pause_button_change()
        return self.datos
    
    def parar(self):
        self.timer.stop()
        self.window.pausando_buttons()
    
    def reanudar(self):
        self.timer.start()
        self.window.reanudando_buttons()