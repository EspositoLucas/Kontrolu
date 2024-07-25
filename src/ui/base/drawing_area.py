import os
from PyQt5.QtWidgets import QWidget, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMenu, QAction, QScrollArea, QTextEdit, QToolTip, QApplication, QComboBox,QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap, QCursor,QFont
from PyQt5.QtCore import Qt, QPointF, QRectF,QPoint
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque,ANCHO,ALTO

MARGEN_HORIZONTAL = 200
MARGEN_VERTICAL = 50
BUTTON_SIZE = 20
RADIO = 40
MARGEN_PARALELO = 20

class DrawingArea(QScrollArea):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.content = DrawingContent(parent, modelo, self)
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
        self.macrobloque = macrobloque
        self.modelo = macrobloque.modelo # es la representacion backend del macrobloque
        self.creating_microbloque = False
        self.seleccion_multiple = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.add_buttons_paralelo = []
        self.selected_microbloques = []
        self.panning = False
        self.load_preview_images()
        self.load_connection_image()
        self.init_ui()
        
    def init_ui(self):
        self.setFocusPolicy(Qt.StrongFocus) # sirve para permitir que el teclado de la compu interactue con la ventana
        self.setContextMenuPolicy(Qt.CustomContextMenu) # sirve para poder mostrar un menu contextual (por ejemplo, cuando hago click derecho)
        self.customContextMenuRequested.connect(self.mostrar_menu_contextual) # permite agregar nuestro propio menu contextual
        # Agregar botón de ayuda
        self.help_button = QPushButton("?", self)
        self.help_button.setGeometry(10, 60, 30, 30)
        self.help_button.clicked.connect(self.show_help)
        self.help_button.setToolTip("Mostrar ayuda")
    
    def load_microbloques(self):
        for microbloque in self.microbloques:
                microbloque.deleteLater() # elimina cada elemento
        self.microbloques.clear() # vacia la lista de microbloques
        self.limpiar_seleccion() # si habia seleccionados, los limpia
        self.dibujar_topologia(self.macrobloque.modelo.topologia, QPointF(ANCHO, (self.height() / 2) - (ALTO / 2))) #le agregue el 40 para que quede centrado
        self.print_topologia(self.macrobloque.modelo.topologia)
        self.ajustar_tamanio_widget()
        self.update()
        
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
        self.connection_image = QPixmap(os.path.join(img_path,'puntoSuma_positiva.png'))
        if self.connection_image.isNull():
            print(f"Error: No se pudo cargar la imagen en {img_path}")
    
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
    
    def ajustar_tamanio_widget(self):
        if self.microbloques:
            max_x = max(mb.pos().x() + mb.width() for mb in self.microbloques)
            max_y = max(mb.pos().y() + mb.height() for mb in self.microbloques)
            nuevo_ancho = max(int(max_x + 400), self.scroll_area.viewport().width())
            nuevo_alto = max(int(max_y + 100), self.scroll_area.viewport().height())
            self.setMinimumSize(nuevo_ancho, nuevo_alto)
        else:
            self.setMinimumSize(self.scroll_area.viewport().width(), self.scroll_area.viewport().height())
    
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
        
    def dibujar_topologia(self, topologia, posicion_inicial):
        if isinstance(topologia, TopologiaSerie):
            return self.dibujar_serie(topologia, posicion_inicial)
        elif isinstance(topologia, TopologiaParalelo):
            return self.dibujar_paralelo(topologia, posicion_inicial)
        elif isinstance(topologia, MicroBloque):
            return self.create_microbloque(topologia, posicion_inicial)
        
    def dibujar_serie(self, serie, posicion_inicial):
        posicion_actual = posicion_inicial
        punto_final = posicion_inicial
        for hijo in serie.hijos:
            punto_final = self.dibujar_topologia(hijo, posicion_actual)
            posicion_actual = QPointF(punto_final.x() + MARGEN_HORIZONTAL, posicion_inicial.y())
        return punto_final

    def dibujar_paralelo(self, paralelo, posicion_inicial):
        posicion_inicial.setX(posicion_inicial.x() + MARGEN_PARALELO)
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL

        y_actual = posicion_inicial.y() - altura_total / 2
        punto_final_max = posicion_inicial
        for hijo in paralelo.hijos:
            centro_del_hijo = y_actual + hijo.alto() / 2
            posicion_del_hijo = QPointF(posicion_inicial.x(), centro_del_hijo)
            punto_final = self.dibujar_topologia(hijo, posicion_del_hijo)
            if punto_final.x() > punto_final_max.x():
                punto_final_max = punto_final
            y_actual += hijo.alto() + MARGEN_VERTICAL

        return QPointF(punto_final_max.x() + MARGEN_PARALELO, posicion_inicial.y())

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        self.update()
        return pos
    
    def clear_all(self):
        if self.microbloques:
            for microbloque in self.microbloques:
                microbloque.deleteLater() # elimina cada elemento
            self.microbloques.clear() # vacia la lista de microbloques
        
         # vacia la lista de botones "+"
        for button in self.add_buttons:
            button.deleteLater()
        self.add_buttons.clear()
        self.macrobloque.modelo.reset_topologia() # si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
        self.load_microbloques() # resetea la vista
        self.update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # Dibujar cuadrícula
        self.draw_grid(painter)
        self.draw_io_blocks(painter)
        
        if not self.microbloques:
            self.draw_empty_connection(painter)
        else:
           punto_inicial = QPointF((50 + RADIO) + RADIO, self.height() / 2)
           punto_final = self.draw_connections(painter, self.macrobloque.modelo.topologia, punto_inicial)
           self.draw_final_connection(painter, punto_final) # punto_final es el punto de salida de la última conexión

    def draw_final_connection(self, painter, start_point):
        if start_point is None:
            return

        mb_mas_lejano = self.encontrar_bloque_mas_a_la_derecha()
        if mb_mas_lejano:
            end_x = mb_mas_lejano.pos().x() + mb_mas_lejano.width() + (MARGEN_HORIZONTAL / 2) - RADIO
        else:
            end_x = self.width() - (130 + RADIO)

        end_point = QPointF(end_x, self.height() / 2) # end_point es el lugar donde está el bloque de salida
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(start_point, end_point)

    def draw_empty_connection(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        entrada = QPointF(130, self.height() / 2)
        salida = QPointF(self.width() - 210, self.height() / 2)
        painter.drawLine(entrada, salida)
        
        # Dibujar el botón "+" en el medio
        center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
        button_rect = QRectF(center.x() - BUTTON_SIZE/2, center.y() - BUTTON_SIZE/2, BUTTON_SIZE, BUTTON_SIZE)
        button_fill_color = QColor("#ADD8E6")
        painter.setBrush(QBrush(button_fill_color))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")

        # Guardar la posición del botón para detectar clics
        self.add_button_rect = button_rect

    def draw_io_blocks(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        
        contour_color = QColor(0, 0, 0)  # Negro para el contorno
        contour_pen = QPen(contour_color, 3)  # Grosor del contorno
        fill_color = QColor(128, 128, 128)
        text_color = QColor(255, 255, 255)  # Blanco para el texto
        text_font = QFont('Arial', int(12))  # Fuente Arial y tamaño ajustado

        painter.setPen(contour_pen)
        painter.setBrush(QBrush(fill_color))

        centro_y = self.height() / 2  # Posición y del centro para ambos círculos
        
        centro_entrada_x = 50 + RADIO  # Posición x del centro del círculo de entrada
        centro_salida_x = self.width() - 130 - RADIO  # Posición x del centro del círculo de salida
        
        # Dibujar el círculo de entrada
        painter.drawEllipse(QPointF(centro_entrada_x, centro_y), RADIO, RADIO)

        mb_mas_lejano = self.encontrar_bloque_mas_a_la_derecha()
        if mb_mas_lejano:
            centro_salida_x = mb_mas_lejano.pos().x() + mb_mas_lejano.width()  + (MARGEN_HORIZONTAL / 2)
        else:
            centro_salida_x = self.width() - (130 + RADIO)

        # Dibujar círculo de salida
        painter.drawEllipse(QPointF(centro_salida_x, centro_y), RADIO, RADIO)

        # Establecer el color y la fuente para el texto
        painter.setPen(text_color)
        painter.setFont(text_font)

        # Dibujar texto en los círculos
        painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Entrada")
        painter.drawText(QRectF(centro_salida_x - 40, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Salida")
    
    def draw_connections(self, painter, topologia, punto_de_partida, is_parallel=False):
        if punto_de_partida is None:
            return None

        painter.setPen(QPen(Qt.black, 2)) # configura el color y grosor de la línea
        
        if isinstance(topologia, TopologiaSerie):
            return self.draw_serie_connections(painter, topologia, punto_de_partida)
        elif isinstance(topologia, TopologiaParalelo):
            return self.draw_paralelo_connections(painter, topologia, punto_de_partida)
        elif isinstance(topologia, MicroBloque):
            return self.draw_microbloque_connection(painter, topologia, punto_de_partida, is_parallel)
        else:
            return punto_de_partida

    def draw_serie_connections(self, painter, serie, punto_inicial):
        """
        Dibuja las conexiones de una serie de microbloques
        @return el punto final de la serie
        """
        if punto_inicial is None:
            return None

        punto_actual = punto_inicial
        for hijo in serie.hijos:
            # para cada elemento de la serie, llama a draw_connections para que dibuje sus componentes (si las hubiera)
            punto_final = self.draw_connections(painter, hijo, punto_actual) 
            punto_actual = punto_final

        return punto_actual

    def draw_paralelo_connections(self, painter, paralelo, punto_inicial):
        if punto_inicial is None:
            return None

        # Calcular punto de bifurcación
        comienzo_de_rama = QPointF(punto_inicial.x() + MARGEN_PARALELO, punto_inicial.y())  # es el margen antes de hacer la bifurcación
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos) # idem que en dibujar_paralelo
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL # idem que en dibujar_paralelo
        
        # Dibujar línea horizontal antes de la bifurcación
        painter.drawLine(punto_inicial, comienzo_de_rama)
        
        # Dibujar conexiones para cada rama
        y_actual = punto_inicial.y() - altura_total / 2
        puntos_finales = []
        for hijo in paralelo.hijos:
            punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2) # deja igual la "x" y pone la "y" en el centro del microbloque
            painter.drawLine(comienzo_de_rama, punto_final_rama_vertical)  # Línea vertical de bifurcación
            punto_final_rama_actual = self.draw_connections(painter, hijo, punto_final_rama_vertical, True) # partiendo desde el extremo de la linea vertical de bifurcacion, comienza a dibujar lo que sigue
            if punto_final_rama_actual is not None:
                puntos_finales.append(punto_final_rama_actual) # se va guardando los puntos finales de cada rama del paralelo
            y_actual += hijo.alto() + MARGEN_VERTICAL # incorpora el margen vertical
        
        if not puntos_finales: # querria decir que no dibujo nada en los paralelos (no creo que pase nunca, pero por las dudas lo dejo)
            return punto_inicial

        # Encontrar el punto final más a la derecha (margen paralelo permite dibujar la linea horizontal final, al salir de una rama paralela)
        max_x = max(point.x() for point in puntos_finales) + MARGEN_PARALELO # esto está por si una rama quedó "mas larga horizontalmente" que la otra
         
        # Dibujar líneas horizontales para reconectar las ramas
        for end_point in puntos_finales:
            painter.drawLine(end_point, QPointF(max_x, end_point.y())) # le sumamos 20 para tener una linea horizontal (al salir del microbloque) antes de reconectar
        
        punto_de_reconexion = QPointF(max_x, punto_inicial.y())  # punto de reconexión (es el punto más a la derecha de la estructura paralelo)
        # insertar imagen de punto suma en el punto de reconexión
        painter.drawEllipse(punto_de_reconexion, 5, 5) # TODO: Cambiar por imagen de punto suma

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
        # busca en la lista de microbloques de la drawing_area, el microbloque que queremos conectar
        for mb in self.microbloques:
            if mb.elemento_back == microbloque: # compara su elemento back
                if es_paralelo:
                    punto_final = QPointF(mb.pos().x(), punto_inicial.y()) # deja igual el "x", y el "y" lo deja igual respecto a de la rama paralela en donde está
                else:
                    punto_final = mb.pos() + QPointF(0, mb.height() / 2) # mb.pos() = da la esquina superior izquierda del microbloque ||| + QPointF(0, mb.height() / 2) = mueve el punto hacia abajo hasta la mitad de la altura del microbloque.
                
                # punto_final seria el punto en donde va a llegar la flecha que proviene del microbloque anterior (punto medio izquierdo del microbloque actual)

                if punto_inicial is not None and punto_final is not None:
                    painter.drawLine(punto_inicial, punto_final) # dibuja la linea
                
                return mb.pos() + QPointF(mb.width(), mb.height() / 2) # retorna un punto que representa la mitad del lado derecho del microbloque. Este punto se usará como punto de inicio para la siguiente conexión.
        
        # Si no se encuentra el microbloque, retornamos el punto de inicio --> Si no encuentra el microbloque en la lista, simplemente retorna el punto_inicial
        return punto_inicial

    def create_new_microbloque(self, pos, relation=None, reference_structure=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nuevo Microbloque")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Nombre del microbloque")
        name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(name_input)

        color_button = QPushButton("Seleccionar Color")
        color_button.setStyleSheet("background-color: #444; color: white;")
        color_button.clicked.connect(lambda: self.select_color(color_button))
        layout.addWidget(color_button)

        transfer_label = QLabel("Función de Transferencia:")
        transfer_label.setStyleSheet("color: white;")
        latex_editor = LatexEditor()
        latex_editor.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        layout.addWidget(transfer_label)
        layout.addWidget(latex_editor)

        save_button = QPushButton("Guardar")
        save_button.setStyleSheet("background-color: #444; color: white;")
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
                self.macrobloque.modelo.topologia.agregar_elemento(new_microbloque) # sería el primer microbloque
            
            self.load_microbloques()  # recargo todos los microbloques
            self.update()
            self.hide_add_buttons() # ocultamos los botones "+" por si quedaron visibles

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
        elif relation == "arriba": 
            reference_serie.crear_paralela_respecto_de_serie_arriba(new_microbloque) # agrega un microbloque en serie arriba de la estructura serie
        else: # abajo 
            reference_serie.crear_paralela_respecto_de_serie_abajo(new_microbloque) # agrega un microbloque en serie abajo de la estructura serie

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
        if event.button() == Qt.LeftButton and event.modifiers() & Qt.ControlModifier:
            self.panning = True
            self.last_pan_pos = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

        if not self.microbloques: # si no hay microbloques y se hace click sobre el único botón "+", entonces se crea un microbloque 
            if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(event.pos()):
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
            button.setStyleSheet("background-color: white; color: black;")
            button.setGeometry(int(pos.x() - BUTTON_SIZE/2), int(pos.y() - BUTTON_SIZE/2), BUTTON_SIZE, BUTTON_SIZE)
            button.clicked.connect(lambda _, d=direction: self.show_add_menu(d))
            button.show()
            self.add_buttons.append(button)
        
        # Agregar tooltip
            tooltip_text = {
                'arriba': "Agregar microbloque arriba",
                'abajo': "Agregar microbloque abajo",
                'izquierda': "Agregar microbloque a la izquierda",
                'derecha': "Agregar microbloque a la derecha"
            }
            button.setToolTip(tooltip_text[direction])

    def hide_add_buttons(self):
        for button in self.add_buttons:
            button.deleteLater()
        self.add_buttons.clear()

    def show_add_menu(self, direction):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                border: 2px solid black;  /* Agrega un borde negro */
            }
        """)
        micro_back = self.selected_microbloque.elemento_back
        parent_structures = micro_back.get_parent_structures()
        
        for parent in [[micro_back, 0]] + parent_structures:
            structure_name = self.get_structure_name(parent)
            action_text = self.get_descriptive_action_text(direction, structure_name)
            action = menu.addAction(action_text)
            # action = menu.addAction(f"Respecto a {self.get_structure_name(parent)}")
            action.triggered.connect(lambda _, s=parent[0]: self.add_microbloque(direction, s))
            
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
        context_menu.setStyleSheet("""
            QMenu {
                border: 2px solid black;  /* Agrega un borde negro */
            }
        """)
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

    def encontrar_bloque_mas_a_la_derecha(self):
        if not self.microbloques:
            return None
        return max(self.microbloques, key=lambda mb: mb.pos().x() + mb.width()) # retorna el que tenga mayor x

    def print_topologia(self, topologia, indent=0):
        """
        Imprime el arbol del macrobloque por consola
        """
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
    
    
    def draw_grid(self, painter):
        painter.save()
        painter.setPen(QPen(QColor(200, 200, 200), 1))
        
        grid_size = 20
        
        for x in range(0, int(self.width()), int(grid_size)):
            painter.drawLine(x, 0, x, self.height())
        
        for y in range(0, int(self.height()), int(grid_size)):
            painter.drawLine(0, y, self.width(), y)
        
        painter.restore()