# from PyQt5.QtWidgets import QWidget, QMenu, QDialog, QVBoxLayout, QLineEdit, QPushButton, QColorDialog, QLabel
# from PyQt5.QtGui import QPainter, QPen, QColor, QPolygonF
# from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF
# from .latex_editor import LatexEditor
# from .micro_bloque import Microbloque

# class DrawingArea(QWidget):
#     microbloque_created = pyqtSignal(object)

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
        
#     def add_microbloque(self, pos, relation='serie', reference_microbloque=None):
#         nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
#         color = self.new_microbloque_config.get('color') or QColor(255, 255, 0)
#         funcion_transferencia = self.new_microbloque_config.get('funcion_transferencia') or ""
#         opciones_adicionales = self.new_microbloque_config.get('opciones_adicionales') or {}
        
#         microbloque = Microbloque(nombre, self, color, funcion_transferencia, opciones_adicionales)
#         microbloque.moved.connect(self.update)
        
#         if reference_microbloque:
#             index = self.microbloques.index(reference_microbloque)
#             if relation == 'izquierda':
#                 self.microbloques.insert(index, microbloque)
#             elif relation == 'derecha':
#                 self.microbloques.insert(index + 1, microbloque)
#             elif relation in ['arriba', 'abajo']:
#                 self.microbloques.append(microbloque)
#                 microbloque.paralelo_con = reference_microbloque
#         else:
#             self.microbloques.append(microbloque)
        
#         microbloque.move(int(pos.x() - microbloque.width() / 2), int(pos.y() - microbloque.height() / 2))
#         microbloque.show()
#         self.microbloque_created.emit(microbloque)
#         self.update()
#         self.reorganize_microbloques()

#     def delete_microbloque(self):
#         if self.selected_microbloque:
#             self.microbloques.remove(self.selected_microbloque)
#             for mb in self.microbloques:
#                 if mb.paralelo_con == self.selected_microbloque:
#                     mb.paralelo_con = None
#             self.selected_microbloque.deleteLater()
#             self.selected_microbloque = None
#             self.update()
#             self.reorganize_microbloques()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.setPen(QPen(Qt.black, 2))
        
#         entrada = QPointF(50, self.height() / 2)
#         salida = QPointF(self.width() - 50, self.height() / 2)
        
#         painter.drawRect(QRectF(entrada.x() - 40, entrada.y() - 30, 80, 60))
#         painter.drawText(int(entrada.x() - 30), int(entrada.y() + 5), "Entrada")
        
#         painter.drawRect(QRectF(salida.x() - 40, salida.y() - 30, 80, 60))
#         painter.drawText(int(salida.x() - 30), int(salida.y() + 5), "Salida")
        
#         self.draw_connections(painter)
#         self.draw_add_buttons(painter)

#     def draw_connections(self, painter):
#         last_point = QPointF(90, self.height() / 2)
#         for microbloque in self.microbloques:
#             if not microbloque.paralelo_con:
#                 current_point = microbloque.get_center()
#                 painter.drawLine(int(last_point.x()), int(last_point.y()), int(current_point.x()), int(current_point.y()))
#                 last_point = QPointF(microbloque.x() + microbloque.width(), microbloque.y() + microbloque.height() / 2)
            
#             if microbloque.paralelo_con:
#                 start = microbloque.paralelo_con.get_center()
#                 end = microbloque.get_center()
#                 mid_x = (start.x() + end.x()) / 2
#                 painter.drawLine(int(start.x()), int(start.y()), int(mid_x), int(start.y()))
#                 painter.drawLine(int(mid_x), int(start.y()), int(mid_x), int(end.y()))
#                 painter.drawLine(int(mid_x), int(end.y()), int(end.x()), int(end.y()))
        
#         painter.drawLine(int(last_point.x()), int(last_point.y()), int(self.width() - 90), int(self.height() / 2))

#     def draw_add_buttons(self, painter):
#         if not self.microbloques:
#             mid_point = QPointF(self.width() / 2, self.height() / 2)
#             self.draw_add_button(painter, mid_point)
#         else:
#             last_x = 90
#             for i, microbloque in enumerate(self.microbloques):
#                 if not microbloque.paralelo_con:
#                     # Botón izquierdo
#                     self.draw_add_button(painter, QPointF(last_x + (microbloque.x() - last_x) / 2, self.height() / 2))
                    
#                     # Botón derecho
#                     next_x = microbloque.x() + microbloque.width() + 100 if i < len(self.microbloques) - 1 else self.width() - 90
#                     self.draw_add_button(painter, QPointF((microbloque.x() + microbloque.width() + next_x) / 2, self.height() / 2))
                    
#                     # Botón arriba
#                     self.draw_add_button(painter, QPointF(microbloque.x() + microbloque.width() / 2, microbloque.y() - 50))
                    
#                     # Botón abajo
#                     self.draw_add_button(painter, QPointF(microbloque.x() + microbloque.width() / 2, microbloque.y() + microbloque.height() + 50))
                    
#                     last_x = microbloque.x() + microbloque.width()

#     def draw_add_button(self, painter, point):
#         painter.drawEllipse(point, 15, 15)
#         painter.drawText(int(point.x() - 5), int(point.y() + 5), "+")

#     def mousePressEvent(self, event):
#         if self.creating_microbloque:
#             add_button = self.add_button_at_pos(event.pos())
#             if add_button:
#                 relation, pos, reference_microbloque = add_button
#                 self.add_microbloque(pos, relation, reference_microbloque)
#             self.creating_microbloque = False
#             self.setCursor(Qt.ArrowCursor)
#         else:
#             clicked_microbloque = self.microbloque_at_pos(event.pos())
#             if clicked_microbloque:
#                 self.selected_microbloque = clicked_microbloque
#             else:
#                 add_button = self.add_button_at_pos(event.pos())
#                 if add_button:
#                     self.create_new_microbloque(add_button)
#                 else:
#                     self.selected_microbloque = None
#         super().mousePressEvent(event)

#     def add_button_at_pos(self, pos):
#         if not self.microbloques:
#             mid_point = QPointF(self.width() / 2, self.height() / 2)
#             if (pos - mid_point).manhattanLength() < 15:
#                 return ('serie', mid_point, None)
        
#         last_x = 90
#         for i, microbloque in enumerate(self.microbloques):
#             if not microbloque.paralelo_con:
#                 # Botón izquierdo
#                 left_mid = QPointF(last_x + (microbloque.x() - last_x) / 2, self.height() / 2)
#                 if (pos - left_mid).manhattanLength() < 15:
#                     return ('izquierda', left_mid, microbloque)
                
#                 # Botón derecho
#                 next_x = microbloque.x() + microbloque.width() + 100 if i < len(self.microbloques) - 1 else self.width() - 90
#                 right_mid = QPointF((microbloque.x() + microbloque.width() + next_x) / 2, self.height() / 2)
#                 if (pos - right_mid).manhattanLength() < 15:
#                     return ('derecha', right_mid, microbloque)
                
#                 # Botón arriba
#                 top_mid = QPointF(microbloque.x() + microbloque.width() / 2, microbloque.y() - 50)
#                 if (pos - top_mid).manhattanLength() < 15:
#                     return ('arriba', top_mid, microbloque)
                
#                 # Botón abajo
#                 bottom_mid = QPointF(microbloque.x() + microbloque.width() / 2, microbloque.y() + microbloque.height() + 50)
#                 if (pos - bottom_mid).manhattanLength() < 15:
#                     return ('abajo', bottom_mid, microbloque)
                
#                 last_x = microbloque.x() + microbloque.width()
        
#         return None

#     def create_new_microbloque(self, add_button_info):
#         if add_button_info:
#             relation, pos, reference_microbloque = add_button_info
#             dialog = QDialog(self)
#             dialog.setWindowTitle("Nuevo Microbloque")
#             layout = QVBoxLayout()

#             name_input = QLineEdit()
#             name_input.setPlaceholderText("Nombre del microbloque")
#             layout.addWidget(name_input)

#             color_button = QPushButton("Seleccionar Color")
#             color_button.clicked.connect(lambda: self.select_color(color_button))
#             layout.addWidget(color_button)

#             transfer_label = QLabel("Función de Transferencia:")
#             latex_editor = LatexEditor()
#             layout.addWidget(transfer_label)
#             layout.addWidget(latex_editor)

#             save_button = QPushButton("Guardar")
#             save_button.clicked.connect(dialog.accept)
#             layout.addWidget(save_button)

#             dialog.setLayout(layout)

#             if dialog.exec_():
#                 nombre = name_input.text() or f"Microbloque {len(self.microbloques) + 1}"
#                 color = color_button.property("selected_color") or QColor(255, 255, 0)
#                 funcion_transferencia = latex_editor.get_latex()
#                 config = {
#                     'nombre': nombre,
#                     'color': color,
#                     'funcion_transferencia': funcion_transferencia,
#                     'opciones_adicionales': {}
#                 }
#                 self.new_microbloque_config = config
#                 self.add_microbloque(pos, relation, reference_microbloque)

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             button.setStyleSheet(f"background-color: {color.name()};")
#             button.setProperty("selected_color", color)
                
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

#     def reorganize_microbloques(self):
#         if not self.microbloques:
#             return

#         start_x = 150
#         start_y = self.height() / 2
#         horizontal_spacing = 100
#         vertical_spacing = 100

#         x = start_x
#         for microbloque in self.microbloques:
#             if not microbloque.paralelo_con:
#                 microbloque.move(int(x), int(start_y - microbloque.height() / 2))
#                 x += microbloque.width() + horizontal_spacing
#             else:
#                 ref_x = microbloque.paralelo_con.x()
#                 ref_y = microbloque.paralelo_con.y()
#                 if microbloque.y() < ref_y:  # Arriba
#                     microbloque.move(int(ref_x), int(ref_y - microbloque.height() - vertical_spacing))
#                 else:  # Abajo
#                     microbloque.move(int(ref_x), int(ref_y + microbloque.paralelo_con.height() + vertical_spacing))

#         self.update()




from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor

class DrawingArea(QWidget):
    microbloque_created = pyqtSignal(object)

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
        
    def add_microbloque(self, pos, relation='serie', reference_microbloque=None):
        nombre = self.new_microbloque_config.get('nombre') or f"Microbloque {len(self.microbloques) + 1}"
        color = self.new_microbloque_config.get('color') or QColor(255, 255, 255)
        funcion_transferencia = self.new_microbloque_config.get('funcion_transferencia') or ""
        opciones_adicionales = self.new_microbloque_config.get('opciones_adicionales') or {}
        
        microbloque = Microbloque(nombre, self, color, funcion_transferencia, opciones_adicionales)
        
        if reference_microbloque:
            if relation in ['arriba', 'abajo']:
                if not hasattr(reference_microbloque, 'paralelo_con'):
                    reference_microbloque.paralelo_con = []
                reference_microbloque.paralelo_con.append(microbloque)
            elif relation == 'derecha':
                if hasattr(reference_microbloque, 'serie_con'):
                    microbloque.serie_con = reference_microbloque.serie_con
                reference_microbloque.serie_con = microbloque
            elif relation == 'izquierda':
                for mb in self.microbloques:
                    if hasattr(mb, 'serie_con') and mb.serie_con == reference_microbloque:
                        mb.serie_con = microbloque
                        break
                microbloque.serie_con = reference_microbloque
        
        self.microbloques.append(microbloque)
        microbloque.show()
        self.microbloque_created.emit(microbloque)
        self.reorganize_microbloques()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        self.draw_connections(painter)
        self.draw_io_blocks(painter)
        
        for microbloque in self.microbloques:
            painter.translate(microbloque.pos())
            microbloque.paintEvent(event)
            painter.translate(-microbloque.pos())
        
        self.draw_add_buttons(painter)

    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        entrada = QRectF(50, self.height() / 2 - 30, 80, 60)
        salida = QRectF(self.width() - 130, self.height() / 2 - 30, 80, 60)
        
        painter.drawRect(entrada)
        painter.drawText(entrada, Qt.AlignCenter, "Entrada")
        
        painter.drawRect(salida)
        painter.drawText(salida, Qt.AlignCenter, "Salida")

    def draw_connections(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        def draw_line(start, end):
            painter.drawLine(start, end)
        
        last_point = QPointF(130, self.height() / 2)
        for microbloque in self.microbloques:
            if not any(mb for mb in self.microbloques if hasattr(mb, 'serie_con') and mb.serie_con == microbloque):
                current_point = microbloque.pos() + QPointF(microbloque.width() / 2, microbloque.height() / 2)
                draw_line(last_point, QPointF(current_point.x() - microbloque.width() / 2, current_point.y()))
                
                if hasattr(microbloque, 'paralelo_con') and microbloque.paralelo_con:
                    top = min(mb.y() for mb in [microbloque] + microbloque.paralelo_con)
                    bottom = max(mb.y() + mb.height() for mb in [microbloque] + microbloque.paralelo_con)
                    mid_y = (top + bottom) / 2
                    draw_line(QPointF(current_point.x() - microbloque.width() / 2, current_point.y()),
                            QPointF(current_point.x() - microbloque.width() / 2, mid_y))
                    for mb in microbloque.paralelo_con:
                        mb_center = mb.pos() + QPointF(mb.width() / 2, mb.height() / 2)
                        draw_line(QPointF(current_point.x() - microbloque.width() / 2, mid_y),
                                QPointF(mb_center.x() - mb.width() / 2, mb_center.y()))
                        draw_line(QPointF(mb_center.x() + mb.width() / 2, mb_center.y()),
                                QPointF(current_point.x() + microbloque.width() / 2, mid_y))
                    draw_line(QPointF(current_point.x() + microbloque.width() / 2, mid_y),
                            QPointF(current_point.x() + microbloque.width() / 2, current_point.y()))
                
                last_point = current_point + QPointF(microbloque.width() / 2, 0)
            
            if hasattr(microbloque, 'serie_con') and microbloque.serie_con:
                start = microbloque.pos() + QPointF(microbloque.width(), microbloque.height() / 2)
                end = microbloque.serie_con.pos() + QPointF(0, microbloque.serie_con.height() / 2)
                draw_line(start, end)
        
        draw_line(last_point, QPointF(self.width() - 130, self.height() / 2))

    def draw_add_buttons(self, painter):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.white))
        
        def draw_button(point):
            painter.drawEllipse(point, 10, 10)
            painter.drawText(QRectF(point.x() - 5, point.y() - 5, 10, 10), Qt.AlignCenter, "+")
        
        if not self.microbloques:
            draw_button(QPointF(self.width() / 2, self.height() / 2))
        else:
            for microbloque in self.microbloques:
                draw_button(microbloque.pos() + QPointF(microbloque.width() + 20, microbloque.height() / 2))
                draw_button(microbloque.pos() + QPointF(-20, microbloque.height() / 2))
                draw_button(microbloque.pos() + QPointF(microbloque.width() / 2, -20))
                draw_button(microbloque.pos() + QPointF(microbloque.width() / 2, microbloque.height() + 20))

    def reorganize_microbloques(self):
        if not self.microbloques:
            return
        
        def organize_branch(start_microbloque, x, y, level=0):
            current_x = x
            current_y = y
            max_height = 0
            
            while start_microbloque:
                parallel_count = len(getattr(start_microbloque, 'paralelo_con', []))
                total_height = start_microbloque.height() * (parallel_count + 1) + 60 * parallel_count
                start_y = current_y - total_height / 2 + start_microbloque.height() / 2
                
                start_microbloque.move(int(current_x), int(start_y))
                max_height = max(max_height, total_height)
                
                if hasattr(start_microbloque, 'paralelo_con') and start_microbloque.paralelo_con:
                    for i, parallel_mb in enumerate(start_microbloque.paralelo_con):
                        parallel_y = start_y + (i + 1) * (start_microbloque.height() + 60)
                        parallel_mb.move(int(current_x), int(parallel_y))
                
                current_x += start_microbloque.width() + 100
                start_microbloque = getattr(start_microbloque, 'serie_con', None)
            
            return max_height
        
        start_microbloque = next((mb for mb in self.microbloques if not any(hasattr(other, 'serie_con') and other.serie_con == mb for other in self.microbloques)), None)
        
        if start_microbloque:
            organize_branch(start_microbloque, 150, self.height() / 2)
        
        self.update()

    def mousePressEvent(self, event):
        clicked_microbloque = self.microbloque_at_pos(event.pos())
        if clicked_microbloque:
            self.selected_microbloque = clicked_microbloque
        else:
            add_button = self.add_button_at_pos(event.pos())
            if add_button:
                self.create_new_microbloque(add_button)
            else:
                self.selected_microbloque = None
        self.update()

    def add_button_at_pos(self, pos):
        if not self.microbloques:
            mid_point = QPointF(self.width() / 2, self.height() / 2)
            if (pos - mid_point).manhattanLength() < 15:
                return ('serie', mid_point, None)
        
        for microbloque in self.microbloques:
            right_mid = microbloque.pos() + QPointF(microbloque.width() + 20, microbloque.height() / 2)
            if (pos - right_mid).manhattanLength() < 15:
                return ('derecha', right_mid, microbloque)
            
            left_mid = microbloque.pos() + QPointF(-20, microbloque.height() / 2)
            if (pos - left_mid).manhattanLength() < 15:
                return ('izquierda', left_mid, microbloque)
            
            top_mid = microbloque.pos() + QPointF(microbloque.width() / 2, -20)
            if (pos - top_mid).manhattanLength() < 15:
                return ('arriba', top_mid, microbloque)
            
            bottom_mid = microbloque.pos() + QPointF(microbloque.width() / 2, microbloque.height() + 20)
            if (pos - bottom_mid).manhattanLength() < 15:
                return ('abajo', bottom_mid, microbloque)
        
        return None

    def create_new_microbloque(self, add_button_info):
        if add_button_info:
            relation, pos, reference_microbloque = add_button_info
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
                color = color_button.property("selected_color") or QColor(255, 255, 255)
                funcion_transferencia = latex_editor.get_latex()
                config = {
                    'nombre': nombre,
                    'color': color,
                    'funcion_transferencia': funcion_transferencia,
                    'opciones_adicionales': {}
                }
                self.new_microbloque_config = config
                self.add_microbloque(pos, relation, reference_microbloque)

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
        delete_action = menu.addAction("Eliminar")
        
        action = menu.exec_(self.mapToGlobal(pos))
        
        if action == delete_action:
            clicked_microbloque = self.microbloque_at_pos(pos)
            if clicked_microbloque:
                self.delete_microbloque(clicked_microbloque)

    def delete_microbloque(self, microbloque=None):
        if microbloque is None:
            microbloque = self.selected_microbloque
        if microbloque:
            self.microbloques.remove(microbloque)
            for mb in self.microbloques:
                if hasattr(mb, 'paralelo_con') and microbloque in mb.paralelo_con:
                    mb.paralelo_con.remove(microbloque)
                if hasattr(mb, 'serie_con') and mb.serie_con == microbloque:
                    mb.serie_con = getattr(microbloque, 'serie_con', None)
            microbloque.deleteLater()
            self.selected_microbloque = None
            self.update()
            self.reorganize_microbloques()