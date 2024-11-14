from PyQt5 import QtWidgets, QtCore
from .latex_editor import LatexEditor
from back.topologia.carga import Carga,TipoCarga
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton,QMessageBox
from ..base.vista_json import VistaJson
from ..base.macro_vista import MacroVista
import os
from PyQt5.QtCore import QRectF
import re
from PyQt5.QtCore import Qt


class ElementoCarga(MacroVista):
    def __init__(self, carga,pos,padre):

        MacroVista.__init__(self, carga, pos,padre)
        self.carga = carga
        self.coeficiente = "1"  # Añadimos este atributo
        self.estado_seleccionado = self.carga.estados[0]["nombre"]  # Inicializamos con el primer estado
        


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_carga()

    def mostrar_configuracion_carga(self):
        # Guardar una copia de los estados antes de abrir el diálogo
        estados_originales = list(self.carga.estados)

        dialog = ConfiguracionCargaDialog(self, self.carga, self.estado_seleccionado)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        if dialog.exec_():
            # Solo se aplica la configuración si se da a OK
            self.carga = dialog.carga
            self.tipo_entrada = dialog.tipo_entrada
            self.estado_seleccionado = dialog.estado_seleccionado
        else:
            # Restaurar los estados originales si se cancela
            self.carga.estados = estados_originales
        self.updateText()
class ConfiguracionCargaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, carga=None, estado_seleccionado=None):
        super().__init__()
        self.padre = parent
        self.setWindowTitle("Configuración de Rendimiento")
        self.carga = carga
        self.tipo_entrada, self.coeficiente = self.determinar_tipo_funcion(carga.funcion_transferencia)
        self.estado_seleccionado = estado_seleccionado
        self.initUI()
    
    def determinar_tipo_funcion(self, latex_funcion):
        if not latex_funcion or latex_funcion == "" or latex_funcion == " ":
            return "Misma que entrada", "1"
        
        #chequar si no tiene s es impulso
        if "s" not in latex_funcion:
            return "Impulso", latex_funcion
        match = re.match(r"\\frac\{(.+?)\}\{s(?:\^(\d+))?\}", latex_funcion)
        if match:
            coeficiente = match.group(1)
            exponente = match.group(2)
            if exponente == "1" or exponente is None:
                return "Escalón", coeficiente
            elif exponente == "2":
                return "Rampa", coeficiente
            elif exponente == "3":
                return "Parabólica", coeficiente
        
        return "Personalizada", "1"

    def initUI(self):
        
        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))
        
        layout = QtWidgets.QVBoxLayout()

        help_button = QPushButton("?", self)
        help_button.setToolTip("Haga clic para ver información detallada sobre la configuración de carga")  # Mensaje de ayuda
        help_button.setFixedSize(30, 30)  # Tamaño del botón
        help_button.move(50, 50)  # Posición del botón en la ventana
        help_button.clicked.connect(self.mostrar_ayuda) 
        # Estilo del botón para darle apariencia de botón de ayuda
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)
        layout.addWidget(help_button)
        # Campo para el nombre
        nombre_layout = QtWidgets.QHBoxLayout()
        nombre_layout.addWidget(QtWidgets.QLabel("Nombre:"))
        self.nombre_input = QtWidgets.QLineEdit(self.carga.nombre)
        nombre_layout.addWidget(self.nombre_input)
        layout.addLayout(nombre_layout)

        # Tipo de carga
        tipo_carga_layout = QtWidgets.QHBoxLayout()
        tipo_carga_layout.addWidget(QtWidgets.QLabel("Tipo de evaluación del rendimiento:"))
        self.tipo_carga_combo = QtWidgets.QComboBox()
        self.tipo_carga_combo.addItems([tipo.value for tipo in TipoCarga])
        self.tipo_carga_combo.setCurrentText(self.carga.tipo_carga.value)
        tipo_carga_layout.addWidget(self.tipo_carga_combo)
        layout.addLayout(tipo_carga_layout)
        
        # Añadimos el campo para el coeficiente
        self.coeficiente_layout = QtWidgets.QHBoxLayout()
        self.coeficiente_text =  QtWidgets.QLabel("Coeficiente:")
        self.coeficiente_layout.addWidget(self.coeficiente_text)
        self.coeficiente_input = QtWidgets.QLineEdit(self.coeficiente)
        self.coeficiente_input.setValidator(QtGui.QDoubleValidator())
        self.coeficiente_input.textChanged.connect(self.actualizar_funcion_transferencia)
        self.coeficiente_layout.addWidget(self.coeficiente_input)
        layout.addLayout(self.coeficiente_layout)

        # Tipo de entrada
        tipo_entrada_layout = QtWidgets.QHBoxLayout()
        tipo_entrada_layout.addWidget(QtWidgets.QLabel("Entrada alternativa para el análisis:"))
        self.tipo_entrada_combo = QtWidgets.QComboBox()
        self.tipo_entrada_combo.addItems(["Misma que entrada","Personalizada", "Impulso", "Escalón", "Rampa", "Parabólica"])
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.tipo_entrada_combo.currentIndexChanged.connect(self.actualizar_interfaz)
        tipo_entrada_layout.addWidget(self.tipo_entrada_combo)
        layout.addLayout(tipo_entrada_layout)

        # Función de transferencia con editor LaTeX
        ft_layout = QtWidgets.QVBoxLayout()
        ft_layout.addWidget(QtWidgets.QLabel("Función de transferencia:"))
        self.latex_editor = LatexEditor()
        self.latex_editor.set_latex(self.carga.funcion_transferencia)
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
        
        # Botones OK, Cancelar y Editar JSON
        button_box = QtWidgets.QDialogButtonBox()
        button_box.addButton(QtWidgets.QDialogButtonBox.Ok)
        button_box.addButton(QtWidgets.QDialogButtonBox.Cancel)

        # Cambiar el texto del botón "OK" a "Guardar" y "Cancel" a "Cancelar"
        button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("Guardar")
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancelar")

        self.btn_editar_json = QtWidgets.QPushButton("Editar JSON")
        button_box.addButton(self.btn_editar_json, QtWidgets.QDialogButtonBox.ActionRole)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.btn_editar_json.clicked.connect(self.editar_json)
        
        layout.addWidget(button_box)
        self.setStyleSheet(ESTILO)

        self.setLayout(layout)
        
        # Actualizamos la interfaz según el tipo de entrada inicial
        self.actualizar_interfaz()
    
    def mostrar_ayuda(self):
        help_dialog = QtWidgets.QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Configuración de Rendimiento")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QtWidgets.QVBoxLayout()

        titulo = QtWidgets.QLabel("Guía de Configuración de Rnedimiento")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)

        contenido = [
            ("<b>¿Qué es una carga?</b>",
            "La carga representa cómo se evalúa el desempeño del sistema, comparando la salida real con la esperada. "
            "Es fundamental para medir la calidad de la respuesta del sistema."),
            
            ("<b>Tipos de carga disponibles:</b>",
            "<ul>"
            "<li><b>Error:</b> Mide la diferencia directa entre el valor deseado y el obtenido</li>"
            "<li><b>Error Proporcional:</b> Calcula el error relativo al valor deseado</li>"
            "<li><b>Integral:</b> Suma la acumulación del error a lo largo del tiempo</li>"
            "<li><b>Integral Proporcional:</b> Acumula el error relativo en el tiempo</li>"
            "<li><b>Final:</b> Evalúa el estado final del sistema</li>"
            "</ul>"),
            
            ("<b>Configuración de estados:</b>",
            "<ul>"
            "<li><b>Estados:</b> Define niveles de desempeño (Excelente, Bueno, Regular, etc.)</li>"
            "<li><b>Mínimo:</b> Valor límite para clasificar en cada estado</li>"
            "<li><b>Prioridad:</b> Orden de importancia entre estados</li>"
            "</ul>"),
            
            ("<b>Función de transferencia:</b>",
            "<ul>"
            "<li><b>Misma que entrada:</b> Replica el comportamiento de la entrada</li>"
            "<li><b>Escalón:</b> Evaluación instantánea del error</li>"
            "<li><b>Rampa:</b> Evaluación con cambio lineal</li>"
            "<li><b>Parabólica:</b> Evaluación con cambio cuadrático</li>"
            "<li><b>Personalizada:</b> Función definida por el usuario</li>"
            "</ul>"),
            
            ("<b>Parámetros adicionales:</b>",
            "<ul>"
            "<li><b>Escalamiento sigmoide:</b> Ajusta la sensibilidad de la evaluación</li>"
            "<li><b>Desplazamiento sigmoide:</b> Modifica el punto medio de evaluación</li>"
            "</ul>")
        ]

        for titulo, texto in contenido:
            seccion = QtWidgets.QLabel()
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
        cerrar_btn = QtWidgets.QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)

        help_dialog.setLayout(layout)
        help_dialog.exec_()
    
    def actualizar_campos(self):
        self.nombre_input.setText(self.carga.nombre)
        self.tipo_carga_combo.setCurrentText(self.carga.tipo_carga.value)
        self.latex_editor.set_latex(self.carga.funcion_transferencia)
        self.escalamiento_sigmoide_input.setText(str(self.carga.escalamiento_sigmoide))
        self.desplazamiento_sigmoide_input.setText(str(self.carga.desplazamiento_sigmoide))
        self.actualizar_lista_estados()
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.coeficiente_input.setText(self.coeficiente)
        self.actualizar_interfaz()

    def editar_json(self):
        vista = VistaJson(self.carga, self)
        vista.exec_()
        if vista.result():
            self.actualizar_campos()
            self.padre.updateText()

    def actualizar_lista_estados(self):
        self.estados_list.clear()
        for estado in self.carga.estados:
            item = QtWidgets.QListWidgetItem(f"{estado['nombre']} - Mín: {estado['minimo']}, Prioridad: {estado['prioridad']}")
            self.estados_list.addItem(item)

    def agregar_estado(self):
        dialog = EditarEstadoDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
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
            dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
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

        es_entrada = tipo_entrada == "Misma que entrada"

        self.latex_editor.setEnabled(es_personalizada)

        self.coeficiente_input.setVisible((not es_personalizada) and (not es_entrada))
        self.coeficiente_text.setVisible((not es_personalizada) and (not es_entrada))

        self.actualizar_funcion_transferencia()


    def actualizar_funcion_transferencia(self):
        tipo_entrada = self.tipo_entrada_combo.currentText()
        coeficiente = self.coeficiente_input.text()
        if tipo_entrada == "Impulso":
            latex = f"{coeficiente}"
        elif tipo_entrada == "Escalón":
            latex = f"\\frac{{{coeficiente}}}{{s}}"
        elif tipo_entrada == "Rampa":
            latex = f"\\frac{{{coeficiente}}}{{s^2}}"
        elif tipo_entrada == "Parabólica":
            latex = f"\\frac{{{coeficiente}}}{{s^3}}"
        elif tipo_entrada == "Misma que entrada":
            latex = f"{self.carga.entrada.funcion_transferencia}"
        else:
            latex = self.carga.funcion_transferencia
        
        self.latex_editor.set_latex(latex)

    def actualizar_info_estado(self):
        estado_actual = self.carga.estados[self.estado_combo.currentIndex()]
        info = f"Mínimo: {estado_actual['minimo']}, Prioridad: {estado_actual['prioridad']}"
        self.info_estado_label.setText(info)

    def accept(self):
        self.tipo_entrada = self.tipo_entrada_combo.currentText()
        
        if not self.latex_editor.es_funcion_valida(self.latex_editor.get_latex()):
            QMessageBox.warning(self, "Función de transferencia inválida", 
                                "La función de transferencia no es válida. Por favor, corríjala antes de continuar.")
            return
        
        # Actualizamos los valores de la carga con los nuevos datos
        self.carga.nombre = self.nombre_input.text()
        self.carga.tipo_carga = TipoCarga(self.tipo_carga_combo.currentText())
        self.carga.funcion_transferencia = self.latex_editor.get_latex()
        self.carga.escalamiento_sigmoide = float(self.escalamiento_sigmoide_input.text())
        self.carga.desplazamiento_sigmoide = float(self.desplazamiento_sigmoide_input.text())

        if self.tipo_entrada == "Misma que entrada":
                self.carga.funcion_transferencia = ""

            
        # Guardamos el estado seleccionado
        current_item = self.estados_list.currentItem()
        if current_item:
            self.estado_seleccionado = current_item.text().split(' - ')[0]  # Obtenemos solo el nombre del estado
        else:
            self.estado_seleccionado = None  # O podrías establecer un valor predeterminado

        super().accept()
        
        
from PyQt5 import QtWidgets, QtCore

class EditarEstadoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, estado=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Estado" if estado else "Agregar Estado")
        self.estado = estado
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        # Aplica el estilo
        self.setStyleSheet(ESTILO)

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
        button_box = QtWidgets.QDialogButtonBox()
        button_box. addButton(QtWidgets.QDialogButtonBox.Ok)
        button_box. addButton(QtWidgets. QDialogButtonBox. Cancel)
        
        # Cambiar el texto del botón "OK" a "Guardar" y "Cancel" a "Cancelar"
        button_box.button(QtWidgets.QDialogButtonBox.Ok).setText("Guardar")
        button_box.button(QtWidgets.QDialogButtonBox.Cancel).setText("Cancelar")
    
        button_box.accepted.connect(self.validate_inputs)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


        self.setLayout(layout)

    def validate_inputs(self):
        # Validar la prioridad como un entero entre 0 y 5
        try:
            prioridad = int(self.prioridad_input.text())
            if prioridad not in range(6):
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "La prioridad debe ser un número entero entre 0 y 5.")
            return

        # Validar el mínimo como un float entre 0 (incluido) y 1 (excluido)
        try:
            minimo = float(self.minimo_input.text())
            if not (0 <= minimo < 1):
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "El mínimo debe ser un número decimal entre 0 y 1, incluyendo 0 pero excluyendo 1.")
            return

        # Si ambas validaciones pasan, aceptar el diálogo
        self.accept()



ESTILO = """
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