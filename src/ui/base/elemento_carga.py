from PyQt5 import QtWidgets, QtCore
from .latex_editor import LatexEditor
from back.topologia.carga import Carga,TipoCarga
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
import os


class ElementoCarga(QPushButton):
    def __init__(self, carga):
        super().__init__()
        self.carga = carga
        
        self.setText(self.carga.nombre)
        self.move(700, 210)
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
            self.mostrar_configuracion_carga()

    def mostrar_configuracion_carga(self):
        dialog = ConfiguracionCargaDialog(None, self.carga)
        if dialog.exec_():
            self.carga = dialog.carga

class ConfiguracionCargaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, carga=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Carga")
        self.carga = carga if carga else Carga()
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
