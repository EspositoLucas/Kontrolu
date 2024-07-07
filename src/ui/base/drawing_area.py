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
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.microbloques = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.add_buttons_paralelo = []
        self.scale_factor = 1.0
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
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
            self.update_microbloques_position()
            self.update()
        else:
            super().wheelEvent(event)

    def update_microbloques_position(self):
        for microbloque in self.microbloques:
            new_pos = microbloque.pos() * self.scale_factor
            microbloque.setGeometry(int(new_pos.x()), int(new_pos.y()),
                                    int(microbloque.width() * self.scale_factor),
                                    int(microbloque.height() * self.scale_factor))

    def load_microbloques(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.dibujar_topologia(self.modelo.topologia, QPointF(ANCHO, (self.height() / 2) - (ALTO / 2)))
        self.update()
        self.ajustar_tamano_widget()
    
    def ajustar_tamano_widget(self):
        if self.microbloques:
            max_x = max(mb.pos().x() + mb.width() for mb in self.microbloques)
            max_y = max(mb.pos().y() + mb.height() for mb in self.microbloques)
            nuevo_ancho = max(max_x + 400, 800)
            nuevo_alto = max(max_y + 100, 600)
            self.setMinimumSize(nuevo_ancho, nuevo_alto)
        else:
            self.setMinimumSize(800, 600)
    
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
        
        self.add_buttons.clear() # vacia la lista de botones "+"
        self.modelo.reset_topologia() # si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
        self.load_microbloques() # resetea la vista
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        transform = QTransform().scale(self.scale_factor, self.scale_factor)
        painter.setTransform(transform)

        self.draw_io_blocks(painter)
        
        if not self.microbloques:
            self.draw_empty_connection(painter)
        else:
           punto_final = self.draw_connections(painter, self.modelo.topologia, QPointF(90, self.height() / 2))
           self.draw_final_connection(painter, punto_final)
    
    def draw_final_connection(self, painter, start_point):
        if start_point is None:
            return

        end_point = QPointF(self.width() - 170, self.height() / 2)
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
        
        punto_de_reconexion = QPointF(max_x + MARGEN_PARALELO, punto_inicial.y())
        
        painter.drawLine(QPointF(max_x, puntos_finales[0].y()), QPointF(max_x, puntos_finales[-1].y()))
        
        painter.drawLine(QPointF(max_x, punto_inicial.y()), punto_de_reconexion)
        
        # coordenada_final = self.boton_agregar_despues_de_paralelo(painter, punto_de_reconexion) # dibuja el botón "+" para agregar un microbloque después de la estructura paralelo
        
        # retorna el punto de reconexión porque es el punto "mas a la derecha" de la estructura paralelo
        return punto_de_reconexion 

    """
    def boton_agregar_despues_de_paralelo(self, painter, pos):
            button_rect = QRectF(pos.x() - BUTTON_SIZE/2, pos.y() - BUTTON_SIZE/2, BUTTON_SIZE, BUTTON_SIZE)
            painter.setBrush(QBrush(Qt.white))
            painter.drawEllipse(button_rect)
            painter.drawText(button_rect, Qt.AlignCenter, "+")
            self.add_buttons_paralelo.append(button_rect)
            punto_derecho = QPointF(pos.x() + BUTTON_SIZE/2, pos.y())
            return punto_derecho
    """
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
            new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.modelo.topologia)

            if isinstance(reference_structure, MicroBloque):
                self.agregar_respecto_microbloque(new_microbloque, relation, reference_structure)
            elif isinstance(reference_structure, TopologiaSerie):
                self.agregar_respecto_serie(new_microbloque, relation, reference_structure)
            elif isinstance(reference_structure, TopologiaParalelo):
                self.agregar_respecto_paralelo(new_microbloque, relation, reference_structure)
            else:
                self.modelo.topologia.agregar_elemento(new_microbloque)
            
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
            reference_paralelo.agregar_en_serie_fuera_de_paralela_despues(new_microbloque) # agrega un microbloque en serie después de la estructura paralelo
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
            for microbloque in self.microbloques:
                if microbloque.geometry().contains(scaled_pos):
                    self.selected_microbloque = microbloque
                    self.show_add_buttons(microbloque) # muestra los botones "+" alrededor del microbloque
                    break
            else:
                self.selected_microbloque = None
                self.hide_add_buttons() # oculta los botones "+"
            """
            for button_rect in self.add_buttons_paralelo:
                if button_rect.contains(scaled_pos):
                    self.create_new_microbloque(button_rect.center(), relation="despues")
                    return
            """
        
        self.update()

    def sizeHint(self):
        return QSize(1000, 600)

    def show_add_buttons(self, microbloque):
        self.hide_add_buttons()
        positions = [
            ('arriba', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() - BUTTON_SIZE/2)),
            ('abajo', QPointF(microbloque.x() + microbloque.width()/2, microbloque.y() + microbloque.height() + BUTTON_SIZE/2)),
            ('izquierda', QPointF(microbloque.x() - BUTTON_SIZE/2, microbloque.y() + microbloque.height()/2)),
            ('derecha', QPointF(microbloque.x() + microbloque.width() + BUTTON_SIZE/2, microbloque.y() + microbloque.height()/2))
        ]
        
        for direction, pos in positions:
            button = QPushButton("+", self)
            button.setGeometry(int(pos.x() - BUTTON_SIZE/2), int(pos.y() - BUTTON_SIZE/2), BUTTON_SIZE, BUTTON_SIZE)
            button.clicked.connect(lambda _, d=direction: self.show_add_menu(d))
            button.show()
            self.add_buttons.append(button)

    def hide_add_buttons(self):
        for button in self.add_buttons:
            button.deleteLater()
        self.add_buttons.clear()

    def show_add_menu(self, direction):
        menu = QMenu(self)
        micro_back = self.selected_microbloque.elemento_back
        parent_structures = micro_back.get_parent_structures()
        for parent in [micro_back] + parent_structures:
            action = menu.addAction(f"Respecto a {self.get_structure_name(parent)}")
            action.triggered.connect(lambda _, s=parent: self.add_microbloque(direction, s))
        
        button = self.sender()
        menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))

    def get_structure_name(self, estructura):
        if isinstance(estructura, MicroBloque):
            return f"Microbloque '{estructura.nombre}'"
        elif isinstance(estructura, TopologiaSerie):
            return "Serie"
        elif isinstance(estructura, TopologiaParalelo):
            return "Paralelo"
        else:
            return "Estructura desconocida"

    def add_microbloque(self, direction, estructura_de_referencia):
        # segun la dirección en la que se hizo click, determino la relación con el microbloque seleccionado
        if estructura_de_referencia:
            if direction in ['arriba', 'abajo']:
                relation = direction
            elif direction == 'izquierda':
                relation = 'antes'
            else:  # derecha
                relation = 'despues'
            
            self.create_new_microbloque(self.selected_microbloque.pos(), relation, estructura_de_referencia)    

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
        for microbloque in self.microbloques:
            if microbloque.geometry().contains(event.pos()):
                menu = QMenu(self)
                delete_action = menu.addAction("Eliminar")
                action = menu.exec_(self.mapToGlobal(event.pos()))
                if action == delete_action:
                    self.delete_microbloque(microbloque)
                break
        
    def delete_microbloque(self, microbloque):
        self.microbloques.remove(microbloque)
        microbloque.elemento_back.borrar_elemento()
        microbloque.deleteLater()
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()


