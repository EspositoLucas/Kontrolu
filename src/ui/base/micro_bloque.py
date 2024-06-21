
# from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QFrame
# from PyQt5.QtGui import QPainter, QColor
# from PyQt5.QtCore import Qt, QSize
# from back.micros.micro_bloque_back import MicroBloqueBack

# class ResizeHandle(QFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setGeometry(0, 0, 10, 10)
#         self.setStyleSheet("background-color: blue;")

# class Microbloque(QWidget):
#     def __init__(self, nombre, parent=None, color=None):
#         super().__init__(parent)
#         self.nombre = nombre
#         self.color = color or QColor(255, 255, 0)  # Amarillo por defecto si no se proporciona color
#         self.setGeometry(50, 50, 100, 50)  # Geometría por defecto
#         self.setMouseTracking(True)
#         self.is_resizing = False
#         self.is_moving = False
#         self.last_mouse_pos = None
#         self.micro_back = MicroBloqueBack(parent.modelo, nombre)  # Pasamos el nombre aquí

#         # Añadir handles para redimensionar
#         self.handles = {
#             'bottom_right': ResizeHandle(self)
#         }
#         self.update_handles()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(Qt.black)
#         painter.setBrush(self.color)
#         painter.drawRect(self.rect())
#         painter.drawText(self.rect(), Qt.AlignCenter, self.nombre)

#     def mouseDoubleClickEvent(self, event):
#         text, ok = QInputDialog.getText(self, 'Editar nombre', 'Nuevo nombre:', QLineEdit.Normal, self.nombre)
#         if ok and text:
#             self.nombre = text
#             self.micro_back.nombre = text  # Actualizar también el nombre en el backend
#             self.update()
            
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.last_mouse_pos = event.pos()
#             self.is_moving = True

#             for handle in self.handles.values():
#                 if handle.geometry().contains(event.pos()):
#                     self.is_resizing = True
#                     self.is_moving = False
#                     break

#     def mouseMoveEvent(self, event):
#         if self.is_moving:
#             delta = event.pos() - self.last_mouse_pos
#             self.move(self.pos() + delta)
#         elif self.is_resizing:
#             delta = event.pos() - self.last_mouse_pos
#             new_size = self.size() + QSize(delta.x(), delta.y())
#             self.resize(new_size)
#             self.update_handles()
#         self.update()

#     def mouseReleaseEvent(self, event):
#         self.is_moving = False
#         self.is_resizing = False

#     def update_handles(self):
#         # Actualizar la posición de los handles para redimensionar
#         self.handles['bottom_right'].move(self.width() - 10, self.height() - 10)




# from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QFrame, QVBoxLayout, QLabel, QPushButton, QColorDialog,QDialog
# from PyQt5.QtGui import QPainter, QColor
# from PyQt5.QtCore import Qt, QSize
# from back.micros.micro_bloque_back import MicroBloqueBack
# class ResizeHandle(QFrame):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setGeometry(0, 0, 10, 10)
#         self.setStyleSheet("background-color: blue;")

# class Microbloque(QWidget):
#     def __init__(self, nombre, parent=None, color=None, funcion_transferencia=None):
#         super().__init__(parent)
#         self.nombre = nombre
#         self.color = color or QColor(255, 255, 0)
#         self.funcion_transferencia = funcion_transferencia or ""
#         self.setGeometry(50, 50, 150, 80)  # Aumentado el tamaño para acomodar la función de transferencia
#         self.setMouseTracking(True)
#         self.is_resizing = False
#         self.is_moving = False
#         self.last_mouse_pos = None
#         self.micro_back = MicroBloqueBack(parent.modelo, nombre)

#         self.handles = {
#             'bottom_right': ResizeHandle(self)
#         }
#         self.update_handles()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(Qt.black)
#         painter.setBrush(self.color)
#         painter.drawRect(self.rect())
        
#         # Dibujar nombre
#         painter.drawText(self.rect(), Qt.AlignTop | Qt.AlignHCenter, self.nombre)
        
#         # Dibujar función de transferencia
#         painter.drawText(self.rect(), Qt.AlignBottom | Qt.AlignHCenter, self.funcion_transferencia)

#     def mouseDoubleClickEvent(self, event):
#         self.edit_properties()

#     def edit_properties(self):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Editar Microbloque")
#         layout = QVBoxLayout()

#         # Nombre
#         name_label = QLabel("Nombre:")
#         name_input = QLineEdit(self.nombre)
#         layout.addWidget(name_label)
#         layout.addWidget(name_input)

#         # Color
#         color_button = QPushButton("Cambiar Color")
#         color_button.clicked.connect(lambda: self.select_color(color_button))
#         layout.addWidget(color_button)

#         # Función de transferencia
#         transfer_label = QLabel("Función de Transferencia:")
#         transfer_input = QLineEdit(self.funcion_transferencia)
#         layout.addWidget(transfer_label)
#         layout.addWidget(transfer_input)

#         # Botón guardar
#         save_button = QPushButton("Guardar")
#         save_button.clicked.connect(dialog.accept)
#         layout.addWidget(save_button)

#         dialog.setLayout(layout)

#         if dialog.exec_():
#             self.nombre = name_input.text()
#             self.funcion_transferencia = transfer_input.text()
#             self.update()

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             self.color = color
#             button.setStyleSheet(f"background-color: {color.name()};")
            
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.last_mouse_pos = event.pos()
#             self.is_moving = True

#             for handle in self.handles.values():
#                 if handle.geometry().contains(event.pos()):
#                     self.is_resizing = True
#                     self.is_moving = False
#                     break

#     def mouseMoveEvent(self, event):
#         if self.is_moving:
#             delta = event.pos() - self.last_mouse_pos
#             self.move(self.pos() + delta)
#         elif self.is_resizing:
#             delta = event.pos() - self.last_mouse_pos
#             new_size = self.size() + QSize(delta.x(), delta.y())
#             self.resize(new_size)
#             self.update_handles()
#         self.update()

#     def mouseReleaseEvent(self, event):
#         self.is_moving = False
#         self.is_resizing = False

#     def update_handles(self):
#         # Actualizar la posición de los handles para redimensionar
#         self.handles['bottom_right'].move(self.width() - 10, self.height() - 10)



from PyQt5.QtWidgets import QWidget, QLineEdit, QInputDialog, QFrame, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from back.micros.micro_bloque_back import MicroBloqueBack
from .latex_editor import LatexEditor

class ResizeHandle(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, 0, 10, 10)
        self.setStyleSheet("background-color: blue;")

class Microbloque(QWidget):
    moved = pyqtSignal()

    def __init__(self, nombre, parent=None, color=None, funcion_transferencia=None, opciones_adicionales=None):
        super().__init__(parent)
        self.nombre = nombre
        self.color = color or QColor(255, 255, 0)
        self.funcion_transferencia = funcion_transferencia or ""
        self.opciones_adicionales = opciones_adicionales or {}
        self.setGeometry(50, 50, 150, 80)
        self.setMouseTracking(True)
        self.is_resizing = False
        self.is_moving = False
        self.last_mouse_pos = None
        self.micro_back = MicroBloqueBack(parent.modelo, nombre)
        self.micro_back.set_funcion_transferencia(funcion_transferencia)
        for key, value in self.opciones_adicionales.items():
            self.micro_back.set_opcion_adicional(key, value)

        self.handles = {
            'bottom_right': ResizeHandle(self)
        }
        self.update_handles()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(self.color)
        painter.drawRect(self.rect())
        
        # Dibujar nombre
        painter.drawText(self.rect(), Qt.AlignCenter, self.nombre)

    def mouseDoubleClickEvent(self, event):
        self.edit_properties()

    def edit_properties(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Microbloque")
        layout = QVBoxLayout()

        # Nombre
        # name_label = QLabel("Nombre:")
        name_input = QLineEdit(self.nombre)
        # layout.addWidget(name_label)
        layout.addWidget(name_input)

        # Color
        color_button = QPushButton("Cambiar Color")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        # Función de transferencia
        transfer_label = QLabel("Función de Transferencia:")
        latex_editor = LatexEditor(initial_latex=self.funcion_transferencia)
        # layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)

        # Opciones adicionales
        for key, value in self.opciones_adicionales.items():
            option_label = QLabel(f"{key}:")
            option_input = QLineEdit(str(value))
            layout.addWidget(option_label)
            layout.addWidget(option_input)

        # Botón guardar
        save_button = QPushButton("Guardar")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            self.nombre = name_input.text()
            self.funcion_transferencia = latex_editor.get_latex()
            self.micro_back.set_funcion_transferencia(self.funcion_transferencia)
            
            # Actualizar opciones adicionales
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
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
            self.is_moving = True

            for handle in self.handles.values():
                if handle.geometry().contains(event.pos()):
                    self.is_resizing = True
                    self.is_moving = False
                    break

    def mouseMoveEvent(self, event):
        if self.is_moving:
            delta = event.pos() - self.last_mouse_pos
            new_pos = self.pos() + delta
            self.move(new_pos)
            self.moved.emit()
        elif self.is_resizing:
            delta = event.pos() - self.last_mouse_pos
            new_size = self.size() + QSize(delta.x(), delta.y())
            self.resize(new_size)
            self.update_handles()
        self.update()

    def mouseReleaseEvent(self, event):
        self.is_moving = False
        self.is_resizing = False

    def update_handles(self):
        # Actualizar la posición de los handles para redimensionar
        self.handles['bottom_right'].move(self.width() - 10, self.height() - 10)