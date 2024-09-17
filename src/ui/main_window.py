# from PyQt5.QtWidgets import QMainWindow, QFileDialog, QToolBar, QPushButton, QVBoxLayout, QDialog, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox
# from PyQt5.QtCore import Qt
# from PyQt5 import QtGui
# from PyQt5.QtGui import QIcon
# import os
# from .menu.archivo import Archivo
# from .menu.menu_bar import Menu
# from .macro_diagrama import MacroDiagrama
# from back.simulacion import Simulacion
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import ctypes
# from back.simulacion import Simulacion
# import math
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('company.app.1')

# class MainWindow(QMainWindow):
#     def __init__(self,sesion):
#         super().__init__()
#         self.sesion = sesion
#         self.initUI()
        

#     def initUI(self):
#         self.setWindowTitle('Kontrolu')
#         self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
#         # Ruta de la imagen del logo
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base/imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(QIcon(icon))
    
#         menuBar = Menu(self)
#         self.setMenuBar(menuBar)

#         self.statusBar().showMessage('Listo')
        
#         self.init_macrobloques() # Diagrama inicial de lazo cerrado
#         boton_simulacion = QPushButton('Iniciar Simulación', self)
#         boton_simulacion.clicked.connect(self.iniciar_simulacion)
        
#         self.showMaximized() # se maximiza al final de todo, luego de cargar todos los elementos
    
        
#     def init_macrobloques(self):
#         self.diagrama = MacroDiagrama()
#         self.diagrama.setupUi(self)
#         self.setCentralWidget(self.diagrama)
#         self.diagrama.mostrarElementos()
#         self.diagrama.zoom_in()

#     def new_project(self):
#         self.statusBar().showMessage('Nuevo proyecto creado')

#     def open_project(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir Proyecto', '', 'Todos los archivos (*);;Archivos de Proyecto (*.prj)', options=options)
#         if file_name:
#             self.statusBar().showMessage(f'Proyecto {file_name} abierto')
#             # Lógica para abrir un proyecto
    
#     def save_project(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', '', 'Archivos de Proyecto (*.prj)', options=options)
#         if file_name:
#             self.statusBar().showMessage(f'Proyecto guardado en {file_name}')
#             # Lógica para guardar un proyecto

#     def iniciar_simulacion(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Parámetros de Simulación")
#         layout = QVBoxLayout()

#         # Función de entrada
#         entrada_layout = QHBoxLayout()
#         entrada_layout.addWidget(QLabel("Función de entrada:"))
#         entrada_combo = QComboBox()
#         entrada_combo.addItems(["Escalón", "Rampa", "Parábola", "Senoidal", "Impulso"])
#         entrada_layout.addWidget(entrada_combo)
#         layout.addLayout(entrada_layout)

#         # Coeficiente para escalón, rampa y parábola
#         coef_layout = QHBoxLayout()
#         coef_layout.addWidget(QLabel("Coeficiente:"))
#         coef_edit = QLineEdit()
#         coef_edit.setText("1")
#         coef_layout.addWidget(coef_edit)
#         layout.addLayout(coef_layout)

#         # Tiempo total
#         tiempo_layout = QHBoxLayout()
#         tiempo_layout.addWidget(QLabel("Tiempo total (s):"))
#         tiempo_edit = QLineEdit()
#         tiempo_edit.setText("10")
#         tiempo_layout.addWidget(tiempo_edit)
#         layout.addLayout(tiempo_layout)

#         # Delta t
#         dt_layout = QHBoxLayout()
#         dt_layout.addWidget(QLabel("Intervalo de tiempo (dt):"))
#         dt_edit = QLineEdit()
#         dt_edit.setText("0.01")
#         dt_layout.addWidget(dt_edit)
#         layout.addLayout(dt_layout)

#         # Setpoint
#         setpoint_layout = QHBoxLayout()
#         setpoint_layout.addWidget(QLabel("Valor de salida esperado:"))
#         setpoint_edit = QLineEdit()
#         setpoint_edit.setText("1")
#         setpoint_layout.addWidget(setpoint_edit)
#         layout.addLayout(setpoint_layout)

#         # Velocidad de animación
#         velocidad_layout = QHBoxLayout()
#         velocidad_layout.addWidget(QLabel("Velocidad de animación:"))
#         velocidad_combo = QComboBox()
#         velocidad_combo.addItems(["Lenta", "Normal", "Rápida"])
#         velocidad_layout.addWidget(velocidad_combo)
#         layout.addLayout(velocidad_layout)

#         # Botones OK y Cancelar
#         button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         button_box.accepted.connect(dialog.accept)
#         button_box.rejected.connect(dialog.reject)
#         layout.addWidget(button_box)

#         dialog.setLayout(layout)

#         if dialog.exec_():
#             entrada_tipo = entrada_combo.currentText()
#             coef = float(coef_edit.text())
#             t_total = float(tiempo_edit.text())
#             dt = float(dt_edit.text())
#             setpoint = float(setpoint_edit.text())
#             velocidad = velocidad_combo.currentText().lower()

#             if entrada_tipo == "Escalón":
#                 entrada = lambda t: coef
#             elif entrada_tipo == "Rampa":
#                 entrada = lambda t: coef * t
#             elif entrada_tipo == "Parábola":
#                 entrada = lambda t: coef * 0.5 * t**2 
#             elif entrada_tipo == "Senoidal":
#                 entrada = lambda t: math.sin(t)   
#             elif entrada_tipo == "Impulso":
#                 entrada = lambda t: 1 if abs(t) < dt/2 else 0
#             else:
#                 entrada = lambda t: 1  # Por defecto, escalón unitario

#             simulacion = Simulacion(self.sesion.controlador, self.sesion.actuador, self.sesion.proceso, self.sesion.medidor)
#             simulacion.ejecutar_simulacion(entrada=entrada, t_total=t_total, dt=dt, setpoint=setpoint, velocidad=velocidad)
#             self.statusBar().showMessage('Simulación completada')


# from PyQt5.QtWidgets import QMainWindow, QFileDialog, QToolBar, QPushButton, QVBoxLayout, QDialog, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox
# from PyQt5.QtCore import Qt
# from PyQt5 import QtGui
# from PyQt5.QtGui import QIcon
# import os
# from .menu.archivo import Archivo
# from .menu.menu_bar import Menu
# from .macro_diagrama import MacroDiagrama
# from back.simulacion import Simulacion
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import ctypes
# from back.simulacion import Simulacion
# import math
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('company.app.1')

# class MainWindow(QMainWindow):
#     def __init__(self,sesion):
#         super().__init__()
#         self.sesion = sesion
#         self.initUI()
        

#     def initUI(self):
#         self.setWindowTitle('Kontrolu')
#         self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
#         # Ruta de la imagen del logo
#         path = os.path.dirname(os.path.abspath(__file__))
#         image_path = os.path.join(path, 'base/imgs', 'logo.png')
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         self.setWindowIcon(QIcon(icon))
    
#         menuBar = Menu(self)
#         self.setMenuBar(menuBar)

#         self.statusBar().showMessage('Listo')
        
#         self.init_macrobloques() # Diagrama inicial de lazo cerrado
#         boton_simulacion = QPushButton('Iniciar Simulación', self)
#         boton_simulacion.clicked.connect(self.iniciar_simulacion)
        
#         self.showMaximized() # se maximiza al final de todo, luego de cargar todos los elementos
    
        
#     def init_macrobloques(self):
#         self.diagrama = MacroDiagrama()
#         self.diagrama.setupUi(self)
#         self.setCentralWidget(self.diagrama)
#         self.diagrama.mostrarElementos()
#         self.diagrama.zoom_in()

#     def new_project(self):
#         self.statusBar().showMessage('Nuevo proyecto creado')

#     def open_project(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir Proyecto', '', 'Todos los archivos (*);;Archivos de Proyecto (*.prj)', options=options)
#         if file_name:
#             self.statusBar().showMessage(f'Proyecto {file_name} abierto')
#             # Lógica para abrir un proyecto
    
#     def save_project(self):
#         options = QFileDialog.Options()
#         file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', '', 'Archivos de Proyecto (*.prj)', options=options)
#         if file_name:
#             self.statusBar().showMessage(f'Proyecto guardado en {file_name}')
#             # Lógica para guardar un proyecto

#     def iniciar_simulacion(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Parámetros de Simulación")
#         layout = QVBoxLayout()

#         # Función de entrada
#         entrada_layout = QHBoxLayout()
#         entrada_layout.addWidget(QLabel("Función de entrada:"))
#         entrada_combo = QComboBox()
#         entrada_combo.addItems(["Escalón", "Rampa", "Parábola", "Senoidal", "Impulso"])
#         entrada_layout.addWidget(entrada_combo)
#         layout.addLayout(entrada_layout)

#         # Coeficiente para escalón, rampa y parábola
#         coef_layout = QHBoxLayout()
#         coef_layout.addWidget(QLabel("Coeficiente:"))
#         coef_edit = QLineEdit()
#         coef_edit.setText("1")
#         coef_layout.addWidget(coef_edit)
#         layout.addLayout(coef_layout)

#         # Tiempo total
#         tiempo_layout = QHBoxLayout()
#         tiempo_layout.addWidget(QLabel("Tiempo total (s):"))
#         tiempo_edit = QLineEdit()
#         tiempo_edit.setText("10")
#         tiempo_layout.addWidget(tiempo_edit)
#         layout.addLayout(tiempo_layout)

#         # Delta t
#         dt_layout = QHBoxLayout()
#         dt_layout.addWidget(QLabel("Intervalo de tiempo (dt):"))
#         dt_edit = QLineEdit()
#         dt_edit.setText("0.01")
#         dt_layout.addWidget(dt_edit)
#         layout.addLayout(dt_layout)

#         # Setpoint
#         setpoint_layout = QHBoxLayout()
#         setpoint_layout.addWidget(QLabel("Valor de salida esperado:"))
#         setpoint_edit = QLineEdit()
#         setpoint_edit.setText("1")
#         setpoint_layout.addWidget(setpoint_edit)
#         layout.addLayout(setpoint_layout)

#         # Velocidad de animación
#         velocidad_layout = QHBoxLayout()
#         velocidad_layout.addWidget(QLabel("Velocidad de animación:"))
#         velocidad_combo = QComboBox()
#         velocidad_combo.addItems(["Lenta", "Normal", "Rápida"])
#         velocidad_layout.addWidget(velocidad_combo)
#         layout.addLayout(velocidad_layout)

#         # Botones OK y Cancelar
#         button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#         button_box.accepted.connect(dialog.accept)
#         button_box.rejected.connect(dialog.reject)
#         layout.addWidget(button_box)

#         dialog.setLayout(layout)

#         if dialog.exec_():
#             entrada_tipo = entrada_combo.currentText()
#             coef = float(coef_edit.text())
#             t_total = float(tiempo_edit.text())
#             dt = float(dt_edit.text())
#             setpoint = float(setpoint_edit.text())
#             velocidad = velocidad_combo.currentText().lower()

#             if entrada_tipo == "Escalón":
#                 entrada = lambda t: coef
#             elif entrada_tipo == "Rampa":
#                 entrada = lambda t: coef * t
#             elif entrada_tipo == "Parábola":
#                 entrada = lambda t: coef * 0.5 * t**2 
#             elif entrada_tipo == "Senoidal":
#                 entrada = lambda t: math.sin(t)   
#             elif entrada_tipo == "Impulso":
#                 entrada = lambda t: 1 if abs(t) < dt/2 else 0
#             else:
#                 entrada = lambda t: 1  # Por defecto, escalón unitario

            
#             simulacion = Simulacion(self.sesion.controlador, self.sesion.actuador, self.sesion.proceso, self.sesion.medidor, delta=dt, ciclos=int(t_total/dt))
#             simulacion.ejecutar_simulacion(entrada=entrada, t_total=t_total, dt=dt, setpoint=setpoint, velocidad=velocidad)
#             self.statusBar().showMessage('Simulación completada')


from PyQt5.QtWidgets import QMainWindow, QFileDialog, QToolBar, QPushButton, QVBoxLayout, QDialog, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox,QWidget,QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
import os
from .menu.archivo import Archivo
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama
from back.simulacion import Simulacion
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import ctypes
from back.simulacion import Simulacion
import math
from ui.base.latex_editor import LatexEditor
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('company.app.1')

class MainWindow(QMainWindow):
    def __init__(self,sesion):
        super().__init__()
        self.sesion = sesion
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Kontrolu')
        self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
        # Ruta de la imagen del logo
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base/imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QIcon(icon))
    
        menuBar = Menu(self)
        self.setMenuBar(menuBar)

        self.statusBar().showMessage('Listo')
        
        self.init_macrobloques() # Diagrama inicial de lazo cerrado
        boton_simulacion = QPushButton('Iniciar Simulación', self)
        boton_simulacion.clicked.connect(self.iniciar_simulacion)
        
        self.showMaximized() # se maximiza al final de todo, luego de cargar todos los elementos
    
        
    def init_macrobloques(self):
        self.diagrama = MacroDiagrama()
        self.diagrama.setupUi(self)
        self.setCentralWidget(self.diagrama)
        self.diagrama.mostrarElementos()
        self.diagrama.zoom_in()

    def new_project(self):
        self.statusBar().showMessage('Nuevo proyecto creado')

    def open_project(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Abrir Proyecto', '', 'Todos los archivos (*);;Archivos de Proyecto (*.prj)', options=options)
        if file_name:
            self.statusBar().showMessage(f'Proyecto {file_name} abierto')
            # Lógica para abrir un proyecto
    
    def save_project(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Guardar Proyecto', '', 'Archivos de Proyecto (*.prj)', options=options)
        if file_name:
            self.statusBar().showMessage(f'Proyecto guardado en {file_name}')
            # Lógica para guardar un proyecto

    def iniciar_simulacion(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Parámetros de Simulación")
        layout = QVBoxLayout()


        # Función de entrada
        entrada_layout = QHBoxLayout()
        entrada_layout.addWidget(QLabel("Función de entrada:"))
        self.entrada_combo = QComboBox()
        self.entrada_combo.addItems(["Escalón", "Rampa", "Parábola", "Senoidal", "Impulso", "Personalizada"])
        self.entrada_combo.currentIndexChanged.connect(self.toggle_input_method)
        entrada_layout.addWidget(self.entrada_combo)
        layout.addLayout(entrada_layout)

        # Stacked widget para alternar entre combo box y editor LaTeX
        self.input_stack = QStackedWidget()
        
        # Widget para el combo box
        combo_widget = QWidget()
        combo_layout = QHBoxLayout(combo_widget)
        self.coef_label = QLabel("Coeficiente:")
        self.coef_edit = QLineEdit()
        self.coef_edit.setText("1")
        combo_layout.addWidget(self.coef_label)
        combo_layout.addWidget(self.coef_edit)
        self.input_stack.addWidget(combo_widget)

        # Widget para el editor LaTeX
        latex_widget = QWidget()
        latex_layout = QVBoxLayout(latex_widget)
        self.latex_editor = LatexEditor()
        latex_layout.addWidget(self.latex_editor)
        self.input_stack.addWidget(latex_widget)

        layout.addWidget(self.input_stack)


        # Tiempo total
        tiempo_layout = QHBoxLayout()
        tiempo_layout.addWidget(QLabel("Tiempo total (s):"))
        tiempo_edit = QLineEdit()
        tiempo_edit.setText("10")
        tiempo_layout.addWidget(tiempo_edit)
        layout.addLayout(tiempo_layout)

        # Delta t
        dt_layout = QHBoxLayout()
        dt_layout.addWidget(QLabel("Intervalo de tiempo (dt):"))
        dt_edit = QLineEdit()
        dt_edit.setText("0.01")
        dt_layout.addWidget(dt_edit)
        layout.addLayout(dt_layout)

        # Setpoint
        setpoint_layout = QHBoxLayout()
        setpoint_layout.addWidget(QLabel("Valor de salida esperado:"))
        setpoint_edit = QLineEdit()
        setpoint_edit.setText("1")
        setpoint_layout.addWidget(setpoint_edit)
        layout.addLayout(setpoint_layout)

        # Velocidad de animación
        velocidad_layout = QHBoxLayout()
        velocidad_layout.addWidget(QLabel("Velocidad de animación:"))
        velocidad_combo = QComboBox()
        velocidad_combo.addItems(["Lenta", "Normal", "Rápida"])
        velocidad_layout.addWidget(velocidad_combo)
        layout.addLayout(velocidad_layout)

        # Botones OK y Cancelar
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)

        if dialog.exec_():
            entrada_tipo = self.entrada_combo.currentText()
            coef = float(self.coef_edit.text())
            t_total = float(tiempo_edit.text())
            dt = float(dt_edit.text())
            setpoint = float(setpoint_edit.text())
            velocidad = velocidad_combo.currentText().lower()

            if entrada_tipo == "Escalón":
                entrada = lambda t: coef
            elif entrada_tipo == "Rampa":
                entrada = lambda t: coef * t
            elif entrada_tipo == "Parábola":
                entrada = lambda t: coef * 0.5 * t**2 
            elif entrada_tipo == "Senoidal":
                entrada = lambda t: math.sin(t)   
            elif entrada_tipo == "Impulso":
                entrada = lambda t: 1 if abs(t) < dt/2 else 0
            else:
                entrada = lambda t: 1  # Por defecto, escalón unitario

            
            simulacion = Simulacion(self.sesion.controlador, self.sesion.actuador, self.sesion.proceso, self.sesion.medidor, delta=dt, ciclos=int(t_total/dt))
            simulacion.ejecutar_simulacion(entrada=entrada, t_total=t_total, dt=dt, setpoint=setpoint, velocidad=velocidad)
            self.statusBar().showMessage('Simulación completada')
            
    def toggle_input_method(self, index):
        if self.entrada_combo.currentText() == "Personalizada":
            self.input_stack.setCurrentIndex(1)
        else:
            self.input_stack.setCurrentIndex(0)

    def parse_latex_function(self, latex_func):
        # This is a placeholder. You'll need to implement proper LaTeX parsing.
        # For now, we'll assume the LaTeX is a valid Python expression
        return lambda t: eval(latex_func.replace('t', 'math.t'))