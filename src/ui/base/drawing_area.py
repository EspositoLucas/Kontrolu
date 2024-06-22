# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtGui import QPainter, QPen, QColor
# from PyQt5.QtCore import Qt, pyqtSignal
# from .micro_bloque import Microbloque

# class DrawingArea(QWidget):
#     microbloque_created = pyqtSignal(Microbloque)

#     def __init__(self, parent=None, modelo=None):
#         super().__init__(parent)
#         self.microbloques = []
#         self.arrows = []
#         self.selected_microbloque = None
#         self.modelo = modelo
#         self.creating_microbloque = False
#         self.new_microbloque_config = {}
#         self.init_ui()

#     def init_ui(self):
#         self.setStyleSheet("background-color: white; border: 1px solid black;")

#     def start_creating_microbloque(self, config):
#         self.creating_microbloque = True
#         self.new_microbloque_config = config
#         self.setCursor(Qt.CrossCursor)

#     def add_microbloque(self, pos):
#         nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
#         color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)  # Amarillo por defecto
#         microbloque = Microbloque(nombre, self, color)
#         microbloque.setGeometry(pos.x() - 50, pos.y() - 25, 100, 50)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         self.microbloque_created.emit(microbloque)
        
#     def delete_microbloque(self):
#         if self.selected_microbloque:
#             self.microbloques.remove(self.selected_microbloque)
#             self.selected_microbloque.deleteLater()
#             self.selected_microbloque = None
#             self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         for arrow in self.arrows:
#             painter.setPen(QPen(Qt.black, 2))
#             painter.drawLine(arrow['start'], arrow['end'])


#     def mousePressEvent(self, event):
#         if self.creating_microbloque:
#             self.add_microbloque(event.pos())
#             self.creating_microbloque = False
#             self.setCursor(Qt.ArrowCursor)
#         else:
#             for microbloque in self.microbloques:
#                 if microbloque.geometry().contains(event.pos()):
#                     self.selected_microbloque = microbloque
#                     break
                
#     def add_arrow(self, start, end):
#         self.arrows.append({'start': start, 'end': end})
#         self.update()

#     def delete_arrow(self):
#         if self.arrows:
#             self.arrows.pop()
#             self.update()






# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtGui import QPainter, QPen, QColor,QPolygonF
# from PyQt5.QtCore import Qt, pyqtSignal, QPointF
# from .micro_bloque import Microbloque
# import math

# class Arrow:
#     def __init__(self, start_microbloque, end_microbloque):
#         self.start_microbloque = start_microbloque
#         self.end_microbloque = end_microbloque

#     def draw(self, painter):
#         start = self.start_microbloque.pos() + QPointF(self.start_microbloque.width()/2, self.start_microbloque.height()/2)
#         end = self.end_microbloque.pos() + QPointF(self.end_microbloque.width()/2, self.end_microbloque.height()/2)
#         painter.drawLine(start, end)
#         # Dibujar punta de flecha
#         angle = math.atan2(end.y() - start.y(), end.x() - start.x())
#         arrowSize = 10
#         painter.drawPolygon(QPolygonF([
#             end,
#             end - QPointF(math.cos(angle + math.pi/6) * arrowSize, math.sin(angle + math.pi/6) * arrowSize),
#             end - QPointF(math.cos(angle - math.pi/6) * arrowSize, math.sin(angle - math.pi/6) * arrowSize),
#         ]))

        
# class DrawingArea(QWidget):
#     microbloque_created = pyqtSignal(Microbloque)

#     def __init__(self, parent=None, modelo=None):
#         super().__init__(parent)
#         self.microbloques = []
#         self.arrows = []
#         self.selected_microbloque = None
#         self.modelo = modelo
#         self.creating_microbloque = False
#         self.new_microbloque_config = {}
#         self.creating_arrow = False
#         self.arrow_start = None
#         self.init_ui()
        
#     def init_ui(self):
#         self.setStyleSheet("background-color: white; border: 1px solid black;")
        
#     def start_creating_microbloque(self, config):
#         self.creating_microbloque = True
#         self.new_microbloque_config = config
#         self.setCursor(Qt.CrossCursor)

#     def add_microbloque(self, pos):
#         nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
#         color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)
#         funcion_transferencia = self.new_microbloque_config.get('funcion_transferencia') or ""
#         microbloque = Microbloque(nombre, self, color, funcion_transferencia)
#         microbloque.setGeometry(pos.x() - 75, pos.y() - 40, 150, 80)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         self.microbloque_created.emit(microbloque)

#     def delete_microbloque(self):
#         if self.selected_microbloque:
#             self.microbloques.remove(self.selected_microbloque)
#             # Eliminar flechas conectadas a este microbloque
#             self.arrows = [arrow for arrow in self.arrows if arrow.start_microbloque != self.selected_microbloque and arrow.end_microbloque != self.selected_microbloque]
#             self.selected_microbloque.deleteLater()
#             self.selected_microbloque = None
#             self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         for arrow in self.arrows:
#             painter.setPen(QPen(Qt.black, 2))
#             arrow.draw(painter)

#     def mousePressEvent(self, event):
#         if self.creating_microbloque:
#             self.add_microbloque(event.pos())
#             self.creating_microbloque = False
#             self.setCursor(Qt.ArrowCursor)
#         elif self.creating_arrow:
#             clicked_microbloque = self.microbloque_at_pos(event.pos())
#             if clicked_microbloque:
#                 if not self.arrow_start:
#                     self.arrow_start = clicked_microbloque
#                 else:
#                     self.add_arrow(self.arrow_start, clicked_microbloque)
#                     self.arrow_start = None
#                     self.creating_arrow = False
#                     self.setCursor(Qt.ArrowCursor)
#         else:
#             for microbloque in self.microbloques:
#                 if microbloque.geometry().contains(event.pos()):
#                     self.selected_microbloque = microbloque
#                     break

#     def microbloque_at_pos(self, pos):
#         for microbloque in self.microbloques:
#             if microbloque.geometry().contains(pos):
#                 return microbloque
#         return None

#     def add_arrow(self, start_microbloque, end_microbloque):
#         self.arrows.append(Arrow(start_microbloque, end_microbloque))
#         self.update()

#     def delete_arrow(self):
#         if self.arrows:
#             self.arrows.pop()
#             self.update()

#     def start_creating_arrow(self):
#         self.creating_arrow = True
#         self.setCursor(Qt.CrossCursor)


# from PyQt5.QtWidgets import QWidget, QMenu
# from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
# from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF
# from .micro_bloque import Microbloque
# import math
# class DrawingArea(QWidget):
#     microbloque_created = pyqtSignal(Microbloque)

#     def __init__(self, parent=None, modelo=None):
#         super().__init__(parent)
#         self.microbloques = []
#         self.selected_microbloque = None
#         self.modelo = modelo
#         self.creating_microbloque = False
#         self.new_microbloque_config = {}
#         self.init_ui()
        
#     def init_ui(self):
#         self.setStyleSheet("background-color: white; border: 1px solid black;")
#         self.setContextMenuPolicy(Qt.CustomContextMenu)
#         self.customContextMenuRequested.connect(self.show_context_menu)
        
#     def start_creating_microbloque(self, config):
#         self.creating_microbloque = True
#         self.new_microbloque_config = config
#         self.setCursor(Qt.CrossCursor)

#     def add_microbloque(self, pos):
#         nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
#         color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)
#         funcion_transferencia = self.new_microbloque_config.get('funcion_transferencia') or ""
#         opciones_adicionales = self.new_microbloque_config.get('opciones_adicionales') or {}
#         microbloque = Microbloque(nombre, self, color, funcion_transferencia, opciones_adicionales)
#         microbloque.setGeometry(pos.x() - 75, pos.y() - 40, 150, 80)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         self.microbloque_created.emit(microbloque)

#     def delete_microbloque(self):
#         if self.selected_microbloque:
#             self.microbloques.remove(self.selected_microbloque)
#             self.selected_microbloque.deleteLater()
#             self.selected_microbloque = None
#             self.update()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setPen(QPen(Qt.black, 2))
        
#         # Dibujar bloques de entrada y salida
#         entrada = QPointF(50, self.height() / 2)
#         salida = QPointF(self.width() - 50, self.height() / 2)
        
#         # Usar QRectF para dibujar los rectángulos
#         painter.drawRect(QRectF(entrada.x() - 40, entrada.y() - 30, 80, 60))
#         painter.drawText(int(entrada.x() - 30), int(entrada.y() + 5), "Entrada")
        
#         painter.drawRect(QRectF(salida.x() - 40, salida.y() - 30, 80, 60))
#         painter.drawText(int(salida.x() - 30), int(salida.y() + 5), "Salida")
        
#         # Dibujar flecha
#         painter.drawLine(int(entrada.x() + 40), int(entrada.y()), int(salida.x() - 40), int(salida.y()))
        
#         # Dibujar botón '+'
#         mid_point = QPointF((entrada.x() + salida.x()) / 2, entrada.y())
#         painter.drawEllipse(mid_point, 15, 15)
#         painter.drawText(int(mid_point.x() - 5), int(mid_point.y() + 5), "+")
        
#     def mousePressEvent(self, event):
#         if self.creating_microbloque:
#             self.add_microbloque(event.pos())
#             self.creating_microbloque = False
#             self.setCursor(Qt.ArrowCursor)
#         else:
#             clicked_microbloque = self.microbloque_at_pos(event.pos())
#             if clicked_microbloque:
#                 self.selected_microbloque = clicked_microbloque
#             else:
#                 self.selected_microbloque = None

#     def microbloque_at_pos(self, pos):
#         for microbloque in self.microbloques:
#             if microbloque.geometry().contains(pos):
#                 return microbloque
#         return None

#     def clear_all(self):
#         for microbloque in self.microbloques:
#             microbloque.deleteLater()
#         self.microbloques.clear()
#         self.update()

#     def show_context_menu(self, pos):
#         menu = QMenu(self)
#         delete_action = menu.addAction("Delete")
        
#         action = menu.exec_(self.mapToGlobal(pos))
        
#         if action == delete_action:
#             self.delete_microbloque()


from PyQt5.QtWidgets import QWidget, QMenu, QInputDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QColorDialog, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
import math

class DrawingArea(QWidget):
    microbloque_created = pyqtSignal(Microbloque)

    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def add_microbloque(self, pos):
        nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
        color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)
        funcion_transferencia = self.new_microbloque_config.get('funcion_transferencia') or ""
        opciones_adicionales = self.new_microbloque_config.get('opciones_adicionales') or {}
        microbloque = Microbloque(nombre, self, color, funcion_transferencia, opciones_adicionales)
        
        # Calcular la posición para el nuevo microbloque
        if self.microbloques:
            last_microbloque = self.microbloques[-1]
            new_x = last_microbloque.x() + last_microbloque.width() + 50  # 50 píxeles de separación
            new_y = last_microbloque.y()
        else:
            new_x = int(pos.x() - 75)
            new_y = int(pos.y() - 40)
        
        microbloque.setGeometry(new_x, new_y, 150, 80)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.microbloque_created.emit(microbloque)
        self.update()

    def delete_microbloque(self):
        if self.selected_microbloque:
            self.microbloques.remove(self.selected_microbloque)
            self.selected_microbloque.deleteLater()
            self.selected_microbloque = None
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2))
        
        entrada = QPointF(50, self.height() / 2)
        salida = QPointF(self.width() - 50, self.height() / 2)
        
        painter.drawRect(QRectF(entrada.x() - 40, entrada.y() - 30, 80, 60))
        painter.drawText(int(entrada.x() - 30), int(entrada.y() + 5), "Entrada")
        
        painter.drawRect(QRectF(salida.x() - 40, salida.y() - 30, 80, 60))
        painter.drawText(int(salida.x() - 30), int(salida.y() + 5), "Salida")
        
        # Dibujar línea entre bloques
        last_point = entrada
        for microbloque in self.microbloques:
            current_point = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height()/2)
            painter.drawLine(int(last_point.x()), int(last_point.y()), int(current_point.x()), int(current_point.y()))
            last_point = current_point
        painter.drawLine(int(last_point.x()), int(last_point.y()), int(salida.x() - 40), int(salida.y()))
        
        # Dibujar botones '+'
        self.draw_add_buttons(painter)

    def draw_add_buttons(self, painter):
        if not self.microbloques:
            mid_point = QPointF(self.width() / 2, self.height() / 2)
            self.draw_add_button(painter, mid_point)
        else:
            for i, microbloque in enumerate(self.microbloques):
                if i == 0:
                    start = QPointF(50, self.height() / 2)
                    end = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height()/2)
                    mid = (start + end) / 2
                    self.draw_add_button(painter, mid)
                
                # Dibujar botones '+' arriba y abajo del microbloque
                top_mid = microbloque.pos() + QPointF(microbloque.width()/2, -20)
                bottom_mid = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height() + 20)
                self.draw_add_button(painter, top_mid)
                self.draw_add_button(painter, bottom_mid)
                
                if i < len(self.microbloques) - 1:
                    next_microbloque = self.microbloques[i+1]
                    start = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height()/2)
                    end = next_microbloque.pos() + QPointF(next_microbloque.width()/2, next_microbloque.height()/2)
                    mid = (start + end) / 2
                    self.draw_add_button(painter, mid)
                
                if i == len(self.microbloques) - 1:
                    start = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height()/2)
                    end = QPointF(self.width() - 50, self.height() / 2)
                    mid = (start + end) / 2
                    self.draw_add_button(painter, mid)

    def draw_add_button(self, painter, point):
        painter.drawEllipse(point, 15, 15)
        painter.drawText(int(point.x() - 5), int(point.y() + 5), "+")

    def mousePressEvent(self, event):
        if self.creating_microbloque:
            self.add_microbloque(event.pos())
            self.creating_microbloque = False
            self.setCursor(Qt.ArrowCursor)
        else:
            clicked_microbloque = self.microbloque_at_pos(event.pos())
            if clicked_microbloque:
                self.selected_microbloque = clicked_microbloque
                self.edit_microbloque(clicked_microbloque)
            else:
                add_button = self.add_button_at_pos(event.pos())
                if add_button:
                    self.create_new_microbloque(add_button)
                else:
                    self.selected_microbloque = None

    def add_button_at_pos(self, pos):
        if not self.microbloques:
            start = QPointF(50, self.height() / 2)
            end = QPointF(self.width() - 50, self.height() / 2)
            mid = (start + end) / 2
            if (pos - mid).manhattanLength() < 15:
                return mid
        else:
            for microbloque in self.microbloques:
                # Verificar botones arriba y abajo
                top_mid = microbloque.pos() + QPointF(microbloque.width()/2, -20)
                bottom_mid = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height() + 20)
                if (pos - top_mid).manhattanLength() < 15:
                    return top_mid
                if (pos - bottom_mid).manhattanLength() < 15:
                    return bottom_mid

            for i, microbloque in enumerate(self.microbloques + [None]):
                if i == 0:
                    start = QPointF(50, self.height() / 2)
                    end = self.microbloques[0].pos() + QPointF(self.microbloques[0].width()/2, self.microbloques[0].height()/2)
                elif i == len(self.microbloques):
                    start = self.microbloques[-1].pos() + QPointF(self.microbloques[-1].width()/2, self.microbloques[-1].height()/2)
                    end = QPointF(self.width() - 50, self.height() / 2)
                else:
                    start = self.microbloques[i-1].pos() + QPointF(self.microbloques[i-1].width()/2, self.microbloques[i-1].height()/2)
                    end = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height()/2)
                
                mid = (start + end) / 2
                if (pos - mid).manhattanLength() < 15:
                    return mid
        return None
    
    def create_new_microbloque(self, pos=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Microbloque")
        layout = QVBoxLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Nombre del microbloque")
        layout.addWidget(name_input)

        color_button = QPushButton("Seleccionar Color")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        transfer_label = QLabel("Función de Transferencia:")
        latex_editor = LatexEditor()
        layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            nombre = name_input.text() or f"Microbloque {len(self.microbloques) + 1}"
            color = color_button.property("selected_color") or QColor(255, 255, 0)
            funcion_transferencia = latex_editor.get_latex()
            config = {
                'nombre': nombre,
                'color': color,
                'funcion_transferencia': funcion_transferencia,
                'opciones_adicionales': {}
            }
            self.new_microbloque_config = config
            if pos:
                self.add_microbloque(pos)
            else:
                self.creating_microbloque = True
                self.setCursor(Qt.CrossCursor)

    def edit_microbloque(self, microbloque):
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Microbloque")
        layout = QVBoxLayout()

        name_input = QLineEdit(microbloque.nombre)
        layout.addWidget(name_input)

        color_button = QPushButton("Cambiar Color")
        color_button.setStyleSheet(f"background-color: {microbloque.color.name()};")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        transfer_label = QLabel("Función de Transferencia:")
        latex_editor = LatexEditor(initial_latex=microbloque.funcion_transferencia)
        layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            microbloque.nombre = name_input.text()
            microbloque.color = color_button.property("selected_color") or microbloque.color
            microbloque.funcion_transferencia = latex_editor.get_latex()
            microbloque.update()
            self.update()

    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")
            button.setProperty("selected_color", color)
                
    def microbloque_at_pos(self, pos):
        for microbloque in self.microbloques:
            if microbloque.geometry().contains(pos):
                return microbloque
        return None

    def clear_all(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.update()

    def show_context_menu(self, pos):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        
        action = menu.exec_(self.mapToGlobal(pos))
        
        if action == delete_action:
            self.delete_microbloque()