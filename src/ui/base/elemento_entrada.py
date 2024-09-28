from PyQt5 import QtWidgets, QtCore
from back.topologia.topologia_serie import MicroBloque
from PyQt5 import QtWidgets, QtCore
from .latex_editor import LatexEditor
from PyQt5 import QtWidgets, QtGui, QtCore
import os


class ElementoEntrada(QtWidgets.QGraphicsRectItem):
    def __init__(self, entrada):
        super().__init__(0, 0, 120, 60)
        self.entrada = entrada
        self.setPos(0, 200)
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 114, 187)))
        self.setPen(QtGui.QPen(QtCore.Qt.black))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.texto = QtWidgets.QGraphicsTextItem(self.entrada.nombre, self)
        self.texto.setPos(25, 12)
        font = QtGui.QFont("Arial", 13)
        font.setBold(True)
        self.texto.setFont(font)
        self.texto.setDefaultTextColor(QtGui.QColor(255, 255, 255))  # Color blanc
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_entrada()        

    def mostrar_configuracion_entrada(self):
        dialog = ConfiguracionEntradaDialog(None, self.entrada)
        if dialog.exec_():
            self.entrada = dialog.entrada
            self.texto.setPlainText(self.entrada.nombre)
            
class ConfiguracionEntradaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, entrada=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Entrada")
        self.entrada = entrada if entrada else MicroBloque()
        self.initUI()

    def initUI(self):
        # Configurar el estilo de la ventana
        self.setStyleSheet("background-color: #ADD8E6;")  # Color azul claro

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))

        layout = QtWidgets.QVBoxLayout()

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
        self.entrada.funcion_transferencia = self.latex_editor.get_latex()
        super().accept()
