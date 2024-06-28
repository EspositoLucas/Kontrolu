# from PyQt5.QtWidgets import QWidget, QLineEdit, QFrame, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog
# from PyQt5.QtGui import QPainter, QColor
# from PyQt5.QtCore import Qt, pyqtSignal, QPointF
# from back.micros.micro_bloque_back import MicroBloqueBack
# from .latex_editor import LatexEditor

# class Microbloque(QWidget):
#     moved = pyqtSignal()

#     def __init__(self, nombre, parent=None, color=None, funcion_transferencia=None, opciones_adicionales=None):
#         super().__init__(parent)
#         self.nombre = nombre
#         self.color = color or QColor(255, 255, 0)
#         self.funcion_transferencia = funcion_transferencia or ""
#         self.opciones_adicionales = opciones_adicionales or {}
#         self.paralelo_con = None
#         self.setFixedSize(150, 80)
#         self.setMouseTracking(True)
#         self.micro_back = MicroBloqueBack(parent.modelo, nombre)
#         self.micro_back.set_funcion_transferencia(funcion_transferencia)
#         for key, value in self.opciones_adicionales.items():
#             self.micro_back.set_opcion_adicional(key, value)

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(Qt.black)
#         painter.setBrush(self.color)
#         painter.drawRect(self.rect())
        
#         painter.drawText(self.rect(), Qt.AlignCenter, self.nombre)

#     def mouseDoubleClickEvent(self, event):
#         self.edit_properties()

#     def edit_properties(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Editar Microbloque")
#         layout = QVBoxLayout()

#         name_input = QLineEdit(self.nombre)
#         layout.addWidget(name_input)

#         color_button = QPushButton("Cambiar Color")
#         color_button.setStyleSheet(f"background-color: {self.color.name()};")
#         color_button.clicked.connect(lambda: self.select_color(color_button))
#         layout.addWidget(color_button)

#         transfer_label = QLabel("Función de Transferencia:")
#         latex_editor = LatexEditor(initial_latex=self.funcion_transferencia)
#         layout.addWidget(transfer_label)
#         layout.addWidget(latex_editor)

#         for key, value in self.opciones_adicionales.items():
#             option_label = QLabel(f"{key}:")
#             option_input = QLineEdit(str(value))
#             layout.addWidget(option_label)
#             layout.addWidget(option_input)

#         save_button = QPushButton("Guardar")
#         save_button.clicked.connect(dialog.accept)
#         layout.addWidget(save_button)

#         dialog.setLayout(layout)

#         if dialog.exec_():
#             self.nombre = name_input.text()
#             self.funcion_transferencia = latex_editor.get_latex()
#             self.micro_back.set_funcion_transferencia(self.funcion_transferencia)
            
#             for i in range(layout.count()):
#                 widget = layout.itemAt(i).widget()
#                 if isinstance(widget, QLineEdit) and widget != name_input:
#                     key = layout.itemAt(i-1).widget().text().rstrip(':')
#                     value = widget.text()
#                     self.opciones_adicionales[key] = value
#                     self.micro_back.set_opcion_adicional(key, value)
            
#             self.update()

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             self.color = color
#             button.setStyleSheet(f"background-color: {color.name()};")

#     def get_center(self):
#         return self.pos() + QPointF(self.width() / 2, self.height() / 2)

#     def set_center(self, point):
#         new_pos = point - QPointF(self.width() / 2, self.height() / 2)
#         self.move(new_pos.toPoint())

#     def mousePressEvent(self, event):
#         self.__mousePressPos = None
#         self.__mouseMovePos = None
#         if event.button() == Qt.LeftButton:
#             self.__mousePressPos = event.globalPos()
#             self.__mouseMovePos = event.globalPos()

#     def mouseMoveEvent(self, event):
#         if event.buttons() == Qt.LeftButton:
#             currPos = self.mapToGlobal(self.pos())
#             globalPos = event.globalPos()
#             diff = globalPos - self.__mouseMovePos
#             newPos = self.mapFromGlobal(currPos + diff)
#             self.move(newPos)
#             self.__mouseMovePos = globalPos
#             self.moved.emit()

#     def mouseReleaseEvent(self, event):
#         if self.__mousePressPos is not None:
#             moved = event.globalPos() - self.__mousePressPos 
#             if moved.manhattanLength() > 3:
#                 event.ignore()
#                 return

#     def __str__(self):
#         return f"Microbloque(nombre={self.nombre}, color={self.color.name()}, funcion_transferencia={self.funcion_transferencia})"

#     def __repr__(self):
#         return self.__str__()



from PyQt5.QtWidgets import QWidget, QLineEdit, QFrame, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from back.micros.micro_bloque_back import MicroBloqueBack
from .latex_editor import LatexEditor

class Microbloque(QWidget):
    moved = pyqtSignal()

    def __init__(self, nombre, parent=None, color=None, funcion_transferencia=None, opciones_adicionales=None):
        super().__init__(parent)
        self.nombre = nombre
        self.color = color or QColor(255, 255, 0)
        self.funcion_transferencia = funcion_transferencia or ""
        self.opciones_adicionales = opciones_adicionales or {}
        self.paralelo_con = []
        self.serie_con = None
        self.setFixedSize(150, 80)
        self.setMouseTracking(True)
        self.micro_back = MicroBloqueBack(parent.modelo, nombre)
        self.micro_back.set_funcion_transferencia(funcion_transferencia)
        for key, value in self.opciones_adicionales.items():
            self.micro_back.set_opcion_adicional(key, value)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(self.color)
        painter.drawRect(self.rect())
        painter.drawText(self.rect(), Qt.AlignCenter, self.nombre)

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

        for key, value in self.opciones_adicionales.items():
            option_label = QLabel(f"{key}:")
            option_input = QLineEdit(str(value))
            layout.addWidget(option_label)
            layout.addWidget(option_input)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            self.nombre = name_input.text()
            self.funcion_transferencia = latex_editor.get_latex()
            self.micro_back.set_funcion_transferencia(self.funcion_transferencia)
            
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
