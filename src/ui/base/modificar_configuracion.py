from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt 
from back.topologia.configuraciones import Configuracion, TipoError



class ModificarConfiguracion(QDialog):

    def __init__(self,configuracion:Configuracion,tipo,padre):
        super().__init__(padre)
        self.configuracion:Configuracion = configuracion
        self.setWindowTitle(f"Editar Configuración de {tipo.capitalize()}")
        self.setStyleSheet(ESTILO)
        self.edit_configuration()
        
    
    def mostrar_ayuda(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Configuración")
        help_dialog.setStyleSheet("""
            QDialog {
                background-color: #B0B0B0;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #505050;
            }
        """)
        help_dialog.setMinimumWidth(600)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Guía de Configuración")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)

        # Contenido específico de configuraciones
        contenido = [
            ("<b>Configuraciones Activas:</b>",
            "<ul>"
            "<li><b>Proporción:</b> Factor de escala estático aplicado al error. Si se marca 'Default', se usa 1 como valor predeterminado.</li>"
            "<li><b>Probabilidad:</b> Factor que influye en la generación del error estocástico (para tipos Gauss y Aleatorio). Si se marca 'Default', se usa 1 como valor predeterminado.</li>"
            "<li><b>Tipo de desviación:</b> Define cómo se aplica el error o desvío en la simulación:"
            "<ul>"
            "<li>Ninguno: Error estático basado solo en la proporción</li>"
            "<li>Gauss: Error estocástico con distribución gaussiana</li>"
            "<li>Aleatorio: Error estocástico con distribución uniforme</li>"
            "</ul></li>"
            "</ul>"),
            
            ("<b>Modo de Simulación:</b>",
            "<ul>"
            "<li><b>Simulación Normal:</b> Modo estándar más rápido pero menos preciso. Los errores se calculan y aplican según las configuraciones anteriores.</li>"
            "<li><b>Simulación Precisa:</b> Modo optimizado que ofrece mayor precisión en aspectos derivativos del control, sin necesidad de configuraciones adicionales de error.</li>"
            "</ul>"),
            
            ("<b>Campos Informativos:</b>",
            "<ul>"
            "<li>Los siguientes campos se mantienen por compatibilidad con la simulación normal y actualmente son solo informativos:</li>"
            "<li>- Límite inferior</li>"
            "<li>- Límite superior</li>"
            "<li>- Límite por ciclo</li>"
            "<li>- Error máximo</li>"
            "<li>- Último valor</li>"
            "</ul>"
            "<br>"
            "<b>Notas importantes:</b>"
            "<ul>"
            "<li>Los errores se calculan y aplican una vez por ciclo de simulación</li>"
            "<li>El error se multiplica tanto a la entrada como a la salida de cada función de transferencia</li>"
            "<li>En la simulación precisa, estas configuraciones de error tienen un impacto reducido ya que el sistema prioriza la precisión matemática</li>"
            "</ul>")
        ]

        for titulo, texto in contenido:
            seccion = QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 10px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)

        # Botón de cerrar
        cerrar_btn = QPushButton("Cerrar")
        cerrar_btn.setStyleSheet("""
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
        """)
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)

        help_dialog.setLayout(layout)
        help_dialog.exec_()
        


    def edit_configuration(self):
        # Definición de estilos
        


        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Agregar botón de ayuda en la parte superior
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.setToolTip("Ayuda sobre la configuración del microbloque")
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
            }
        """)
        help_button.clicked.connect(self.mostrar_ayuda)
        
        # Crear un layout horizontal para el botón de ayuda
        help_layout = QHBoxLayout()
        help_layout.addStretch()
        help_layout.addWidget(help_button)
        self.layout.addLayout(help_layout)

        # Limite inferior
        self.limite_inf_row = QHBoxLayout()

        self.limite_inf_nombre = QLabel("Límite inferior")

        self.limite_inf_field = QLineEdit()
        self.limite_inf_field.setValidator(QDoubleValidator())
        self.limite_inf_field.setVisible(not self.configuracion.es_default_limite_inferior())
        self.limite_inf_field.setText("0" if self.configuracion.es_default_limite_inferior() else str(self.configuracion.limite_inferior))

        self.limite_inf_check = QCheckBox("Default")
        self.limite_inf_check.setChecked(self.configuracion.es_default_limite_inferior())
        self.limite_inf_check.stateChanged.connect(lambda state: self.limite_inf_field.setVisible(state == Qt.Unchecked))
        self.limite_inf_check.stateChanged.connect(lambda state: self.limite_inf_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_inferior)))

        self.limite_inf_row.addWidget(self.limite_inf_nombre)
        self.limite_inf_row.addWidget(self.limite_inf_field)
        self.limite_inf_row.addWidget(self.limite_inf_check)

        self.layout.addLayout(self.limite_inf_row)

        # Limite superior
        self.limite_sup_row = QHBoxLayout()

        self.limite_sup_nombre = QLabel("Límite superior")

        self.limite_sup_field = QLineEdit()
        self.limite_sup_field.setValidator(QDoubleValidator())
        self.limite_sup_field.setVisible(not self.configuracion.es_default_limite_superior())
        self.limite_sup_field.setText("0" if self.configuracion.es_default_limite_superior() else str(self.configuracion.limite_superior))

        self.limite_sup_check = QCheckBox("Default")
        self.limite_sup_check.setChecked(self.configuracion.es_default_limite_superior())
        self.limite_sup_check.stateChanged.connect(lambda state: self.limite_sup_field.setVisible(state == Qt.Unchecked))
        self.limite_sup_check.stateChanged.connect(lambda state: self.limite_sup_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_superior)))

        self.limite_sup_row.addWidget(self.limite_sup_nombre)
        self.limite_sup_row.addWidget(self.limite_sup_field)
        self.limite_sup_row.addWidget(self.limite_sup_check)

        self.layout.addLayout(self.limite_sup_row)

        # Limite por ciclo
        self.limite_ciclo_row = QHBoxLayout()
        
        self.limite_ciclo_nombre = QLabel("Límite por ciclo")

        self.limite_ciclo_field = QLineEdit()
        self.limite_ciclo_field.setValidator(QDoubleValidator())
        self.limite_ciclo_field.setVisible(not self.configuracion.es_default_limite_por_ciclo())
        self.limite_ciclo_field.setText("0" if self.configuracion.es_default_limite_por_ciclo() else str(self.configuracion.limite_por_ciclo))

        self.limite_ciclo_check = QCheckBox("Default")
        self.limite_ciclo_check.setChecked(self.configuracion.es_default_limite_por_ciclo())
        self.limite_ciclo_check.stateChanged.connect(lambda state: self.limite_ciclo_field.setVisible(state == Qt.Unchecked))
        self.limite_ciclo_check.stateChanged.connect(lambda state: self.limite_ciclo_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_por_ciclo)))

        self.limite_ciclo_row.addWidget(self.limite_ciclo_nombre)
        self.limite_ciclo_row.addWidget(self.limite_ciclo_field)
        self.limite_ciclo_row.addWidget(self.limite_ciclo_check)

        self.layout.addLayout(self.limite_ciclo_row)

        # Error máximo
        self.error_max_row = QHBoxLayout()

        self.error_max_nombre = QLabel("Error máximo")

        self.error_max_field = QLineEdit()
        self.error_max_field.setValidator(QDoubleValidator())
        self.error_max_field.setVisible(not self.configuracion.es_default_error_maximo())
        self.error_max_field.setText("0" if self.configuracion.es_default_error_maximo() else str(self.configuracion.error_maximo))

        self.error_max_check = QCheckBox("Default")
        self.error_max_check.setChecked(self.configuracion.es_default_error_maximo())
        self.error_max_check.stateChanged.connect(lambda state: self.error_max_field.setVisible(state == Qt.Unchecked))
        self.error_max_check.stateChanged.connect(lambda state: self.error_max_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.error_maximo)))

        self.error_max_row.addWidget(self.error_max_nombre)
        self.error_max_row.addWidget(self.error_max_field)
        self.error_max_row.addWidget(self.error_max_check)

        self.layout.addLayout(self.error_max_row)

        # Proporción
        self.proporcion_row = QHBoxLayout()
        
        self.proporcion_nombre = QLabel("Proporción")

        self.proporcion_field = QLineEdit()
        self.proporcion_field.setValidator(QDoubleValidator())
        self.proporcion_field.setVisible(not self.configuracion.es_default_proporcion())
        self.proporcion_field.setText("1" if self.configuracion.es_default_proporcion() else str(self.configuracion.proporcion))

        self.proporcion_check = QCheckBox("Default")
        self.proporcion_check.setChecked(self.configuracion.es_default_proporcion())
        self.proporcion_check.stateChanged.connect(lambda state: self.proporcion_field.setVisible(state == Qt.Unchecked))
        self.proporcion_check.stateChanged.connect(lambda state: self.proporcion_field.setText("1" if state == Qt.Unchecked else str(self.configuracion.proporcion)))

        self.proporcion_row.addWidget(self.proporcion_nombre)
        self.proporcion_row.addWidget(self.proporcion_field)
        self.proporcion_row.addWidget(self.proporcion_check)

        self.layout.addLayout(self.proporcion_row)

        # Último valor
        self.ultimo_valor_row = QHBoxLayout()

        self.ultimo_valor_nombre = QLabel("Último valor")

        self.ultimo_valor_field = QLineEdit()
        self.ultimo_valor_field.setValidator(QDoubleValidator())
        self.ultimo_valor_field.setVisible(not self.configuracion.es_default_ultimo_valor())
        self.ultimo_valor_field.setText("0" if self.configuracion.es_default_ultimo_valor() else str(self.configuracion.ultimo_valor))

        self.ultimo_valor_check = QCheckBox("Default")
        self.ultimo_valor_check.setChecked(self.configuracion.es_default_ultimo_valor())
        self.ultimo_valor_check.stateChanged.connect(lambda state: self.ultimo_valor_field.setVisible(state == Qt.Unchecked))
        self.ultimo_valor_check.stateChanged.connect(lambda state: self.ultimo_valor_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.ultimo_valor)))

        self.ultimo_valor_row.addWidget(self.ultimo_valor_nombre)
        self.ultimo_valor_row.addWidget(self.ultimo_valor_field)
        self.ultimo_valor_row.addWidget(self.ultimo_valor_check)

        self.layout.addLayout(self.ultimo_valor_row)

        # Probabilidad
        self.probabilidad_row = QHBoxLayout()

        self.probabilidad_nombre = QLabel("Probabilidad")
        
        self.probabilidad_field = QLineEdit()
        self.probabilidad_field.setValidator(QDoubleValidator())
        self.probabilidad_field.setVisible(not self.configuracion.es_default_probabilidad())
        self.probabilidad_field.setText("1" if self.configuracion.es_default_probabilidad() else str(self.configuracion.probabilidad))

        self.probabilidad_check = QCheckBox("Default")
        self.probabilidad_check.setChecked(self.configuracion.es_default_probabilidad())
        self.probabilidad_check.stateChanged.connect(lambda state: self.probabilidad_field.setVisible(state == Qt.Unchecked))
        self.probabilidad_check.stateChanged.connect(lambda state: self.probabilidad_field.setText("1" if state == Qt.Unchecked else str(self.configuracion.probabilidad)))

        self.probabilidad_row.addWidget(self.probabilidad_nombre)
        self.probabilidad_row.addWidget(self.probabilidad_field)
        self.probabilidad_row.addWidget(self.probabilidad_check)

        self.layout.addLayout(self.probabilidad_row)

        self.tipo_desbvio_box = QHBoxLayout()

        # Tipo de error
        tipo_error_label = QLabel("Tipo de Desviación: ")
        self.tipo_desbvio_box.addWidget(tipo_error_label)
        
        self.tipo_error_combo = QComboBox()
        for error_type in TipoError:
            self.tipo_error_combo.addItem(error_type.value)
        self.tipo_error_combo.setCurrentText(self.configuracion.tipo.value)
        self.tipo_desbvio_box.addWidget(self.tipo_error_combo)

        self.layout.addLayout(self.tipo_desbvio_box)

        # Botón guardar
        self.save_button = QPushButton("Guardar cambios")
        self.save_button.clicked.connect(self.save_configuration)

        
        self.layout.addWidget(self.save_button)


        self.setLayout(self.layout)
        self.exec_()

    
    def save_configuration(self):
        if self.limite_inf_check.isChecked():
            self.configuracion.default_limite_inferior()
        else:
            try:
                self.configuracion.limite_inferior = float(self.limite_inf_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Límite inferior")
                return

        if self.limite_sup_check.isChecked():
            self.configuracion.default_limite_superior()
        else:
            try:
                self.configuracion.limite_superior = float(self.limite_sup_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Límite superior")
                return

        if self.limite_ciclo_check.isChecked():
            self.configuracion.default_limite_por_ciclo()
        else:
            try:
                self.configuracion.limite_por_ciclo = float(self.limite_ciclo_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Límite por ciclo")
                return

        if self.error_max_check.isChecked():
            self.configuracion.default_error_maximo()
        else:
            try:
                self.configuracion.error_maximo = float(self.error_max_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Error máximo")
                return

        if self.proporcion_check.isChecked():
            self.configuracion.default_proporcion()
        else:
            try:
                self.configuracion.proporcion = float(self.proporcion_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Proporción")
                return

        if self.ultimo_valor_check.isChecked():
            self.configuracion.default_ultimo_valor()
        else:
            try:
                self.configuracion.ultimo_valor = float(self.ultimo_valor_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Último valor")
                return

        if self.probabilidad_check.isChecked():
            self.configuracion.default_probabilidad()
        else:
            try:
                self.configuracion.probabilidad = float(self.probabilidad_field.text())
            except ValueError:
                QMessageBox.warning(self, "Error", "Valor inválido para Probabilidad")
                return

        self.configuracion.tipo = TipoError(self.tipo_error_combo.currentText())
        self.accept()


ESTILO = """
    QCheckBox {
        spacing: 5px;  /* Espaciado entre el cuadro y el texto */
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tamaño de fuente */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía */
        font-weight: bold;  /* Texto en negrita */
    }

    QCheckBox::indicator {
        width: 20px;  /* Ancho del cuadro de verificación */
        height: 20px;  /* Alto del cuadro de verificación */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 5px;  /* Bordes redondeados */
        background-color: #FAF8F6;  /* Color de fondo del cuadro */
    }

    QCheckBox::indicator:checked {
        background-color: #808080;  /* Fondo gris oscuro cuando está marcado */
        border: 2px solid #505050;  /* Borde gris oscuro */
    }

    QCheckBox::indicator:unchecked {
        background-color: #FAF8F6;  /* Fondo claro cuando no está marcado */
    }



    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #707070;  /* Un gris más oscuro para mayor contraste */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;  /* Texto en negrita */
        font-family: "Segoe UI", "Arial", sans-serif;

    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
    }


    QLineEdit {
        background-color: #FAF8F6;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }
    
    QTextEdit {
        background-color: #FAF8F6;  /* Fondo blanco pastel */
    }

    QLabel {
        color: #2B2D42;  /* Texto gris oscuro */
        background-color: transparent;
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox {
        background-color: #D0D0D0;  /* Fondo gris claro */
        color: #2B2D42;  /* Texto gris oscuro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 5px;
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox QAbstractItemView {
        background-color: #D0D0D0;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: #2B2D42;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }

    QTabWidget::pane {
        border: 2px solid #505050;
        border-radius: 10px;
        background-color: #FAF8F6;
        padding: 10px;
    }

    QTabBar::tab {
        background-color: #D0D0D0;
        color: #2B2D42;
        border: 2px solid #505050;
        border-radius: 5px;
        padding: 12px 30px;  /* Aumentar el padding para más espacio */
        min-width: 140px;   /* Tamaño mínimo para evitar solapamiento */
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-weight: bold;  /* Texto en negrita */
    }


    QTabBar::tab:selected {
        background-color: #808080;  /* Fondo gris oscuro al seleccionar */
        color: white;  /* Texto en blanco en la pestaña seleccionada */
    }

    QTabBar::tab:hover {
        background-color: #606060;  /* Fondo gris más oscuro al pasar el cursor */
        color: white;  /* Texto en blanco al pasar el cursor */
    }


    QTableWidget {
        background-color: #FAF8F6;  /* Color de fondo del área sin celdas */
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        gridline-color: #505050;  /* Color de las líneas de la cuadrícula */
    }

    QTableWidget::item {
        background-color: #D0D0D0;  /* Color de fondo de las celdas */
        border: none;
    }

    QHeaderView::section {
        background-color: #808080;
        color: white;
        padding: 5px;
        border: 1px solid #505050;
    }

    QTableCornerButton::section {
        background-color: #808080;  /* Color del botón de esquina */
        border: 1px solid #505050;
    }


    QListWidget {
        background-color: #D0D0D0;
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QListWidget::item:selected {
        background-color: #808080;
        color: white;
    }
"""