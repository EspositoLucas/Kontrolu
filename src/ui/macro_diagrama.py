from PyQt5 import QtWidgets, QtCore
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.punto_suma import PuntoSuma
from .base.flecha import Flecha
from .base.latex_editor import LatexEditor
from PyQt5 import QtWidgets, QtGui, QtCore

class MacroDiagrama(QtWidgets.QWidget):
    def setupUi(self, mainWindow):
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, mainWindow)
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        
        # Modificar la creación de la flecha de entrada
        self.flecha_entrada = FlechaEntrada(QtCore.QPointF(110, 230), QtCore.QPointF(141, 230), 2, 2, 4)
        self.scene.addItem(self.flecha_entrada)
        
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
    
    def zoom_in(self):
        self.view.scale(1.25, 1.25)
        pass
    
class FlechaEntrada(Flecha):
    def __init__(self, start, end, width, height, arrow_size):
        super().__init__(start, end, width, height, arrow_size)
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.tipo_entrada_actual = "Escalón"  # Valor por defecto
        self.setToolTip("Haz click para configurar la entrada del sistema")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_entrada()

    def mostrar_configuracion_entrada(self):
        dialog = ConfiguracionEntradaDialog(self.scene().views()[0], self.tipo_entrada_actual)
        if dialog.exec_():
            self.tipo_entrada_actual = dialog.entrada_combo.currentText()

class ConfiguracionEntradaDialog(QtWidgets.QDialog):
        def __init__(self, parent=None, tipo_entrada_actual="Escalón"):
            super().__init__(parent)
            self.setWindowTitle("Parámetros de Entrada")
            self.tipo_entrada_actual = tipo_entrada_actual
            self.initUI()

        def initUI(self):
            layout = QtWidgets.QVBoxLayout()

            # Función de entrada
            entrada_layout = QtWidgets.QHBoxLayout()
            entrada_layout.addWidget(QtWidgets.QLabel("Función de entrada:"))
            self.entrada_combo = QtWidgets.QComboBox()
            self.entrada_combo.addItems(["Escalón", "Rampa", "Parábola", "Senoidal", "Impulso", "Personalizada"])
            self.entrada_combo.setCurrentText(self.tipo_entrada_actual)
            self.entrada_combo.currentIndexChanged.connect(self.toggle_input_method)
            entrada_layout.addWidget(self.entrada_combo)
            layout.addLayout(entrada_layout)
            

            # Stacked widget para alternar entre nada y editor LaTeX
            self.input_stack = QtWidgets.QStackedWidget()
            
            # Widget vacío para entradas no personalizadas
            empty_widget = QtWidgets.QWidget()
            self.input_stack.addWidget(empty_widget)

            # Widget para el editor LaTeX
            self.latex_widget = QtWidgets.QWidget()
            latex_layout = QtWidgets.QVBoxLayout(self.latex_widget)
            self.latex_editor = LatexEditor()
            latex_layout.addWidget(self.latex_editor)
            self.input_stack.addWidget(self.latex_widget)
            layout.addWidget(self.latex_widget)
            self.latex_widget.hide()  # Inicialmente oculto
            

            layout.addWidget(self.input_stack)

            # Botones OK y Cancelar
            button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)

            self.setLayout(layout)
            
            # Inicializar el estado correcto
            self.toggle_input_method(self.entrada_combo.currentIndex())

        def toggle_input_method(self, index):
            if self.entrada_combo.currentText() == "Personalizada":
                self.input_stack.setCurrentIndex(1)
                self.latex_widget.show()
            else:
                self.input_stack.setCurrentIndex(0)
                self.latex_widget.hide()