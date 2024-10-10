from PyQt5 import QtWidgets, QtCore
from back.topologia.microbloque import MicroBloque
from PyQt5 import QtWidgets, QtCore
from .latex_editor import LatexEditor
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
import os


class ElementoEntrada(QPushButton):
    
    def __init__(self, entrada):
        super().__init__()
        self.entrada = entrada
        self.tipo_entrada = "Personalizada"  # Añadimos este atributo
        self.coeficiente = "1"  # Añadimos este atributo
        
        self.setText(self.entrada.nombre)
        self.move(0, 210)
        self.setFixedSize(121, 41)
        self.clicked.connect(self.mousePressEvent)
        self.setStyleSheet("""
            background-color: #0072BB;;  /* Color de fondo azul /
            font-weight: bold;          /* Texto en negrita */
            font-weight: bold;          /* Texto en negrita */
            color: white;               /* Color de texto blanco */
            font-size: 15px;            /* Tamaño de fuente */
            font-family: Arial;  
        """)
      
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_entrada()        

    def mostrar_configuracion_entrada(self):
        dialog = ConfiguracionEntradaDialog(None, self.entrada, self.tipo_entrada, self.coeficiente)
        if dialog.exec_():
            self.entrada = dialog.entrada
            self.tipo_entrada = dialog.tipo_entrada
            self.coeficiente = dialog.coeficiente
            self.setText(self.entrada.nombre)
            
class ConfiguracionEntradaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, entrada=None, tipo_entrada="Personalizada",coeficiente="1"):
        super().__init__(parent)
        
        self.setWindowTitle("Configuración de Entrada")
        self.entrada = entrada if entrada else MicroBloque()
        self.tipo_entrada = tipo_entrada
        self.coeficiente = coeficiente
        self.initUI()

    def initUI(self):

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base', 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))

        layout = QtWidgets.QVBoxLayout()

        # Campo para el nombre
        nombre_layout = QtWidgets.QHBoxLayout()
        nombre_layout.addWidget(QtWidgets.QLabel("Nombre:"))
        self.nombre_input = QtWidgets.QLineEdit(self.entrada.nombre)
        nombre_layout.addWidget(self.nombre_input)
        layout.addLayout(nombre_layout)

        # Tipo de entrada
        tipo_entrada_layout = QtWidgets.QHBoxLayout()
        tipo_entrada_layout.addWidget(QtWidgets.QLabel("Tipo de entrada:"))
        self.tipo_entrada_combo = QtWidgets.QComboBox()
        self.tipo_entrada_combo.addItems(["Personalizada", "Escalón", "Rampa", "Parábola"])
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.tipo_entrada_combo.currentIndexChanged.connect(self.actualizar_interfaz)
        tipo_entrada_layout.addWidget(self.tipo_entrada_combo)
        layout.addLayout(tipo_entrada_layout)

        # Nuevo campo para el coeficiente
        coeficiente_layout = QtWidgets.QHBoxLayout()
        coeficiente_layout.addWidget(QtWidgets.QLabel("Coeficiente:"))
        self.coeficiente_input = QtWidgets.QLineEdit(self.coeficiente)
        self.coeficiente_input.setValidator(QtGui.QDoubleValidator())
        self.coeficiente_input.textChanged.connect(self.actualizar_funcion_transferencia)
        coeficiente_layout.addWidget(self.coeficiente_input)
        layout.addLayout(coeficiente_layout)

        # Función de transferencia con editor LaTeX
        ft_layout = QtWidgets.QVBoxLayout()
        ft_layout.addWidget(QtWidgets.QLabel("Función de transferencia:"))
        self.latex_editor = LatexEditor()
        self.latex_editor.set_latex(self.entrada.funcion_transferencia or "")
        self.latex_editor.setEnabled(self.tipo_entrada == "Personalizada")
        ft_layout.addWidget(self.latex_editor)
        layout.addLayout(ft_layout)

        # Botones OK y Cancelar
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #333; color: white;")
        
        # Actualizamos la interfaz según el tipo de entrada inicial
        self.actualizar_interfaz()

    def actualizar_interfaz(self):
        tipo_entrada = self.tipo_entrada_combo.currentText()
        es_personalizada = tipo_entrada == "Personalizada"
        
        self.latex_editor.setEnabled(es_personalizada)
        self.coeficiente_input.setEnabled(not es_personalizada)
        
        if not es_personalizada:
            self.actualizar_funcion_transferencia()
        else:
            self.latex_editor.set_latex(self.entrada.funcion_transferencia)

    def actualizar_funcion_transferencia(self):
        tipo_entrada = self.tipo_entrada_combo.currentText()
        coeficiente = self.coeficiente_input.text()
        
        if not coeficiente:
            coeficiente = "1"
        
        if tipo_entrada == "Escalón":
            latex = f"\\frac{{{coeficiente}}}{{s}}"
        elif tipo_entrada == "Rampa":
            latex = f"\\frac{{{coeficiente}}}{{s^2}}"
        elif tipo_entrada == "Parábola":
            latex = f"\\frac{{{coeficiente}}}{{s^3}}"
        else:
            return  # No actualizamos para entrada personalizada
        
        self.latex_editor.set_latex(latex)
        
    def accept(self):
        self.entrada.nombre = self.nombre_input.text()
        self.tipo_entrada = self.tipo_entrada_combo.currentText()
        
        if self.tipo_entrada == "Personalizada":
            self.entrada.funcion_transferencia = self.latex_editor.get_latex()
            self.coeficiente = "1"
        else:
            self.coeficiente = self.coeficiente_input.text() or "1"
            self.entrada.funcion_transferencia = self.latex_editor.get_latex()
        
        super().accept()
