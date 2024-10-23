from PyQt5.QtWidgets import (
    QMessageBox, 
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QSpinBox, 
    QHBoxLayout, 
    QPushButton,
    QCheckBox
)
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
        
        # Establecer el estilo general del diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #B0B0B0;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #505050;
            }
            
            QPushButton {
                background-color: #808080;
                color: white;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 16px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
            
            QPushButton:hover {
                background-color: #606060;
            }
            
            QTextEdit {
        background-color: #FAF8F6;  /* Fondo blanco pastel */
    }
            
            QLabel {
                color: #2B2D42;
                background-color: transparent;
                font-size: 16px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
            
            QCheckBox {
                color: #2B2D42;
                font-size: 14px;
                font-family: "Segoe UI", "Arial", sans-serif;
                background-color: #FAF8F6;
            }
            
            QSpinBox {
                background-color: #D0D0D0;
                color: #2B2D42;
                border: 2px solid #505050;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                font-family: "Segoe UI", "Arial", sans-serif;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Espaciado entre widgets
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes del layout

        # Función de Transferencia
        self.ft_label = QLabel("Función de Transferencia:")
        self.ft_editor = LatexEditor(self.perturbacion_back.funcion_transferencia)
        self.ft_editor.setStyleSheet("""
            background-color: #D0D0D0;
            color: #2B2D42;
            border: 2px solid #505050;
            border-radius: 10px;
            padding: 8px;
            font-size: 14px;
            font-family: "Segoe UI", "Arial", sans-serif;
        """)
        layout.addWidget(self.ft_label)
        layout.addWidget(self.ft_editor)

        # Checkbox Perturbar ahora
        self.perturbar_ahora_checkbox = QCheckBox("Perturbar ahora")
        self.perturbar_ahora_checkbox.setChecked(self.perturbacion_back.ahora)
        layout.addWidget(self.perturbar_ahora_checkbox)

        # Tiempo de inicio
        self.ciclos = QLabel("Tiempo de inicio (s):")
        self.ciclos_editor = QSpinBox()
        self.ciclos_editor.setValue(self.perturbacion_back.inicio)
        self.ciclos_editor.setMinimum(0)
        layout.addWidget(self.ciclos)
        layout.addWidget(self.ciclos_editor)

        # Duración
        self.dentro_de_label = QLabel("Duración (s):")
        self.dentro_de_editor = QSpinBox()
        self.dentro_de_editor.setValue(self.perturbacion_back.duracion)
        self.dentro_de_editor.setMinimum(0)
        layout.addWidget(self.dentro_de_label)
        layout.addWidget(self.dentro_de_editor)

        # Función para toggle de visibilidad
        def toggle_inicio_editor():
            self.ciclos.setVisible(not self.perturbar_ahora_checkbox.isChecked())
            self.ciclos_editor.setVisible(not self.perturbar_ahora_checkbox.isChecked())

        # Conectar checkbox
        self.perturbar_ahora_checkbox.stateChanged.connect(toggle_inicio_editor)
        toggle_inicio_editor()

        # Botones
        buttons = QHBoxLayout()
        buttons.setSpacing(10)  # Espaciado entre botones
        
        ok_button = QPushButton("Aceptar")
        cancel_button = QPushButton("Cancelar")
        editar_json_button = QPushButton("Editar JSON")

        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        buttons.addWidget(editar_json_button)
        
        layout.addLayout(buttons)

        # Conectar señales de los botones
        editar_json_button.clicked.connect(self.editar_json)
        ok_button.clicked.connect(self.aceptar)
        cancel_button.clicked.connect(self.reject)

        self.setLayout(layout)

    def aceptar(self):
        
        if not self.ft_editor.es_funcion_valida(self.ft_editor.get_latex()):
            QMessageBox.warning(self, "Función de transferencia inválida", 
                                "La función de transferencia no es válida. Por favor, corríjala antes de continuar.")
            return
        
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