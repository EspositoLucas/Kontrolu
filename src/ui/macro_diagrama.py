
from PyQt5 import QtWidgets, QtCore
from .base.elemento_control import ElementoControl
from .base.elemento_actuador import ElementoActuador
from .base.elemento_proceso import ElementoProceso
from .base.elemento_medicion import ElementoMedicion
from .base.punto_suma import PuntoSuma
from .base.flecha import Flecha
from .base.latex_editor import LatexEditor
from back.topologia.carga import Carga,TipoCarga
from back.topologia.topologia_serie import MicroBloque
from back.topologia.configuraciones import Configuracion
from PyQt5 import QtWidgets, QtGui, QtCore

class MacroDiagrama(QtWidgets.QWidget):
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi()
        
    def setupUi(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        self.setLayout(layout)
        
        # Modificar la creación de la flecha de entrada
        self.flecha_entrada = FlechaEntrada(QtCore.QPointF(110, 230), QtCore.QPointF(141, 230), 2, 2, 4,self.main_window)
        self.scene.addItem(self.flecha_entrada)
        
        # Modificar la creación de la flecha de salida
        self.flecha_salida = FlechaSalida(QtCore.QPointF(641,230), QtCore.QPointF(720, 230), 2, 2, 4, self.main_window)
        self.scene.addItem(self.flecha_salida)
        
        # CONTROLADOR
        controlador = ElementoControl(self.main_window.sesion.controlador)
        self.scene.addWidget(controlador)

        # ACTUADOR
        actuador = ElementoActuador(self.main_window.sesion.actuador)
        self.scene.addWidget(actuador)

        # PROCESO
        proceso = ElementoProceso(self.main_window.sesion.proceso)
        self.scene.addWidget(proceso)

        # MEDIDOR
        medidor = ElementoMedicion(self.main_window.sesion.medidor)
        self.scene.addWidget(medidor)

        # PUNTO SUMA
        puntoSuma = PuntoSuma(self.main_window.sesion.punto_suma)
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

        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    
    def mostrarElementos(self):
        for item in self.scene.items():
            if isinstance(item, QtWidgets.QWidget):
                item.show()
    
    def zoom_in(self):
        self.view.scale(1.25, 1.25)
        pass
    
class FlechaEntrada(Flecha):
    def __init__(self, start, end, width, height, arrow_size,main_window):
        super().__init__(start, end, width, height, arrow_size)
        self.main_window = main_window
        self.hover_color = QtGui.QColor(0, 128, 255)  # Azul claro para hover
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolTip("Haz click para configurar la entrada del sistema")
    
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        # Dibujar un pequeño triángulo en el punto de inicio
        triangle = QtGui.QPolygonF()
        triangle.append(self._sourcePoint)
        triangle.append(self._sourcePoint + QtCore.QPointF(-10, -5))
        triangle.append(self._sourcePoint + QtCore.QPointF(-10, 5))
        painter.setBrush(self.current_color)
        painter.drawPolygon(triangle)

    def shape(self):
        path = super().shape()
        triangle = QtGui.QPolygonF()
        triangle.append(self._sourcePoint)
        triangle.append(self._sourcePoint + QtCore.QPointF(-10, -5))
        triangle.append(self._sourcePoint + QtCore.QPointF(-10, 5))
        path.addPolygon(triangle)
        return path

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_entrada()

    def mostrar_configuracion_entrada(self):
        entrada_actual = self.main_window.sesion.entrada
        dialog = ConfiguracionEntradaDialog(self.main_window, entrada_actual)
        if dialog.exec_():
            # Actualizamos la entrada en la sesión con la nueva configuración
            self.main_window.entrada = dialog.entrada

class ConfiguracionEntradaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, entrada=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Entrada")
        self.entrada = entrada if entrada else MicroBloque()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Nombre de la entrada
        nombre_layout = QtWidgets.QHBoxLayout()
        nombre_layout.addWidget(QtWidgets.QLabel("Nombre:"))
        self.nombre_input = QtWidgets.QLineEdit(self.entrada.nombre)
        nombre_layout.addWidget(self.nombre_input)
        layout.addLayout(nombre_layout)

        # Función de transferencia con editor LaTeX
        ft_layout = QtWidgets.QVBoxLayout()
        ft_layout.addWidget(QtWidgets.QLabel("Función de transferencia:"))
        self.latex_editor = LatexEditor()
        self.latex_editor.set_latex(self.entrada.funcion_transferencia or "")
        ft_layout.addWidget(self.latex_editor)
        layout.addLayout(ft_layout)


        # Botones OK y Cancelar
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color_button.setStyleSheet(f"background-color: {color.name()}")
            self.entrada.color = color

    def accept(self):
        # Actualizamos los valores de la entrada con los nuevos datos
        self.entrada.nombre = self.nombre_input.text()
        self.entrada.funcion_transferencia = self.latex_editor.get_latex()
        super().accept()

class FlechaSalida(Flecha):
    def __init__(self, start, end, width, height, arrow_size, main_window):
        super().__init__(start, end, width, height, arrow_size)
        self.main_window = main_window
        self.hover_color = QtGui.QColor(57, 255, 20)  # verde para hover
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolTip("Haz click para configurar la carga del sistema")
    
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        # Dibujar un pequeño triángulo en el punto final
        triangle = QtGui.QPolygonF()
        triangle.append(self._destinationPoint)
        triangle.append(self._destinationPoint + QtCore.QPointF(10, -5))
        triangle.append(self._destinationPoint + QtCore.QPointF(10, 5))
        painter.setBrush(self.current_color)
        painter.drawPolygon(triangle)

    def shape(self):
        path = super().shape()
        triangle = QtGui.QPolygonF()
        triangle.append(self._destinationPoint)
        triangle.append(self._destinationPoint + QtCore.QPointF(10, -5))
        triangle.append(self._destinationPoint + QtCore.QPointF(10, 5))
        path.addPolygon(triangle)
        return path
        
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_carga()

    def mostrar_configuracion_carga(self):
        carga_actual = self.main_window.sesion.carga
        dialog = ConfiguracionCargaDialog(self.main_window, carga_actual)
        if dialog.exec_():
            # Actualizamos la carga en la sesión con la nueva configuración
            self.main_window.sesion.carga = dialog.carga

class ConfiguracionCargaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, carga=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Carga")
        self.carga = carga if carga else Carga()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Tipo de carga
        tipo_carga_layout = QtWidgets.QHBoxLayout()
        tipo_carga_layout.addWidget(QtWidgets.QLabel("Tipo de carga:"))
        self.tipo_carga_combo = QtWidgets.QComboBox()
        self.tipo_carga_combo.addItems([tipo.value for tipo in TipoCarga])
        self.tipo_carga_combo.setCurrentText(self.carga.tipo_carga.value)
        tipo_carga_layout.addWidget(self.tipo_carga_combo)
        layout.addLayout(tipo_carga_layout)

        # Función de transferencia con editor LaTeX
        ft_layout = QtWidgets.QVBoxLayout()
        ft_layout.addWidget(QtWidgets.QLabel("Función de transferencia:"))
        self.latex_editor = LatexEditor()
        self.latex_editor.set_latex(self.carga.funcion_de_transferencia)
        ft_layout.addWidget(self.latex_editor)
        layout.addLayout(ft_layout)

        # Escalamiento sigmoide
        es_layout = QtWidgets.QHBoxLayout()
        es_layout.addWidget(QtWidgets.QLabel("Escalamiento sigmoide:"))
        self.escalamiento_sigmoide_input = QtWidgets.QLineEdit(str(self.carga.escalamiento_sigmoide))
        es_layout.addWidget(self.escalamiento_sigmoide_input)
        layout.addLayout(es_layout)

        # Desplazamiento sigmoide
        ds_layout = QtWidgets.QHBoxLayout()
        ds_layout.addWidget(QtWidgets.QLabel("Desplazamiento sigmoide:"))
        self.desplazamiento_sigmoide_input = QtWidgets.QLineEdit(str(self.carga.desplazamiento_sigmoide))
        ds_layout.addWidget(self.desplazamiento_sigmoide_input)
        layout.addLayout(ds_layout)

        # Botones OK y Cancelar
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        
    def accept(self):
        # Actualizamos los valores de la carga con los nuevos datos
        self.carga.tipo_carga = TipoCarga(self.tipo_carga_combo.currentText())
        self.carga.funcion_de_transferencia = self.latex_editor.get_latex()
        self.carga.escalamiento_sigmoide = float(self.escalamiento_sigmoide_input.text())
        self.carga.desplazamiento_sigmoide = float(self.desplazamiento_sigmoide_input.text())
        super().accept()