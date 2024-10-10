from PyQt5.QtWidgets import (
    QGraphicsEllipseItem, 
    QMenu, 
    QAction, 
    QMessageBox, 
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QSpinBox, 
    QHBoxLayout, 
    QPushButton, 
    QGraphicsItem, 
    QGraphicsItemGroup,
    QGraphicsPolygonItem,
    QGraphicsLineItem,
    QGraphicsTextItem, QCheckBox
)
from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF, QFont
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import Qt
from .latex_editor import LatexEditor
from .vista_json import VistaJson

class EditarPerturbacion(QDialog):

    def __init__(self, padre, perturbacion_back):
        super().__init__(padre)
        self.padre = padre
        self.perturbacion_back = perturbacion_back
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Editar Perturbación")
        layout = QVBoxLayout()

        self.ft_label = QLabel("Función de Transferencia:")
        self.ft_label.setStyleSheet("color: white;")
        self.ft_editor = LatexEditor(self.perturbacion_back.funcion_transferencia)
        self.ft_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(self.ft_label)
        layout.addWidget(self.ft_editor)

        # Checkbox para "Perturbar ahora"
        self.perturbar_ahora_checkbox = QCheckBox("Perturbar ahora")
        self.perturbar_ahora_checkbox.setChecked(self.perturbacion_back.ahora)
        self.perturbar_ahora_checkbox.setStyleSheet("color: white;")
        layout.addWidget(self.perturbar_ahora_checkbox)

        # Editor de inicio de self.ciclos
        self.ciclos = QLabel("Tiempo de inicio (s):")
        self.ciclos.setStyleSheet("color: white;")
        self.ciclos_editor = QSpinBox()
        self.ciclos_editor.setValue(self.perturbacion_back.inicio)
        self.ciclos_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.ciclos_editor.setMinimum(0)
        layout.addWidget(self.ciclos)
        layout.addWidget(self.ciclos_editor)

        # Editor de duración
        self.dentro_de_label = QLabel("Duración (s):")
        self.dentro_de_editor = QSpinBox()
        self.dentro_de_editor.setValue(self.perturbacion_back.duracion)
        self.dentro_de_editor.setMinimum(0)
        self.dentro_de_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(self.dentro_de_label)
        layout.addWidget(self.dentro_de_editor)

        # Conectar el checkbox para ocultar/mostrar el editor de inicio
        def toggle_inicio_editor():
            self.ciclos.setVisible(not self.perturbar_ahora_checkbox.isChecked())
            self.ciclos_editor.setVisible(not self.perturbar_ahora_checkbox.isChecked())

        # Conectar el checkbox a la función para que oculte el editor de inicio
        self.perturbar_ahora_checkbox.stateChanged.connect(toggle_inicio_editor)
        toggle_inicio_editor()  # Para que se oculte/visualice según el estado inicial del checkbox

        buttons = QHBoxLayout()
        ok_button = QPushButton("Aceptar")
        cancel_button = QPushButton("Cancelar")
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        # Botón para editar JSON
        editar_json_button = QPushButton("Editar JSON")
        buttons.addWidget(editar_json_button)

        editar_json_button.clicked.connect(self.editar_json)

        self.setStyleSheet("background-color: #333; color: white;")
        self.setLayout(layout)

        ok_button.clicked.connect(self.aceptar)
        cancel_button.clicked.connect(self.reject)

            

    def aceptar(self):
        self.perturbacion_back.set_funcion_transferencia(self.ft_editor.get_latex())
        ahora = self.perturbar_ahora_checkbox.isChecked()
        inicio = self.ciclos_editor.value()
        duracion = self.dentro_de_editor.value()
        self.perturbacion_back.set_valores(inicio, duracion, ahora)
        self.accept()

    def actualizar_campos(self):
        self.ciclos_editor.setValue(self.perturbacion_back.inicio)
        self.dentro_de_editor.setValue(self.perturbacion_back.duracion)
        self.perturbar_ahora_checkbox.setChecked(self.perturbacion_back.ahora)
    
    
    def editar_json(self):
        vista = VistaJson(self.perturbacion_back, self)
        vista.exec_()
        if vista.result():
            self.actualizar_campos()