from PyQt5 import QtCore, QtWidgets
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.punto_suma import PuntoSuma
from .base.flecha import Flecha

class MacroDiagrama(QtWidgets.QWidget):
    def setupUi(self, mainWindow):

        # CONTROLADOR
        controlador = ElementoControl(mainWindow.sesion.controlador)
        controlador.setParent(mainWindow) # asigno al diagrama el objeto de la ventana principal
        self.controlador = controlador # asigno al diagrama el objeto del controlador (idem los demas)

        # ACTUADOR
        actuador = ElementoActuador(mainWindow.sesion.actuador)
        actuador.setParent(mainWindow)
        self.actuador = actuador 

        # PROCESO
        proceso = ElementoProceso(mainWindow.sesion.proceso)
        proceso.setParent(mainWindow)
        self.proceso = proceso

        # MEDIDOR
        medidor = ElementoMedicion(mainWindow.sesion.medidor)
        medidor.setParent(mainWindow)
        self.medidor = medidor
        
        # PUNTO SUMA
        puntoSuma = PuntoSuma(mainWindow.sesion.punto_suma)
        puntoSuma.setParent(mainWindow)
        self.puntoSuma = puntoSuma

        # LINEAS: 
        self.line = Flecha(QtCore.QPointF(341, 230), QtCore.QPointF(371, 230), 2, 2, 4) # controlador a actuador
        self.line.setParent(mainWindow)
        
        self.line_1 = Flecha(QtCore.QPointF(491, 230), QtCore.QPointF(521, 230), 2, 2, 4) # actuador a proceso
        self.line_1.setParent(mainWindow)

        self.line_2 = Flecha(QtCore.QPointF(661, 300), QtCore.QPointF(490, 300), 2, 2, 4) # proceso a medidor (lazo realimentado)
        self.line_2.setParent(mainWindow)

        self.line_3 = Flecha(QtCore.QPointF(600, 230), QtCore.QPointF(600, 230), 2, 2, 4) # proceso a salida
        self.line_3.setParent(mainWindow)

        self.line_4 = Flecha(QtCore.QPointF(370, 300), QtCore.QPointF(170, 300), 2, 2, 4) # medidor a punto suma (horizontal)
        self.line_4.setParent(mainWindow)

        self.line_5 = Flecha(QtCore.QPointF(165, 305), QtCore.QPointF(165, 257), 2, 2, 4) # medidor a punto suma (vertical)
        self.line_5.setParent(mainWindow)

        self.line_6 = Flecha(QtCore.QPointF(190, 230), QtCore.QPointF(221, 230),2, 2, 4) # punto suma a controlador
        self.line_6.setParent(mainWindow)

        self.line_7 = Flecha(QtCore.QPointF(110, 230), QtCore.QPointF(141, 230),2, 2, 4) # entrada a punto suma
        self.line_7.setParent(mainWindow)

        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    
    def mostrarElementos(self):
        self.controlador.show()
        self.actuador.show()
        self.proceso.show()
        self.medidor.show()
        self.puntoSuma.show()
        self.line.show()
        self.line_1.show()
        self.line_2.show()
        self.line_3.show()
        self.line_4.show()
        self.line_5.show()
        self.line_6.show()
        self.line_7.show()
        
