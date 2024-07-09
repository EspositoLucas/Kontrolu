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

class MainWindow(QMainWindow):
    def __init__(self,sesion):
        super().__init__()
        self.sesion = sesion
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Kontrolu')
        self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro
        
        #self.setStyleSheet("""
        #background-color: qradialgradient(
        #cx: 0.5, cy: 0.5, radius: 0.5,
        #fx: 0.5, fy: 0.5,
        #stop: 0 #ADD8E6,
        #stop: 1 #4B86B4
        #    );
        #""")
       
        # Ruta de la imagen del logo
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base/imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
    
        menuBar = Menu(self)
        self.setMenuBar(menuBar)

        self.statusBar().showMessage('Listo')
        
        # Diagrama inicial de lazo cerrado
        self.init_macrobloques()
        
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