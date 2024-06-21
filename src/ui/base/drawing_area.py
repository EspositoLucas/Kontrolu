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


from PyQt5.QtWidgets import QWidget, QMenu
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from .micro_bloque import Microbloque
import math

class Arrow:
    def __init__(self, start_microbloque, end_microbloque):
        self.start_microbloque = start_microbloque
        self.end_microbloque = end_microbloque
        self.direction = 1  # 1 for forward, -1 for backward

    def draw(self, painter):
        start = self.calculate_edge_point(self.start_microbloque, self.end_microbloque.pos())
        end = self.calculate_edge_point(self.end_microbloque, self.start_microbloque.pos())
        
        painter.drawLine(start, end)
        
        # Draw arrowhead
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrowSize = 10
        arrowP1 = end - QPointF(math.cos(angle + math.pi/6) * arrowSize, math.sin(angle + math.pi/6) * arrowSize)
        arrowP2 = end - QPointF(math.cos(angle - math.pi/6) * arrowSize, math.sin(angle - math.pi/6) * arrowSize)
        
        if self.direction == 1:
            painter.drawPolygon(QPolygonF([end, arrowP1, arrowP2]))
        else:
            painter.drawPolygon(QPolygonF([start, start + (arrowP1 - end), start + (arrowP2 - end)]))

    def calculate_edge_point(self, microbloque, target):
        center = microbloque.pos() + QPointF(microbloque.width()/2, microbloque.height()/2)
        angle = math.atan2(target.y() - center.y(), target.x() - center.x())
        
        width = microbloque.width() / 2
        height = microbloque.height() / 2
        
        if abs(math.cos(angle)) * height > abs(math.sin(angle)) * width:
            x = width if math.cos(angle) > 0 else -width
            y = x * math.tan(angle)
        else:
            y = height if math.sin(angle) > 0 else -height
            x = y / math.tan(angle) if math.tan(angle) != 0 else width
        
        return center + QPointF(x, y)

class DrawingArea(QWidget):
    microbloque_created = pyqtSignal(Microbloque)

    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.arrows = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.creating_arrow = False
        self.arrow_start = None
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def start_creating_microbloque(self, config):
        self.creating_microbloque = True
        self.new_microbloque_config = config
        self.setCursor(Qt.CrossCursor)

    def add_microbloque(self, pos):
        nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
        color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)
        funcion_transferencia = self.new_microbloque_config.get('funcion_transferencia') or ""
        opciones_adicionales = self.new_microbloque_config.get('opciones_adicionales') or {}
        microbloque = Microbloque(nombre, self, color, funcion_transferencia, opciones_adicionales)
        microbloque.setGeometry(pos.x() - 75, pos.y() - 40, 150, 80)
        microbloque.moved.connect(self.update_arrows)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.microbloque_created.emit(microbloque)

    def delete_microbloque(self):
        if self.selected_microbloque:
            self.microbloques.remove(self.selected_microbloque)
            # Eliminar flechas conectadas a este microbloque
            self.arrows = [arrow for arrow in self.arrows if arrow.start_microbloque != self.selected_microbloque and arrow.end_microbloque != self.selected_microbloque]
            self.selected_microbloque.deleteLater()
            self.selected_microbloque = None
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for arrow in self.arrows:
            painter.setPen(QPen(Qt.black, 2))
            arrow.draw(painter)

    def mousePressEvent(self, event):
        if self.creating_microbloque:
            self.add_microbloque(event.pos())
            self.creating_microbloque = False
            self.setCursor(Qt.ArrowCursor)
        elif self.creating_arrow:
            clicked_microbloque = self.microbloque_at_pos(event.pos())
            if clicked_microbloque:
                if not self.arrow_start:
                    self.arrow_start = clicked_microbloque
                else:
                    self.add_arrow(self.arrow_start, clicked_microbloque)
                    self.arrow_start = None
                    self.creating_arrow = False
                    self.setCursor(Qt.ArrowCursor)
        else:
            clicked_microbloque = self.microbloque_at_pos(event.pos())
            if clicked_microbloque:
                self.selected_microbloque = clicked_microbloque
            else:
                self.selected_microbloque = None


    def microbloque_at_pos(self, pos):
        for microbloque in self.microbloques:
            if microbloque.geometry().contains(pos):
                return microbloque
        return None

    def add_arrow(self, start_microbloque, end_microbloque):
        new_arrow = Arrow(start_microbloque, end_microbloque)
        self.arrows.append(new_arrow)
        self.update()

    def delete_arrow(self):
        if self.arrows:
            self.arrows.pop()
            self.update()

    def start_creating_arrow(self):
        self.creating_arrow = True
        self.setCursor(Qt.CrossCursor)

    def clear_all(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.arrows.clear()
        self.update()

    def update_arrows(self):
        for arrow in self.arrows:
            arrow.start_microbloque.moved.connect(self.update)
            arrow.end_microbloque.moved.connect(self.update)
        self.update()
        
    def arrow_contains_point(self, arrow, point):
        start = arrow.calculate_edge_point(arrow.start_microbloque, arrow.end_microbloque.pos())
        end = arrow.calculate_edge_point(arrow.end_microbloque, arrow.start_microbloque.pos())
        
        # Check if point is close to the line
        distance = self.point_line_distance(point, start, end)
        return distance < 5  # Adjust this value for click sensitivity

    def point_line_distance(self, point, line_start, line_end):
        n = abs((line_end.x() - line_start.x()) * (line_start.y() - point.y()) - 
                (line_start.x() - point.x()) * (line_end.y() - line_start.y()))
        d = math.sqrt((line_end.x() - line_start.x())**2 + (line_end.y() - line_start.y())**2)
        return n / d
    
    
    def delete_arrow_at_pos(self, pos):
        for arrow in self.arrows:
            if self.arrow_contains_point(arrow, pos):
                self.arrows.remove(arrow)
                self.update()
                break

    def change_arrow_direction_at_pos(self, pos):
        for arrow in self.arrows:
            if self.arrow_contains_point(arrow, pos):
                arrow.direction *= -1
                self.update()
                break

    def detach_arrow_at_pos(self, pos):
        for arrow in self.arrows:
            if self.arrow_contains_point(arrow, pos):
                # Implement detach logic here
                # For example, you could set one end of the arrow to a fixed point
                pass
            
    def show_context_menu(self, pos):
        menu = QMenu(self)
        delete_action = menu.addAction("Delete")
        change_direction_action = menu.addAction("Change Direction")
        detach_action = menu.addAction("Detach")
        
        action = menu.exec_(self.mapToGlobal(pos))
        
        if action == delete_action:
            self.delete_arrow_at_pos(pos)
        elif action == change_direction_action:
            self.change_arrow_direction_at_pos(pos)
        elif action == detach_action:
            self.detach_arrow_at_pos(pos)
