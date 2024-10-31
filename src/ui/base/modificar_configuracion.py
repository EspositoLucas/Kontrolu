from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, QMessageBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt 
from back.topologia.configuraciones import Configuracion, TipoError



class ModificarConfiguracion(QDialog):

    def __init__(self,configuracion:Configuracion,tipo,padre):
        super().__init__(padre)
        self.configuracion:Configuracion = configuracion
        self.setWindowTitle(f"Editar Configuración de {tipo.capitalize()}")
        self.setStyleSheet("background-color: #333; color: white;")
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
            ("<b>Configuraciones de Entrada/Salida:</b>",
            "<ul>"
            "<li><b>Nombre de entrada/salida:</b> Identifica las variables de entrada y salida</li>"
            "<li><b>Unidades:</b> Especifica las unidades físicas de las variables</li>"
            "<li><b>Configuración avanzada:</b> Permite ajustar parámetros específicos mediante los botones 'Configurar'</li>"
            "</ul>"),
            
            ("<b>Configuración Avanzada:</b>",
            "<ul>"
            "<li><b>Límite inferior:</b> Define el valor mínimo permitido para la variable. Si se marca 'Default', se usa 0 como valor predeterminado.</li>"
            "<li><b>Límite superior:</b> Define el valor máximo permitido para la variable. Si se marca 'Default', se usa 0 como valor predeterminado.</li>"
            "<li><b>Límite por ciclo:</b> Establece la máxima variación permitida por ciclo de simulación. Si se marca 'Default', se usa 0 como valor predeterminado.</li>"
            "<li><b>Error máximo:</b> Define la tolerancia máxima de error permitida en los cálculos. Si se marca 'Default', se usa 0 como valor predeterminado.</li>"
            "<li><b>Proporción:</b> Factor de escala aplicado a los valores. Si se marca 'Default', se usa 1 como valor predeterminado.</li>"
            "<li><b>Último valor:</b> Almacena el último valor calculado para la variable. Si se marca 'Default', se usa 0 como valor predeterminado.</li>"
            "<li><b>Probabilidad:</b> Define la probabilidad de ocurrencia de ciertos eventos en la simulación. Si se marca 'Default', se usa 1 como valor predeterminado.</li>"
            "<li><b>Tipo de error:</b> Especifica cómo se manejan y calculan los errores en la simulación. Puede seleccionarse de una lista predefinida de tipos de error.</li>"
            "</ul>"
            "<br>"
            "<b>Notas importantes:</b>"
            "<ul>"
            "<li>Cada parámetro puede configurarse con un valor específico o usar su valor predeterminado mediante la casilla 'Default'.</li>"
            "<li>Los valores numéricos deben ser válidos para evitar errores en la configuración.</li>"
            "<li>La interfaz proporciona validación para asegurar que solo se ingresen valores numéricos válidos.</li>"
            "<li>Los cambios se aplican al presionar el botón 'Guardar cambios' y solo se guardarán si todos los valores son válidos.</li>"
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
                cursor: pointer;
            }
        """)
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)

        help_dialog.setLayout(layout)
        help_dialog.exec_()
        


    def edit_configuration(self):
        # Definición de estilos
        label_style = """
            color: #2B2D42;
            font-size: 16px;
            font-family: "Segoe UI", "Arial", sans-serif;
        """
        
        line_edit_style = """
            background-color: #D0D0D0;
            color: #2B2D42;
            border: 2px solid #505050;
            border-radius: 10px;
            padding: 8px;
            font-size: 14px;
            font-family: "Segoe UI", "Arial", sans-serif;
        """
        
        checkbox_style = """
            color: #2B2D42;
            background-color:#FAF8F6;
            font-size: 14px;
            font-family: "Segoe UI", "Arial", sans-serif;
        """
        
        combobox_style = """
            background-color: #D0D0D0;
            color: #2B2D42;
            border: 2px solid #505050;
            border-radius: 10px;
            padding: 5px;
            font-size: 14px;
            font-family: "Segoe UI", "Arial", sans-serif;
        """
        
        button_style = """
            background-color: #808080;
            color: white;
            border: 2px solid #505050;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            font-family: "Segoe UI", "Arial", sans-serif;
        """

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
                cursor: pointer;
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
        self.limite_inf_nombre.setStyleSheet(label_style)

        self.limite_inf_field = QLineEdit()
        self.limite_inf_field.setStyleSheet(line_edit_style)
        self.limite_inf_field.setValidator(QDoubleValidator())
        self.limite_inf_field.setVisible(not self.configuracion.es_default_limite_inferior())
        self.limite_inf_field.setText("0" if self.configuracion.es_default_limite_inferior() else str(self.configuracion.limite_inferior))

        self.limite_inf_check = QCheckBox("Default")
        self.limite_inf_check.setChecked(self.configuracion.es_default_limite_inferior())
        self.limite_inf_check.setStyleSheet(checkbox_style)
        self.limite_inf_check.stateChanged.connect(lambda state: self.limite_inf_field.setVisible(state == Qt.Unchecked))
        self.limite_inf_check.stateChanged.connect(lambda state: self.limite_inf_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_inferior)))

        self.limite_inf_row.addWidget(self.limite_inf_nombre)
        self.limite_inf_row.addWidget(self.limite_inf_field)
        self.limite_inf_row.addWidget(self.limite_inf_check)

        self.layout.addLayout(self.limite_inf_row)

        # Limite superior
        self.limite_sup_row = QHBoxLayout()

        self.limite_sup_nombre = QLabel("Límite superior")
        self.limite_sup_nombre.setStyleSheet(label_style)

        self.limite_sup_field = QLineEdit()
        self.limite_sup_field.setStyleSheet(line_edit_style)
        self.limite_sup_field.setValidator(QDoubleValidator())
        self.limite_sup_field.setVisible(not self.configuracion.es_default_limite_superior())
        self.limite_sup_field.setText("0" if self.configuracion.es_default_limite_superior() else str(self.configuracion.limite_superior))

        self.limite_sup_check = QCheckBox("Default")
        self.limite_sup_check.setChecked(self.configuracion.es_default_limite_superior())
        self.limite_sup_check.setStyleSheet(checkbox_style)
        self.limite_sup_check.stateChanged.connect(lambda state: self.limite_sup_field.setVisible(state == Qt.Unchecked))
        self.limite_sup_check.stateChanged.connect(lambda state: self.limite_sup_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_superior)))

        self.limite_sup_row.addWidget(self.limite_sup_nombre)
        self.limite_sup_row.addWidget(self.limite_sup_field)
        self.limite_sup_row.addWidget(self.limite_sup_check)

        self.layout.addLayout(self.limite_sup_row)

        # Limite por ciclo
        self.limite_ciclo_row = QHBoxLayout()
        
        self.limite_ciclo_nombre = QLabel("Límite por ciclo")
        self.limite_ciclo_nombre.setStyleSheet(label_style)

        self.limite_ciclo_field = QLineEdit()
        self.limite_ciclo_field.setStyleSheet(line_edit_style)
        self.limite_ciclo_field.setValidator(QDoubleValidator())
        self.limite_ciclo_field.setVisible(not self.configuracion.es_default_limite_por_ciclo())
        self.limite_ciclo_field.setText("0" if self.configuracion.es_default_limite_por_ciclo() else str(self.configuracion.limite_por_ciclo))

        self.limite_ciclo_check = QCheckBox("Default")
        self.limite_ciclo_check.setChecked(self.configuracion.es_default_limite_por_ciclo())
        self.limite_ciclo_check.setStyleSheet(checkbox_style)
        self.limite_ciclo_check.stateChanged.connect(lambda state: self.limite_ciclo_field.setVisible(state == Qt.Unchecked))
        self.limite_ciclo_check.stateChanged.connect(lambda state: self.limite_ciclo_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_por_ciclo)))

        self.limite_ciclo_row.addWidget(self.limite_ciclo_nombre)
        self.limite_ciclo_row.addWidget(self.limite_ciclo_field)
        self.limite_ciclo_row.addWidget(self.limite_ciclo_check)

        self.layout.addLayout(self.limite_ciclo_row)

        # Error máximo
        self.error_max_row = QHBoxLayout()

        self.error_max_nombre = QLabel("Error máximo")
        self.error_max_nombre.setStyleSheet(label_style)

        self.error_max_field = QLineEdit()
        self.error_max_field.setStyleSheet(line_edit_style)
        self.error_max_field.setValidator(QDoubleValidator())
        self.error_max_field.setVisible(not self.configuracion.es_default_error_maximo())
        self.error_max_field.setText("0" if self.configuracion.es_default_error_maximo() else str(self.configuracion.error_maximo))

        self.error_max_check = QCheckBox("Default")
        self.error_max_check.setChecked(self.configuracion.es_default_error_maximo())
        self.error_max_check.setStyleSheet(checkbox_style)
        self.error_max_check.stateChanged.connect(lambda state: self.error_max_field.setVisible(state == Qt.Unchecked))
        self.error_max_check.stateChanged.connect(lambda state: self.error_max_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.error_maximo)))

        self.error_max_row.addWidget(self.error_max_nombre)
        self.error_max_row.addWidget(self.error_max_field)
        self.error_max_row.addWidget(self.error_max_check)

        self.layout.addLayout(self.error_max_row)

        # Proporción
        self.proporcion_row = QHBoxLayout()
        
        self.proporcion_nombre = QLabel("Proporción")
        self.proporcion_nombre.setStyleSheet(label_style)

        self.proporcion_field = QLineEdit()
        self.proporcion_field.setStyleSheet(line_edit_style)
        self.proporcion_field.setValidator(QDoubleValidator())
        self.proporcion_field.setVisible(not self.configuracion.es_default_proporcion())
        self.proporcion_field.setText("1" if self.configuracion.es_default_proporcion() else str(self.configuracion.proporcion))

        self.proporcion_check = QCheckBox("Default")
        self.proporcion_check.setChecked(self.configuracion.es_default_proporcion())
        self.proporcion_check.setStyleSheet(checkbox_style)
        self.proporcion_check.stateChanged.connect(lambda state: self.proporcion_field.setVisible(state == Qt.Unchecked))
        self.proporcion_check.stateChanged.connect(lambda state: self.proporcion_field.setText("1" if state == Qt.Unchecked else str(self.configuracion.proporcion)))

        self.proporcion_row.addWidget(self.proporcion_nombre)
        self.proporcion_row.addWidget(self.proporcion_field)
        self.proporcion_row.addWidget(self.proporcion_check)

        self.layout.addLayout(self.proporcion_row)

        # Último valor
        self.ultimo_valor_row = QHBoxLayout()

        self.ultimo_valor_nombre = QLabel("Último valor")
        self.ultimo_valor_nombre.setStyleSheet(label_style)

        self.ultimo_valor_field = QLineEdit()
        self.ultimo_valor_field.setStyleSheet(line_edit_style)
        self.ultimo_valor_field.setValidator(QDoubleValidator())
        self.ultimo_valor_field.setVisible(not self.configuracion.es_default_ultimo_valor())
        self.ultimo_valor_field.setText("0" if self.configuracion.es_default_ultimo_valor() else str(self.configuracion.ultimo_valor))

        self.ultimo_valor_check = QCheckBox("Default")
        self.ultimo_valor_check.setChecked(self.configuracion.es_default_ultimo_valor())
        self.ultimo_valor_check.setStyleSheet(checkbox_style)
        self.ultimo_valor_check.stateChanged.connect(lambda state: self.ultimo_valor_field.setVisible(state == Qt.Unchecked))
        self.ultimo_valor_check.stateChanged.connect(lambda state: self.ultimo_valor_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.ultimo_valor)))

        self.ultimo_valor_row.addWidget(self.ultimo_valor_nombre)
        self.ultimo_valor_row.addWidget(self.ultimo_valor_field)
        self.ultimo_valor_row.addWidget(self.ultimo_valor_check)

        self.layout.addLayout(self.ultimo_valor_row)

        # Probabilidad
        self.probabilidad_row = QHBoxLayout()

        self.probabilidad_nombre = QLabel("Probabilidad")
        self.probabilidad_nombre.setStyleSheet(label_style)
        
        self.probabilidad_field = QLineEdit()
        self.probabilidad_field.setStyleSheet(line_edit_style)
        self.probabilidad_field.setValidator(QDoubleValidator())
        self.probabilidad_field.setVisible(not self.configuracion.es_default_probabilidad())
        self.probabilidad_field.setText("1" if self.configuracion.es_default_probabilidad() else str(self.configuracion.probabilidad))

        self.probabilidad_check = QCheckBox("Default")
        self.probabilidad_check.setChecked(self.configuracion.es_default_probabilidad())
        self.probabilidad_check.setStyleSheet(checkbox_style)
        self.probabilidad_check.stateChanged.connect(lambda state: self.probabilidad_field.setVisible(state == Qt.Unchecked))
        self.probabilidad_check.stateChanged.connect(lambda state: self.probabilidad_field.setText("1" if state == Qt.Unchecked else str(self.configuracion.probabilidad)))

        self.probabilidad_row.addWidget(self.probabilidad_nombre)
        self.probabilidad_row.addWidget(self.probabilidad_field)
        self.probabilidad_row.addWidget(self.probabilidad_check)

        self.layout.addLayout(self.probabilidad_row)

        # Tipo de error
        tipo_error_label = QLabel("Tipo de error")
        tipo_error_label.setStyleSheet(label_style)
        self.layout.addWidget(tipo_error_label)
        
        self.tipo_error_combo = QComboBox()
        self.tipo_error_combo.setStyleSheet(combobox_style)
        for error_type in TipoError:
            self.tipo_error_combo.addItem(error_type.value)
        self.tipo_error_combo.setCurrentText(self.configuracion.tipo.value)
        self.layout.addWidget(self.tipo_error_combo)

        # Botón guardar
        self.save_button = QPushButton("Guardar cambios")
        self.save_button.setStyleSheet(button_style)
        self.save_button.clicked.connect(self.save_configuration)
        
        # Agregar efecto hover al botón
        self.save_button.enterEvent = lambda e: self.save_button.setStyleSheet(
            button_style + "background-color: #606060;"
        )
        self.save_button.leaveEvent = lambda e: self.save_button.setStyleSheet(button_style)
        
        self.layout.addWidget(self.save_button)

        # Estilo del diálogo principal
        self.setStyleSheet("""
            QDialog {
                background-color: #B0B0B0;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #505050;
            }
            
            QTextEdit {
        background-color: #FAF8F6;  /* Fondo blanco pastel */
    }
        """)

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