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
from PyQt5.QtCore import Qt

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
                cursor: pointer;
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
        
        # Agregar botón de ayuda en la parte superior
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.setToolTip("Ayuda sobre la configuración de perturbaciones")
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border: 2px solid #505050;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #606060;
                cursor: pointer;
            }
        """)
        help_button.clicked.connect(self.mostrar_ayuda)

        # Crear un layout horizontal para el botón de ayuda
        help_layout = QHBoxLayout()
        help_layout.addStretch()
        help_layout.addWidget(help_button)
        layout.addLayout(help_layout)

        # Función de Transferencia
        self.ft_label = QLabel("Respuesta de la perturbación:")
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
        self.ciclos_editor.setValue(int(self.perturbacion_back.inicio))
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

    def mostrar_ayuda(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Configuración de Perturbación")
        help_dialog.setStyleSheet(self.styleSheet())
        help_dialog.setMinimumWidth(500)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()
        
        # Título principal
        titulo = QLabel("Guía de Configuración de Perturbación")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        # Contenido organizado en secciones
        contenido = [
            ("<b>¿Qué es una perturbación?</b>", 
            "La perturbación representa una señal externa no deseada que afecta al sistema de control y debe ser compensada."),
            
            ("<b>Configuración temporal:</b>",
            "<ul>"
            "<li><b>Perturbar ahora:</b> Activa la perturbación inmediatamente al iniciar la simulación</li>"
            "<li><b>Tiempo de inicio:</b> Define cuando comenzará a actuar la perturbación (en segundos)</li>"
            "<li><b>Duración:</b> Establece por cuánto tiempo actuará la perturbación (en segundos)</li>"
            "</ul>"),
            
            ("<b>Respuesta de la perturbación:</b>",
            "<ul>"
            "<li>Define matemáticamente cómo la perturbación afecta al sistema</li>"
            "<li>Se escribe usando notación LaTeX para expresiones matemáticas</li>"
            "<li>Puede incluir variables s, exponentes, fracciones y otros operadores</li>"
            "<li>Ejemplo: Una perturbación constante sería 1/s</li>"
            "</ul>"),
            
            ("<b>Editor JSON:</b>",
            "Permite modificar directamente la configuración en formato JSON.")
        ]
        
        for titulo, texto in contenido:
            seccion = QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 5px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)
        
        # Botón de cerrar
        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)
        
        help_dialog.setLayout(layout)
        help_dialog.exec_()
        
    def aceptar(self):
        
        if not self.ft_editor.es_funcion_valida(self.ft_editor.get_latex()):
            QMessageBox.warning(self, "Respuesta de la perturbación inválida", 
                                "La respuesta de la perturbación no es válida. Por favor, corríjala antes de continuar.")
            return
        
        self.perturbacion_back.set_funcion_transferencia(self.ft_editor.get_latex())
        ahora = self.perturbar_ahora_checkbox.isChecked()
        inicio = self.ciclos_editor.value()
        duracion = self.dentro_de_editor.value()
        self.perturbacion_back.set_valores(inicio, duracion, ahora)
        self.accept()

    def actualizar_campos(self):
        self.ciclos_editor.setValue(int(self.perturbacion_back.inicio))
        self.dentro_de_editor.setValue(self.perturbacion_back.duracion)
        self.perturbar_ahora_checkbox.setChecked(self.perturbacion_back.ahora)
    
    
    def editar_json(self):
        vista = VistaJson(self.perturbacion_back, self)
        vista.exec_()
        if vista.result():
            self.actualizar_campos()