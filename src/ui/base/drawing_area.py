# from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
# from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QCursor
# from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPoint
# from .micro_bloque import Microbloque
# from .latex_editor import LatexEditor
# from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

# class DrawingArea(QWidget):
#     def __init__(self, parent=None, modelo=None):
#         super().__init__(parent)
#         self.microbloques = []
#         self.selected_microbloque = None
#         self.modelo = modelo # es la representacion backend del macrobloque
#         self.creating_microbloque = False
#         self.new_microbloque_config = {}
#         self.add_buttons = []
#         self.button_size = 20
#         self.init_ui()
        
#     def init_ui(self):
#         self.setStyleSheet("background-color: white; border: 1px solid black;")
#         self.setContextMenuPolicy(Qt.CustomContextMenu)
    
#     def load_microbloques(self):
#         self.microbloques = []
#         self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
#         self.update()
    
#     def dibujar_topologia(self, topologia, posicion_inicial):
#         if isinstance(topologia, TopologiaSerie):
#             self.dibujar_serie(topologia, posicion_inicial)
#         elif isinstance(topologia, TopologiaParalelo):
#             self.dibujar_paralelo(topologia, posicion_inicial)
#         elif isinstance(topologia, MicroBloque):
#             self.create_microbloque(topologia, posicion_inicial)
        
#     def dibujar_serie(self, serie, posicion_inicial):
#         posicion_actual = posicion_inicial
#         for hijo in serie.hijos:
#             self.dibujar_topologia(hijo, posicion_actual)
#             posicion_actual.setX(posicion_actual.x() + 200) # TODO: Modificar el valor segun convenga (es el margen horizontal entre microbloques)

#     def dibujar_paralelo(self, paralelo, posicion_inicial):
#         posicion_actual = posicion_inicial
#         for hijo in paralelo.hijos:
#             self.dibujar_topologia(hijo, posicion_actual)
#             posicion_actual.setY(posicion_actual.y() + 100) # TODO: Modificar el valor segun convenga (es el margen vertical entre microbloques)

#     def create_microbloque(self, microbloque_back, pos):
#         microbloque = Microbloque(self, microbloque_back)
#         microbloque.setParent(self)
#         microbloque.setPos(pos)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         self.update_connections()
    
#     def clear_all(self):
#         self.microbloques = []
#         # TODO: Si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
#         self.update_connections()
    
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         painter = QPainter(self)
#         self.draw_io_blocks(painter)
        
#         if not self.microbloques:
#             self.draw_empty_connection(painter)
#         else:
#             self.draw_connections(painter)

#     def draw_empty_connection(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
#         entrada = QPointF(90, self.height() / 2)
#         salida = QPointF(self.width() - 170, self.height() / 2)
#         painter.drawLine(entrada, salida)
        
#         # Dibujar el botón "+" en el medio
#         center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
#         button_size = 30
#         button_rect = QRectF(center.x() - button_size/2, center.y() - button_size/2, button_size, button_size)
#         painter.setBrush(QBrush(Qt.white))
#         painter.drawEllipse(button_rect)
#         painter.drawText(button_rect, Qt.AlignCenter, "+")

#         # Guardar la posición del botón para detectar clics
#         self.add_button_rect = button_rect

#     def draw_io_blocks(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
        
#         radio = 40  # Radio del círculo
#         centro_y = self.height() / 2  # Posición y del centro para ambos círculos
        
#         centro_entrada_x = 50 + radio  # Posición x del centro del círculo de entrada
#         centro_salida_x = self.width() - 130 - radio  # Posición x del centro del círculo de salida
        
#         # Dibujar los círculos de entrada y salida
#         painter.drawEllipse(QPointF(centro_entrada_x, centro_y), radio, radio)
#         painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Entrada")
        
#         painter.drawEllipse(QPointF(centro_salida_x, centro_y), radio, radio)
#         painter.drawText(QRectF(self.width()-209, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Salida")
    
#     def draw_connections(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
#         for i in range(len(self.microbloques) - 1):
#             start = self.microbloques[i].pos() + QPoint(self.microbloques[i].width(), self.microbloques[i].height() // 2)
#             end = self.microbloques[i+1].pos() + QPoint(0, self.microbloques[i+1].height() // 2)
#             painter.drawLine(start, end)

#         # Conectar el primer microbloque con la entrada
#         if self.microbloques:
#             entrada = QPointF(90, self.height() / 2)
#             primer_micro = self.microbloques[0].pos() + QPoint(0, self.microbloques[0].height() // 2)
#             painter.drawLine(entrada, primer_micro)

#         # Conectar el último microbloque con la salida
#         if self.microbloques:
#             salida = QPointF(self.width() - 170, self.height() / 2)
#             ultimo_micro = self.microbloques[-1].pos() + QPoint(self.microbloques[-1].width(), self.microbloques[-1].height() // 2)
#             painter.drawLine(ultimo_micro, salida)

#     def create_new_microbloque(self, pos, relation=None, reference_microbloque=None):
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
#             config = {
#                 'nombre': nombre,
#                 'color': color,
#                 'funcion_transferencia': funcion_transferencia,
#                 'opciones_adicionales': {}
#             }
#             new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.modelo.topologia)

#             if reference_microbloque and relation == "arriba":
#                 reference_microbloque.elemento_back.agregar_arriba(new_microbloque)
#             elif reference_microbloque and relation == "abajo":
#                 reference_microbloque.elemento_back.agregar_abajo(new_microbloque)
#             elif reference_microbloque and relation == "antes":
#                 reference_microbloque.elemento_back.agregar_antes(new_microbloque)
#             elif reference_microbloque and relation == "despues":
#                 reference_microbloque.elemento_back.agregar_despues(new_microbloque)
#             else:
#                 self.modelo.topologia.agregar_elemento(new_microbloque) # sería el primer microbloque
            
#             self.load_microbloques()  # recargo todos los microbloques
#             self.update()
#             self.hide_add_buttons() # ocultamos los botones "+" por si quedaron visibles

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             button.setStyleSheet(f"background-color: {color.name()};")
#             button.setProperty("selected_color", color)
    
#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)

#         if not self.microbloques: # si no hay microbloques y se hace click sobre el único botón "+", entonces se crea un microbloque 
#             if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(event.pos()):
#                 self.create_new_microbloque(self.add_button_rect.center())
#         else: # si hay microbloques, se busca el microbloque que se seleccionó
#             for microbloque in self.microbloques:
#                 if microbloque.geometry().contains(event.pos()):
#                     self.selected_microbloque = microbloque
#                     self.show_add_buttons(microbloque) # muestra los botones "+" alrededor del microbloque
#                     break
#             else:
#                 self.selected_microbloque = None
#                 self.hide_add_buttons() # oculta los botones "+"
        
#         self.update()

#     def show_add_buttons(self, microbloque):
#         self.hide_add_buttons()
#         positions = [
#             ('arriba', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() - self.button_size/2)),
#             ('abajo', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() + microbloque.height() + self.button_size/2)),
#             ('izquierda', QPointF(microbloque.x() - self.button_size/2, microbloque.y() + microbloque.height()/2)),
#             ('derecha', QPointF(microbloque.x() + microbloque.width() + self.button_size/2, microbloque.y() + microbloque.height()/2))
#         ]
        
#         for direction, pos in positions:
#             button = QPushButton("+", self)
#             button.setGeometry(int(pos.x() - self.button_size/2), int(pos.y() - self.button_size/2), self.button_size, self.button_size)
#             button.clicked.connect(lambda _, d=direction: self.add_microbloque(d))
#             button.show()
#             self.add_buttons.append(button)

#     def hide_add_buttons(self):
#         for button in self.add_buttons:
#             button.deleteLater()
#         self.add_buttons.clear()

#     def add_microbloque(self, direction):
#         # segun la dirección en la que se hizo click, determino la relación con el microbloque seleccionado
#         if self.selected_microbloque:
#             if direction in ['arriba', 'abajo']:
#                 relation = direction
#             elif direction == 'izquierda':
#                 relation = 'antes'
#             else:  # derecha
#                 relation = 'despues'
            
#             self.create_new_microbloque(self.selected_microbloque.pos(), relation, self.selected_microbloque)

#     def update_connections(self):
#         self.update()

from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPoint
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

class DrawingArea(QWidget):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.button_size = 20
        self.margen_paralelo = 30  # Margen para las bifurcaciones
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
    
    def load_microbloques(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
        self.update()
    
    def dibujar_topologia(self, topologia, posicion_inicial):
        if isinstance(topologia, TopologiaSerie):
            return self.dibujar_serie(topologia, posicion_inicial)
        elif isinstance(topologia, TopologiaParalelo):
            return self.dibujar_paralelo(topologia, posicion_inicial)
        elif isinstance(topologia, MicroBloque):
            return self.create_microbloque(topologia, posicion_inicial)
        
    def dibujar_serie(self, serie, posicion_inicial):
        posicion_actual = posicion_inicial
        microbloques_serie = []
        for hijo in serie.hijos:
            micro = self.dibujar_topologia(hijo, posicion_actual)
            if isinstance(micro, list):
                microbloques_serie.extend(micro)
                if micro:  # Solo ajusta la posición si se crearon microbloques
                    posicion_actual.setX(posicion_actual.x() + 200 + self.margen_paralelo * 2)
            elif micro:
                microbloques_serie.append(micro)
                posicion_actual.setX(posicion_actual.x() + 200)
        return microbloques_serie

    def dibujar_paralelo(self, paralelo, posicion_inicial):
        microbloques_paralelos = []
        posicion_actual = posicion_inicial.y()
        for hijo in paralelo.hijos:
            micro = self.dibujar_topologia(hijo, QPointF(posicion_inicial.x() + self.margen_paralelo, posicion_actual))
            if isinstance(micro, list):
                microbloques_paralelos.extend(micro)
            elif micro:
                microbloques_paralelos.append(micro)
            if micro:  # Solo ajusta la posición si se crearon microbloques
                posicion_actual += 100
        return microbloques_paralelos

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        return microbloque
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        self.draw_io_blocks(painter)
        
        if not self.microbloques:
            self.draw_empty_connection(painter)
        else:
            self.draw_connections(painter)

    def draw_empty_connection(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        entrada = QPointF(90, self.height() / 2)
        salida = QPointF(self.width() - 170, self.height() / 2)
        painter.drawLine(entrada, salida)
        
        center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
        button_size = 30
        button_rect = QRectF(center.x() - button_size/2, center.y() - button_size/2, button_size, button_size)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")
        self.add_button_rect = button_rect

    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        radio = 40
        centro_y = self.height() / 2
        
        centro_entrada_x = 50 + radio
        centro_salida_x = self.width() - 130 - radio
        
        painter.drawEllipse(QPointF(centro_entrada_x, centro_y), radio, radio)
        painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Entrada")
        
        painter.drawEllipse(QPointF(centro_salida_x, centro_y), radio, radio)
        painter.drawText(QRectF(self.width()-209, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Salida")
    
    def draw_connections(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        if self.microbloques:
            entrada = QPointF(90, self.height() / 2)
            salida = QPointF(self.width() - 170, self.height() / 2)
            
            self.draw_connection_tree(painter, self.modelo.topologia, entrada, salida)

    def draw_connection_tree(self, painter, topologia, start, end):
        if isinstance(topologia, TopologiaSerie):
            self.draw_serie_connections(painter, topologia, start, end)
        elif isinstance(topologia, TopologiaParalelo):
            self.draw_paralelo_connections(painter, topologia, start, end)
        elif isinstance(topologia, MicroBloque):
            microbloque = next(m for m in self.microbloques if m.elemento_back == topologia)
            painter.drawLine(start, microbloque.pos() + QPoint(0, microbloque.height() // 2))
            painter.drawLine(microbloque.pos() + QPoint(microbloque.width(), microbloque.height() // 2), end)

    def draw_serie_connections(self, painter, serie, start, end):
        current_pos = start
        for i, hijo in enumerate(serie.hijos):
            if i == len(serie.hijos) - 1:
                next_pos = end
            else:
                next_pos = QPointF(current_pos.x() + 200, current_pos.y())
            self.draw_connection_tree(painter, hijo, current_pos, next_pos)
            current_pos = next_pos

    def draw_paralelo_connections(self, painter, paralelo, start, end):
        bifurcacion = QPointF(start.x() + self.margen_paralelo, start.y())
        unificacion = QPointF(end.x() - self.margen_paralelo, end.y())
        
        painter.drawLine(start, bifurcacion)
        painter.drawLine(unificacion, end)
        
        y_positions = []
        for hijo in paralelo.hijos:
            if isinstance(hijo, MicroBloque):
                microbloque = next((m for m in self.microbloques if m.elemento_back == hijo), None)
                if microbloque:
                    y_positions.append(microbloque.pos().y() + microbloque.height() // 2)
            elif isinstance(hijo, TopologiaSerie):
                # Calculamos la posición Y promedio de los microbloques en la serie
                serie_y_positions = [m.pos().y() + m.height() // 2 for m in self.microbloques if m.elemento_back in hijo.hijos]
                if serie_y_positions:
                    y_positions.append(sum(serie_y_positions) / len(serie_y_positions))
        
        for y in y_positions:
            painter.drawLine(bifurcacion, QPointF(bifurcacion.x(), y))
            painter.drawLine(QPointF(unificacion.x(), y), unificacion)
        
        for i, hijo in enumerate(paralelo.hijos):
            if i < len(y_positions):
                self.draw_connection_tree(painter, hijo, 
                                        QPointF(bifurcacion.x(), y_positions[i]),
                                        QPointF(unificacion.x(), y_positions[i]))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if not self.microbloques:
            if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(event.pos()):
                self.create_new_microbloque(self.add_button_rect.center())
        else:
            for microbloque in self.microbloques:
                if microbloque.geometry().contains(event.pos()):
                    self.selected_microbloque = microbloque
                    self.show_add_buttons(microbloque)
                    break
            else:
                self.selected_microbloque = None
                self.hide_add_buttons()
        
        self.update()

    def show_add_buttons(self, microbloque):
        self.hide_add_buttons()
        positions = [
            ('arriba', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() - self.button_size/2)),
            ('abajo', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() + microbloque.height() + self.button_size/2)),
            ('izquierda', QPointF(microbloque.x() - self.button_size/2, microbloque.y() + microbloque.height()/2)),
            ('derecha', QPointF(microbloque.x() + microbloque.width() + self.button_size/2, microbloque.y() + microbloque.height()/2))
        ]
        
        for direction, pos in positions:
            button = QPushButton("+", self)
            button.setGeometry(int(pos.x() - self.button_size/2), int(pos.y() - self.button_size/2), self.button_size, self.button_size)
            button.clicked.connect(lambda _, d=direction: self.add_microbloque(d))
            button.show()
            self.add_buttons.append(button)

    def hide_add_buttons(self):
        for button in self.add_buttons:
            button.deleteLater()
        self.add_buttons.clear()

    def add_microbloque(self, direction):
        if self.selected_microbloque:
            if direction in ['arriba', 'abajo']:
                relation = direction
            elif direction == 'izquierda':
                relation = 'antes'
            else:
                relation = 'despues'
            
            self.create_new_microbloque(self.selected_microbloque.pos(), relation, self.selected_microbloque)

    def create_new_microbloque(self, pos, relation=None, reference_microbloque=None):
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
            new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.modelo.topologia)

            if reference_microbloque and relation == "arriba":
                reference_microbloque.elemento_back.agregar_arriba(new_microbloque)
            elif reference_microbloque and relation == "abajo":
                reference_microbloque.elemento_back.agregar_abajo(new_microbloque)
            elif reference_microbloque and relation == "antes":
                reference_microbloque.elemento_back.agregar_antes(new_microbloque)
            elif reference_microbloque and relation == "despues":
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

    def delete_microbloque(self, microbloque):
        self.microbloques.remove(microbloque)
        if isinstance(self.modelo.topologia, TopologiaSerie):
            self.modelo.topologia.hijos.remove(microbloque.elemento_back)
        elif isinstance(self.modelo.topologia, TopologiaParalelo):
            for serie in self.modelo.topologia.hijos:
                if microbloque.elemento_back in serie.hijos:
                    serie.hijos.remove(microbloque.elemento_back)
                    break
        microbloque.deleteLater()
        self.selected_microbloque = None
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()

    def clear_all(self):
        self.microbloques = []
        # TODO: Si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
        self.update_connections()