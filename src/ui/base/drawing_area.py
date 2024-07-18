import os
from PyQt5.QtWidgets import QWidget, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMenu, QAction, QScrollArea,QTextEdit,QToolTip,QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush,QTransform,QPixmap,QCursor
from PyQt5.QtCore import Qt, QPointF, QRectF, QTimer,QSize,QPoint
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
        self.content = DrawingContent(parent, modelo, self)  # Pasamos self como referencia
        self.setWidget(self.content)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

class DrawingContent(QWidget):
    def __init__(self, macrobloque=None, ventana=None, scroll_area=None):
        super().__init__(ventana)
        self.scroll_area = scroll_area  # Guardamos la referencia al QScrollArea
        self.microbloques = []
        self.selected_microbloque = None
        self.selected_microbloques = [] 
        self.macrobloque = macrobloque
        self.creating_microbloque = False
        self.seleccion_multiple = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.add_buttons_paralelo = []
        self.selected_microbloques = []
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.resize_retardado)
        self.scale_factor = 1.0
        self.panning = False
        # self.help_level = "principiante"  # Nivel de ayuda por defecto
        self.load_preview_images()
        self.load_connection_image()
        self.init_ui()


    def load_preview_images(self):
        # Obtener la ruta del directorio actual del script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navegar hacia arriba dos niveles y luego a la carpeta 'imgs'
        imgs_dir = os.path.join(current_dir, '..', 'base', 'imgs')
        
        self.preview_images = {
            'arriba': QPixmap(os.path.join(imgs_dir, 'paralelo.png')),
            'abajo': QPixmap(os.path.join(imgs_dir, 'paralelo.png')),
            'izquierda': QPixmap(os.path.join(imgs_dir, 'serie.png')),
            'derecha': QPixmap(os.path.join(imgs_dir, 'serie.png'))
        }
    
    def load_connection_image(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, '..','base', 'imgs')
        self.connection_image = QPixmap(os.path.join(img_path,'puntoSuma.png'))
        if self.connection_image.isNull():
            print(f"Error: No se pudo cargar la imagen en {img_path}")
    
    def resizeEvent(self, event):
        # reinicia el temporizador cada vez que se produce un evento de cambio de tamaño
        super().resizeEvent(event)
        self.resize_timer.start(200) # 200 ms

    def resize_retardado(self):
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()

    def init_ui(self):
        self.setStyleSheet("background-color: white; border: 1px solid black;")
        self.setFocusPolicy(Qt.StrongFocus) # sirve para permitir que el teclado de la compu interactue con la ventana
        self.setContextMenuPolicy(Qt.CustomContextMenu) # sirve para poder mostrar un menu contextual (por ejemplo, cuando hago click derecho)
        self.customContextMenuRequested.connect(self.mostrar_menu_contextual) # permite agregar nuestro propio menu contextual
        # Agregar botón de ayuda
        self.help_button = QPushButton("?", self)
        self.help_button.setGeometry(10, 10, 30, 30)
        self.help_button.clicked.connect(self.show_help)
        self.help_button.setToolTip("Mostrar ayuda")
    
    def show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda")
        layout = QVBoxLayout()

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h2>Bienvenido al sistema de ayuda</h2>
        <h3>Creación de microbloques</h3>
        <p>Para crear un nuevo microbloque:</p>
        <ol>
            <li>Haga clic en el botón '+' en el centro del diagrama vacío, o en los botones '+' alrededor de un microbloque existente.</li>
            <li>Seleccione la ubicación deseada en el menú desplegable.</li>
            <li>Complete la información requerida en el diálogo que aparece.</li>
        </ol>

        <h3>Edición de microbloques</h3>
        <p>Para editar un microbloque existente:</p>
        <ul>
            <li>Haga doble clic en el microbloque para abrir el diálogo de edición.</li>
            <li>Para eliminar un microbloque, selecciónelo y presione la tecla 'Suprimir' o use el menú contextual (clic derecho).</li>
        </ul>

        <h3>Navegación</h3>
        <p>Use la rueda del ratón para hacer zoom. Mantenga presionada la tecla Ctrl mientras arrastra para desplazarse por el diagrama.</p>

        <h3>Selección múltiple</h3>
        <p>Mantenga presionada la tecla Ctrl mientras hace clic para seleccionar varios microbloques a la vez.</p>
        """)
        layout.addWidget(help_text)

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(help_dialog.close)
        layout.addWidget(close_button)
        help_dialog.setLayout(layout)
        help_dialog.exec_()

        
    def calcular_factor_escala(self):
        ancho_ventana = self.width()
        alto_ventana = self.height()
        factor_ancho = ancho_ventana / 600 
        factor_alto = alto_ventana / 600
        self.escala = min(factor_ancho, factor_alto)  # Usamos el menor para mantener la proporción
        print("usando factor de escala: ", self.escala)    

    def load_microbloques(self):
        for microbloque in self.microbloques:
                microbloque.deleteLater() # elimina cada elemento
        self.microbloques.clear() # vacia la lista de microbloques
        self.limpiar_seleccion() # si habia seleccionados, los limpia
        self.calcular_factor_escala()
        self.dibujar_topologia(self.macrobloque.modelo.topologia, QPointF(ANCHO + 100, (self.height() / 2)))
        #self.print_topologia(self.macrobloque.modelo.topologia)
        self.update()
    
    
    def dibujar_topologia(self, topologia, posicion_inicial):
        if isinstance(topologia, TopologiaSerie):
            return self.dibujar_serie(topologia, posicion_inicial, self.escala)
        elif isinstance(topologia, TopologiaParalelo):
            return self.dibujar_paralelo(topologia, posicion_inicial, self.escala)
        elif isinstance(topologia, MicroBloque):
            return self.create_microbloque(topologia, posicion_inicial, self.escala)
        
    def dibujar_serie(self, serie, posicion_inicial, factor_escala):
        posicion_actual = posicion_inicial
        punto_final = posicion_inicial
        for hijo in serie.hijos:
            punto_final = self.dibujar_topologia(hijo, posicion_actual)
            posicion_actual = QPointF(punto_final.x() + MARGEN_HORIZONTAL * factor_escala, posicion_inicial.y())
        return punto_final

    def dibujar_paralelo(self, paralelo, posicion_inicial, factor_escala):
        posicion_inicial.setX(posicion_inicial.x() + MARGEN_PARALELO * factor_escala)
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos) 
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL * factor_escala

        y_actual = posicion_inicial.y() - altura_total / 2
        punto_final_max = posicion_inicial
        for hijo in paralelo.hijos:
            centro_del_hijo = y_actual + hijo.alto() / 2
            posicion_del_hijo = QPointF(posicion_inicial.x(), centro_del_hijo)
            punto_final = self.dibujar_topologia(hijo, posicion_del_hijo)
            if punto_final.x() > punto_final_max.x():
                punto_final_max = punto_final
            y_actual += hijo.alto() * factor_escala + MARGEN_VERTICAL * factor_escala

        return QPointF(punto_final_max.x() + MARGEN_PARALELO * factor_escala, posicion_inicial.y())
    
    def create_microbloque(self, microbloque_back, pos, factor_escala):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        microbloque.setScale(factor_escala)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.update()
        print(f"Microbloque {microbloque_back.nombre} creado en {pos}")
        print(f"Centro del microbloque calculado con microbloque.pos(): {microbloque.pos() + QPointF(microbloque.width() / 2, microbloque.height() / 2)}")
        print(f"Altura vertical de la topologia {self.calcular_punto_medio_topologia()}")
        return pos
    
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
        
        centro_y = self.calcular_punto_medio_topologia()

        if not self.microbloques:
            self.draw_empty_connection(painter, centro_y)
        else:
            punto_inicial = QPointF((50 + RADIO) * self.escala + RADIO * self.escala, centro_y)
            punto_final = self.draw_connections(painter, self.macrobloque.modelo.topologia, punto_inicial)
            self.draw_final_connection(painter, punto_final, centro_y)

    def draw_final_connection(self, painter, start_point, centro_y):
        if start_point is None:
            return

        mb_mas_lejano = self.encontrar_bloque_mas_a_la_derecha()
        if mb_mas_lejano:
            end_x = mb_mas_lejano.pos().x() + mb_mas_lejano.width() * self.escala + (MARGEN_HORIZONTAL / 2) * self.escala
        else:
            end_x = self.width() - (130 + RADIO) * self.escala

        end_point = QPointF(end_x, centro_y)
        painter.setPen(QPen(Qt.black, 2 * self.escala))
        painter.drawLine(start_point, end_point)

    def draw_empty_connection(self, painter, centro_y):
        painter.setPen(QPen(Qt.black, 2 * self.escala))
        entrada = QPointF(130 * self.escala, centro_y)
        salida = QPointF(self.width() - (130 + RADIO) * self.escala, centro_y)
        painter.drawLine(entrada, salida)

        center = QPointF((entrada.x() + salida.x()) / 2, centro_y)
        button_size = BUTTON_SIZE * self.escala
        button_rect = QRectF(center.x() - button_size/2, center.y() - button_size/2, button_size, button_size)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")

        self.add_button_rect = button_rect
        
        # Agregar un QToolTip para el botón '+'
        QToolTip.showText(self.mapToGlobal(button_rect.center().toPoint()), "Agregar nuevo microbloque", self)
    
    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2 * self.escala))

        centro_y = self.calcular_punto_medio_topologia()
        
        centro_entrada_x = (50 + RADIO) * self.escala

        radio_escalado = RADIO * self.escala

        # Dibujar círculo de entrada
        painter.drawEllipse(QPointF(centro_entrada_x, centro_y), radio_escalado, radio_escalado)
        painter.drawText(QRectF(50 * self.escala, centro_y - 30 * self.escala, 80 * self.escala, 60 * self.escala), Qt.AlignCenter, "Entrada")

        # Calcular posición del círculo de salida
        mb_mas_lejano = self.encontrar_bloque_mas_a_la_derecha()
        if mb_mas_lejano:
            centro_salida_x = mb_mas_lejano.pos().x() + mb_mas_lejano.width() * self.escala + (MARGEN_HORIZONTAL / 2) * self.escala
        else:
            centro_salida_x = self.width() - (130 + RADIO) * self.escala

        # Dibujar círculo de salida
        painter.drawEllipse(QPointF(centro_salida_x + radio_escalado, centro_y), radio_escalado, radio_escalado)
        painter.drawText(QRectF(centro_salida_x - 40 * self.escala + radio_escalado, centro_y - 30 * self.escala, 80 * self.escala, 60 * self.escala), Qt.AlignCenter, "Salida")
    
    def draw_connections(self, painter, topologia, punto_de_partida, is_parallel=False):
        if punto_de_partida is None:
            return None

        painter.setPen(QPen(Qt.black, 2 * self.escala))  # Ajusta el grosor de la línea
        
        if isinstance(topologia, TopologiaSerie):
            return self.draw_serie_connections(painter, topologia, punto_de_partida, self.escala)
        elif isinstance(topologia, TopologiaParalelo):
            return self.draw_paralelo_connections(painter, topologia, punto_de_partida, self.escala)
        elif isinstance(topologia, MicroBloque):
            return self.draw_microbloque_connection(painter, topologia, punto_de_partida, is_parallel, self.escala)
        else:
            return punto_de_partida

    def draw_serie_connections(self, painter, serie, punto_inicial, factor_escala):
        if punto_inicial is None:
            return None

        punto_actual = punto_inicial # borde entrada 
        for hijo in serie.hijos:
            punto_final = self.draw_connections(painter, hijo, punto_actual)
            if punto_final:
                punto_actual = punto_final

        return punto_actual

    def draw_paralelo_connections(self, painter, paralelo, punto_inicial, factor_escala):
        if punto_inicial is None:
            return None
        
        comienzo_de_rama = QPointF(punto_inicial.x() + MARGEN_PARALELO * factor_escala, punto_inicial.y())
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
        print("Altura total: ", altura_total)
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL * factor_escala

        # Dibujar línea horizontal antes de la bifurcación
        painter.drawLine(punto_inicial, comienzo_de_rama)
        
        # Dibujar conexiones para cada rama        
        y_actual = punto_inicial.y() - altura_total / 2
        puntos_finales = []
        for hijo in paralelo.hijos:
            print("y_actual: ", y_actual)
            punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2)
            print("punto_final_rama_vertical: ", punto_final_rama_vertical)
            painter.drawLine(comienzo_de_rama, punto_final_rama_vertical)
            punto_final_rama_actual = self.draw_connections(painter, hijo, punto_final_rama_vertical, True)
            print("punto_final_rama_actual: ", punto_final_rama_actual)
            if punto_final_rama_actual is not None:
                puntos_finales.append(punto_final_rama_actual)
            y_actual += hijo.alto() + MARGEN_VERTICAL * factor_escala
        
        if not puntos_finales:
            return punto_inicial

        max_x = max(point.x() for point in puntos_finales) + MARGEN_PARALELO * factor_escala
        
        for end_point in puntos_finales:
            painter.drawLine(end_point, QPointF(max_x, end_point.y()))
        
        # punto_de_reconexion = QPointF(max_x, punto_inicial.y())
        # painter.drawEllipse(punto_de_reconexion, 5 * factor_escala, 5 * factor_escala)
        
        punto_de_reconexion = QPointF(max_x, punto_inicial.y())
        if not self.connection_image.isNull():
            # Escalamos la imagen según el factor de escala
            scaled_image = self.connection_image.scaled(
                int(40 * factor_escala), 
                int(40 * factor_escala), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            # Convertimos las coordenadas a enteros y ajustamos por el tamaño de la imagen
            x = int(punto_de_reconexion.x() - scaled_image.width() / 2)
            y = int(punto_de_reconexion.y() - scaled_image.height() / 2)
            painter.drawPixmap(x, y, scaled_image)
        else:
            painter.drawEllipse(punto_de_reconexion, 5 * factor_escala, 5 * factor_escala)

        punto_mas_alejado = QPointF(max_x + MARGEN_PARALELO * factor_escala, punto_inicial.y())

        painter.drawLine(QPointF(max_x, puntos_finales[0].y()), QPointF(max_x, puntos_finales[-1].y()))
        
        painter.drawLine(QPointF(max_x, punto_inicial.y()), punto_mas_alejado)
        
        return punto_mas_alejado 
    
    def draw_microbloque_connection(self, painter, microbloque, punto_inicial, es_paralelo, factor_escala):
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
        
        if event.button() == Qt.LeftButton and event.modifiers() & Qt.ControlModifier:
            self.panning = True
            self.last_pan_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return

        super().mousePressEvent(event)
        
        scaled_pos = event.pos() / self.scale_factor

        if not self.microbloques:
            if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(scaled_pos):
                self.create_new_microbloque(self.add_button_rect.center())
        else: 
            if event.button() == Qt.LeftButton: # si se hace click izquierdo
                for microbloque in self.microbloques: # si hay microbloques, se busca el microbloque que se seleccionó
                    if microbloque.geometry().contains(event.pos()):
                        if self.seleccion_multiple: # si está activa la seleccion multiple
                            if microbloque in self.selected_microbloques: # si el microbloque seleccionado ya estaba seleccionado
                                self.selected_microbloques.remove(microbloque) # lo deseleccionamos
                                microbloque.setSeleccionado(False) # cambiar el color del borde del microbloque deseleccionado
                            else: # si no está seleccionado
                                self.selected_microbloques.append(microbloque) # lo agregamos
                                microbloque.setSeleccionado(True) # cambiar el color del borde del microbloque seleccionado
                        else: # si no está activada la seleccion multiple, quiere decir que se está queriendo seleccionar 1 microbloque
                            if self.selected_microbloque: # si ya había un microbloque seleccionado
                                self.selected_microbloque.setSeleccionado(False)
                                self.hide_add_buttons() # ocultamos los botones "+"
                            self.selected_microbloque = microbloque
                            microbloque.setSeleccionado(True) # cambiar el color del borde del microbloque seleccionado
                            self.show_add_buttons(microbloque) # muestra los botones "+" alrededor del microbloque
                        break
                else: # quiere decir que se hizo click izquierdo pero en un lugar que no es un microbloque
                    if not self.seleccion_multiple: # si no está activada la seleccion multiple
                        if self.selected_microbloque: # si ya había un microbloque seleccionado
                            self.selected_microbloque.setSeleccionado(False) # cambiar el color del borde del microbloque deseleccionado
                        self.selected_microbloque = None
                        self.hide_add_buttons() # oculta los botones "+"

            elif event.button() == Qt.RightButton: # si se hace click derecho
                self.hide_add_buttons()
                for microbloque in self.microbloques: # busca el microbloque que se seleccionó
                    if microbloque.geometry().contains(event.pos()):
                        if not self.seleccion_multiple: # si no está activada la seleccion multiple
                            self.selected_microbloque = microbloque # seleccionamos el microbloque
                            microbloque.setSeleccionado(True) # cambiar el color del borde del microbloque seleccionado
                        break
                else: # si se hizo click derecho pero en un lugar que no es un microbloque
                    if self.selected_microbloque:
                        self.selected_microbloque.setSeleccionado(False)
                    self.selected_microbloque = None
                    self.limpiar_seleccion()
        
        self.update()
    
    def mouseMoveEvent(self, event):
        if self.panning and self.last_pan_pos:
            delta = event.pos() - self.last_pan_pos
            h_bar = self.scroll_area.horizontalScrollBar()
            v_bar = self.scroll_area.verticalScrollBar()
            
            h_bar.setValue(h_bar.value() - delta.x())
            v_bar.setValue(v_bar.value() - delta.y())
            
            self.last_pan_pos = event.pos()
            event.accept()
            return

        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        if self.panning:
            self.panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return

        super().mouseReleaseEvent(event)
        
    def sizeHint(self):
        return QSize(1000, 600)

    def show_add_buttons(self, microbloque):
        self.hide_add_buttons()
        
        # Obtener la posición y dimensiones reales del microbloque
        mb_pos = microbloque.pos()
        mb_width = microbloque.width()
        mb_height = microbloque.height()
        
        # Calcular el tamaño del botón
        button_size = int(BUTTON_SIZE * self.escala)
        
        positions = [
            ('arriba', QPointF(mb_pos.x() + mb_width/2, mb_pos.y() - button_size/2)),
            ('abajo', QPointF(mb_pos.x() + mb_width/2, mb_pos.y() + mb_height + button_size/2)),
            ('izquierda', QPointF(mb_pos.x() - button_size/2, mb_pos.y() + mb_height/2)),
            ('derecha', QPointF(mb_pos.x() + mb_width + button_size/2, mb_pos.y() + mb_height/2))
        ]

        for direction, pos in positions:
            button = QPushButton("+", self)
            button.setGeometry(
                int(pos.x() - button_size/2),
                int(pos.y() - button_size/2),
                button_size,
                button_size
            )
            button.clicked.connect(lambda _, d=direction: self.show_add_menu(d))
            
            # Agregar tooltip
            tooltip_text = {
                'arriba': "Agregar microbloque arriba",
                'abajo': "Agregar microbloque abajo",
                'izquierda': "Agregar microbloque a la izquierda",
                'derecha': "Agregar microbloque a la derecha"
            }
            button.setToolTip(tooltip_text[direction])
            
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
        
        for parent in [[micro_back, 0]] + parent_structures:
            structure_name = self.get_structure_name(parent)
            action_text = self.get_descriptive_action_text(direction, structure_name)
            action = menu.addAction(action_text)
            action.triggered.connect(lambda checked, s=parent: self.add_microbloque(direction, s[0] if isinstance(s, list) else s))
            
            # Conectar los eventos de entrada y salida del mouse
            action.hovered.connect(lambda s=parent, d=direction: self.show_preview(d, s))
            action.triggered.connect(self.hide_preview)
        
        button = self.sender()
        menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))

    def show_preview(self, direction, structure):
        if not hasattr(self, 'preview_dialog'):
            self.preview_dialog = QDialog(self)
            self.preview_dialog.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
            layout = QVBoxLayout()
            self.preview_label = QLabel()
            self.description_label = QLabel()
            self.description_label.setWordWrap(True)
            layout.addWidget(self.preview_label)
            layout.addWidget(self.description_label)
            self.preview_dialog.setLayout(layout)
        
        preview_pixmap = self.preview_images[direction].scaled(300, 175, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview_label.setPixmap(preview_pixmap)
        self.description_label.setText(self.get_preview_description(direction, structure))
        
        self.preview_dialog.adjustSize()
        
        # Calcular la posición del diálogo
        cursor_pos = QCursor.pos()
        dialog_pos = cursor_pos + QPoint(50, -self.preview_dialog.height() // 2)
        
        # Asegurarse de que el diálogo no se salga de la pantalla
        screen = QApplication.primaryScreen().geometry()
        if dialog_pos.x() + self.preview_dialog.width() > screen.width():
            dialog_pos.setX(cursor_pos.x() - self.preview_dialog.width() - 20)
        if dialog_pos.y() + self.preview_dialog.height() > screen.height():
            dialog_pos.setY(screen.height() - self.preview_dialog.height())
        elif dialog_pos.y() < 0:
            dialog_pos.setY(0)
        
        self.preview_dialog.move(dialog_pos)
        self.preview_dialog.show()
    
    def hide_preview(self):
        if hasattr(self, 'preview_dialog'):
            self.preview_dialog.hide()
    

    def get_descriptive_action_text(self, direction, structure_name):
        direction_text = {
            'arriba': "encima de",
            'abajo': "debajo de",
            'izquierda': "antes de",
            'derecha': "después de"
        }
        return f"Agregar {direction_text[direction]} {structure_name}"

    def get_structure_name(self, estructura):
        if isinstance(estructura, list):
            nodo = estructura[0]
            nivel = estructura[1]
        else:
            nodo = estructura
            nivel = 0

        if isinstance(nodo, MicroBloque):
            return f"el microbloque '{nodo.nombre}'"
        elif isinstance(nodo, TopologiaSerie):
            return f"la estructura en serie (nivel {nivel})"
        elif isinstance(nodo, TopologiaParalelo):
            return f"la estructura en paralelo (nivel {nivel})"
        else:
            return "la estructura desconocida"

    def get_preview_description(self, direction, estructura):
        structure_name = self.get_structure_name(estructura)
        direction_text = {
            'arriba': "encima de",
            'abajo': "debajo de",
            'izquierda': "antes de",
            'derecha': "después de"
        }
        return f"Se agregará un nuevo microbloque {direction_text[direction]} {structure_name}."
        
    def mostrar_menu_contextual(self, position):
        context_menu = QMenu(self) # creamos el menu
        if self.seleccion_multiple and len(self.selected_microbloques) > 0: # si está activa la seleccion multiple y hay microbloques seleccionados
            delete_action = QAction("Eliminar microbloques", self) # definimos una opción: será la accion de eliminar los microbloques seleccionados
            delete_action.triggered.connect(lambda: self.delete_selected_microbloques()) # la funcion a la que se llama cuando se elige esa opción
            context_menu.addAction(delete_action) # agregamos la opción al menu
        elif self.selected_microbloque: # si se seleccionó un microbloque
            delete_action = QAction("Eliminar microbloque", self) # definimos una opción: será la accion de eliminar el microbloque
            delete_action.triggered.connect(lambda: self.delete_microbloque(self.selected_microbloque)) # la funcion a la que se llama cuando se elige esa opción
            context_menu.addAction(delete_action) # agregamos la opción al menu
        if context_menu.actions(): # si hay opciones en el menu
            context_menu.exec_(self.mapToGlobal(position)) # mostramos el menu en la posición del mouse

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete: # si se aprieta la tecla "Delete" ("Suprimir")
            if self.seleccion_multiple and self.selected_microbloques: # si está activa la seleccion multiple y hay microbloques seleccionados
                self.delete_selected_microbloques() # borramos los microbloques seleccionados
            elif self.selected_microbloque: # si hay un microbloque seleccionado (y no está activa la seleccion multiple)
                self.delete_microbloque(self.selected_microbloque) # borramos el microbloque seleccionado
        else:
            super().keyPressEvent(event)

    def delete_microbloque(self, microbloque):
        self.microbloques.remove(microbloque)
        microbloque.elemento_back.borrar_elemento()
        microbloque.deleteLater()
        self.selected_microbloque = None
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()

    def delete_selected_microbloques(self):
        for microbloque in self.selected_microbloques:
            self.microbloques.remove(microbloque)
            microbloque.elemento_back.borrar_elemento()
            microbloque.deleteLater()
            self.hide_add_buttons()
        self.selected_microbloques.clear() # limpio la lista de microbloques seleccionados
        self.load_microbloques()
        self.update()

    def set_seleccion_multiple(self, valor):
        self.seleccion_multiple = valor # seteamos el valor
        if not valor: # si se deselecciona la opción de seleccionar varios
            self.limpiar_seleccion() # limpiamos la selección
        self.update()

    def limpiar_seleccion(self):
        for microbloque in self.selected_microbloques:
            microbloque.setSeleccionado(False)
        self.selected_microbloques.clear()
        if self.selected_microbloque:
            self.selected_microbloque.setSeleccionado(False)
            self.selected_microbloque = None

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

    def calcular_punto_medio_topologia(self):
        if not self.microbloques:
            return self.height() / 2
        top = float('inf') # infinito
        bottom = float('-inf') # - infinito
        for mb in self.microbloques:
            mb_centro = mb.pos().y() + mb.height() / 2
            top = min(top, mb_centro)
            bottom = max(bottom, mb_centro)
        return (top + bottom) / 2

    def encontrar_bloque_mas_a_la_derecha(self):
        if not self.microbloques:
            return None
        return max(self.microbloques, key=lambda mb: mb.pos().x() + mb.width()) # retorna el que tenga mayor x

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
    

