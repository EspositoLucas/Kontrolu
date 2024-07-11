from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QTransform
from PyQt5.QtCore import Qt, QPointF, QRectF, QSize
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque, ANCHO, ALTO
MARGEN_HORIZONTAL = 200
MARGEN_VERTICAL = 50
BUTTON_SIZE = 20
RADIO = 40
MARGEN_PARALELO = 20

class DrawingArea(QScrollArea):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.content = DrawingContent(parent, modelo)
        self.setWidget(self.content)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

class DrawingContent(QWidget):
    def __init__(self, macrobloque=None, ventana=None):
        super().__init__(ventana)
        self.microbloques = []
        self.selected_microbloque = None
        self.selected_microbloques = [] 
        self.macrobloque = macrobloque
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.add_buttons_paralelo = []
        self.scale_factor = 1.0
        self.multiple_selection_active = False
        self.add_selection_button()
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setMinimumSize(800, 600)


    def ajustar_tamano_widget(self):
        if self.microbloques:
            max_x = max(mb.pos().x() + mb.width() for mb in self.microbloques)
            max_y = max(mb.pos().y() + mb.height() for mb in self.microbloques)
            nuevo_ancho = int(max(max_x + 400, 800) * self.scale_factor)
            nuevo_alto = int(max(max_y + 100, 600) * self.scale_factor)
            self.setMinimumSize(nuevo_ancho, nuevo_alto)
        else:
            self.setMinimumSize(800, 600)


    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            zoom_in_factor = 1.25
            zoom_out_factor = 1 / zoom_in_factor

            if event.angleDelta().y() > 0:
                self.scale_factor *= zoom_in_factor
            else:
                self.scale_factor *= zoom_out_factor

            self.scale_factor = max(0.1, min(self.scale_factor, 10.0))
            self.update()
        else:
            super().wheelEvent(event)

    def load_microbloques(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.selected_microbloques.clear()  # Limpiamos la lista de seleccionados
        self.dibujar_topologia(self.macrobloque.modelo.topologia, QPointF(ANCHO, (self.height() / 2) - (ALTO / 2)))
        self.ajustar_tamano_widget()
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
            posicion_actual.setX(posicion_actual.x() + MARGEN_HORIZONTAL)

    def dibujar_paralelo(self, paralelo, posicion_inicial):
        posicion_inicial.setX(posicion_inicial.x() + MARGEN_PARALELO)
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL

        y_actual = posicion_inicial.y() - altura_total / 2
        for hijo in paralelo.hijos:
            centro_del_hijo = y_actual + hijo.alto() / 2
            posicion_del_hijo = QPointF(posicion_inicial.x(), centro_del_hijo)
            self.dibujar_topologia(hijo, posicion_del_hijo)
            y_actual += hijo.alto() + MARGEN_VERTICAL

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.update()
    
    def clear_all(self):
        if self.microbloques:
            for microbloque in self.microbloques:
                microbloque.deleteLater()
            self.microbloques.clear()
            self.selected_microbloques.clear()  # Limpiamos la lista de seleccionados
        
        self.add_buttons.clear()
        self.macrobloque.modelo.reset_topologia()
        self.load_microbloques()
        self.hide_add_buttons()
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        transform = QTransform().scale(self.scale_factor, self.scale_factor)
        painter.setTransform(transform)
        
        # Dibujar borde alrededor de los microbloques seleccionados
        painter.setPen(QPen(Qt.blue, 2, Qt.DashLine))
        for microbloque in self.selected_microbloques[:]:  # Usamos una copia de la lista
            if microbloque in self.microbloques:  # Verificamos si aún existe
                painter.drawRect(microbloque.geometry())
            else:
                self.selected_microbloques.remove(microbloque)  # Eliminamos de la selección si ya no existe

        
        # Dibujar cuadrícula
        self.draw_grid(painter)

        self.draw_io_blocks(painter)
        
        if not self.microbloques:
            self.draw_empty_connection(painter)
        else:
            punto_final = self.draw_connections(painter, self.macrobloque.modelo.topologia, QPointF(90, self.height() / 2))
            self.draw_final_connection(painter, punto_final)

    def draw_final_connection(self, painter, start_point):
        if start_point is None:
            return

        ancho, _ = self.calcular_tamano_topologia()
        end_point = QPointF(ancho - 170, self.height() / 2)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(start_point, end_point)

    def draw_empty_connection(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        entrada = QPointF(130, self.height() / 2)
        salida = QPointF(self.width() - 210, self.height() / 2)
        painter.drawLine(entrada, salida)
        
        center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
        button_rect = QRectF(center.x() - BUTTON_SIZE/2, center.y() - BUTTON_SIZE/2, BUTTON_SIZE, BUTTON_SIZE)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")

        self.add_button_rect = button_rect

    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        centro_y = self.height() / 2
        
        centro_entrada_x = 50 + RADIO
        centro_salida_x = self.width() - 130 - RADIO
        
        painter.drawEllipse(QPointF(centro_entrada_x, centro_y), RADIO, RADIO)
        painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Entrada")
        
        painter.drawEllipse(QPointF(centro_salida_x, centro_y), RADIO, RADIO)
        painter.drawText(QRectF(self.width()-209, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Salida")

    def draw_connections(self, painter, topologia, punto_de_partida, is_parallel=False):
        if punto_de_partida is None:
            return None

        painter.setPen(QPen(Qt.black, 2))
        
        if isinstance(topologia, TopologiaSerie):
            return self.draw_serie_connections(painter, topologia, punto_de_partida)
        elif isinstance(topologia, TopologiaParalelo):
            return self.draw_paralelo_connections(painter, topologia, punto_de_partida)
        elif isinstance(topologia, MicroBloque):
            return self.draw_microbloque_connection(painter, topologia, punto_de_partida, is_parallel)
        else:
            return punto_de_partida

    def draw_serie_connections(self, painter, serie, punto_inicial):
        if punto_inicial is None:
            return None

        punto_actual = punto_inicial
        for hijo in serie.hijos:
            punto_final = self.draw_connections(painter, hijo, punto_actual) 
            punto_actual = punto_final

        return punto_actual

    def draw_paralelo_connections(self, painter, paralelo, punto_inicial):
        if punto_inicial is None:
            return None

        comienzo_de_rama = QPointF(punto_inicial.x() + MARGEN_PARALELO, punto_inicial.y())
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL
        
        painter.drawLine(punto_inicial, comienzo_de_rama)
        
        y_actual = punto_inicial.y() - altura_total / 2
        puntos_finales = []
        for hijo in paralelo.hijos:
            punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2)
            painter.drawLine(comienzo_de_rama, punto_final_rama_vertical)
            punto_final_rama_actual = self.draw_connections(painter, hijo, punto_final_rama_vertical, True)
            if punto_final_rama_actual is not None:
                puntos_finales.append(punto_final_rama_actual)
            y_actual += hijo.alto() + MARGEN_VERTICAL
        
        if not puntos_finales:
            return punto_inicial

        max_x = max(point.x() for point in puntos_finales) + MARGEN_PARALELO
         
        for end_point in puntos_finales:
            painter.drawLine(end_point, QPointF(max_x, end_point.y()))
        
        punto_de_reconexion = QPointF(max_x, punto_inicial.y())  # punto de reconexión (es el punto más a la derecha de la estructura paralelo)
        # insertar imagen de punto suma en el punto de reconexión
        painter.drawEllipse(punto_de_reconexion, 5, 5)

        # Punto de reconexión
        punto_mas_alejado = QPointF(max_x + MARGEN_PARALELO, punto_inicial.y())

        # Dibujar líneas verticales para reconectar (En realidad es una unica linea desde una rama a la otra)
        # QPointF(max_x + 20, puntos_finales[0].y()) --> es para la rama de arriba (indice 0 es el primer elemento de una lista)
        # QPointF(max_x + 20, puntos_finales[-1].y()) --> es para la rama de abajo (indice -1 es el último elemento de una lista)
        painter.drawLine(QPointF(max_x, puntos_finales[0].y()), QPointF(max_x, puntos_finales[-1].y()))
        
        # Dibujar línea horizontal final (para salir de la estructura paralelo)
        painter.drawLine(QPointF(max_x, punto_inicial.y()), punto_mas_alejado)
        
        # retorna el punto de reconexión porque es el punto "mas a la derecha" de la estructura paralelo
        return punto_mas_alejado 
    
    def draw_microbloque_connection(self, painter, microbloque, punto_inicial, es_paralelo):
        for mb in self.microbloques:
            if mb.elemento_back == microbloque:
                if es_paralelo:
                    punto_final = QPointF(mb.pos().x(), punto_inicial.y())
                else:
                    punto_final = mb.pos() + QPointF(0, mb.height() / 2)
                
                if punto_inicial is not None and punto_final is not None:
                    painter.drawLine(punto_inicial, punto_final)
                
                return mb.pos() + QPointF(mb.width(), mb.height() / 2)
        
        return punto_inicial

    def create_new_microbloque(self, pos, relation=None, reference_structure=None):
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
            new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.macrobloque.modelo.topologia)

            if isinstance(reference_structure, MicroBloque):
                self.agregar_respecto_microbloque(new_microbloque, relation, reference_structure)
            elif isinstance(reference_structure, TopologiaSerie):
                self.agregar_respecto_serie(new_microbloque, relation, reference_structure)
            elif isinstance(reference_structure, TopologiaParalelo):
                self.agregar_respecto_paralelo(new_microbloque, relation, reference_structure)
            else:
                self.macrobloque.modelo.topologia.agregar_elemento(new_microbloque)
            
            self.load_microbloques()
            self.update()
            self.hide_add_buttons()
            
    def agregar_respecto_microbloque(self, new_microbloque, relation, reference_microbloque):
        if relation == "arriba":
            reference_microbloque.agregar_arriba(new_microbloque) # agrega el nuevo microbloque arriba del microbloque de referencia
        elif relation == "abajo":
            reference_microbloque.agregar_abajo(new_microbloque) # agrega el nuevo microbloque abajo del microbloque de referencia
        elif relation == "antes": # izquierda
            reference_microbloque.agregar_antes(new_microbloque) # agrega el nuevo microbloque antes del microbloque de referencia
        else: # despues
            reference_microbloque.agregar_despues(new_microbloque) # agrega el nuevo microbloque después del microbloque de referencia

    def agregar_respecto_serie(self, new_microbloque, relation, reference_serie):
        if relation == "antes":
            reference_serie.agregar_elemento(new_microbloque, 0) # agrega el nuevo microbloque al principio de la serie
        elif relation == "despues": 
            reference_serie.agregar_elemento(new_microbloque, len(reference_serie.hijos)) # agrega el nuevo microbloque al final de la serie
        elif relation == "arriba": # TODO: No funciona cuando la serie es la serie principal
            reference_serie.agregar_serie_arriba(new_microbloque) # agrega un microbloque en serie arriba de la estructura serie
        else: # abajo # TODO: No funciona cuando la serie es la serie principal
            reference_serie.agregar_serie_abajo(new_microbloque) # agrega un microbloque en serie abajo de la estructura serie

    def agregar_respecto_paralelo(self, new_microbloque, relation, reference_paralelo):
        if relation == "antes":
            reference_paralelo.agregar_en_serie_fuera_de_paralela_antes(new_microbloque) # agrega un microbloque en serie antes de la estructura paralelo
        elif relation == "despues":
            reference_paralelo.agregar_en_serie_fuera_de_paralela_despues(new_microbloque) # agrega un microbloque en serie después de la estructura paralelo # TODO: A veces se dibuja mal
        elif relation == "arriba":
            reference_paralelo.agregar_arriba_de(new_microbloque, self.selected_microbloque.elemento_back.padre) # agrega una rama más, arriba de la rama actual
        else: # abajo
            reference_paralelo.agregar_abajo_de(new_microbloque, self.selected_microbloque.elemento_back.padre) # agrega una rama más, abajo de la rama actual

    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")
            button.setProperty("selected_color", color)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        scaled_pos = event.pos() / self.scale_factor

        if not self.microbloques:
            if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(scaled_pos):
                self.create_new_microbloque(self.add_button_rect.center())
        else:
            clicked_microbloque = None
            for microbloque in self.microbloques:
                if microbloque.geometry().contains(scaled_pos):
                    clicked_microbloque = microbloque
                    break
            
            if clicked_microbloque:
                if self.multiple_selection_active:
                    if clicked_microbloque in self.selected_microbloques:
                        self.selected_microbloques.remove(clicked_microbloque)
                    else:
                        self.selected_microbloques.append(clicked_microbloque)
                else:
                    self.selected_microbloques = [clicked_microbloque]
                self.show_add_buttons(clicked_microbloque)
            elif not self.multiple_selection_active:
                self.selected_microbloques.clear()
                self.hide_add_buttons()
        
        self.update()

    def sizeHint(self):
        return QSize(1000, 600)

    def show_add_buttons(self, microbloque):
        self.hide_add_buttons()
        if not microbloque:
            return
        positions = [
            ('arriba', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() - BUTTON_SIZE/2)),
            ('abajo', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() + microbloque.height() + BUTTON_SIZE/2)),
            ('izquierda', QPointF(microbloque.x() - BUTTON_SIZE/2, microbloque.y() + microbloque.height()/2)),
            ('derecha', QPointF(microbloque.x() + microbloque.width() + BUTTON_SIZE/2, microbloque.y() + microbloque.height()/2))
        ]
        
        for direction, pos in positions:
            button = QPushButton("+", self)
            button.setGeometry(int(pos.x() - BUTTON_SIZE/2), int(pos.y() - BUTTON_SIZE/2), BUTTON_SIZE, BUTTON_SIZE)
            button.clicked.connect(lambda _, d=direction, m=microbloque: self.show_add_menu(d, m))
            button.show()
            self.add_buttons.append(button)

    def hide_add_buttons(self):
        for button in self.add_buttons:
            button.deleteLater()
        self.add_buttons.clear()

    def show_add_menu(self, direction, microbloque):
        menu = QMenu(self)
        if microbloque and microbloque.elemento_back:
            micro_back = microbloque.elemento_back
            parent_structures = micro_back.get_parent_structures()
            for parent in [[micro_back, 0]] + parent_structures:
                action = menu.addAction(f"Respecto a {self.get_structure_name(parent)}")
                action.triggered.connect(lambda _, s=parent[0], m=microbloque: self.add_microbloque(direction, s, m))
        
        button = self.sender()
        menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))

    def get_structure_name(self, estructura):
        nodo = estructura[0]
        nivel = estructura[1]
        if isinstance(nodo, MicroBloque):
            return nodo.nombre
        elif isinstance(nodo, TopologiaSerie):
            return f"Serie {nivel}"
        elif isinstance(nodo, TopologiaParalelo):
            return f"Paralelo {nivel}"
        else:
            return "Estructura desconocida"

    def add_microbloque(self, direction, estructura_de_referencia, microbloque):
        if microbloque and estructura_de_referencia:
            if direction in ['arriba', 'abajo']:
                relation = direction
            elif direction == 'izquierda':
                relation = 'antes'
            else:  # derecha
                relation = 'despues'
            
            self.create_new_microbloque(microbloque.pos(), relation, estructura_de_referencia)
            
    def print_topologia(self, topologia, indent=0):
        space = ' ' * (indent * 2)
        if isinstance(topologia, TopologiaSerie):
            print(f"{space}Serie:")
            for hijo in topologia.hijos:
                self.print_topologia(hijo, indent + 1)
        elif isinstance(topologia, TopologiaParalelo):
            print(f"{space}Paralelo:")
            for hijo in topologia.hijos:
                self.print_topologia(hijo, indent + 1)
        elif isinstance(topologia, MicroBloque):
            print(f"{space}MicroBloque: {topologia.nombre}")
    
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        if self.selected_microbloques:
            delete_selected_action = menu.addAction("Borrar seleccionados")
            delete_selected_action.triggered.connect(self.delete_selected_microbloques)
        
        for microbloque in self.microbloques:
            if microbloque.geometry().contains(event.pos()):
                delete_action = menu.addAction("Eliminar")
                delete_action.triggered.connect(lambda: self.delete_microbloque(microbloque))
                break
        
        menu.exec_(self.mapToGlobal(event.pos()))
        
    def delete_microbloque(self, microbloque):
        self.microbloques.remove(microbloque)
        microbloque.elemento_back.borrar_elemento()
        microbloque.deleteLater()
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()
    
    def delete_selected_microbloques(self):
        for microbloque in self.selected_microbloques[:]:  # Creamos una copia de la lista
            if microbloque in self.microbloques:  # Verificamos si aún existe
                self.microbloques.remove(microbloque)
                microbloque.elemento_back.borrar_elemento()
                microbloque.deleteLater()
        self.selected_microbloques.clear()
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()
        
    def draw_grid(self, painter):
        painter.save()
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        
        grid_size = 20 * self.scale_factor
        
        for x in range(0, int(self.width()), int(grid_size)):
            painter.drawLine(x, 0, x, self.height())
        
        for y in range(0, int(self.height()), int(grid_size)):
            painter.drawLine(0, y, self.width(), y)
        
        painter.restore()
    
    def add_selection_button(self):
        self.selection_button = QPushButton("Selección múltiple", self)
        self.selection_button.setGeometry(10, 40, 150, 30)  # Ajusta la posición según necesites
        self.selection_button.clicked.connect(self.toggle_multiple_selection)
        self.selection_button.show()

    def toggle_multiple_selection(self):
        if self.selection_button.text() == "Selección múltiple":
            self.selection_button.setText("Desactivar selección")
            self.multiple_selection_active = True
        else:
            self.selection_button.setText("Selección múltiple")
            self.multiple_selection_active = False
            self.selected_microbloques.clear()
        self.update()
    