import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PyQt5.QtGui import QColor, QTextCursor, QTextCharFormat
from PyQt5.QtCore import QRegExp

class VistaJson(QDialog):

    def __init__(self, microbloque, parent):
        print("VistaJson")
        super().__init__(parent)
        self.microbloque = microbloque
        self.setWindowTitle("Json")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("background-color: white;")
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
        print("VistaJson")

    def copiar(self):
        print("copiar")
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())
        print("copiar")

    def aplicar(self):
        print("aplicar")
        json_text = self.text_edit.toPlainText()
        try:
            json_format = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            from PyQt5.QtWidgets import QMessageBox
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
            print(f"Error loading JSON: {e}")
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error al cargar el JSON")
            msg.setInformativeText(str(e))
            msg.setWindowTitle("JSON Error")
            msg.exec_()
            return
        self.microbloque.from_json(json_format)
        self.accept()
        print("aplicar")

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
        document = self.text_edit.document()
        document_size = document.size()
        self.resize(int(document_size.width()) + 50, int(document_size.height()) + 100)
