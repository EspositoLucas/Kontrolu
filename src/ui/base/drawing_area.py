# from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
# from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
# from PyQt5.QtCore import Qt, QPointF, QRectF
# from .micro_bloque import Microbloque
# from .latex_editor import LatexEditor
# from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

# class DrawingArea(QWidget):
#     def __init__(self, parent=None, modelo=None):
#         super().__init__(parent)
#         self.microbloques = []
#         self.selected_microbloque = None
#         self.modelo = modelo
#         self.margen_paralelo = 30
#         self.init_ui()
        
#     def init_ui(self):
#         self.setStyleSheet("background-color: white; border: 1px solid black;")
    
#     def load_microbloques(self):
#         for microbloque in self.microbloques:
#             microbloque.deleteLater()
#         self.microbloques.clear()
#         self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
#         self.update()
    
#     def dibujar_topologia(self, topologia, posicion_inicial):
#         if isinstance(topologia, TopologiaSerie):
#             return self.dibujar_serie(topologia, posicion_inicial)
#         elif isinstance(topologia, TopologiaParalelo):
#             return self.dibujar_paralelo(topologia, posicion_inicial)
#         elif isinstance(topologia, MicroBloque):
#             return self.create_microbloque(topologia, posicion_inicial)
        
#     def dibujar_serie(self, serie, posicion_inicial):
#         posicion_actual = posicion_inicial
#         microbloques_serie = []
#         for hijo in serie.hijos:
#             micro = self.dibujar_topologia(hijo, posicion_actual)
#             if isinstance(micro, list):
#                 microbloques_serie.extend(micro)
#                 if micro:
#                     posicion_actual.setX(posicion_actual.x() + 200 + self.margen_paralelo * 2)
#             elif micro:
#                 microbloques_serie.append(micro)
#                 posicion_actual.setX(posicion_actual.x() + 200)
#         return microbloques_serie

#     def dibujar_paralelo(self, paralelo, posicion_inicial):
#         microbloques_paralelos = []
#         posicion_actual = posicion_inicial.y()
#         for hijo in paralelo.hijos:
#             micro = self.dibujar_topologia(hijo, QPointF(posicion_inicial.x() + self.margen_paralelo, posicion_actual))
#             if isinstance(micro, list):
#                 microbloques_paralelos.extend(micro)
#             elif micro:
#                 microbloques_paralelos.append(micro)
#             if micro:
#                 posicion_actual += 100
#         return microbloques_paralelos

#     def create_microbloque(self, microbloque_back, pos):
#         microbloque = Microbloque(self, microbloque_back)
#         microbloque.setParent(self)
#         microbloque.setPos(pos)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         return microbloque
    
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         self.draw_io_blocks(painter)
        
#         if not self.microbloques:
#             self.draw_empty_connection(painter)
#         else:
#             self.draw_connections(painter)

#     def draw_empty_connection(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
#         entrada = QPointF(130, self.height() / 2)
#         salida = QPointF(self.width() - 210, self.height() /2)
#         painter.drawLine(entrada, salida)
        
#         center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
#         button_size = 30
#         button_rect = QRectF(center.x() - button_size/2, center.y() - button_size/2, button_size, button_size)
#         painter.setBrush(QBrush(Qt.white))
#         painter.drawEllipse(button_rect)
#         painter.drawText(button_rect, Qt.AlignCenter, "+")
#         self.add_button_rect = button_rect

#     def draw_io_blocks(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
        
#         radio = 40
#         centro_y = self.height() / 2
        
#         centro_entrada_x = 50 + radio
#         centro_salida_x = self.width() - 130 - radio
        
#         painter.drawEllipse(QPointF(centro_entrada_x, centro_y), radio, radio)
#         painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "ENTRADA")
        
#         painter.drawEllipse(QPointF(centro_salida_x, centro_y), radio, radio)
#         painter.drawText(QRectF(self.width()-209, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "SALIDA")
    
#     def draw_connections(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
        
#         if self.microbloques:
#             entrada = QPointF(130, self.height() / 2)
#             salida = QPointF(self.width() - 210, self.height() / 2)
            
#             self.draw_connection_tree(painter, self.modelo.topologia, entrada, salida)

#     def draw_connection_tree(self, painter, topologia, start, end):
#         if isinstance(topologia, TopologiaSerie):
#             self.draw_serie_connections(painter, topologia, start, end)
#         elif isinstance(topologia, TopologiaParalelo):
#             self.draw_paralelo_connections(painter, topologia, start, end)
#         elif isinstance(topologia, MicroBloque):
#             microbloque = next(m for m in self.microbloques if m.elemento_back == topologia)
#             painter.drawLine(start, microbloque.pos() + QPointF(0, microbloque.height() // 2))
#             painter.drawLine(microbloque.pos() + QPointF(microbloque.width(), microbloque.height() // 2), end)

#     def draw_serie_connections(self, painter, serie, start, end):
#         current_pos = start
#         for i, hijo in enumerate(serie.hijos):
#             if i == len(serie.hijos) - 1:
#                 next_pos = end
#             else:
#                 next_pos = QPointF(current_pos.x() + 200, current_pos.y())
#             self.draw_connection_tree(painter, hijo, current_pos, next_pos)
#             current_pos = next_pos

#     def draw_paralelo_connections(self, painter, paralelo, start, end):
#         bifurcacion = QPointF(start.x() + self.margen_paralelo, start.y())
#         unificacion = QPointF(end.x() - self.margen_paralelo, end.y())
        
#         painter.drawLine(start, bifurcacion)
#         painter.drawLine(unificacion, end)
        
#         y_positions = []
#         for hijo in paralelo.hijos:
#             if isinstance(hijo, MicroBloque):
#                 microbloque = next((m for m in self.microbloques if m.elemento_back == hijo), None)
#                 if microbloque:
#                     y_positions.append(microbloque.pos().y() + microbloque.height() // 2)
#             elif isinstance(hijo, TopologiaSerie):
#                 serie_y_positions = [m.pos().y() + m.height() // 2 for m in self.microbloques if m.elemento_back in hijo.hijos]
#                 if serie_y_positions:
#                     y_positions.append(sum(serie_y_positions) / len(serie_y_positions))
        
#         for y in y_positions:
#             painter.drawLine(bifurcacion, QPointF(bifurcacion.x(), y))
#             painter.drawLine(QPointF(unificacion.x(), y), unificacion)
        
#         for i, hijo in enumerate(paralelo.hijos):
#             if i < len(y_positions):
#                 self.draw_connection_tree(painter, hijo, 
#                                         QPointF(bifurcacion.x(), y_positions[i]),
#                                         QPointF(unificacion.x(), y_positions[i]))

#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)

#         if not self.microbloques:
#             if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(event.pos()):
#                 self.create_new_microbloque(self.add_button_rect.center())
#         else:
#             for microbloque in self.microbloques:
#                 if microbloque.geometry().contains(event.pos()):
#                     self.selected_microbloque = microbloque
#                     self.show_context_menu(event.pos())
#                     break
#             else:
#                 self.selected_microbloque = None

#     def show_context_menu(self, pos):
#         context_menu = QMenu(self)
#         add_serie = context_menu.addAction("Agregar en Serie")
#         add_paralelo = context_menu.addAction("Agregar en Paralelo")
#         delete_action = context_menu.addAction("Eliminar")

#         action = context_menu.exec_(self.mapToGlobal(pos))
#         if action == add_serie:
#             self.add_microbloque_serie()
#         elif action == add_paralelo:
#             self.add_microbloque_paralelo()
#         elif action == delete_action:
#             self.delete_microbloque(self.selected_microbloque)

#     def add_microbloque_serie(self):
#         if self.selected_microbloque:
#             self.create_new_microbloque(self.selected_microbloque.pos(), 'serie')

#     def add_microbloque_paralelo(self):
#         if self.selected_microbloque:
#             self.create_new_microbloque(self.selected_microbloque.pos(), 'paralelo')

#     def create_new_microbloque(self, pos, relation=None):
#         dialog = QDialog(self)
#         dialog.setWindowTitle("Nuevo Microbloque")
#         layout = QVBoxLayout()

#         name_input = QLineEdit()
#         name_input.setPlaceholderText("Nombre del microbloque")
#         layout.addWidget(name_input)

#         color_button = QPushButton("Seleccionar Color")
#         color_button.clicked.connect(lambda: self.select_color(color_button))
#         layout.addWidget(color_button)

#         transfer_label = QLabel("Función de Transferencia:")
#         latex_editor = LatexEditor()
#         layout.addWidget(transfer_label)
#         layout.addWidget(latex_editor)

#         save_button = QPushButton("Guardar")
#         save_button.clicked.connect(dialog.accept)
#         layout.addWidget(save_button)

#         dialog.setLayout(layout)

#         if dialog.exec_():
#             nombre = name_input.text() or f"Microbloque {len(self.microbloques) + 1}"
#             color = color_button.property("selected_color") or QColor(255, 255, 255)
#             funcion_transferencia = latex_editor.get_latex()
#             new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {})

#             if relation == 'serie':
#                 self.modelo.topologia.agregar_despues_de(new_microbloque, self.selected_microbloque.elemento_back)
#             elif relation == 'paralelo':
#                 self.modelo.topologia.agregar_arriba_de(new_microbloque, self.selected_microbloque.elemento_back)
#             else:
#                 self.modelo.topologia.agregar_elemento(new_microbloque)
            
#             self.load_microbloques()
#             self.update()

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             button.setStyleSheet(f"background-color: {color.name()};")
#             button.setProperty("selected_color", color)

#     def delete_microbloque(self, microbloque):
#         if microbloque:
#             microbloque.elemento_back.borrar_elemento()
#             self.microbloques.remove(microbloque)
#             microbloque.deleteLater()
#             self.selected_microbloque = None
#             self.load_microbloques()
#             self.update()

#     def clear_all(self):
#         for microbloque in self.microbloques:
#             microbloque.deleteLater()
#         self.microbloques.clear()
#         self.modelo.topologia = TopologiaSerie()
#         self.update()


from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPoint
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

class DrawingArea(QGraphicsView):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.canvas = Canvas(modelo)
        self.scene.addItem(self.canvas)
        self.scale(1, 1)  # Escala inicial

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)

class Canvas(QGraphicsItem):
    def __init__(self, modelo=None):
        super().__init__()
        self.microbloques = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.button_size = 20
        self.bifurcation_points = []
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        return QRectF(-10000, -10000, 20000, 20000)  # Área de dibujo muy grande

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        self.draw_io_blocks(painter)
        
        if not self.microbloques:
            self.draw_empty_connection(painter)
        else:
            self.draw_connections(painter)

    def load_microbloques(self):
        for microbloque in self.microbloques:
            self.scene().removeItem(microbloque)
        self.microbloques.clear()
        self.bifurcation_points.clear()
        self.dibujar_topologia(self.modelo.topologia, QPointF(0, 0))
        self.update()

    def dibujar_topologia(self, topologia, posicion_inicial):
        if isinstance(topologia, TopologiaSerie):
            self.dibujar_serie(topologia, posicion_inicial)
        elif isinstance(topologia, TopologiaParalelo):
            self.dibujar_paralelo(topologia, posicion_inicial)
        elif isinstance(topologia, MicroBloque):
            self.create_microbloque(topologia, posicion_inicial)

    def dibujar_serie(self, serie, posicion_inicial):
        posicion_actual = posicion_inicial
        for hijo in serie.hijos:
            self.dibujar_topologia(hijo, posicion_actual)
            posicion_actual.setX(posicion_actual.x() + 200)

    def dibujar_paralelo(self, paralelo, posicion_inicial):
        num_hijos = len(paralelo.hijos)
        espaciado_vertical = 100
        altura_total = (num_hijos - 1) * espaciado_vertical
        posicion_inicial_y = posicion_inicial.y() - altura_total / 2
        
        punto_bifurcacion_entrada = QPointF(posicion_inicial.x() - 50, posicion_inicial.y())
        self.bifurcation_points.append(punto_bifurcacion_entrada)
        
        for i, hijo in enumerate(paralelo.hijos):
            posicion_actual = QPointF(posicion_inicial.x(), posicion_inicial_y + i * espaciado_vertical)
            self.dibujar_topologia(hijo, posicion_actual)
        
        ultimo_hijo = paralelo.hijos[-1]
        if isinstance(ultimo_hijo, MicroBloque):
            x_salida = posicion_inicial.x() + 200
        else:
            x_salida = max(microbloque.pos().x() for microbloque in self.microbloques if microbloque.elemento_back in paralelo.hijos) + 200
        
        punto_bifurcacion_salida = QPointF(x_salida, posicion_inicial.y())
        self.bifurcation_points.append(punto_bifurcacion_salida)

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.update()

    def clear_all(self):
        for microbloque in self.microbloques:
            self.scene().removeItem(microbloque)
        self.microbloques.clear()
        self.bifurcation_points.clear()
        self.modelo.reset_topologia()
        self.load_microbloques()
        self.update()

    def draw_empty_connection(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        entrada = QPointF(-100, 0)
        salida = QPointF(100, 0)
        painter.drawLine(entrada, salida)
        
        center = QPointF(0, 0)
        button_size = 30
        button_rect = QRectF(center.x() - button_size/2, center.y() - button_size/2, button_size, button_size)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")
        self.add_button_rect = button_rect

    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        radio = 40
        
        painter.drawEllipse(QPointF(-150, 0), radio, radio)
        painter.drawText(QRectF(-190, -30, 80, 60), Qt.AlignCenter, "Entrada")
        
        painter.drawEllipse(QPointF(150, 0), radio, radio)
        painter.drawText(QRectF(110, -30, 80, 60), Qt.AlignCenter, "Salida")

    def draw_connections(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        for point in self.bifurcation_points:
            painter.drawEllipse(point, 5, 5)
        
        for i, microbloque in enumerate(self.microbloques):
            start = microbloque.pos() + QPointF(0, microbloque.boundingRect().height() / 2)
            end = microbloque.pos() + QPointF(microbloque.boundingRect().width(), microbloque.boundingRect().height() / 2)
            
            if i == 0 or microbloque.elemento_back.padre != self.microbloques[i-1].elemento_back.padre:
                for point in self.bifurcation_points:
                    if abs(point.y() - start.y()) < 1 and point.x() < start.x():
                        painter.drawLine(point, start)
                        break
                else:
                    entrada = QPointF(-100, 0)
                    painter.drawLine(entrada, start)
            
            if i == len(self.microbloques) - 1 or microbloque.elemento_back.padre != self.microbloques[i+1].elemento_back.padre:
                for point in self.bifurcation_points:
                    if abs(point.y() - end.y()) < 1 and point.x() > end.x():
                        painter.drawLine(end, point)
                        break
                else:
                    salida = QPointF(100, 0)
                    painter.drawLine(end, salida)
            
            if i < len(self.microbloques) - 1 and microbloque.elemento_back.padre == self.microbloques[i+1].elemento_back.padre:
                next_start = self.microbloques[i+1].pos() + QPointF(0, self.microbloques[i+1].boundingRect().height() / 2)
                painter.drawLine(end, next_start)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.microbloques:
            if self.add_button_rect.contains(event.pos()):
                self.create_new_microbloque(self.add_button_rect.center())
        else:
            item = self.scene().itemAt(event.scenePos(), self.transform())
            if isinstance(item, Microbloque):
                self.selected_microbloque = item
                self.show_context_menu(event.scenePos())
            else:
                self.selected_microbloque = None

    def show_context_menu(self, pos):
        context_menu = QMenu()
        add_action = context_menu.addAction("Agregar microbloque")
        delete_action = context_menu.addAction("Eliminar microbloque")
        
        action = context_menu.exec_(self.mapToGlobal(pos.toPoint()))
        
        if action == add_action:
            self.show_add_buttons(self.selected_microbloque)
        elif action == delete_action:
            self.delete_microbloque(self.selected_microbloque)

    def show_add_buttons(self, microbloque):
        self.hide_add_buttons()
        positions = [
            ('arriba', QPointF(0, -microbloque.boundingRect().height()/2 - self.button_size/2)),
            ('abajo', QPointF(0, microbloque.boundingRect().height()/2 + self.button_size/2)),
            ('izquierda', QPointF(-microbloque.boundingRect().width()/2 - self.button_size/2, 0)),
            ('derecha', QPointF(microbloque.boundingRect().width()/2 + self.button_size/2, 0))
        ]
        
        for direction, offset in positions:
            button = QPushButton("+")
            button.setFixedSize(self.button_size, self.button_size)
            button.clicked.connect(lambda _, d=direction: self.add_microbloque(d))
            proxy = self.scene().addWidget(button)
            proxy.setPos(microbloque.pos() + offset)
            self.add_buttons.append(proxy)

    def hide_add_buttons(self):
        for button in self.add_buttons:
            self.scene().removeItem(button)
        self.add_buttons.clear()

    def add_microbloque(self, direction):
        if self.selected_microbloque:
            relation = 'despues' if direction == 'derecha' else 'antes' if direction == 'izquierda' else direction
            self.create_new_microbloque(self.selected_microbloque.pos(), relation, self.selected_microbloque)

    def delete_microbloque(self, microbloque):
        if microbloque in self.microbloques:
            self.microbloques.remove(microbloque)
            microbloque.elemento_back.borrar_elemento()
            self.scene().removeItem(microbloque)
            self.load_microbloques()

    def create_new_microbloque(self, pos, relation=None, reference_microbloque=None):
        dialog = QDialog()
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
            new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.modelo.topologia)

            if reference_microbloque:
                if relation == "arriba":
                    reference_microbloque.elemento_back.agregar_arriba(new_microbloque)
                elif relation == "abajo":
                    reference_microbloque.elemento_back.agregar_abajo(new_microbloque)
                elif relation == "antes":
                    reference_microbloque.elemento_back.agregar_antes(new_microbloque)
                elif relation == "despues":
                    reference_microbloque.elemento_back.agregar_despues(new_microbloque)
            else:
                self.modelo.topologia.agregar_elemento(new_microbloque)
            
            self.load_microbloques()
            self.update()
            self.hide_add_buttons()

    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")
            button.setProperty("selected_color", color)
