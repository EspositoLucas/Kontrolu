from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from .base.elemento_control import ElementoControl
from .base.elemento_correccion import ElementoCorreccion
from .base.elemento_proceso import Proceso
from .base.elemento_medicion import ElementoMedicion


class MacroDiagrama(QWidget):
    def __init__(self,sesion):
        super().__init__()
        self.sesion = sesion
        self.generar_diagrama()


    def generar_diagrama(self):

        layout = QVBoxLayout(self) 
        
        control = ElementoControl(self.sesion.controlador)
        # self.addShape(control)
        correccion = ElementoCorreccion(self.sesion.actuador)
        # self.addShape(correccion)
        proceso = Proceso(self.sesion.proceso)
        # self.addShape(proceso)
        medicion = ElementoMedicion(self.sesion.mediciones)
        
        layout.addWidget(control)
        layout.addWidget(correccion)
        layout.addWidget(proceso)
        layout.addWidget(medicion)