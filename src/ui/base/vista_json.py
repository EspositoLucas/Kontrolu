import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat
from PyQt5.QtCore import QRegExp
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
        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)
        pretty_json = json.dumps(self.microbloque.to_json(), indent=4)
        self.text_edit.setPlainText(pretty_json)
        self.highlight_json()
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

    def cargar_json(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar JSON", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                json_text = file.read()
                self.text_edit.setPlainText(json_text)
                self.highlight_json()

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
        self.apply_syntax_highlighting()

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
        self.setMinimumSize(400, 400)


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
        background-color: #F1F1F1;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: white;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }
"""