from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QToolBar, QHBoxLayout, QWidget, QPushButton,QGraphicsScene,QGraphicsView
from PyQt5.QtGui import QPen, QBrush, QPolygonF, QTransform, QPainter
from PyQt5.QtCore import Qt,QPointF

from .base.elemento_control import ElementoControl
from .base.elemento_correccion import ElementoCorreccion
from .base.elemento_proceso import Proceso
from .base.elemento_medicion import ElementoMedicion
from .base.flecha import Flecha


class MacroDiagrama(QGraphicsScene):
    def __init__(self,sesion,main_window):
        super().__init__(main_window)
        self.sesion = sesion
        self.initUI()
        self.generar_diagrama()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.show()

    def generar_diagrama(self):  
        
        # self.scene = QGraphicsScene()
        # self.view = QGraphicsView(self.scene)

        arrow = Flecha(QPointF(0, 0), QPointF(0, 100), 10, 30, 10)
        self.addItem(arrow)

        self.view.show()

        control = ElementoControl(self.sesion.controlador,self)
        correccion = ElementoCorreccion(self.sesion.actuador,self)
        proceso = Proceso(self.sesion.proceso,self)
        medicion = ElementoMedicion(self.sesion.mediciones,self)
        control.show()
        correccion.show()
        proceso.show()
        medicion.show()





    # def __init__(self, args):
    #     super().__init__(args)
        
    #     # Create the scene
    #     self.scene = QGraphicsScene()
        
    #     # Create a view to visualize the scene
    #     self.view = QGraphicsView(self.scene)
    #     self.view.setRenderHint(QPainter.Antialiasing)
    #     self.view.setWindowTitle("Arrow Line Example")
        
    #     # Add an arrow line to the scene
        
    #     arrow_line.addToScene(self.scene)
        
    #     # Show the view
    #     self.view.show()
