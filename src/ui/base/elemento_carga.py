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
        self.tipo_entrada = "Personalizada"  # Añadimos este atributo
        self.estado_seleccionado = self.carga.estados[0]["nombre"]  # Inicializamos con el primer estado
        
        
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
        dialog = ConfiguracionCargaDialog(None, self.carga, self.tipo_entrada, self.estado_seleccionado)
        if dialog.exec_():
            self.carga = dialog.carga
            self.tipo_entrada = dialog.tipo_entrada
            self.estado_seleccionado = dialog.estado_seleccionado
            # self.setText(self.carga.nombre)

class ConfiguracionCargaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, carga=None, tipo_entrada="Personalizada", estado_seleccionado=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Carga")
        self.carga = carga if carga else Carga()
        self.tipo_entrada = tipo_entrada
        self.estado_seleccionado = estado_seleccionado
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

        # Campo para el nombre
        nombre_layout = QtWidgets.QHBoxLayout()
        nombre_layout.addWidget(QtWidgets.QLabel("Nombre:"))
        self.nombre_input = QtWidgets.QLineEdit(self.carga.nombre)
        nombre_layout.addWidget(self.nombre_input)
        layout.addLayout(nombre_layout)

        # Tipo de carga
        tipo_carga_layout = QtWidgets.QHBoxLayout()
        tipo_carga_layout.addWidget(QtWidgets.QLabel("Tipo de carga:"))
        self.tipo_carga_combo = QtWidgets.QComboBox()
        self.tipo_carga_combo.addItems([tipo.value for tipo in TipoCarga])
        self.tipo_carga_combo.setCurrentText(self.carga.tipo_carga.value)
        tipo_carga_layout.addWidget(self.tipo_carga_combo)
        layout.addLayout(tipo_carga_layout)

        # Tipo de entrada
        tipo_entrada_layout = QtWidgets.QHBoxLayout()
        tipo_entrada_layout.addWidget(QtWidgets.QLabel("Tipo de entrada:"))
        self.tipo_entrada_combo = QtWidgets.QComboBox()
        self.tipo_entrada_combo.addItems(["Personalizada", "Escalón", "Rampa", "Parábola"])
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.tipo_entrada_combo.currentIndexChanged.connect(self.actualizar_funcion_transferencia)
        tipo_entrada_layout.addWidget(self.tipo_entrada_combo)
        layout.addLayout(tipo_entrada_layout)

        # Función de transferencia con editor LaTeX
        ft_layout = QtWidgets.QVBoxLayout()
        ft_layout.addWidget(QtWidgets.QLabel("Función de transferencia:"))
        self.latex_editor = LatexEditor()
        self.latex_editor.set_latex(self.carga.funcion_de_transferencia)
        ft_layout.addWidget(self.latex_editor)
        layout.addLayout(ft_layout)

        # Estados
        estados_layout = QtWidgets.QVBoxLayout()
        estados_layout.addWidget(QtWidgets.QLabel("Estado:"))
        self.estado_combo = QtWidgets.QComboBox()
        for estado in self.carga.estados:
            self.estado_combo.addItem(estado["nombre"])
        if self.estado_seleccionado:
            index = self.estado_combo.findText(self.estado_seleccionado)
            if index >= 0:
                self.estado_combo.setCurrentIndex(index)
        self.estado_combo.currentIndexChanged.connect(self.actualizar_info_estado)
        estados_layout.addWidget(self.estado_combo)

        self.info_estado_label = QtWidgets.QLabel()
        estados_layout.addWidget(self.info_estado_label)
        layout.addLayout(estados_layout)

        # Inicializamos la información del estado
        self.actualizar_info_estado()

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

    def actualizar_funcion_transferencia(self):
        tipo_entrada = self.tipo_entrada_combo.currentText()
        if tipo_entrada == "Escalón":
            self.latex_editor.set_latex("\\frac{1}{s}")
        elif tipo_entrada == "Rampa":
            self.latex_editor.set_latex("\\frac{1}{s^2}")
        elif tipo_entrada == "Parábola":
            self.latex_editor.set_latex("\\frac{1}{s^3}")
        self.latex_editor.setEnabled(tipo_entrada == "Personalizada")

    def actualizar_info_estado(self):
        estado_actual = self.carga.estados[self.estado_combo.currentIndex()]
        info = f"Mínimo: {estado_actual['minimo']}, Prioridad: {estado_actual['prioridad']}"
        self.info_estado_label.setText(info)

    def accept(self):
        # Actualizamos los valores de la carga con los nuevos datos
        self.carga.nombre = self.nombre_input.text()
        self.carga.tipo_carga = TipoCarga(self.tipo_carga_combo.currentText())
        self.carga.funcion_de_transferencia = self.latex_editor.get_latex()
        self.carga.escalamiento_sigmoide = float(self.escalamiento_sigmoide_input.text())
        self.carga.desplazamiento_sigmoide = float(self.desplazamiento_sigmoide_input.text())
        self.tipo_entrada = self.tipo_entrada_combo.currentText()
        
        # Guardamos el estado seleccionado
        self.estado_seleccionado = self.estado_combo.currentText()
        
        super().accept()