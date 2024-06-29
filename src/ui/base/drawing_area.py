from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
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
        self.modelo = modelo # es la representacion backend del macrobloque
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.button_size = 20
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setContextMenuPolicy(Qt.CustomContextMenu)
    
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
            posicion_actual.setX(posicion_actual.x() + 200) # TODO: Modificar el valor segun convenga (es el margen horizontal entre microbloques)

    def dibujar_paralelo(self, paralelo, posicion_inicial):
        posicion_actual = posicion_inicial
        for hijo in paralelo.hijos:
            self.dibujar_topologia(hijo, posicion_actual)
            posicion_actual.setY(posicion_actual.y() + 100) # TODO: Modificar el valor segun convenga (es el margen vertical entre microbloques)

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(microbloque_back.nombre, self, microbloque_back.color, microbloque_back.funcion_transferencia, microbloque_back.opciones_adicionales)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.update_connections()
    
    def clear_all(self):
        self.microbloques = []
        # TODO: Si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
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
        
        # Dibujar el botón "+" en el medio
        center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
        button_size = 30
        button_rect = QRectF(center.x() - button_size/2, center.y() - button_size/2, button_size, button_size)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")

        # Guardar la posición del botón para detectar clics
        self.add_button_rect = button_rect

    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        radio = 40  # Radio del círculo
        centro_y = self.height() / 2  # Posición y del centro para ambos círculos
        
        centro_entrada_x = 50 + radio  # Posición x del centro del círculo de entrada
        centro_salida_x = self.width() - 130 - radio  # Posición x del centro del círculo de salida
        
        # Dibujar los círculos de entrada y salida
        painter.drawEllipse(QPointF(centro_entrada_x, centro_y), radio, radio)
        painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Entrada")
        
        painter.drawEllipse(QPointF(centro_salida_x, centro_y), radio, radio)
        painter.drawText(QRectF(self.width()-209, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Salida")
    
    def draw_connections(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        for i in range(len(self.microbloques) - 1):
            start = self.microbloques[i].pos() + QPoint(self.microbloques[i].width(), self.microbloques[i].height() / 2)
            end = self.microbloques[i+1].pos() + QPoint(0, self.microbloques[i+1].height() / 2)
            painter.drawLine(start, end)

        # Conectar el primer microbloque con la entrada
        if self.microbloques:
            entrada = QPointF(90, self.height() / 2)
            primer_micro = self.microbloques[0].pos() + QPoint(0, self.microbloques[0].height() // 2)
            painter.drawLine(entrada, primer_micro)

        # Conectar el último microbloque con la salida
        if self.microbloques:
            salida = QPointF(self.width() - 170, self.height() / 2)
            ultimo_micro = self.microbloques[-1].pos() + QPoint(self.microbloques[-1].width(), self.microbloques[-1].height() // 2)
            painter.drawLine(ultimo_micro, salida)

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
            config = {
                'nombre': nombre,
                'color': color,
                'funcion_transferencia': funcion_transferencia,
                'opciones_adicionales': {}
            }
            new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.modelo.topologia)

            if reference_microbloque and relation == "arriba":
                self.modelo.topologia.agregar_arriba(reference_microbloque, new_microbloque)
            elif reference_microbloque and relation == "abajo":
                self.modelo.topologia.agregar_abajo(reference_microbloque, new_microbloque)
            elif reference_microbloque and relation == "antes":
                self.modelo.topologia.agregar_antes(reference_microbloque, new_microbloque)
            elif reference_microbloque and relation == "despues":
                self.modelo.topologia.agregar_despues(reference_microbloque, new_microbloque)
            else:
                self.modelo.topologia.agregar_elemento(new_microbloque) # sería el primer microbloque
            
            self.load_microbloques()  # recargo todos los microbloques
            self.update()
            self.hide_add_buttons() # ocultamos los botones "+" por si quedaron visibles

    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")
            button.setProperty("selected_color", color)
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        if not self.microbloques: # si no hay microbloques y se hace click sobre el único botón "+", entonces se crea un microbloque 
            if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(event.pos()):
                self.create_new_microbloque(self.add_button_rect.center())
        else: # si hay microbloques, se busca el microbloque que se seleccionó
            for microbloque in self.microbloques:
                if microbloque.geometry().contains(event.pos()):
                    self.selected_microbloque = microbloque
                    self.show_add_buttons(microbloque) # muestra los botones "+" alrededor del microbloque
                    break
            else:
                self.selected_microbloque = None
                self.hide_add_buttons() # oculta los botones "+"
        
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
        # segun la dirección en la que se hizo click, determino la relación con el microbloque seleccionado
        if self.selected_microbloque:
            if direction in ['arriba', 'abajo']:
                relation = direction
            elif direction == 'izquierda':
                relation = 'antes'
            else:  # derecha
                relation = 'despues'
            
            self.create_new_microbloque(self.selected_microbloque.pos(), relation, self.selected_microbloque)

    def update_connections(self):
        self.update()
