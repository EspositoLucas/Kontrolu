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
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def load_microbloques(self):
        self.microbloques = []
        self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
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
        posicion_actual = posicion_inicial
        vertical_offset = 100
        for i, hijo in enumerate(paralelo.hijos):
            y_offset = (i - (len(paralelo.hijos) - 1) / 2) * vertical_offset
            self.dibujar_topologia(hijo, QPointF(posicion_actual.x(), posicion_actual.y() + y_offset))

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.update_connections()
    
    def clear_all(self):
        reply = QMessageBox.question(self, 'Confirmar borrado', '¿Está seguro de que desea borrar todos los microbloques?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for microbloque in self.microbloques:
                microbloque.deleteLater()
            self.microbloques = []
            self.modelo.topologia = TopologiaSerie()
            self.update_connections()
    
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
        self.draw_topologia_connections(self.modelo.topologia, painter)

        if self.microbloques:
            entrada = QPointF(90, self.height() / 2)
            primer_micro = self.microbloques[0].pos() + QPoint(0, self.microbloques[0].height() // 2)
            painter.drawLine(entrada, primer_micro)

            salida = QPointF(self.width() - 170, self.height() / 2)
            ultimo_micro = self.microbloques[-1].pos() + QPoint(self.microbloques[-1].width(), self.microbloques[-1].height() // 2)
            painter.drawLine(ultimo_micro, salida)

    def draw_topologia_connections(self, topologia, painter):
        if isinstance(topologia, TopologiaSerie):
            self.draw_serie_connections(topologia, painter)
        elif isinstance(topologia, TopologiaParalelo):
            self.draw_paralelo_connections(topologia, painter)

    def draw_serie_connections(self, serie, painter):
        for i in range(len(serie.hijos) - 1):
            start = self.get_microbloque_by_back(serie.hijos[i]).pos() + QPoint(self.microbloques[0].width(), self.microbloques[0].height() // 2)
            end = self.get_microbloque_by_back(serie.hijos[i+1]).pos() + QPoint(0, self.microbloques[0].height() // 2)
            painter.drawLine(start, end)

    def draw_paralelo_connections(self, paralelo, painter):
        start_x = min(self.get_microbloque_by_back(hijo).pos().x() for hijo in paralelo.hijos)
        end_x = max(self.get_microbloque_by_back(hijo).pos().x() + self.microbloques[0].width() for hijo in paralelo.hijos)
        
        start_y = sum(self.get_microbloque_by_back(hijo).pos().y() + self.microbloques[0].height() // 2 for hijo in paralelo.hijos) / len(paralelo.hijos)
        
        start_point = QPointF(start_x, start_y)
        end_point = QPointF(end_x, start_y)
        
        painter.drawLine(start_point, end_point)
        
        for hijo in paralelo.hijos:
            microbloque = self.get_microbloque_by_back(hijo)
            start = QPointF(start_x, microbloque.pos().y() + microbloque.height() // 2)
            end = microbloque.pos() + QPoint(0, microbloque.height() // 2)
            painter.drawLine(start, end)
            
            start = microbloque.pos() + QPoint(microbloque.width(), microbloque.height() // 2)
            end = QPointF(end_x, microbloque.pos().y() + microbloque.height() // 2)
            painter.drawLine(start, end)

    def get_microbloque_by_back(self, back):
        for microbloque in self.microbloques:
            if microbloque.elemento_back == back:
                return microbloque
        return None

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

    def update_connections(self):
        self.update()

    def show_context_menu(self, position):
        if self.selected_microbloque:
            context_menu = QMenu(self)
            delete_action = context_menu.addAction("Borrar microbloque")
            action = context_menu.exec_(self.mapToGlobal(position))
            if action == delete_action:
                self.delete_microbloque(self.selected_microbloque)

    def delete_microbloque(self, microbloque):
        self.microbloques.remove(microbloque)
        # En lugar de llamar a eliminar(), vamos a eliminar el microbloque de la topología
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

