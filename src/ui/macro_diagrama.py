from PyQt5 import QtCore, QtWidgets
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion

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
        
        # LINEAS
        self.line = QtWidgets.QFrame(mainWindow)
        self.line.setGeometry(QtCore.QRect(240, 210, 31, 41))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(mainWindow)
        self.line_2.setGeometry(QtCore.QRect(390, 210, 31, 41))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(mainWindow)
        self.line_3.setGeometry(QtCore.QRect(390, 280, 91, 41))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(mainWindow)
        self.line_4.setGeometry(QtCore.QRect(180, 280, 91, 41))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(mainWindow)
        self.line_5.setGeometry(QtCore.QRect(422, 250, 121, 51))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(mainWindow)
        self.line_6.setGeometry(QtCore.QRect(120, 250, 121, 51))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    
    def mostrarElementos(self):
        self.controlador.show()
        self.actuador.show()
        self.proceso.show()
        self.medidor.show()
        self.line.show()
        self.line_2.show()
        self.line_3.show()
        self.line_4.show()
        self.line_5.show()
        self.line_6.show()
        
