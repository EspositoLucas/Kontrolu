from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from .latex_editor import LatexEditor

class Microbloque(QWidget):
    def __init__(self, parent=None, microbloque_back=None):
        super().__init__(parent)
        self.elemento_back = microbloque_back
        self.nombre = microbloque_back.nombre
        self.color = microbloque_back.color or QColor(255, 255, 255)
        self.funcion_transferencia = microbloque_back.funcion_transferencia or ""
        self.opciones_adicionales = microbloque_back.opciones_adicionales or {}
        self.setFixedSize(150, 80)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {self.color.name()}; border: 2px solid black;")

    def setPos(self, pos):
        self.move(pos.toPoint())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(self.color)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(Qt.black)
        text_rect = self.rect().adjusted(5, 5, -5, -5)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.nombre)

    def mouseDoubleClickEvent(self, event):
        self.edit_properties()

    def edit_properties(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Microbloque")
        layout = QVBoxLayout()

        name_input = QLineEdit(self.nombre)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(name_input)

        color_button = QPushButton("Cambiar Color")
        color_button.setStyleSheet(f"background-color: {self.color.name()};")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        transfer_label = QLabel("Función de Transferencia:")
        latex_editor = LatexEditor(initial_latex=self.funcion_transferencia)
        layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            self.nombre = name_input.text()
            self.elemento_back.nombre = self.nombre
            self.funcion_transferencia = latex_editor.get_latex()
            self.elemento_back.funcion_transferencia = self.funcion_transferencia
            self.update()

    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            self.elemento_back.color = color
            button.setStyleSheet(f"background-color: {color.name()};")
            self.setStyleSheet(f"background-color: {color.name()}; border: 2px solid black;")

    def get_center(self):
        return self.pos() + QPointF(self.width() / 2, self.height() / 2)

    def set_center(self, point):
        new_pos = point - QPointF(self.width() / 2, self.height() / 2)
        self.move(new_pos.toPoint())



