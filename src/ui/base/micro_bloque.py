from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QPointF
from .latex_editor import LatexEditor

class Microbloque(QWidget):
    def __init__(self, parent=None, microbloque_back=None):
        super().__init__(parent)
        self.elemento_back = microbloque_back
        self.nombre = microbloque_back.nombre
        self.color = microbloque_back.color or QColor(255, 255, 0)
        self.funcion_transferencia = microbloque_back.funcion_transferencia or ""
        self.opciones_adicionales = microbloque_back.opciones_adicionales or {}
        self.esta_selecionado = False
        self.setFixedSize(microbloque_back.ancho(), microbloque_back.alto())
        self.setAttribute(Qt.WA_StyledBackground, True)
        color_texto = self.calcular_color(self.color)
        self.setStyleSheet(f"""
            font-weight: bold;          /* Texto en negrita */
            font-weight: bold;          /* Texto en negrita */
            color: {color_texto};               /* Color de texto blanco */
            font-family: Arial;  
            background-color: {self.color.name()};
        """)
    
    def es_color_claro(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        return r * 0.299 + g * 0.587 + b * 0.114 > 186

    def calcular_color(self, color):
        fondo_color = color
        es_claro = self.es_color_claro(fondo_color)
        color_texto = "black" if es_claro else "white"
        return color_texto

    def setPos(self, pos):
        self.move(pos.toPoint())

    def setSeleccionado(self, seleccionado):
        self.esta_selecionado = seleccionado
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Dibuja el rectángulo
        if self.esta_selecionado:
            painter.setPen(QPen(Qt.red, 3))  # Borde rojo y más grueso para seleccionados
        else:
            painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(self.color)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        
        # Configura la fuente
        font = QFont("Arial", max(1, round(10)), QFont.Bold)
        painter.setFont(font)

        # Configura el color del texto
        color_texto = self.calcular_color(self.color)
        painter.setPen(QPen(QColor(color_texto)))
        
        # Dibuja el texto
        text_rect = self.rect().adjusted(5, 5, -5, -5)  # Margen para el texto
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.nombre)

    def mouseDoubleClickEvent(self, event):
        self.edit_properties()

    def edit_properties(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Microbloque")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        name_input = QLineEdit(self.nombre)
        name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(name_input)

        color_button = QPushButton("Cambiar Color")
        color_button.setStyleSheet(f"background-color: {self.color.name()};")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        transfer_label = QLabel("Función de Transferencia:")
        transfer_label.setStyleSheet("color: white;")
        latex_editor = LatexEditor(initial_latex=self.funcion_transferencia)
        latex_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)

        for key, value in self.opciones_adicionales.items():
            option_label = QLabel(f"{key}:")
            option_input = QLineEdit(str(value))
            layout.addWidget(option_label)
            layout.addWidget(option_input)

        save_button = QPushButton("Guardar")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            self.elemento_back.nombre = name_input.text()
            self.elemento_back.color = self.color
            self.nombre = name_input.text()
            self.elemento_back.funcion_transferencia = latex_editor.get_latex()
            self.funcion_transferencia = latex_editor.get_latex()
            
            for i in range(layout.count()):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QLineEdit) and widget != name_input:
                    key = layout.itemAt(i-1).widget().text().rstrip(':')
                    value = widget.text()
                    self.opciones_adicionales[key] = value
                    self.micro_back.set_opcion_adicional(key, value)
            
            self.update()


    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            button.setStyleSheet(f"background-color: {color.name()};")

    def get_center(self):
        return self.pos() + QPointF(self.width() / 2, self.height() / 2)

    def set_center(self, point):
        new_pos = point - QPointF(self.width() / 2, self.height() / 2)
        self.move(new_pos.toPoint())

    def __str__(self):
        return f"Microbloque(nombre={self.nombre}, color={self.color.name()}, funcion_transferencia={self.funcion_transferencia})"

    def __repr__(self):
        return self.__str__()
  
