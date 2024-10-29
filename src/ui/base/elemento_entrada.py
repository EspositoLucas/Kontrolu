from PyQt5 import QtWidgets, QtCore
from back.topologia.microbloque import MicroBloque
from PyQt5.QtWidgets import QMessageBox
from .latex_editor import LatexEditor
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
import os
from ..base.vista_json import VistaJson
from ..base.macro_vista import MacroVista
from PyQt5.QtCore import QRectF




class ElementoEntrada(MacroVista):
    
    def __init__(self, entrada,pos,padre):
        MacroVista.__init__(self, entrada, pos,padre)
        self.entrada = entrada
        self.tipo_entrada = "Personalizada"  # Añadimos este atributo
        self.coeficiente = "1"  # Añadimos este atributo

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mostrar_configuracion_entrada()        

    def mostrar_configuracion_entrada(self):
        dialog = ConfiguracionEntradaDialog(self, self.entrada, self.tipo_entrada, self.coeficiente)
        if dialog.exec_():
            self.entrada = dialog.entrada
            self.tipo_entrada = dialog.tipo_entrada
            self.coeficiente = dialog.coeficiente
            self.updateText()

                
class ConfiguracionEntradaDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, entrada=None, tipo_entrada="Personalizada",coeficiente="1"):
        super().__init__()
        self.padre = parent
        self.setWindowTitle("Configuración de Entrada")
        self.entrada = entrada if entrada else MicroBloque()
        self.tipo_entrada = tipo_entrada
        self.coeficiente = coeficiente
        self.initUI()
        

    def initUI(self):

        layout = QtWidgets.QVBoxLayout()
        self.setStyleSheet(ESTILO)
        
        # Agregar botón de ayuda
        help_button = QPushButton("?", self)
        help_button.setFixedSize(30, 30)
        help_button.move(50, 50)  # Posición del botón en la ventana
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
        
        help_button.clicked.connect(self.mostrar_ayuda)
        # Estilo del botón para darle apariencia de botón de ayuda
        layout.addWidget(help_button)

        # Configurar el icono de la ventana
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path,'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon(icon))

        # Campo para el nombre
        nombre_layout = QtWidgets.QHBoxLayout()
        nombre_layout.addWidget(QtWidgets.QLabel("Nombre:"))
        self.nombre_input = QtWidgets.QLineEdit(self.entrada.nombre)
        nombre_layout.addWidget(self.nombre_input)
        layout.addLayout(nombre_layout)

        # Tipo de entrada
        tipo_entrada_layout = QtWidgets.QHBoxLayout()
        tipo_entrada_layout.addWidget(QtWidgets.QLabel("Tipo de entrada:"))
        self.tipo_entrada_combo = QtWidgets.QComboBox()
        self.tipo_entrada_combo.addItems(["Personalizada", "Escalón", "Rampa", "Parábola"])
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.tipo_entrada_combo.currentIndexChanged.connect(self.actualizar_interfaz)
        tipo_entrada_layout.addWidget(self.tipo_entrada_combo)
        layout.addLayout(tipo_entrada_layout)

        # Nuevo campo para el coeficiente
        coeficiente_layout = QtWidgets.QHBoxLayout()
        coeficiente_layout.addWidget(QtWidgets.QLabel("Coeficiente:"))
        self.coeficiente_input = QtWidgets.QLineEdit(self.coeficiente)
        self.coeficiente_input.setValidator(QtGui.QDoubleValidator())
        self.coeficiente_input.textChanged.connect(self.actualizar_funcion_transferencia)
        coeficiente_layout.addWidget(self.coeficiente_input)
        layout.addLayout(coeficiente_layout)


        # Función de transferencia con editor LaTeX
        ft_layout = QtWidgets.QVBoxLayout()
        ft_layout.addWidget(QtWidgets.QLabel("Función de transferencia:"))
        # Pasar el valor inicial directamente en el constructor
        self.latex_editor = LatexEditor(self.entrada.funcion_transferencia or "")
        self.latex_editor.setEnabled(self.tipo_entrada == "Personalizada")
        ft_layout.addWidget(self.latex_editor)
        layout.addLayout(ft_layout)

        # Botones OK y Cancelar
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Botón Editar JSON
        self.boton_editar_json = QtWidgets.QPushButton("Editar JSON")
        self.boton_editar_json.clicked.connect(self.editar_json)
        button_box.addButton(self.boton_editar_json, QtWidgets.QDialogButtonBox.ActionRole)
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        # Actualizamos la interfaz según el tipo de entrada inicial
        self.actualizar_interfaz()
    
    def mostrar_ayuda(self):
        help_dialog = QtWidgets.QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Configuración de Entrada")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)

        layout = QtWidgets.QVBoxLayout()

        # Título principal
        titulo = QtWidgets.QLabel("Guía de Configuración de Entrada")
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
            ("<b>¿Qué es una entrada?</b>", 
             "La entrada representa la señal que excita o estimula al sistema de control."),
            
            ("<b>Tipos de entrada disponibles:</b>",
             "<ul>"
             "<li><b>Escalón:</b> Cambio instantáneo y constante (ejemplo: encender un interruptor)</li>"
             "<li><b>Rampa:</b> Cambio que aumenta linealmente con el tiempo (ejemplo: acelerador de un auto)</li>"
             "<li><b>Parábola:</b> Cambio que aumenta cuadráticamente con el tiempo</li>"
             "<li><b>Personalizada:</b> Cualquier otra función definida por el usuario</li>"
             "</ul>"),
            
            ("<b>Campos de configuración:</b>",
             "<ul>"
             "<li><b>Nombre:</b> Identificador único para la entrada</li>"
             "<li><b>Tipo de entrada:</b> Selecciona el comportamiento de la señal</li>"
             "<li><b>Coeficiente:</b> Ajusta la magnitud de la señal (actúa como un multiplicador)</li>"
             "<li><b>Función de transferencia:</b> Fórmula matemática que describe el comportamiento</li>"
             "</ul>"),
             
            ("<b>Editor LaTeX:</b>",
             "Permite escribir funciones matemáticas usando notación LaTeX. Incluye botones para símbolos comunes como exponentes, fracciones y variables.")
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

    def actualizar_campos_con_microbloque(self, microbloque):
        self.nombre_input.setText(microbloque.nombre)
        self.tipo_entrada_combo.setCurrentText(self.tipo_entrada)
        self.coeficiente_input.setText(self.coeficiente)
        self.latex_editor.set_latex(microbloque.funcion_transferencia or "")
        self.actualizar_interfaz()

    def editar_json(self):
        vista = VistaJson(self.entrada, self)
        vista.exec_()
        if vista.result():
            self.actualizar_campos_con_microbloque()
            self.padre.setText(self.entrada.nombre)


    def actualizar_interfaz(self):
        tipo_entrada = self.tipo_entrada_combo.currentText()
        es_personalizada = tipo_entrada == "Personalizada"
        
        self.latex_editor.setEnabled(es_personalizada)
        self.coeficiente_input.setEnabled(not es_personalizada)
        
        if not es_personalizada:
            self.actualizar_funcion_transferencia()
        else:
            self.latex_editor.set_latex(self.entrada.funcion_transferencia)

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
        
    def accept(self):
        
        if not self.latex_editor.es_funcion_valida(self.latex_editor.get_latex()):
            QMessageBox.warning(self, "Función de transferencia inválida", 
                                "La función de transferencia no es válida. Por favor, corríjala antes de continuar.")
            return
    
        self.entrada.nombre = self.nombre_input.text()
        self.tipo_entrada = self.tipo_entrada_combo.currentText()
        
        if self.tipo_entrada == "Personalizada":
            self.entrada.funcion_transferencia = self.latex_editor.get_latex()
            self.coeficiente = "1"
        else:
            self.coeficiente = self.coeficiente_input.text() or "1"
            self.entrada.funcion_transferencia = self.latex_editor.get_latex()
        self.padre.update_fdt()
        super().accept()
ESTILO = """
    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #808080;  /* Botones en gris oscuro pastel */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;  /* Tamaño de botón más grande */
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía moderna */
    }

    QPushButton:hover {
        background-color: #606060;  /* Gris aún más oscuro al pasar el cursor */
    }

    QLineEdit {
        background-color: #D0D0D0;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
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
"""