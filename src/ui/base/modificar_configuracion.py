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
        


    def edit_configuration(self):
        
        self.layout = QVBoxLayout()

        # Limite inferior
        self.limite_inf_row = QHBoxLayout()

        self.limite_inf_nombre = QLabel("Límite inferior")
        self.limite_inf_nombre.setStyleSheet("color: white;")

        self.limite_inf_field = QLineEdit()
        self.limite_inf_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.limite_inf_field.setValidator(QDoubleValidator())
        self.limite_inf_field.setVisible(not self.configuracion.es_default_limite_inferior())  # Set visibility based on default status
        self.limite_inf_field.setText("0" if self.configuracion.es_default_limite_inferior() else str(self.configuracion.limite_inferior))  # Set initial value

        self.limite_inf_check = QCheckBox("Default")
        self.limite_inf_check.setChecked(self.configuracion.es_default_limite_inferior())
        self.limite_inf_check.setStyleSheet("color: white;")
        self.limite_inf_check.stateChanged.connect(lambda state: self.limite_inf_field.setVisible(state == Qt.Unchecked))
        self.limite_inf_check.stateChanged.connect(lambda state: self.limite_inf_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_inferior)))

        self.limite_inf_row.addWidget(self.limite_inf_nombre)
        self.limite_inf_row.addWidget(self.limite_inf_field)
        self.limite_inf_row.addWidget(self.limite_inf_check)

        self.layout.addLayout(self.limite_inf_row)

        # Limite superior
        self.limite_sup_row = QHBoxLayout()

        self.limite_sup_nombre = QLabel("Límite superior")
        self.limite_sup_nombre.setStyleSheet("color: white;")

        self.limite_sup_field = QLineEdit()
        self.limite_sup_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.limite_sup_field.setValidator(QDoubleValidator())
        self.limite_sup_field.setVisible(not self.configuracion.es_default_limite_superior())  # Set visibility based on default status
        self.limite_sup_field.setText("0" if self.configuracion.es_default_limite_superior() else str(self.configuracion.limite_superior))  # Set initial value

        self.limite_sup_check = QCheckBox("Default")
        self.limite_sup_check.setChecked(self.configuracion.es_default_limite_superior())
        self.limite_sup_check.setStyleSheet("color: white;")
        self.limite_sup_check.stateChanged.connect(lambda state: self.limite_sup_field.setVisible(state == Qt.Unchecked))
        self.limite_sup_check.stateChanged.connect(lambda state: self.limite_sup_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_superior)))

        self.limite_sup_row.addWidget(self.limite_sup_nombre)
        self.limite_sup_row.addWidget(self.limite_sup_field)
        self.limite_sup_row.addWidget(self.limite_sup_check)

        self.layout.addLayout(self.limite_sup_row)

        # Limite por ciclo
        self.limite_ciclo_row = QHBoxLayout()
        
        self.limite_ciclo_nombre = QLabel("Límite por ciclo")
        self.limite_ciclo_nombre.setStyleSheet("color: white;")

        self.limite_ciclo_field = QLineEdit()
        self.limite_ciclo_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.limite_ciclo_field.setValidator(QDoubleValidator())
        self.limite_ciclo_field.setVisible(not self.configuracion.es_default_limite_por_ciclo())  # Set visibility based on default status
        self.limite_ciclo_field.setText("0" if self.configuracion.es_default_limite_por_ciclo() else str(self.configuracion.limite_por_ciclo))  # Set initial value

        self.limite_ciclo_check = QCheckBox("Default")
        self.limite_ciclo_check.setChecked(self.configuracion.es_default_limite_por_ciclo())
        self.limite_ciclo_check.setStyleSheet("color: white;")
        self.limite_ciclo_check.stateChanged.connect(lambda state: self.limite_ciclo_field.setVisible(state == Qt.Unchecked))
        self.limite_ciclo_check.stateChanged.connect(lambda state: self.limite_ciclo_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.limite_por_ciclo)))

        self.limite_ciclo_row.addWidget(self.limite_ciclo_nombre)
        self.limite_ciclo_row.addWidget(self.limite_ciclo_field)
        self.limite_ciclo_row.addWidget(self.limite_ciclo_check)

        self.layout.addLayout(self.limite_ciclo_row)

        # Error máximo
        self.error_max_row = QHBoxLayout()

        self.error_max_nombre = QLabel("Error máximo")
        self.error_max_nombre.setStyleSheet("color: white;")

        self.error_max_field = QLineEdit()
        self.error_max_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.error_max_field.setValidator(QDoubleValidator())
        self.error_max_field.setVisible(not self.configuracion.es_default_error_maximo())  # Set visibility based on default status
        self.error_max_field.setText("0" if self.configuracion.es_default_error_maximo() else str(self.configuracion.error_maximo))  # Set initial value

        self.error_max_check = QCheckBox("Default")
        self.error_max_check.setChecked(self.configuracion.es_default_error_maximo())
        self.error_max_check.setStyleSheet("color: white;")
        self.error_max_check.stateChanged.connect(lambda state: self.error_max_field.setVisible(state == Qt.Unchecked))
        self.error_max_check.stateChanged.connect(lambda state: self.error_max_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.error_maximo)))

        self.error_max_row.addWidget(self.error_max_nombre)
        self.error_max_row.addWidget(self.error_max_field)
        self.error_max_row.addWidget(self.error_max_check)

        self.layout.addLayout(self.error_max_row)

        # Proporción
        self.proporcion_row = QHBoxLayout()
        
        self.proporcion_nombre = QLabel("Proporción")
        self.proporcion_nombre.setStyleSheet("color: white;")

        self.proporcion_field = QLineEdit()
        self.proporcion_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.proporcion_field.setValidator(QDoubleValidator())
        self.proporcion_field.setVisible(not self.configuracion.es_default_proporcion())  # Set visibility based on default status
        self.proporcion_field.setText("1" if self.configuracion.es_default_proporcion() else str(self.configuracion.proporcion))  # Set initial value

        self.proporcion_check = QCheckBox("Default")
        self.proporcion_check.setChecked(self.configuracion.es_default_proporcion())
        self.proporcion_check.setStyleSheet("color: white;")
        self.proporcion_check.stateChanged.connect(lambda state: self.proporcion_field.setVisible(state == Qt.Unchecked))
        self.proporcion_check.stateChanged.connect(lambda state: self.proporcion_field.setText("1" if state == Qt.Unchecked else str(self.configuracion.proporcion)))

        self.proporcion_row.addWidget(self.proporcion_nombre)
        self.proporcion_row.addWidget(self.proporcion_field)
        self.proporcion_row.addWidget(self.proporcion_check)

        self.layout.addLayout(self.proporcion_row)

        # Último valor
        self.ultimo_valor_row = QHBoxLayout()

        self.ultimo_valor_nombre = QLabel("Último valor")
        self.ultimo_valor_nombre.setStyleSheet("color: white;")

        self.ultimo_valor_field = QLineEdit()
        self.ultimo_valor_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.ultimo_valor_field.setValidator(QDoubleValidator())
        self.ultimo_valor_field.setVisible(not self.configuracion.es_default_ultimo_valor())  # Set visibility based on default status
        self.ultimo_valor_field.setText("0" if self.configuracion.es_default_ultimo_valor() else str(self.configuracion.ultimo_valor))  # Set initial value

        self.ultimo_valor_check = QCheckBox("Default")
        self.ultimo_valor_check.setChecked(self.configuracion.es_default_ultimo_valor())
        self.ultimo_valor_check.setStyleSheet("color: white;")
        self.ultimo_valor_check.stateChanged.connect(lambda state: self.ultimo_valor_field.setVisible(state == Qt.Unchecked))
        self.ultimo_valor_check.stateChanged.connect(lambda state: self.ultimo_valor_field.setText("0" if state == Qt.Unchecked else str(self.configuracion.ultimo_valor)))

        self.ultimo_valor_row.addWidget(self.ultimo_valor_nombre)
        self.ultimo_valor_row.addWidget(self.ultimo_valor_field)
        self.ultimo_valor_row.addWidget(self.ultimo_valor_check)

        self.layout.addLayout(self.ultimo_valor_row)

        # Probabilidad
        self.probabilidad_row = QHBoxLayout()

        self.probabilidad_nombre = QLabel("Probabilidad")
        self.probabilidad_nombre.setStyleSheet("color: white;")
        
        self.probabilidad_field = QLineEdit()
        self.probabilidad_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        self.probabilidad_field.setValidator(QDoubleValidator())
        self.probabilidad_field.setVisible(not self.configuracion.es_default_probabilidad())  # Set visibility based on default status
        self.probabilidad_field.setText("1" if self.configuracion.es_default_probabilidad() else str(self.configuracion.probabilidad))  # Set initial value

        self.probabilidad_check = QCheckBox("Default")
        self.probabilidad_check.setChecked(self.configuracion.es_default_probabilidad())
        self.probabilidad_check.setStyleSheet("color: white;")
        self.probabilidad_check.stateChanged.connect(lambda state: self.probabilidad_field.setVisible(state == Qt.Unchecked))
        self.probabilidad_check.stateChanged.connect(lambda state: self.probabilidad_field.setText("1" if state == Qt.Unchecked else str(self.configuracion.probabilidad)))

        self.probabilidad_row.addWidget(self.probabilidad_nombre)
        self.probabilidad_row.addWidget(self.probabilidad_field)
        self.probabilidad_row.addWidget(self.probabilidad_check)

        self.layout.addLayout(self.probabilidad_row)

        # Tipo de error
        self.tipo_error_combo = QComboBox()
        self.tipo_error_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        for error_type in TipoError:
            self.tipo_error_combo.addItem(error_type.value)
        self.tipo_error_combo.setCurrentText(self.configuracion.tipo.value)
        self.layout.addWidget(QLabel("Tipo de error"))
        self.layout.addWidget(self.tipo_error_combo)

        self.save_button = QPushButton("Guardar cambios")
        self.save_button.setStyleSheet("background-color: #444; color: white;")
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