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
from sympy import latex,inverse_laplace_transform, simplify
from sympy.abc import s,z,t
import control as ctrl
import numpy as np
import time
from latex2sympy2 import latex2sympy

class Simulacion(QObject):

    def __init__(self,graficadora =None,window = None,sesion = None):
        super().__init__()      
        self.sesion = sesion
        self.controlador : MacroControlador = sesion.controlador
        self.actuador : MacroActuador = sesion.actuador
        self.proceso : MacroProceso = sesion.proceso
        self.medidor : MacroMedidor = sesion.medidor        
        self.entrada : MicroBloque = sesion.entrada
        self.carga : Carga = sesion.carga
        self.entrada = sesion.entrada

        self.controlador.vaciar_datos()
        self.actuador.vaciar_datos()
        self.proceso.vaciar_datos()
        self.medidor.vaciar_datos()
        self.entrada.vaciar_datos()
        self.carga.vaciar_datos()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simular_paso_timer)

        self.paso_actual = 0

        self.delta = sesion.delta_t
        self.multiplicador= 2/self.delta
        self.t_total = sesion.tiempo_total
        self.ciclos = self.t_total/self.delta
        self.salida_cero = sesion.salida_inicial
        self.datos = {'tiempo': [], 'controlador': [], 'actuador': [], 'proceso': [], 'medidor': [], 'entrada': [], 'error': [], 'salida': [], 'carga': []}
        self.graficadora = graficadora
        self.graficadora.add_simulacion(self)
        self.continuar_simulacion = True
        self.window = window
        self.precisa = sesion.precisa
        self.velocidad = sesion.velocidad
        
        if self.graficadora:
            self.graficadora.closeEvent = self.confirmar_cierre  # Reemplaza el evento de cierre
        self.cerrando = False  # Nueva variable para controlar el cierre

    def redimensionar_estado(self, nuevo_tam, estado_anterior):
        """
        Redimensiona el vector de estados preservando los valores anteriores donde sea posible
        """
        nuevo_estado = np.zeros((nuevo_tam, 1))
        if hasattr(self, 'x'):
            # Determinar el tamaño mínimo entre el estado anterior y nuevo
            min_tam = min(estado_anterior.shape[0], nuevo_tam)
            # Copiar los valores que podamos del estado anterior
            nuevo_estado[:min_tam] = estado_anterior[:min_tam]
        return nuevo_estado



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
        self.datos['error'].append(error)
        
        # Simula cada componente del sistema en secuencia
        # Cada componente recibe el mismo vector de tiempo
        y_controlador = self.controlador.simular(tiempo, self.delta, error)
        self.datos['controlador'].append(y_controlador)
        
        y_actuador = self.actuador.simular(tiempo, self.delta, y_controlador)
        self.datos['actuador'].append(y_actuador)

        y_proceso = self.proceso.simular(tiempo, self.delta, y_actuador)
        self.datos['proceso'].append(y_proceso)

        self.datos['salida'].append(y_proceso)

        estado_carga = self.carga.simular(tiempo, self.delta, y_proceso)
        self.datos['carga'].append(estado_carga)
        print(f"Estado de carga: {estado_carga}")
        print(f"Histórico de estados de carga: {self.datos['carga']}")

        datos_paso = {
            'tiempo': tiempo,
            'controlador': y_controlador,
            'actuador': y_actuador,
            'proceso': y_proceso,
            'medidor': y_medidor,
            'entrada': y_entrada,
            'error': error,
            'salida': y_proceso,
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

    def calcular_ft_global(self):
        self.ft_controlador = self.controlador.obtener_fdt_simpy(tiempo=self.paso_actual*self.delta)
        self.ft_actuador = self.actuador.obtener_fdt_simpy(tiempo=self.paso_actual*self.delta)
        self.ft_proceso = self.proceso.obtener_fdt_simpy(tiempo=self.paso_actual*self.delta)
        self.ft_lazo_directo = self.ft_controlador * self.ft_actuador * self.ft_proceso
        self.ft_medidor = self.medidor.obtener_fdt_simpy(tiempo=self.paso_actual*self.delta)
        self.ft_global = self.ft_lazo_directo / (1 + (self.ft_lazo_directo * self.ft_medidor))
        self.ft_global_simplificada = simplify(self.ft_global)
        return self.ft_global_simplificada
    
    def is_improper_tf(self,num_coef, den_coef):
        """
        Check if a transfer function is improper.
        
        An improper transfer function has a numerator degree 
        greater than or equal to the denominator degree.
        
        Args:
        num_coef (array-like): Numerator coefficients
        den_coef (array-like): Denominator coefficients
        
        Returns:
        bool: True if improper, False if proper
        """
        return len(num_coef) >= len(den_coef)
    
    def make_tf_proper(self,num_coef, den_coef):
        # Perform polynomial division
        quotient, remainder = np.polydiv(num_coef, den_coef)
        
        # The first coefficient of quotient is the static gain
        static_gain = quotient[0] if len(quotient) > 0 else 0
        
        # Remainder becomes the new numerator
        new_num_coef = remainder
        
        return new_num_coef, den_coef, static_gain
    def match_polynomial_degrees(self,num_coef, den_coef):
        if len(num_coef) > len(den_coef):
            # Pad denominator with leading zeros
            den_coef = np.pad(den_coef, (len(num_coef) - len(den_coef), 0), mode='constant')
        elif len(den_coef) > len(num_coef):
            # Pad numerator with leading zeros
            num_coef = np.pad(num_coef, (len(den_coef) - len(num_coef), 0), mode='constant')
        
        return num_coef, den_coef
    
    def truncate_to_proper(self,num_coef, den_coef):
        return num_coef[-len(den_coef):], den_coef

    def preprocess_tf(self,num_coef,den_coef):
        # Option 1: Try polynomial division first
        try:
            new_num, new_den, static_gain = self.make_tf_proper(num_coef, den_coef)
            return new_num, new_den, static_gain
        except:
            # Option 2: Try degree matching
            try:
                new_num, new_den = self.match_polynomial_degrees(num_coef, den_coef)
                return new_num, new_den, 1.0
            except:
                # Option 3: Truncation as last resort
                new_num, new_den = self.truncate_to_proper(num_coef, den_coef)
                return new_num, new_den, 1.0

    def crear_state_space(self, ft_global):
        numerador,denominador = ft_global.as_numer_denom()
        num_coef = numerador.as_poly(s).all_coeffs()
        den_coef = denominador.as_poly(s).all_coeffs()
        num_coef = [float(x) for x in num_coef]
        den_coef = [float(x) for x in den_coef]
        static_gain = 1.0

        if self.is_improper_tf(num_coef, den_coef):
            num_coef, den_coef, static_gain = self.preprocess_tf(num_coef, den_coef)

        self.H = ctrl.tf(num_coef, den_coef) * static_gain
        self.system_ss = ctrl.tf2ss(self.H)
        self.system_d = ctrl.sample_system(self.system_ss, self.delta, method='zoh')

        numerador,denominador = self.ft_medidor.as_numer_denom()
        num_coef = numerador.as_poly(s).all_coeffs()
        den_coef = denominador.as_poly(s).all_coeffs()
        num_coef = [float(x) for x in num_coef]
        den_coef = [float(x) for x in den_coef]
        static_gain = 1.0

        if self.is_improper_tf(num_coef, den_coef):
            num_coef, den_coef, static_gain = self.preprocess_tf(num_coef, den_coef)

        self.H_medidor = ctrl.tf(num_coef, den_coef) * static_gain
        self.system_ss_medidor = ctrl.tf2ss(self.H_medidor)
        self.system_d_medidor = ctrl.sample_system(self.system_ss_medidor, self.delta, method='zoh')

        numerador,denominador = self.ft_controlador.as_numer_denom()
        num_coef = numerador.as_poly(s).all_coeffs()
        den_coef = denominador.as_poly(s).all_coeffs()
        num_coef = [float(x) for x in num_coef]
        den_coef = [float(x) for x in den_coef]
        static_gain = 1.0

        if self.is_improper_tf(num_coef, den_coef):
            num_coef, den_coef, static_gain = self.preprocess_tf(num_coef, den_coef)

        self.H_controlador = ctrl.tf(num_coef, den_coef)*static_gain
        self.system_ss_controlador = ctrl.tf2ss(self.H_controlador)
        self.system_d_controlador = ctrl.sample_system(self.system_ss_controlador, self.delta, method='zoh')

        numerador,denominador = self.ft_actuador.as_numer_denom()
        num_coef = numerador.as_poly(s).all_coeffs()
        den_coef = denominador.as_poly(s).all_coeffs()
        num_coef = [float(x) for x in num_coef]
        den_coef = [float(x) for x in den_coef]
        static_gain = 1.0

        if self.is_improper_tf(num_coef, den_coef):
            num_coef, den_coef, static_gain = self.preprocess_tf(num_coef, den_coef)

        self.H_actuador = ctrl.tf(num_coef, den_coef) * static_gain
        self.system_ss_actuador = ctrl.tf2ss(self.H_actuador)
        self.system_d_actuador = ctrl.sample_system(self.system_ss_actuador, self.delta, method='zoh')
        
        
  
    def simular_paso_timer(self):
        # Simula un paso de la simulación
        if self.paso_actual <= self.ciclos:
            if not self.continuar_simulacion:
                while self.graficadora: # esto provoca que cuando se pausa la simulacion, se termina y se quiere salir de la aplcacion, en la terminal se sigue igual ejecutando por el multihilo
                    self.graficadora.procesar_eventos()   # esto provoca que cuando se pausa la simulacion, se termina y se quiere salir de la aplcacion, en la terminal se sigue igual ejecutando por el multihilo
            if not self.continuar_simulacion:
                self.timer.stop()
            if self.precisa:
                self.simular_paso_preciso()
            else:
                self.y_salida = self.simular_paso(self.y_salida, self.paso_actual)
            self.paso_actual += 1
        else:
            self.timer.stop()  # Detener el temporizador cuando la simulación termine
            print("Simulación completada:", self.datos)
            return self.datos  # Retornar los datos al final
    



    def simular_paso_preciso(self):
        tiempo = self.paso_actual * self.delta
        try:
            u = self.entrada.simular(tiempo, self.delta)
            # Verificar dimensiones antes de realizar operaciones
            if self.x.shape[0] != self.system_d.A.shape[0]:
                self.x = self.redimensionar_estado(self.system_d.A.shape[0], self.x)
            
            self.x = np.dot(self.system_d.A, self.x) + np.dot(self.system_d.B, u)
            y = np.dot(self.system_d.C, self.x) + np.dot(self.system_d.D, u)

            # Verificar dimensiones antes de realizar operaciones
            if self.x_medidor.shape[0] != self.system_d_medidor.A.shape[0]:
                self.x_medidor = self.redimensionar_estado(self.system_d_medidor.A.shape[0], self.x_medidor)
            
            self.x_medidor = np.dot(self.system_d_medidor.A, self.x_medidor) + np.dot(self.system_d_medidor.B, y[0,0])
            y_medidor = np.dot(self.system_d_medidor.C, self.x_medidor) + np.dot(self.system_d_medidor.D, y[0,0])

            error = u - y_medidor[0, 0]

            # Verificar dimensiones antes de realizar operaciones
            if self.x_controlador.shape[0] != self.system_d_controlador.A.shape[0]:
                self.x_controlador = self.redimensionar_estado(self.system_d_controlador.A.shape[0], self.x_controlador)
            
            self.x_controlador = np.dot(self.system_d_controlador.A, self.x_controlador) + np.dot(self.system_d_controlador.B, error)
            y_controlador = np.dot(self.system_d_controlador.C, self.x_controlador) + np.dot(self.system_d_controlador.D, error)

            # Verificar dimensiones antes de realizar operaciones
            if self.x_actuador.shape[0] != self.system_d_actuador.A.shape[0]:
                self.x_actuador = self.redimensionar_estado(self.system_d_actuador.A.shape[0], self.x_actuador)
            
            self.x_actuador = np.dot(self.system_d_actuador.A, self.x_actuador) + np.dot(self.system_d_actuador.B, y_controlador)
            y_actuador = np.dot(self.system_d_actuador.C, self.x_actuador) + np.dot(self.system_d_actuador.D, y_controlador)


            

            estado_carga = self.carga.simular(tiempo, self.delta, y[0, 0])
            
            self.datos['carga'].append(estado_carga)
            self.datos['tiempo'].append(tiempo)
            self.datos['entrada'].append(u)
            self.datos['salida'].append(y[0, 0])
            self.datos['error'].append(u - y[0, 0])
            self.datos['medidor'].append(y_medidor[0, 0])
            self.datos['controlador'].append(y_controlador[0, 0])
            self.datos['actuador'].append(y_actuador[0, 0])
            
            datos_paso = {
                'tiempo': tiempo,
                'entrada': u,
                'salida': y[0, 0],
                'error': u - y[0, 0],
                'carga': estado_carga,
                'medidor': y_medidor[0, 0],
                'controlador': y_controlador[0, 0],
                'actuador': y_actuador[0, 0]
            }

            if self.graficadora:
                self.graficadora.agregar_datos(datos_paso)
                self.graficadora.procesar_eventos()
            
            print(f"\nCiclo {self.paso_actual}:")
            print(f"Tiempo: {tiempo}")
            print(f"Entrada: {u}")
            print(f"Salida actual: {y[0][0]}")
            print(f"Error: {u - y[0][0]}")
            print(f"Dimensión del estado: {self.x.shape}")
            print("-" * 30)
            
        except Exception as e:
            print(f"Error en simulación: {str(e)}")
            self.timer.stop()
            if self.graficadora:
                QMessageBox.warning(self.graficadora, "Error de Simulación",
                                  f"Error durante la simulación: {str(e)}\nLa simulación se ha detenido.")
        
        ft_global = self.calcular_ft_global()
        self.crear_state_space(ft_global)

    
    def simular_sistema_completo(self):
        ft_global = self.calcular_ft_global()
        # Guardar el estado anterior si existe
        estado_anterior = self.x if hasattr(self, 'x') else None
        tam_anterior = estado_anterior.shape[0] if estado_anterior is not None else 0

        estado_medidor_anterior = self.x_medidor if hasattr(self, 'x_medidor') else None
        tam_medidor_anterior = estado_medidor_anterior.shape[0] if estado_medidor_anterior is not None else 0

        estado_controlador_anterior = self.x_controlador if hasattr(self, 'x_controlador') else None
        tam_controlador_anterior = estado_controlador_anterior.shape[0] if estado_controlador_anterior is not None else 0

        estado_actuador_anterior = self.x_actuador if hasattr(self, 'x_actuador') else None
        tam_actuador_anterior = estado_actuador_anterior.shape[0] if estado_actuador_anterior is not None else 0


        
        # Crear el nuevo sistema
        self.crear_state_space(ft_global)
        nuevo_tam = self.system_d.A.shape[0]
        nuevo_tam_medidor = self.system_d_medidor.A.shape[0]
        nuevo_tam_controlador = self.system_d_controlador.A.shape[0]
        nuevo_tam_actuador = self.system_d_actuador.A.shape[0]
        
        # Si tenemos un estado anterior y las dimensiones cambiaron
        if estado_anterior is not None and tam_anterior != nuevo_tam:
            self.x = self.redimensionar_estado(nuevo_tam, estado_anterior)
            print(f"Sistema redimensionado: {tam_anterior} -> {nuevo_tam} estados")
        else:
            # Primera inicialización
            self.x = np.zeros((nuevo_tam, 1))

        if estado_medidor_anterior is not None and tam_medidor_anterior != nuevo_tam_medidor:
            self.x_medidor = self.redimensionar_estado(nuevo_tam_medidor, estado_medidor_anterior)
            print(f"Sistema redimensionado: {tam_medidor_anterior} -> {nuevo_tam_medidor} estados")
        else:
            # Primera inicialización
            self.x_medidor = np.zeros((nuevo_tam_medidor, 1))

        if estado_controlador_anterior is not None and tam_controlador_anterior != nuevo_tam_controlador:
            self.x_controlador = self.redimensionar_estado(nuevo_tam_controlador, estado_controlador_anterior)
            print(f"Sistema redimensionado: {tam_controlador_anterior} -> {nuevo_tam_controlador} estados")
        else:
            # Primera inicialización
            self.x_controlador = np.zeros((nuevo_tam_controlador, 1))

        if estado_actuador_anterior is not None and tam_actuador_anterior != nuevo_tam_actuador:
            self.x_actuador = self.redimensionar_estado(nuevo_tam_actuador, estado_actuador_anterior)
            print(f"Sistema redimensionado: {tam_actuador_anterior} -> {nuevo_tam_actuador} estados")
        else:
            # Primera inicialización
            self.x_actuador = np.zeros((nuevo_tam_actuador, 1))
            
        if not hasattr(self, 'datos'):
            self.datos = {'tiempo': [], 'entrada': [], 'salida': [], 'error': [], 'carga': [], 'medidor': [], 'controlador': [], 'actuador': []}
        
        self.paso_actual = len(self.datos['tiempo'])  # Mantener el paso actual basado en los datos

    def simulacion_inicio_real(self):
        if self.precisa:
            self.simular_sistema_completo()
        else:
            self.simular_sistema_tiempo_real()
        self.timer.setInterval(int(self.velocidad))
        self.timer.start()



    def simular_sistema_tiempo_real(self):
        self.paso_actual = 1  # Reiniciar el contador de pasos
        self.y_salida = self.salida_cero  # Reiniciar el valor de salida
        self.datos = {'tiempo': [], 'controlador': [], 'actuador': [], 'proceso': [], 'medidor': [], 'entrada': [], 'error': [], 'salida': [], 'carga': []}

    
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