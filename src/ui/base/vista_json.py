import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QApplication,QLabel
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat
from PyQt5.QtCore import QRegExp,Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileDialog
class VistaJson(QDialog):

    def __init__(self, microbloque, parent):
        super().__init__(parent)
        self.microbloque = microbloque
        self.setWindowTitle("Json")
        self.layout = QVBoxLayout()
        self.setStyleSheet(ESTILO)
        self.setLayout(self.layout)
        
        # Agregar botón de ayuda
        help_button = QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.clicked.connect(self.mostrar_ayuda_json)
        help_button.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #808080;
                color: white;
                font-weight: bold;
            }
        """)
        self.layout.addWidget(help_button, alignment=Qt.AlignRight)
        
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        json_a = self.microbloque.to_json()


        pretty_json = json.dumps(json_a, indent=4)
        self.text_edit.setPlainText(pretty_json)
        #self.highlight_json()
        self.adjust_dialog_size()
        self.boton = QPushButton("Copiar")
        self.boton.clicked.connect(self.copiar)
        self.layout.addWidget(self.boton)
        self.boton_guardar = QPushButton("Aplicar")
        self.boton_guardar.clicked.connect(self.aplicar)
        self.layout.addWidget(self.boton_guardar)
        self.show()
        self.boton_cargar = QPushButton("Cargar JSON")
        self.boton_cargar.clicked.connect(self.cargar_json)
        self.layout.addWidget(self.boton_cargar)

        self.boton_descargar = QPushButton("Descargar JSON")
        self.boton_descargar.clicked.connect(self.descargar_json)
        self.layout.addWidget(self.boton_descargar)
    
    def mostrar_ayuda_json(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda - Editor JSON")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout()

        # Título principal
        titulo = QLabel("Guía del Editor JSON")
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
            ("<b>¿Qué es el Editor JSON?</b>", 
            "El editor JSON es una herramienta que permite visualizar, editar y gestionar la configuración "
            "de los microbloques en formato JSON. Este formato estructurado facilita la manipulación y "
            "almacenamiento de los parámetros del sistema."),
            
            ("<b>Funcionalidades Principales:</b>",
            "<ul>"
            "<li><b>Copiar:</b> Copia el contenido JSON actual al portapapeles para su uso en otras aplicaciones</li>"
            "<li><b>Aplicar:</b> Guarda los cambios realizados en el editor y los aplica al microbloque</li>"
            "<li><b>Cargar JSON:</b> Permite importar una configuración JSON desde un archivo externo</li>"
            "<li><b>Descargar JSON:</b> Guarda la configuración actual en un archivo JSON en su computadora</li>"
            "</ul>"),
            
            ("<b>Formato JSON:</b>",
            "El JSON se muestra con formato indentado para mejor legibilidad. Los elementos principales son:"
            "<ul>"
            "<li>Propiedades del microbloque en pares clave-valor</li>"
            "<li>Valores numéricos sin comillas</li>"
            "<li>Textos entre comillas dobles</li>"
            "<li>Arrays entre corchetes [ ]</li>"
            "<li>Objetos entre llaves { }</li>"
            "</ul>"),
            
            ("<b>Recomendaciones de Uso:</b>",
            "<ul>"
            "<li>Verifique la sintaxis JSON antes de aplicar cambios</li>"
            "<li>Mantenga copias de seguridad de configuraciones importantes</li>"
            "<li>Use la función de copiar para compartir configuraciones</li>"
            "<li>Respete el formato y estructura del JSON original</li>"
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

    def cargar_json(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar JSON", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                json_text = file.read()
                self.text_edit.setPlainText(json_text)
                #self.highlight_json()

    def descargar_json(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Descargar JSON", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                json_text = self.text_edit.toPlainText()
                file.write(json_text)

    def copiar(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

    def aplicar(self):
        json_text = self.text_edit.toPlainText()
        try:
            json_format = json.loads(json_text)
        except json.JSONDecodeError as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("La estructura del JSON es incorrecta")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("JSON Error")
            msg.exec_()
            return
        try:
            self.microbloque.validar_dict(json_format)
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error al cargar el JSON")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("JSON Error")
            msg.exec_()
            return
        self.microbloque.from_json(json_format)
        self.accept()

    def highlight_json(self):
        json_text = self.text_edit.toPlainText()
        json_format = json.loads(json_text)
        pretty_json = json.dumps(json_format, indent=4)
        self.text_edit.setPlainText(pretty_json)
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        self.text_edit.setTextCursor(cursor)
        #self.apply_syntax_highlighting()

    def apply_syntax_highlighting(self):
        json_text = self.text_edit.toPlainText()
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

        patterns = {
            '"[^"]*"': QColor("brown"),  # Strings
            '\\b(true|false|null)\\b': QColor("blue"),  # Keywords
            '\\b[0-9]+\\b': QColor("magenta"),  # Numbers
            '[{}\\[\\],:]': QColor("black")  # Punctuation
        }

        for pattern, color in patterns.items():
            regex = QRegExp(pattern)
            format = QTextCharFormat()
            format.setForeground(color)
            cursor = self.text_edit.textCursor()
            pos = 0
            index = regex.indexIn(json_text, pos)
            while index != -1:
                cursor.setPosition(index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, regex.matchedLength())
                cursor.mergeCharFormat(format)
                pos = index + regex.matchedLength()
                index = regex.indexIn(json_text, pos)

    def adjust_dialog_size(self):
        """
        document = self.text_edit.document()
        document_size = document.size()
        self.resize(int(document_size.width()) + 50, int(document_size.height()) + 100)
        """
        self.setMinimumSize(800, 600)



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
        border: 2px solid #505050;
        border-radius: 10px;
        padding: 10px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;
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