import os
from PyQt5 import sip 
from PyQt5.QtWidgets import QWidget, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMenu, QAction, QTextEdit, QApplication, QComboBox, QMessageBox, QHBoxLayout, QInputDialog, QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPixmapItem, QGraphicsProxyWidget,QTabWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPixmap, QCursor,QFont
from PyQt5.QtCore import Qt, QPointF, QRectF,QPoint,QTimer,QSize
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
from .funcion_transferencia import FuncionTransferencia
from .add_button import AddButton
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque, ANCHO, ALTO
from back.topologia.configuraciones import Configuracion,TipoError
from back.topologia.perturbacion import Perturbacion

MARGEN_HORIZONTAL = 200
MARGEN_VERTICAL = 50
BUTTON_SIZE = 20
RADIO = 40
MARGEN_PARALELO = 20

class DrawingArea(QGraphicsView):
    def __init__(self, macrobloque=None, ventana=None):
        super().__init__(ventana)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.initial_rect = QRectF(0, 0, 1000, 1000)
        self.scene.setSceneRect(self.initial_rect)

        self.microbloques = []
        self.grid_lines = []
        self.selected_microbloque = None
        self.macrobloque = macrobloque
        self.modelo = macrobloque.modelo # es la representacion backend del macrobloque
        self.creating_microbloque = False
        self.seleccion_multiple = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.add_buttons_paralelo = []
        self.selected_microbloques = []
        self.punto_salida_actual = None
        self.panning = False
        self.input_widget = None
        self.config_layout = QVBoxLayout()
        self.edit_config_layout = QVBoxLayout()
        self.lista_configuraciones = None
        self.load_preview_images()
        self.load_connection_image()
    
        self.init_ui()
        
    def init_ui(self):
        self.setFocusPolicy(Qt.StrongFocus) # sirve para permitir que el teclado de la compu interactue con la ventana
        self.setContextMenuPolicy(Qt.CustomContextMenu) # sirve para poder mostrar un menu contextual (por ejemplo, cuando hago click derecho)
        self.customContextMenuRequested.connect(self.mostrar_menu_contextual) # permite agregar nuestro propio menu contextual

    def update_scene_rect(self, item_rect):
        current_rect = self.scene.sceneRect() # obtiene el rectangulo actual de la escena
        new_rect = current_rect.united(item_rect) # une el rectangulo actual con el rectangulo del item
        
        if new_rect != current_rect: # si el nuevo rectangulo es distinto al actual
            margin = 100  # es un espacio para que no quede tan pegado al borde
            new_rect = new_rect.adjusted(-margin, -margin, margin, margin) # ajusta el rectangulo usando el margen
            self.scene.setSceneRect(new_rect) # se lo setea a la escena
            self.draw_grid() # redibujo la cuadricula porque cambié el tamaño del fondo
        

    def add_item(self, item): 
        # NO BORRAR: es un metodo que se podría usar en vez de llamar a self.scene.addItem(item)
        self.scene.addItem(item)
        item_rect = item.sceneBoundingRect()
        self.update_scene_rect(item_rect)

    def resizeEvent(self, event):
        # sobreescribo el resizeEvent propio de QGraphicsView
        super().resizeEvent(event)
        visible_rect = self.mapToScene(self.viewport().rect()).boundingRect() # calcula el rectangulo en el cual entran todos los items de la escena
        self.update_scene_rect(visible_rect) # actualiza el rectangulo de la escena

    def load_microbloques(self):
        self.limpiar_escena()
        self.scene.setSceneRect(self.initial_rect) # reinicia el rectangulo al tamaño default
        self.microbloques.clear() # vacia la lista de microbloques
        self.limpiar_seleccion() # si habia seleccionados, los limpia
        self.dibujar_topologia(self.macrobloque.modelo.topologia, QPointF(ANCHO, (self.height() / 2) - (ALTO / 2))) #le agregue el 40 para que quede centrado
        self.dibujar_lo_demas()
        # self.print_topologia(self.macrobloque.modelo.topologia)
        self.update_scene_rect(self.scene.itemsBoundingRect()) # actualiza el rectangulo de la escena en funcion de lo dibujado
        self.update()
        
    def load_preview_images(self):
        current_dir = os.path.dirname(os.path.abspath(__file__)) # obtiene la ruta actual del archivo actual
        imgs_dir = os.path.join(current_dir, '..', 'base', 'imgs') # navega hacia arriba dos niveles y luego a la carpeta 'imgs'
        
        self.preview_images = { # arma las rutas y carga las imagenes
            'arriba': QPixmap(os.path.join(imgs_dir, 'paralelo.png')),
            'abajo': QPixmap(os.path.join(imgs_dir, 'paralelo.png')),
            'izquierda': QPixmap(os.path.join(imgs_dir, 'serie.png')),
            'derecha': QPixmap(os.path.join(imgs_dir, 'serie.png'))
        }
    
    def load_connection_image(self): # dibuja la imagen de punto suma en las conexiones de paralelo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, '..','base', 'imgs')
        self.connection_image = QPixmap(os.path.join(img_path, 'puntoSuma_positiva.png'))
        if self.connection_image.isNull():
            print(f"Error: No se pudo cargar la imagen en {img_path}")
    
    def show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Ayuda")
        layout = QVBoxLayout()

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        
        # Leer el contenido HTML del archivo externo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        help_file_path = os.path.join(current_dir, 'help_content.html')
        with open(help_file_path, 'r', encoding='utf-8') as help_file:
            help_content = help_file.read()

        help_text.setHtml(help_content)
        layout.addWidget(help_text)

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(help_dialog.close)
        layout.addWidget(close_button)
        help_dialog.setLayout(layout)
        help_dialog.exec_()

    def mouseMoveEvent(self, event): 
        if self.panning and self.last_pan_pos: # si se está moviendo el mouse y se está haciendo panning (arrastrar la pantalla)
            delta = event.pos() - self.last_pan_pos
            self.last_pan_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            return

        super().mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        if self.panning: # si se estaba haciendo panning
            self.panning = False # se desactiva el panning
            self.setCursor(Qt.ArrowCursor) # se cambia el cursor a la flecha
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
        elif isinstance(topologia, Perturbacion):
            return self.draw_perturbacion(topologia, posicion_inicial)
        
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
        microbloque = Microbloque(microbloque_back)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        self.scene.addItem(microbloque)
        return pos
    
    def clear_all(self):
        if self.microbloques:
            for microbloque in self.microbloques:
                #microbloque.deleteLater() # elimina cada elemento
                self.scene.removeItem(microbloque)
            self.microbloques.clear() # vacia la lista de microbloques
        
         # vacia la lista de botones "+"
        for button in self.add_buttons:
            self.scene.removeItem(button)
        self.add_buttons.clear()
        self.macrobloque.modelo.reset_topologia() # si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
        self.load_microbloques() # resetea la vista
        self.update()
    
    def dibujar_lo_demas(self):
        
        if not self.microbloques:
            self.draw_empty_connection()
        else:
           punto_inicial = QPointF((50 + RADIO) + RADIO, self.height() / 2) # punto de inicio de la primera conexión
           punto_final = self.draw_connections(self.macrobloque.modelo.topologia, punto_inicial)
           self.draw_final_connection(punto_final) # punto_final es el punto de salida de la última conexión
           self.update()

        self.draw_io_blocks()

    def draw_final_connection(self, start_point):
        if start_point is None:
            return
        
        if self.punto_salida_actual is None:
            self.punto_salida_actual = QPointF(self.width() - 130 - RADIO, self.height() / 2)

        if start_point.x() < self.punto_salida_actual.x():
            end_x = self.punto_salida_actual.x()
        else:
            self.punto_salida_actual.setX(start_point.x() + MARGEN_HORIZONTAL)
            end_x = self.punto_salida_actual.x()

        end_point = QPointF(end_x, self.height() / 2) # end_point es el lugar donde está el bloque de salida
        #painter.setPen(QPen(Qt.black, 2))
        #painter.drawLine(start_point, end_point)
        line = QGraphicsLineItem(start_point.x(), start_point.y(), end_point.x(), end_point.y())
        line.setPen(QPen(Qt.black, 2))
        self.scene.addItem(line)

        self.update()

    def draw_empty_connection(self):
        entrada = QPointF(130, self.height() / 2)
        salida = QPointF(self.width() - 210, self.height() / 2)
        self.punto_salida_actual = salida
        line = QGraphicsLineItem(entrada.x(), entrada.y(), salida.x(), salida.y())
        line.setPen(QPen(Qt.black, 3))
        self.scene.addItem(line)
        
        # Dibujar el botón "+" en el medio
        center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
        button = QGraphicsEllipseItem(center.x() - BUTTON_SIZE/2, center.y() - BUTTON_SIZE/2, BUTTON_SIZE, BUTTON_SIZE)
        button.setBrush(QBrush(QColor("#ADD8E6")))
        button.setPen(QPen(Qt.black, 2))
        self.scene.addItem(button)

        text = QGraphicsTextItem("+")
        text.setFont(QFont("Arial", 12, QFont.Bold))
        text.setDefaultTextColor(Qt.black)
        text.setPos(center.x() - text.boundingRect().width() / 2, center.y() - text.boundingRect().height() / 2)
        self.scene.addItem(text)

        # Guardar la posición del botón para detectar clics
        self.add_button_rect = QRectF(center.x() - BUTTON_SIZE/2, center.y() - BUTTON_SIZE/2, BUTTON_SIZE, BUTTON_SIZE)

    def draw_io_blocks(self):
        centro_y = self.height() / 2  # Posición y del centro para ambos círculos 
        centro_entrada_x = 50 + RADIO  # Posición x del centro del círculo de entrada
        centro_salida_x = self.width() - 130 - RADIO  # Posición x del centro del círculo de salida
        
        # Dibujar el círculo de entrada
        entrada = QGraphicsEllipseItem(centro_entrada_x - RADIO, centro_y - RADIO, RADIO * 2, RADIO * 2)
        entrada.setBrush(QBrush(QColor(128, 128, 128)))
        entrada.setPen(QPen(Qt.black, 3))
        self.scene.addItem(entrada)

        # Colocar texto "Entrada" en el círculo de entrada
        text = QGraphicsTextItem("Entrada")
        text.setFont(QFont("Arial", 12))
        text.setDefaultTextColor(Qt.black)
        text.setPos(centro_entrada_x - text.boundingRect().width() / 2, centro_y - text.boundingRect().height() / 2)
        self.scene.addItem(text)

        if not self.punto_salida_actual:
            centro_salida_x = self.width() - (130 + RADIO)
        else:
            centro_salida_x = self.punto_salida_actual.x() + RADIO

        if not self.microbloques:
            centro_salida_x = self.width() - (130 + RADIO)
            self.punto_salida_actual = None

        # Dibujar círculo de salida
        salida = QGraphicsEllipseItem(centro_salida_x - RADIO, centro_y - RADIO, RADIO * 2, RADIO * 2)
        salida.setBrush(QBrush(QColor(128, 128, 128)))
        salida.setPen(QPen(Qt.black, 3))
        self.scene.addItem(salida)

        # Colocar texto "Salida" en el círculo de salida
        text = QGraphicsTextItem("Salida")
        text.setFont(QFont("Arial", 12))
        text.setDefaultTextColor(Qt.black)
        text.setPos(centro_salida_x - text.boundingRect().width() / 2, centro_y - text.boundingRect().height() / 2)
        self.scene.addItem(text)       
        
        self.update()
    
    def draw_connections(self, topologia, punto_de_partida, is_parallel=False):
        if punto_de_partida is None:
            return None
        
        if isinstance(topologia, TopologiaSerie):
            return self.draw_serie_connections(topologia, punto_de_partida)
        elif isinstance(topologia, TopologiaParalelo):
            return self.draw_paralelo_connections(topologia, punto_de_partida)
        elif isinstance(topologia, MicroBloque):
            return self.draw_microbloque_connection(topologia, punto_de_partida, is_parallel)
        else:
            return punto_de_partida
        

    def draw_serie_connections(self, serie, punto_inicial):
        """
        Dibuja las conexiones de una serie de microbloques
        @return el punto final de la serie
        """
        if punto_inicial is None:
            return None

        punto_actual = punto_inicial
        for hijo in serie.hijos:
            # para cada elemento de la serie, llama a draw_connections para que dibuje sus componentes (si las hubiera)
            punto_final = self.draw_connections(hijo, punto_actual) 
            punto_actual = punto_final

        return punto_actual

    def draw_paralelo_connections(self, paralelo, punto_inicial):
        if punto_inicial is None:
            return None

        # Calcular punto de bifurcación
        comienzo_de_rama = QPointF(punto_inicial.x() + MARGEN_PARALELO, punto_inicial.y())  # es el margen antes de hacer la bifurcación
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos) # idem que en dibujar_paralelo
        altura_total += (len(paralelo.hijos) - 1) * MARGEN_VERTICAL # idem que en dibujar_paralelo
        
        # Dibujar línea horizontal antes de la bifurcación (desde el punto inicial hasta el comienzo de la rama)
        line = QGraphicsLineItem(punto_inicial.x(), punto_inicial.y(), comienzo_de_rama.x(), comienzo_de_rama.y())
        line.setPen(QPen(Qt.black, 2))
        self.scene.addItem(line)
        
        # Dibujar conexiones para cada rama
        y_actual = punto_inicial.y() - altura_total / 2
        puntos_finales = []
        for hijo in paralelo.hijos:
            punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2) # deja igual la "x" y pone la "y" en el centro del microbloque
            
            line = QGraphicsLineItem(comienzo_de_rama.x(), comienzo_de_rama.y(), punto_final_rama_vertical.x(), punto_final_rama_vertical.y()) # Línea vertical de bifurcación (desde el comienzo de la rama hasta el punto final rama vertical)
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)
            
            punto_final_rama_actual = self.draw_connections(hijo, punto_final_rama_vertical, True) # partiendo desde el extremo de la linea vertical de bifurcacion, comienza a dibujar lo que sigue
            if punto_final_rama_actual is not None:
                puntos_finales.append(punto_final_rama_actual) # se va guardando los puntos finales de cada rama del paralelo
            y_actual += hijo.alto() + MARGEN_VERTICAL # incorpora el margen vertical
        
        if not puntos_finales: # querria decir que no dibujo nada en los paralelos (no creo que pase nunca, pero por las dudas lo dejo)
            return punto_inicial

        # Encontrar el punto final más a la derecha (margen paralelo permite dibujar la linea horizontal final, al salir de una rama paralela)
        max_x = max(point.x() for point in puntos_finales) + MARGEN_PARALELO # esto está por si una rama quedó "mas larga horizontalmente" que la otra
         
        # Dibujar líneas horizontales para reconectar las ramas
        for end_point in puntos_finales:
            #painter.drawLine(end_point, QPointF(max_x, end_point.y())) # le sumamos 20 para tener una linea horizontal (al salir del microbloque) antes de reconectar
            line = QGraphicsLineItem(end_point.x(), end_point.y(), max_x, end_point.y())
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)

        punto_de_reconexion = QPointF(max_x, punto_inicial.y())  # punto de reconexión (es el punto más a la derecha de la estructura paralelo)
        
        if not self.connection_image.isNull():
            scaled_image = self.connection_image.scaled(
                int(40), 
                int(40), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            x = int(punto_de_reconexion.x() - scaled_image.width() / 2)
            y = int(punto_de_reconexion.y() - scaled_image.height() / 2)
            image = QGraphicsPixmapItem(scaled_image)
            image.setPos(x, y)
            self.scene.addItem(image)
            
            # Calcular el centro y radio de la imagen del punto suma
            imagen_centro = QPointF(x + scaled_image.width() / 2, y + scaled_image.height() / 2)
            radio_imagen = scaled_image.width() / 2
            
            # Dibujar línea desde la rama superior al borde superior de la imagen
            punto_superior = QPointF(imagen_centro.x(), imagen_centro.y() - radio_imagen)
            line = QGraphicsLineItem(max_x, puntos_finales[0].y(), punto_superior.x(), punto_superior.y())
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)
            
            # Dibujar línea desde la rama inferior al borde inferior de la imagen
            punto_inferior = QPointF(imagen_centro.x(), imagen_centro.y() + radio_imagen)
            line = QGraphicsLineItem(max_x, puntos_finales[-1].y(), punto_inferior.x(), punto_inferior.y())
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)
            
            # Dibujar línea horizontal final desde el borde derecho de la imagen
            punto_derecho = QPointF(imagen_centro.x() + radio_imagen, imagen_centro.y())
            punto_mas_alejado = QPointF(max_x + MARGEN_PARALELO, punto_inicial.y())
            line = QGraphicsLineItem(punto_derecho.x(), punto_derecho.y(), punto_mas_alejado.x(), punto_mas_alejado.y())
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)
        else:
            ellipse = QGraphicsEllipseItem(punto_de_reconexion.x() - 5, punto_de_reconexion.y() - 5, 10, 10)
            ellipse.setBrush(QBrush(Qt.black))
            self.scene.addItem(ellipse)
            
            punto_mas_alejado = QPointF(max_x + MARGEN_PARALELO, punto_inicial.y())
            
            line = QGraphicsLineItem(max_x, puntos_finales[0].y(), max_x, puntos_finales[-1].y())
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)
            
            line = QGraphicsLineItem(max_x, punto_inicial.y(), punto_mas_alejado.x(), punto_mas_alejado.y())
            line.setPen(QPen(Qt.black, 2))
            self.scene.addItem(line)

        return punto_mas_alejado
    
    def draw_microbloque_connection(self, microbloque, punto_inicial, es_paralelo):
        # busca en la lista de microbloques de la drawing_area, el microbloque que queremos conectar
        for mb in self.microbloques: # los microbloques ahora heredan de QGraphicsItem
            if mb.elemento_back == microbloque: # compara su elemento back
                if es_paralelo:
                    punto_final = QPointF(mb.pos().x(), punto_inicial.y()) # deja igual el "x", y el "y" lo deja igual respecto a de la rama paralela en donde está
                else:
                    punto_final = mb.pos() + QPointF(0, mb.height() / 2) # mb.pos() = da la esquina superior izquierda del microbloque ||| + QPointF(0, mb.height() / 2) = mueve el punto hacia abajo hasta la mitad de la altura del microbloque.
                
                # punto_final seria el punto en donde va a llegar la flecha que proviene del microbloque anterior (punto medio izquierdo del microbloque actual)

                if punto_inicial is not None and punto_final is not None:
                    # dibujar la linea desde el punto_inicial hasta el punto_final
                    line = QGraphicsLineItem(punto_inicial.x(), punto_inicial.y(), punto_final.x(), punto_final.y())
                    line.setPen(QPen(Qt.black, 2))
                    self.scene.addItem(line)
                
                return mb.pos() + QPointF(mb.width(), mb.height() / 2) # retorna un punto que representa la mitad del lado derecho del microbloque. Este punto se usará como punto de inicio para la siguiente conexión.
        
        # Si no se encuentra el microbloque, retornamos el punto de inicio --> Si no encuentra el microbloque en la lista, simplemente retorna el punto_inicial
        return punto_inicial

    def create_perturbacion(self, pos, relation, reference_element):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nueva Perturbación")
        dialog.setStyleSheet("background-color: #333; color: white;")
        layout = QVBoxLayout()

        # TODO: agregar inputs para datos necesarios

        save_button = QPushButton("Guardar")
        save_button.setStyleSheet("background-color: #444; color: white;")
        save_button.clicked.connect(dialog.accept)
        layout.addWidget(save_button)

        dialog.setLayout(layout)

        if dialog.exec_():
            perturbacion = Perturbacion()
            if relation == "antes":
                reference_element.agregar_perturbacion_antes(perturbacion, reference_element)
            else:  # despues
                reference_element.agregar_perturbacion_despues(perturbacion, reference_element)

            self.load_microbloques()

    def draw_perturbacion(self, perturbacion, pos):
        perturbacion_item = QGraphicsEllipseItem(pos.x(), pos.y(), perturbacion.radio(), perturbacion.radio())
        perturbacion_item.setBrush(QBrush(Qt.yellow))
        self.scene.addItem(perturbacion_item)
        return perturbacion_item


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
            
            new_microbloque = MicroBloque(nombre, color, funcion_transferencia, self.lista_configuraciones, self.macrobloque.modelo.topologia)
            self.lista_configuraciones = None
            
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
    
    # def add_configuration(self, layout):
    #     config_row = QHBoxLayout()
        
    #     name_input = QLineEdit()
    #     name_input.setPlaceholderText("Nombre de la configuración")
    #     name_input.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        
    #     input_config = Configuracion("Entrada")
    #     output_config = Configuracion("Salida")
        
    #     input_button = QPushButton("Configurar Entrada")
    #     input_button.setStyleSheet("background-color: #444; color: white;")
    #     input_button.clicked.connect(lambda: self.edit_configuration(input_config))
        
    #     output_button = QPushButton("Configurar Salida")
    #     output_button.setStyleSheet("background-color: #444; color: white;")
    #     output_button.clicked.connect(lambda: self.edit_configuration(output_config))
        
    #     delete_button = QPushButton("Eliminar")
    #     delete_button.setStyleSheet("background-color: #444; color: white;")
    #     delete_button.clicked.connect(lambda: self.delete_configuration(config_row, layout))
        
    #     config_row.addWidget(name_input)
    #     config_row.addWidget(input_button)
    #     config_row.addWidget(output_button)
    #     config_row.addWidget(delete_button)
        
    #     layout.insertLayout(layout.count() - 1, config_row)
    
    # def delete_configuration(self, config_row, layout):
    #     for i in range(layout.count()):
    #         if layout.itemAt(i) == config_row:
    #             while config_row.count():
    #                 item = config_row.takeAt(0)
    #                 widget = item.widget()
    #                 if widget:
    #                     widget.deleteLater()
    #             layout.removeItem(config_row)
    #             break
    #     self.update()
    
        
    # def guardar_configuracion_editada(self, dialog, configuracion):
    #     # Obtener los nuevos valores de la configuración
    #     configuracion.nombre = self.find_widget(self.config_entrada_layout, QLineEdit, 0).text()
    #     configuracion.limite_inferior = float(self.find_widget(self.config_entrada_layout, QLineEdit, 1).text())
    #     configuracion.limite_superior = float(self.find_widget(self.config_entrada_layout, QLineEdit, 2).text())
    #     configuracion.limite_por_ciclo = float(self.find_widget(self.config_entrada_layout, QLineEdit, 3).text())
    #     configuracion.error_maximo = float(self.find_widget(self.config_entrada_layout, QLineEdit, 4).text())
    #     configuracion.proporcion = float(self.find_widget(self.config_entrada_layout, QLineEdit, 5).text())
    #     configuracion.tipo = self.find_widget(self.config_entrada_layout, QLineEdit, 6).text()
    #     configuracion.ultimo_valor = float(self.find_widget(self.config_entrada_layout, QLineEdit, 7).text())

    #     dialog.accept()

    # def edit_configuration(self, configuracion):
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle(f"Editar Configuración: {configuracion.nombre}")
    #     dialog.setStyleSheet("background-color: #333; color: white;")
    #     layout = QVBoxLayout()

    #     fields = [
    #         ("Límite inferior", "limite_inferior", ""),
    #         ("Límite superior", "limite_superior", ""),
    #         ("Límite por ciclo", "limite_por_ciclo", str(configuracion.limite_por_ciclo)),
    #         ("Error máximo", "error_maximo", str(configuracion.error_maximo)),
    #         ("Proporción", "proporcion", str(configuracion.proporcion)),
    #         ("Último valor", "ultimo_valor", str(configuracion.ultimo_valor)),
    #         ("Probabilidad", "probabilidad", str(configuracion.probabilidad))
    #     ]

    #     for label, attr, default in fields:
            
    #         row = QHBoxLayout()
    #         lbl = QLabel(label)
    #         lbl.setStyleSheet("color: white;")
    #         input_field = QLineEdit()
    #         input_field.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
        
    #         value = getattr(configuracion, attr)
    #         if value == float('inf'):
    #             input_field.setPlaceholderText("Sin límite")
    #         elif value == float('-inf'):
    #             input_field.setPlaceholderText("Sin límite")
    #         else:
    #             input_field.setText(str(value))
                
    #         row.addWidget(lbl)
    #         row.addWidget(input_field)
    #         layout.addLayout(row)
            
            
    #     # Agregar el campo de tipo de error como QComboBox
    #     row = QHBoxLayout()
    #     lbl = QLabel("Tipo de error")
    #     lbl.setStyleSheet("color: white;")
    #     tipo_error_combo = QComboBox()
    #     tipo_error_combo.setStyleSheet("background-color: #444; color: white; border: 1px solid #555;")
    #     for error_type in TipoError:
    #         tipo_error_combo.addItem(error_type.value)
        
    #     # Establecer el valor actual del tipo de error
    #     current_tipo = configuracion.tipo
    #     if isinstance(current_tipo, TipoError):
    #         tipo_error_combo.setCurrentText(current_tipo.value)
    #         print(current_tipo.value)
    #     else:
    #         tipo_error_combo.setCurrentText(TipoError.NINGUNO.value)
        
    #     row.addWidget(lbl)
    #     row.addWidget(tipo_error_combo)
    #     layout.addLayout(row)
        

    #     save_button = QPushButton("Guardar cambios")
    #     save_button.setStyleSheet("background-color: #444; color: white;")
    #     save_button.clicked.connect(lambda: self.save_configuration(dialog, configuracion, layout))
    #     layout.addWidget(save_button)

    #     dialog.setLayout(layout)
    #     dialog.exec_()
        
    def find_widget(self, layout, widget_type, occurrence=1):
        counter = 0
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, widget_type):
                counter += 1
                if counter == occurrence:
                    return widget
        return None
    
    # def agregar_boton_configuracion(self, nombre, layout):
    #     if not hasattr(self, 'config_buttons_layout'):
    #         self.config_buttons_layout = QHBoxLayout()
    #         self.config_buttons_layout.setAlignment(Qt.AlignLeft)  # Alinear a la izquierda
    #         layout.insertLayout(layout.count() - 2, self.config_buttons_layout)
        
    #     botonSize = QSize(40, 40)  # Tamaño más pequeño
    #     boton_de_la_configuracion = QPushButton(nombre)
    #     boton_de_la_configuracion.setStyleSheet("""
    #         background-color: red; 
    #         color: white; 
    #         border-radius: 5px; 
    #         font-size: 10px;
    #     """)
    #     boton_de_la_configuracion.setFixedSize(botonSize)
    #     boton_de_la_configuracion.clicked.connect(lambda: self.edit_configuracion(nombre))
    #     self.config_buttons_layout.addWidget(boton_de_la_configuracion)

    #     # Verificar si necesitamos crear una nueva fila
    #     if self.config_buttons_layout.count() % 5 == 0:  # Cada 5 botones
    #         self.config_buttons_layout = QHBoxLayout()
    #         self.config_buttons_layout.setAlignment(Qt.AlignLeft)
    #         layout.insertLayout(layout.count() - 2, self.config_buttons_layout)
    

    # def save_configuration(self, dialog, configuracion, layout):
    #     for i in range(layout.count() - 1):  # -1 para ignorar el botón de guardar
    #         row = layout.itemAt(i)
    #         if isinstance(row, QHBoxLayout):
    #             widget = row.itemAt(1).widget()
    #             attr = self.get_attr_from_label(row.itemAt(0).widget().text())
                
    #             if isinstance(widget, QComboBox):  # Para el tipo de error
    #                 value = TipoError(widget.currentText())
    #             else:  # Para otros campos
    #                 value = widget.text()
                
    #             if attr == "tipo":
    #                 setattr(configuracion, attr, value)
    #             elif isinstance(value, str):
    #                 if value == "" or value.lower() == "sin límite":
    #                     if attr in ["limite_inferior", "limite_superior"]:
    #                         value = float('-inf') if attr == "limite_inferior" else float('inf')
    #                     else:
    #                         value = getattr(Configuracion(), attr)  # Usar el valor por defecto
    #                 else:
    #                     try:
    #                         value = float(value)
    #                     except ValueError:
    #                         QMessageBox.warning(dialog, "Error", f"Valor inválido para {attr}")
    #                         return
    #                 setattr(configuracion, attr, value)
        
    #     dialog.accept()


    # def get_attr_from_label(self, label):
    #     attr_map = {
    #         "Límite inferior": "limite_inferior",
    #         "Límite superior": "limite_superior",
    #         "Límite por ciclo": "limite_por_ciclo",
    #         "Error máximo": "error_maximo",
    #         "Proporción": "proporcion",
    #         "Tipo": "tipo",
    #         "Último valor": "ultimo_valor"
    #     }
    #     return attr_map.get(label, "")
        
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
        if event.button() == Qt.RightButton: # si se hace click izquierdo y se mantiene presionado "Ctrl"
            self.panning = True # activa el panning (arrastrar la pantalla)
            self.last_pan_pos = event.pos() # guarda la posición actual
            self.setCursor(Qt.ClosedHandCursor) # cambia el cursor (mano cerrada)
            event.accept()
            return
        super().mousePressEvent(event)

        scene_pos = self.mapToScene(event.pos()) # lugar del click en la escena

        if not self.microbloques: # si no hay microbloques y se hace click sobre el único botón "+", entonces se crea un microbloque 
            if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(scene_pos):
                self.create_new_microbloque(self.add_button_rect.center())
        else: 
            if event.button() == Qt.LeftButton: # si se hace click izquierdo
                for microbloque in self.microbloques: # si hay microbloques, se busca el microbloque que se seleccionó
                    if microbloque.boundingRect().contains(microbloque.mapFromScene(scene_pos)):
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
                    if microbloque.geometry().contains(scene_pos):
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
        rect = microbloque.boundingRect()
        microbloque_pos = microbloque.scenePos()
        button_width = BUTTON_SIZE
        button_height = BUTTON_SIZE
        positions = [
            ('arriba', QPointF(rect.center().x() - button_width/2, rect.top() - button_height)),
            ('abajo', QPointF(rect.center().x() - button_width/2, rect.bottom())),
            ('izquierda', QPointF(rect.left() - button_width, rect.center().y() - button_height/2)),
            ('derecha', QPointF(rect.right(), rect.center().y() - button_height/2))
        ]
        
        for direction, pos in positions:
            scene_pos = microbloque_pos + pos
            button = AddButton(scene_pos.x(), scene_pos.y(), button_width, button_height, direction)
            self.scene.addItem(button)
            self.add_buttons.append(button)

            tooltip_text = {
                'arriba': "Agregar microbloque arriba",
                'abajo': "Agregar microbloque abajo",
                'izquierda': "Agregar microbloque a la izquierda",
                'derecha': "Agregar microbloque a la derecha"
            }
            button.setToolTip(tooltip_text[direction])
    
    def hide_add_buttons(self):
        for button in self.add_buttons:
            try:
                if button.scene():
                    button.scene().removeItem(button)
            except RuntimeError:
                # El objeto ya fue eliminado, continuar con el siguiente
                pass
        self.add_buttons.clear()

    def show_add_menu(self, direction, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                border: 2px solid black;
            }
        """)
        micro_back = self.selected_microbloque.elemento_back
        parent_structures = micro_back.get_parent_structures()
        for parent in [[micro_back, 0]] + parent_structures:
            structure_name = self.get_structure_name(parent)
            action_text = self.get_descriptive_action_text(direction, structure_name)
            action = menu.addAction(action_text)
            
            # Usamos una función lambda que llama directamente a add_microbloque
            action.triggered.connect(lambda checked, m=self.selected_microbloque,d=direction, s=parent[0]: 
                QTimer.singleShot(0, lambda: self.add_microbloque(m, d, s)))
            
            action.hovered.connect(lambda s=parent, d=direction: self.show_preview(d, s))
        
        menu.setMouseTracking(True)
        menu.leaveEvent = lambda event: self.hide_preview()
        
        menu.exec_(self.mapToGlobal(self.mapFromScene(pos))) # Usamos la posición pasada como argumento para mostrar el menú

    def show_preview(self, direction, structure):
        # Si ya existe un timer, lo detenemos
        if hasattr(self, 'preview_timer'):
            self.preview_timer.stop()
        
        # Creamos un nuevo timer
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(lambda: self.show_preview_now(direction, structure))
        self.preview_timer.start(100)  # 100 ms de retraso
    
    def show_preview_now(self, direction, structure):
        if not hasattr(self, 'preview_dialog'):
            self.preview_dialog = QDialog(self) # crea un diálogo
            self.preview_dialog.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint) # le quita el borde
            layout = QVBoxLayout() # crea un layout vertical
            self.preview_label = QLabel() # crea un label
            self.description_label = QLabel() # crea otro label
            self.description_label.setWordWrap(True) # permite que el texto se ajuste al tamaño del label
            layout.addWidget(self.preview_label) # agrega el label al layout
            layout.addWidget(self.description_label) # agrega el otro label al layout
            self.preview_dialog.setLayout(layout) # agrega el layout al diálogo
        
        preview_pixmap = self.preview_images[direction].scaled(300, 175, Qt.KeepAspectRatio, Qt.SmoothTransformation) # escala la imagen para que no sea tan grande
        self.preview_label.setPixmap(preview_pixmap) # muestra la imagen en el label
        self.description_label.setText(self.get_preview_description(direction, structure)) # muestra la descripción en el otro label
        
        self.preview_dialog.adjustSize() # ajusta el tamaño del diálogo
        
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
    
    def hide_preview(self): # oculta el diálogo de vista previa
        if hasattr(self, 'preview_dialog'): # si existe el diálogo
            self.preview_dialog.hide() # lo oculta
    
    def get_descriptive_action_text(self, direction, structure_name):
        direction_text = { # textos segun direccion
            'arriba': "encima de",
            'abajo': "debajo de",
            'izquierda': "antes de",
            'derecha': "después de"
        }
        return f"Agregar {direction_text[direction]} {structure_name}" # retorna el string formateado segun la dirección y la estructura

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

            perturbacion_antes_action = QAction("Insertar perturbación antes", self)
            perturbacion_antes_action.triggered.connect(lambda: self.create_perturbacion(self.selected_microbloque, "antes", self.selected_microbloque.elemento_back))
            context_menu.addAction(perturbacion_antes_action)

            perturbacion_despues_action = QAction("Insertar perturbación después", self)
            perturbacion_despues_action.triggered.connect(lambda: self.create_perturbacion(self.selected_microbloque, "despues", self.selected_microbloque.elemento_back))
            context_menu.addAction(perturbacion_despues_action)

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
        self.scene.removeItem(microbloque)
        self.selected_microbloque = None
        self.hide_add_buttons()
        self.load_microbloques()
        self.update()

    def delete_selected_microbloques(self):
        for microbloque in self.selected_microbloques:
            self.microbloques.remove(microbloque)
            microbloque.elemento_back.borrar_elemento()
            self.scene.removeItem(microbloque)
            self.hide_add_buttons()
        self.selected_microbloques.clear() # limpio la lista de microbloques seleccionados
        self.load_microbloques()
        self.update()

    def set_seleccion_multiple(self, valor):
        self.seleccion_multiple = valor # seteamos el valor
        if not valor: # si se deselecciona la opción de seleccionar varios
            self.limpiar_seleccion() # limpiamos la selección
        else:
            if self.selected_microbloque:
                self.selected_microbloques.append(self.selected_microbloque)
                self.selected_microbloque = None
        self.update()

    def limpiar_seleccion(self):
        for microbloque in self.selected_microbloques:
            microbloque.setSeleccionado(False)
        self.selected_microbloques.clear()
        if self.selected_microbloque:
            self.selected_microbloque.setSeleccionado(False)
            self.selected_microbloque = None
        self.update()

    def add_microbloque(self, microbloque, direction, estructura_de_referencia):
        if estructura_de_referencia:
            if direction in ['arriba', 'abajo']:
                relation = direction
            elif direction == 'izquierda':
                relation = 'antes'
            else:  # derecha
                relation = 'despues'
            
            # Llamamos directamente a create_new_microbloque
            self.create_new_microbloque(microbloque.pos(), relation, estructura_de_referencia)
        
        self.hide_preview()
        
    
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
    
    def draw_grid(self):
        if len(self.grid_lines) > 0: # si ya hay lineas en la escena
            for line in self.grid_lines: # las borramos
                self.scene.removeItem(line) # primero las saco de la escena
            self.grid_lines.clear() # luego, limpio toda la lista de lineas

        rect = self.scene.sceneRect() # obtengo el rectángulo actual de la escena

        for x in range(int(rect.left()), int(rect.right()), 50): # lineas verticales
            line = QGraphicsLineItem(x, rect.top(), x, rect.bottom())
            line.setZValue(-1) # la dibujo en el fondo
            line.setPen(QPen(QColor(200, 200, 200)))
            self.scene.addItem(line)
            self.grid_lines.append(line)
        for y in range(int(rect.top()), int(rect.bottom()), 50): # lineas horizontales
            line = QGraphicsLineItem(rect.left(), y, rect.right(), y)
            line.setZValue(-1) # la dibujo en el fondo
            line.setPen(QPen(QColor(200, 200, 200)))
            self.scene.addItem(line)
            self.grid_lines.append(line)

    def limpiar_escena(self):
        self.scene.clear()
        self.grid_lines.clear()
        self.microbloques.clear()
        self.selected_microbloque = None
        self.selected_microbloques.clear()
        self.hide_add_buttons()
        self.update()
