from PyQt5 import QtCore, QtWidgets
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.punto_suma import PuntoSuma

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

        # LINEAS
        self.line = QtWidgets.QFrame(mainWindow)
        self.line.setGeometry(QtCore.QRect(340, 210, 31, 41))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(mainWindow)
        self.line_2.setGeometry(QtCore.QRect(490, 210, 31, 41))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(mainWindow)
        self.line_3.setGeometry(QtCore.QRect(490, 280, 171, 41))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(mainWindow)
        self.line_4.setGeometry(QtCore.QRect(170, 280, 201, 41))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(mainWindow)
        self.line_5.setGeometry(QtCore.QRect(600, 230, 121, 71))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(mainWindow)
        self.line_6.setGeometry(QtCore.QRect(110, 260, 121, 41))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(mainWindow)
        self.line_7.setGeometry(QtCore.QRect(170, 280, 201, 41))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8 = QtWidgets.QFrame(mainWindow)
        self.line_8.setGeometry(QtCore.QRect(600, 230, 121, 71))
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9 = QtWidgets.QFrame(mainWindow)
        self.line_9.setGeometry(QtCore.QRect(110, 260, 121, 41))
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10 = QtWidgets.QFrame(mainWindow)
        self.line_10.setGeometry(QtCore.QRect(190, 210, 31, 41))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11 = QtWidgets.QFrame(mainWindow)
        self.line_11.setGeometry(QtCore.QRect(640, 210, 31, 41))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12 = QtWidgets.QFrame(mainWindow)
        self.line_12.setGeometry(QtCore.QRect(110, 220, 31, 41))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    
    def mostrarElementos(self):
        self.controlador.show()
        self.actuador.show()
        self.proceso.show()
        self.medidor.show()
        self.puntoSuma.show()
        self.line.show()
        self.line_2.show()
        self.line_3.show()
        self.line_4.show()
        self.line_5.show()
        self.line_6.show()
        self.line_7.show()
        self.line_8.show()
        self.line_9.show()
        self.line_10.show()
        self.line_11.show()
        self.line_12.show()
        
