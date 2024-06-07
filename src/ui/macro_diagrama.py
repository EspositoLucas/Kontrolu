from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QHBoxLayout, QWidget, QPushButton
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
        self.initUI()
        self.generar_diagrama()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.show()

    def generar_diagrama(self):  
        control = ElementoControl(self.sesion.controlador)
        correccion = ElementoCorreccion(self.sesion.actuador)
        proceso = Proceso(self.sesion.proceso)
        medicion = ElementoMedicion(self.sesion.mediciones)

        control.setParent(self)
        correccion.setParent(self)
        proceso.setParent(self)
        medicion.setParent(self)
        
        