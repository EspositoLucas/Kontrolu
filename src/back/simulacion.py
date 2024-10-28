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
        self.controlador : MacroControlador = controlador
        self.actuador : MacroActuador = actuador
        self.proceso : MacroProceso = proceso
        self.medidor : MacroMedidor = medidor        
        self.entrada : MicroBloque = entrada
        self.carga : Carga = carga

        self.controlador.vaciar_datos()
        self.actuador.vaciar_datos()
        self.proceso.vaciar_datos()
        self.medidor.vaciar_datos()
        self.entrada.vaciar_datos()
        self.carga.vaciar_datos()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simular_paso_timer)

        self.paso_actual = 0

        self.delta = delta
        self.multiplicador = 2/self.delta
        self.ciclos = ciclos
        self.salida_cero = salida_cero
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

        y_medidor = self.medidor.simular(tiempo, self.delta, y_actual)
        
        self.datos['medidor'].append(y_medidor)
        print(f"Medición actual: {y_medidor}")
        print(f"Histórico de mediciones: {self.datos['medidor']}")

        y_entrada =  self.entrada.simular(tiempo, self.delta)
        self.datos['entrada'].append(y_entrada)
        print(f"Entrada actual: {y_entrada}")
        print(f"Histórico de entradas: {self.datos['entrada']}")

        error = y_entrada - y_medidor        
        self.datos['error'].append(error*self.multiplicador)
        
        # Simula cada componente del sistema en secuencia
        # Cada componente recibe el mismo vector de tiempo
        y_controlador = self.controlador.simular(tiempo, self.delta, error)
        self.datos['controlador'].append(y_controlador*self.multiplicador)
        
        y_actuador = self.actuador.simular(tiempo, self.delta, y_controlador)
        self.datos['actuador'].append(y_actuador*self.multiplicador)

        y_proceso = self.proceso.simular(tiempo, self.delta, y_actuador)
        self.datos['proceso'].append(y_proceso*self.multiplicador)

        self.datos['salida'].append(y_proceso*self.multiplicador)

        estado_carga = self.carga.simular(tiempo, self.delta, y_proceso)
        self.datos['carga'].append(estado_carga)
        print(f"Estado de carga: {estado_carga}")
        print(f"Histórico de estados de carga: {self.datos['carga']}")

        datos_paso = {
            'tiempo': tiempo,
            'controlador': y_controlador*self.multiplicador,
            'actuador': y_actuador*self.multiplicador,
            'proceso': y_proceso*self.multiplicador,
            'medidor': y_medidor*self.multiplicador,
            'entrada': y_entrada*self.multiplicador,
            'error': error*self.multiplicador,
            'salida': y_proceso*self.multiplicador,
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
        print(f"Salida actual: {y_proceso}")
        print(f"Estado de la carga: {estado_carga}")
        print("-" * 30)

        return y_proceso
    
    def calcular_salida_convolucion(self, y_proceso):
        """
        Calcula la salida usando convolución pero respetando la estructura actual
        """
        print("\nDETALLES DE LA CONVOLUCIÓN:")
        print(f"Valor actual del proceso: {y_proceso}")
        
        max_historic_samples = 1000
        
        if len(self.datos['proceso']) > max_historic_samples:
            historical_values = self.datos['proceso'][-max_historic_samples:]
            print(f"Histórico limitado a {max_historic_samples} muestras")
        else:
            historical_values = self.datos['proceso']
            print(f"Usando histórico completo: {len(historical_values)} muestras")
        
        print("\nCálculo de convolución paso a paso:")
        salida = y_proceso  # Inicializar con el valor actual
        print(f"Valor inicial (y_proceso actual): {salida}")
        
        for i, valor in enumerate(historical_values[:-1]):
            peso = (i + 1) / len(historical_values)
            contribucion = valor * peso * self.delta
            salida += contribucion
            print(f"Paso {i+1}:")
            print(f"  - Valor histórico: {valor}")
            print(f"  - Peso aplicado: {peso:.4f}")
            print(f"  - Delta tiempo: {self.delta}")
            print(f"  - Contribución: {contribucion:.4f}")
            print(f"  - Salida acumulada: {salida:.4f}")
        
        print(f"\nSalida final después de la convolución: {salida}")
        return salida
    
    
    def confirmar_cierre(self, event):
        self.timer.stop()
        self.window.no_buttons()
        if self.cerrando:
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
        
        # Aplicar el nuevo estilo
        dialog.setStyleSheet("""
            QMessageBox {
                background-color: #B0B0B0;
                border: 2px solid #505050;
                border-radius: 15px;
                padding: 20px;
            }
            QMessageBox QLabel {
                color: #2B2D42;
                font-size: 16px;
                font-family: "Segoe UI", "Arial", sans-serif;
                background-color: transparent;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background-color: #808080;
                color: white;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: "Segoe UI", "Arial", sans-serif;
                min-width: 80px;
                min-height: 30px;
            }
            QMessageBox QPushButton:hover {
                background-color: #606060;
            }
        """)
        
        # Cambiar el texto del botón "Yes" a "Si"
        yes_button = dialog.button(QMessageBox.Yes)
        if yes_button:
            yes_button.setText("Si")

        reply = dialog.exec_()

        if reply == QMessageBox.Yes:
            self.window.deteniendo_buttons()
            self.timer.stop()
            self.continuar_simulacion = False
            self.cerrando = True
            self.graficadora.close()
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