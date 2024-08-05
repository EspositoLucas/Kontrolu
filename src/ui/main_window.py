from PyQt5.QtWidgets import QMainWindow, QFileDialog, QToolBar, QPushButton
from PyQt5.QtCore import Qt
import os
from .menu.archivo import Archivo
from .menu.menu_bar import Menu
from .macro_diagrama import MacroDiagrama
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
import ctypes
from back.simulacion import Simulacion
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
        # self.setWindowIcon(icon)
        self.setWindowIcon(QtGui.QIcon(icon))
    
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
        simulacion = Simulacion(self.sesion.controlador, self.sesion.actuador, self.sesion.proceso, self.sesion.medidor)
        entrada = 1
        t_total = 10
        dt = 0.01
        simulacion.simular_sistema_tiempo_real(entrada=entrada, t_total=t_total, dt=dt)