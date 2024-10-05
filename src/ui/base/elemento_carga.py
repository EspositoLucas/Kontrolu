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
        self.coeficiente = "1"  # Añadimos este atributo
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
            self.setText(self.carga.nombre)

class ConfiguracionCargaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, carga=None, tipo_entrada="Personalizada", estado_seleccionado=None, coeficiente="1"):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Carga")
        self.carga = carga if carga else Carga()
        self.tipo_entrada = tipo_entrada
        self.estado_seleccionado = estado_seleccionado
        self.coeficiente = coeficiente
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
        
        # Añadimos el campo para el coeficiente
        coeficiente_layout = QtWidgets.QHBoxLayout()
        coeficiente_layout.addWidget(QtWidgets.QLabel("Coeficiente:"))
        self.coeficiente_input = QtWidgets.QLineEdit(self.coeficiente)
        self.coeficiente_input.setValidator(QtGui.QDoubleValidator())
        self.coeficiente_input.textChanged.connect(self.actualizar_funcion_transferencia)
        coeficiente_layout.addWidget(self.coeficiente_input)
        layout.addLayout(coeficiente_layout)

        # Tipo de entrada
        tipo_entrada_layout = QtWidgets.QHBoxLayout()
        tipo_entrada_layout.addWidget(QtWidgets.QLabel("Tipo de entrada:"))
        self.tipo_entrada_combo = QtWidgets.QComboBox()
        self.tipo_entrada_combo.addItems(["Personalizada", "Escalón", "Rampa", "Parábola"])
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.tipo_entrada_combo.currentIndexChanged.connect(self.actualizar_interfaz)
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
        estados_layout.addWidget(QtWidgets.QLabel("Estados:"))
        self.estados_list = QtWidgets.QListWidget()
        self.actualizar_lista_estados()
        estados_layout.addWidget(self.estados_list)

        # Botones para manejar estados
        botones_estados_layout = QtWidgets.QHBoxLayout()
        self.btn_agregar_estado = QtWidgets.QPushButton("Agregar Estado")
        self.btn_editar_estado = QtWidgets.QPushButton("Editar Estado")
        self.btn_eliminar_estado = QtWidgets.QPushButton("Eliminar Estado")
        
        self.btn_agregar_estado.clicked.connect(self.agregar_estado)
        self.btn_editar_estado.clicked.connect(self.editar_estado)
        self.btn_eliminar_estado.clicked.connect(self.eliminar_estado)
        
        botones_estados_layout.addWidget(self.btn_agregar_estado)
        botones_estados_layout.addWidget(self.btn_editar_estado)
        botones_estados_layout.addWidget(self.btn_eliminar_estado)
        
        estados_layout.addLayout(botones_estados_layout)
        layout.addLayout(estados_layout)

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
        
        # Actualizamos la interfaz según el tipo de entrada inicial
        self.actualizar_interfaz()
    
    def actualizar_lista_estados(self):
        self.estados_list.clear()
        for estado in self.carga.estados:
            item = QtWidgets.QListWidgetItem(f"{estado['nombre']} - Mín: {estado['minimo']}, Prioridad: {estado['prioridad']}")
            self.estados_list.addItem(item)

    def agregar_estado(self):
        dialog = EditarEstadoDialog(self)
        if dialog.exec_():
            nuevo_estado = {
                "nombre": dialog.nombre_input.text(),
                "minimo": float(dialog.minimo_input.text()),
                "prioridad": int(dialog.prioridad_input.text())
            }
            self.carga.estados.append(nuevo_estado)
            self.actualizar_lista_estados()

    def editar_estado(self):
        current_item = self.estados_list.currentItem()
        if current_item:
            index = self.estados_list.row(current_item)
            estado_actual = self.carga.estados[index]
            dialog = EditarEstadoDialog(self, estado_actual)
            if dialog.exec_():
                estado_actual["nombre"] = dialog.nombre_input.text()
                estado_actual["minimo"] = float(dialog.minimo_input.text())
                estado_actual["prioridad"] = int(dialog.prioridad_input.text())
                self.actualizar_lista_estados()

    def eliminar_estado(self):
        current_item = self.estados_list.currentItem()
        if current_item:
            index = self.estados_list.row(current_item)
            del self.carga.estados[index]
            self.actualizar_lista_estados()
    
    def actualizar_interfaz(self):
        tipo_entrada = self.tipo_entrada_combo.currentText()
        es_personalizada = tipo_entrada == "Personalizada"
        
        self.latex_editor.setEnabled(es_personalizada)
        self.coeficiente_input.setEnabled(not es_personalizada)
        
        if not es_personalizada:
            self.actualizar_funcion_transferencia()
        else:
            self.latex_editor.set_latex(self.carga.funcion_de_transferencia)

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

        if self.tipo_entrada == "Personalizada":
                self.carga.funcion_de_transferencia = self.latex_editor.get_latex()
                self.coeficiente = "1"
        else:
                self.coeficiente = self.coeficiente_input.text() or "1"
                self.entrada.funcion_transferencia = self.latex_editor.get_latex()
            
        # Guardamos el estado seleccionado
        current_item = self.estados_list.currentItem()
        if current_item:
            self.estado_seleccionado = current_item.text().split(' - ')[0]  # Obtenemos solo el nombre del estado
        else:
            self.estado_seleccionado = None  # O podrías establecer un valor predeterminado

        super().accept()
        
        
class EditarEstadoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, estado=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Estado" if estado else "Agregar Estado")
        self.estado = estado
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Nombre del estado
        nombre_layout = QtWidgets.QHBoxLayout()
        nombre_layout.addWidget(QtWidgets.QLabel("Nombre:"))
        self.nombre_input = QtWidgets.QLineEdit(self.estado["nombre"] if self.estado else "")
        nombre_layout.addWidget(self.nombre_input)
        layout.addLayout(nombre_layout)

        # Mínimo
        minimo_layout = QtWidgets.QHBoxLayout()
        minimo_layout.addWidget(QtWidgets.QLabel("Mínimo:"))
        self.minimo_input = QtWidgets.QLineEdit(str(self.estado["minimo"]) if self.estado else "")
        minimo_layout.addWidget(self.minimo_input)
        layout.addLayout(minimo_layout)

        # Prioridad
        prioridad_layout = QtWidgets.QHBoxLayout()
        prioridad_layout.addWidget(QtWidgets.QLabel("Prioridad:"))
        self.prioridad_input = QtWidgets.QLineEdit(str(self.estado["prioridad"]) if self.estado else "")
        prioridad_layout.addWidget(self.prioridad_input)
        layout.addLayout(prioridad_layout)

        # Botones OK y Cancelar
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)


