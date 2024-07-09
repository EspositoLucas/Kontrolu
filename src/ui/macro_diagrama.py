from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.punto_suma import PuntoSuma
from .base.flecha import Flecha
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor
from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class MacroDiagrama(QtWidgets.QWidget):
    def setupUi(self, mainWindow):
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, mainWindow)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        
        # CONTROLADOR
        controlador = ElementoControl(mainWindow.sesion.controlador)
        self.scene.addWidget(controlador)

        # ACTUADOR
        actuador = ElementoActuador(mainWindow.sesion.actuador)
        self.scene.addWidget(actuador)

        # PROCESO
        proceso = ElementoProceso(mainWindow.sesion.proceso)
        self.scene.addWidget(proceso)

        # MEDIDOR
        medidor = ElementoMedicion(mainWindow.sesion.medidor)
        self.scene.addWidget(medidor)

        # PUNTO SUMA
        puntoSuma = PuntoSuma(mainWindow.sesion.punto_suma)
        self.scene.addWidget(puntoSuma)

        # LINEAS: 
        line = Flecha(QtCore.QPointF(341, 230), QtCore.QPointF(371, 230), 2, 2, 4) # controlador a actuador
        self.scene.addItem(line)
        
        self.line_1 = Flecha(QtCore.QPointF(491, 230), QtCore.QPointF(521, 230), 2, 2, 4) # actuador a proceso
        self.scene.addItem(self.line_1)

        self.line_2 = Flecha(QtCore.QPointF(681, 300), QtCore.QPointF(490, 300), 2, 2, 4,) # proceso a medidor (lazo realimentado - horizontal)
        self.scene.addItem(self.line_2)

        self.line_3 = Flecha(QtCore.QPointF(677, 235), QtCore.QPointF(677, 300), 2, 2, 4, arrow=False) # proceso a medidor (lazo realimentado - vertical)
        self.scene.addItem(self.line_3)

        self.line_4 = Flecha(QtCore.QPointF(641,230), QtCore.QPointF(720, 230), 2, 2, 4) # proceso a salida
        self.scene.addItem(self.line_4)

        self.line_5 = Flecha(QtCore.QPointF(370, 300), QtCore.QPointF(165, 300), 2, 2, 4, arrow=False) # medidor a punto suma (horizontal)
        self.scene.addItem(self.line_5)

        self.line_6 = Flecha(QtCore.QPointF(165, 304), QtCore.QPointF(165, 257), 2, 2, 4) # medidor a punto suma (vertical)
        self.scene.addItem(self.line_6)

        self.line_7 = Flecha(QtCore.QPointF(190, 230), QtCore.QPointF(221, 230),2, 2, 4) # punto suma a controlador
        self.scene.addItem(self.line_7)

        self.line_8 = Flecha(QtCore.QPointF(110, 230), QtCore.QPointF(141, 230),2, 2, 4) # entrada a punto suma
        self.scene.addItem(self.line_8)

        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    
    def mostrarElementos(self):
        for item in self.scene.items():
            if isinstance(item, QtWidgets.QWidget):
                item.show()
        
