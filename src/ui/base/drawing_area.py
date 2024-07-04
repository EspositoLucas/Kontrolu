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
    
#     def load_microbloques(self):
#         for microbloque in self.microbloques:
#                 microbloque.deleteLater() # elimina cada elemento
#         self.microbloques.clear() # vacia la lista de microbloques
#         self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
#         #self.print_topologia(self.modelo.topologia)
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
#         altura_total = sum(hijo.alto() for hijo in paralelo.hijos) # la altura total de los microbloques es la suma de sus alturas (porque se dibujan uno debajo del otro)
#         vertical_margin = 50  # TODO: Modificar el valor segun convenga (es el margen vertical entre microbloques)
#         altura_total += (len(paralelo.hijos) - 1) * vertical_margin # se agrega el margen vertical entre microbloques

#         y_actual = posicion_inicial.y() - altura_total / 2 # empiezo desde la mitad de la altura total
#         for hijo in paralelo.hijos:
#             centro_del_hijo = y_actual + hijo.alto() / 2 # centro del microbloque
#             posicion_del_hijo = QPointF(posicion_inicial.x(), centro_del_hijo)
#             self.dibujar_topologia(hijo, posicion_del_hijo)
#             y_actual += hijo.alto() + vertical_margin # la posicion del siguiente será más abajo

#     def create_microbloque(self, microbloque_back, pos):
#         microbloque = Microbloque(self, microbloque_back)
#         microbloque.setParent(self)
#         microbloque.setPos(pos)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         self.update()
    
#     def clear_all(self):
#         if self.microbloques:
#             for microbloque in self.microbloques:
#                 microbloque.deleteLater() # elimina cada elemento
#             self.microbloques.clear() # vacia la lista de microbloques
        
#         self.modelo.reset_topologia() # si limpiamos todo, deberíamos limpiar también el arbol del macrobloque
#         self.load_microbloques() # resetea la vista
#         self.update()
    
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         painter = QPainter(self)
#         self.draw_io_blocks(painter)
        
#         if not self.microbloques:
#             self.draw_empty_connection(painter)
#         else:
#            punto_final = self.draw_connections(painter, self.modelo.topologia, QPointF(90, self.height() / 2))
#            self.draw_final_connection(painter, punto_final) # punto_final es el punto de salida de la última conexión

#     def draw_final_connection(self, painter, start_point):
#         if start_point is None:
#             return

#         end_point = QPointF(self.width() - 170, self.height() / 2) # end_point es el lugar donde está el bloque de salida
#         painter.setPen(QPen(Qt.black, 2))
#         painter.drawLine(start_point, end_point)

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
    
#     def draw_connections(self, painter, topologia, punto_de_partida, is_parallel=False):
#         if punto_de_partida is None:
#             return None

#         painter.setPen(QPen(Qt.black, 2)) # configura el color y grosor de la línea
        
#         if isinstance(topologia, TopologiaSerie):
#             return self.draw_serie_connections(painter, topologia, punto_de_partida)
#         elif isinstance(topologia, TopologiaParalelo):
#             return self.draw_paralelo_connections(painter, topologia, punto_de_partida)
#         elif isinstance(topologia, MicroBloque):
#             return self.draw_microbloque_connection(painter, topologia, punto_de_partida, is_parallel)
#         else:
#             return punto_de_partida

#     def draw_serie_connections(self, painter, serie, punto_inicial):
#         """
#         Dibuja las conexiones de una serie de microbloques
#         @return el punto final de la serie
#         """
#         if punto_inicial is None:
#             return None

#         punto_actual = punto_inicial
#         for hijo in serie.hijos:
#             # para cada elemento de la serie, llama a draw_connections para que dibuje sus componentes (si las hubiera)
#             punto_final = self.draw_connections(painter, hijo, punto_actual) 
#             punto_actual = punto_final

#         return punto_actual

#     def draw_paralelo_connections(self, painter, paralelo, punto_inicial):
#         if punto_inicial is None:
#             return None

#         # Calcular punto de bifurcación
#         comienzo_de_rama = QPointF(punto_inicial.x() + 20, punto_inicial.y())  # 20 pixels antes del bloque (es el margen antes de hacer la bifurcación)
#         altura_total = sum(hijo.alto() for hijo in paralelo.hijos) # idem que en dibujar_paralelo
#         vertical_margin = 50 # idem que en dibujar_paralelo
#         altura_total += (len(paralelo.hijos) - 1) * vertical_margin # idem que en dibujar_paralelo
        
#         # Dibujar línea horizontal antes de la bifurcación
#         painter.drawLine(punto_inicial, comienzo_de_rama)
        
#         # Dibujar conexiones para cada rama
#         y_actual = punto_inicial.y() - altura_total / 2
#         puntos_finales = []
#         for hijo in paralelo.hijos:
#             punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2) # deja igual la "x" y pone la "y" en el centro del microbloque
#             painter.drawLine(comienzo_de_rama, punto_final_rama_vertical)  # Línea vertical de bifurcación
#             punto_final_rama_actual = self.draw_connections(painter, hijo, punto_final_rama_vertical, True) # partiendo desde el extremo de la linea vertical de bifurcacion, comienza a dibujar lo que sigue
#             if punto_final_rama_actual is not None:
#                 puntos_finales.append(punto_final_rama_actual) # se va guardando los puntos finales de cada rama del paralelo
#             y_actual += hijo.alto() + vertical_margin # incorpora el margen vertical
        
#         if not puntos_finales: # querria decir que no dibujo nada en los paralelos (no creo que pase nunca, pero por las dudas lo dejo)
#             return punto_inicial

#         margen_horizontal_final = 30 # margen horizontal para salir del paralelo
#         # Encontrar el punto final más a la derecha
#         max_x = max(point.x() for point in puntos_finales) + margen_horizontal_final # esto está por si una rama quedó "mas larga horizontalmente" que la otra
         
#         # Dibujar líneas horizontales para reconectar las ramas
#         for end_point in puntos_finales:
#             painter.drawLine(end_point, QPointF(max_x, end_point.y())) # le sumamos 20 para tener una linea horizontal (al salir del microbloque) antes de reconectar
        
#         # Punto de reconexión
#         punto_de_reconexion = QPointF(max_x, punto_inicial.y())
        
#         # Dibujar líneas verticales para reconectar (En realidad es una unica linea desde una rama a la otra)
#         # QPointF(max_x + 20, puntos_finales[0].y()) --> es para la rama de arriba (indice 0 es el primer elemento de una lista)
#         # QPointF(max_x + 20, puntos_finales[-1].y()) --> es para la rama de abajo (indice -1 es el último elemento de una lista)
#         painter.drawLine(QPointF(max_x, puntos_finales[0].y()), QPointF(max_x, puntos_finales[-1].y()))
        
#         # Dibujar línea horizontal final (para salir de la estructura paralelo)
#         painter.drawLine(QPointF(max_x, punto_inicial.y()), punto_de_reconexion)
        
#         # retorna el punto de reconexión porque es el punto "mas a la derecha" de la estructura paralelo
#         return punto_de_reconexion 

#     def draw_microbloque_connection(self, painter, microbloque, punto_inicial, es_paralelo):
#         # busca en la lista de microbloques de la drawing_area, el microbloque que queremos conectar
#         for mb in self.microbloques:
#             if mb.elemento_back == microbloque: # compara su elemento back
#                 if es_paralelo:
#                     punto_final = QPointF(mb.pos().x(), punto_inicial.y()) # deja igual el "x", y el "y" lo deja igual respecto a de la rama paralela en donde está
#                 else:
#                     punto_final = mb.pos() + QPointF(0, mb.height() / 2) # mb.pos() = da la esquina superior izquierda del microbloque ||| + QPointF(0, mb.height() / 2) = mueve el punto hacia abajo hasta la mitad de la altura del microbloque.
                
#                 # punto_final seria el punto en donde va a llegar la flecha que proviene del microbloque anterior (punto medio izquierdo del microbloque actual)

#                 if punto_inicial is not None and punto_final is not None:
#                     painter.drawLine(punto_inicial, punto_final) # dibuja la linea
                
#                 return mb.pos() + QPointF(mb.width(), mb.height() / 2) # retorna un punto que representa la mitad del lado derecho del microbloque. Este punto se usará como punto de inicio para la siguiente conexión.
        
#         # Si no se encuentra el microbloque, retornamos el punto de inicio --> Si no encuentra el microbloque en la lista, simplemente retorna el punto_inicial
#         return punto_inicial

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

#     def print_topologia(self, topologia, indent=0):
#         """
#         Imprime el arbol del macrobloque por consola
#         """
#         space = ' ' * (indent * 2)
#         if isinstance(topologia, TopologiaSerie):
#             print(f"{space}Serie:")
#             for hijo in topologia.hijos:
#                 self.print_topologia(hijo, indent + 1)
#         elif isinstance(topologia, TopologiaParalelo):
#             print(f"{space}Paralelo:")
#             for hijo in topologia.hijos:
#                 self.print_topologia(hijo, indent + 1)
#         elif isinstance(topologia, MicroBloque):
#             print(f"{space}MicroBloque: {topologia.nombre}")













# from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QSizePolicy
# from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QCursor
# from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPoint
# from .micro_bloque import Microbloque
# from .latex_editor import LatexEditor
# from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

# class DrawingArea(QScrollArea):
#     def __init__(self, parent=None, modelo=None):
#         super().__init__(parent)
#         self.canvas = Canvas(modelo)
#         self.setWidget(self.canvas)
#         self.setWidgetResizable(True)
#         self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         self.canvas.adjust_size()

# class Canvas(QWidget):
#     def __init__(self, modelo=None):
#         super().__init__()
#         self.microbloques = []
#         self.selected_microbloque = None
#         self.modelo = modelo
#         self.creating_microbloque = False
#         self.new_microbloque_config = {}
#         self.add_buttons = []
#         self.button_size = 20
#         self.add_button_after_parallel = None
#         self.init_ui()
        
#     def init_ui(self):
#         self.setStyleSheet("background-color: white;")
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.setMinimumSize(2000, 1000)  # Tamaño inicial grande para permitir scroll
    
#     def adjust_size(self):
#         max_x = max([mb.pos().x() + mb.width() for mb in self.microbloques], default=0)
#         max_y = max([mb.pos().y() + mb.height() for mb in self.microbloques], default=0)
#         self.setMinimumSize(max(self.parent().width(), max_x + 200), max(self.parent().height(), max_y + 200))

#     def load_microbloques(self):
#         for microbloque in self.microbloques:
#             microbloque.deleteLater()
#         self.microbloques.clear()
#         self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
#         self.adjust_size()
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
#         for hijo in serie.hijos:
#             posicion_actual = self.dibujar_topologia(hijo, posicion_actual)
#             posicion_actual.setX(posicion_actual.x() + 200)
#         return posicion_actual

#     def dibujar_paralelo(self, paralelo, posicion_inicial):
#         altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
#         vertical_margin = 50
#         altura_total += (len(paralelo.hijos) - 1) * vertical_margin

#         y_actual = posicion_inicial.y() - altura_total / 2
#         max_x = posicion_inicial.x()
#         for hijo in paralelo.hijos:
#             centro_del_hijo = y_actual + hijo.alto() / 2
#             posicion_del_hijo = QPointF(posicion_inicial.x(), centro_del_hijo)
#             punto_final = self.dibujar_topologia(hijo, posicion_del_hijo)
#             max_x = max(max_x, punto_final.x())
#             y_actual += hijo.alto() + vertical_margin

#         return QPointF(max_x, posicion_inicial.y())

#     def create_microbloque(self, microbloque_back, pos):
#         microbloque = Microbloque(self, microbloque_back)
#         microbloque.setParent(self)
#         microbloque.setPos(pos)
#         self.microbloques.append(microbloque)
#         microbloque.show()
#         return QPointF(pos.x() + microbloque.width(), pos.y() + microbloque.height() / 2)
    
#     def clear_all(self):
#         for microbloque in self.microbloques:
#             microbloque.deleteLater()
#         self.microbloques.clear()
#         self.modelo.reset_topologia()
#         self.load_microbloques()
#         self.update()
#         self.hide_add_buttons()
    
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         painter = QPainter(self)
#         self.draw_io_blocks(painter)
        
#         if not self.microbloques:
#             self.draw_empty_connection(painter)
#         else:
#            punto_final = self.draw_connections(painter, self.modelo.topologia, QPointF(90, self.height() / 2))
#            self.draw_final_connection(painter, punto_final)

#     def draw_final_connection(self, painter, start_point):
#         if start_point is None:
#             return

#         end_point = QPointF(self.width() - 170, self.height() / 2)
#         painter.setPen(QPen(Qt.black, 2))
#         painter.drawLine(start_point, end_point)

#         # Dibujar el botón "+" para agregar bloques en serie después del paralelo
#         if isinstance(self.modelo.topologia, TopologiaParalelo) or (isinstance(self.modelo.topologia, TopologiaSerie) and isinstance(self.modelo.topologia.hijos[-1], TopologiaParalelo)):
#             button_pos = QPointF((start_point.x() + end_point.x()) / 2, start_point.y())
#             self.draw_add_button_after_parallel(painter, button_pos)

#     def draw_add_button_after_parallel(self, painter, pos):
#         button_size = 20
#         button_rect = QRectF(pos.x() - button_size/2, pos.y() - button_size/2, button_size, button_size)
#         painter.setBrush(QBrush(Qt.white))
#         painter.drawEllipse(button_rect)
#         painter.drawText(button_rect, Qt.AlignCenter, "+")
#         self.add_button_after_parallel_rect = button_rect
        

#     def draw_empty_connection(self, painter):
#         painter.setPen(QPen(Qt.black, 2))
#         entrada = QPointF(90, self.height() / 2)
#         salida = QPointF(self.width() - 170, self.height() / 2)
#         painter.drawLine(entrada, salida)
        
#         center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
#         self.draw_add_button(painter, center)
        
#     def draw_add_button(self, painter, pos):
#         button_size = 20
#         button_rect = QRectF(pos.x() - button_size/2, pos.y() - button_size/2, button_size, button_size)
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
#         painter.drawText(QRectF(50, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Entrada")
        
#         painter.drawEllipse(QPointF(centro_salida_x, centro_y), radio, radio)
#         painter.drawText(QRectF(self.width()-209, self.height() / 2 - 30, 80, 60), Qt.AlignCenter, "Salida")
    
#     def draw_connections(self, painter, topologia, punto_de_partida, is_parallel=False):
#         if punto_de_partida is None:
#             return None

#         painter.setPen(QPen(Qt.black, 2))
        
#         if isinstance(topologia, TopologiaSerie):
#             return self.draw_serie_connections(painter, topologia, punto_de_partida)
#         elif isinstance(topologia, TopologiaParalelo):
#             return self.draw_paralelo_connections(painter, topologia, punto_de_partida)
#         elif isinstance(topologia, MicroBloque):
#             return self.draw_microbloque_connection(painter, topologia, punto_de_partida, is_parallel)
#         else:
#             return punto_de_partida

#     def draw_serie_connections(self, painter, serie, punto_inicial):
#         punto_actual = punto_inicial
#         for hijo in serie.hijos:
#             punto_final = self.draw_connections(painter, hijo, punto_actual) 
#             punto_actual = punto_final

#         return punto_actual

#     def draw_paralelo_connections(self, painter, paralelo, punto_inicial):
#         if punto_inicial is None:
#             return None

#         comienzo_de_rama = QPointF(punto_inicial.x() + 20, punto_inicial.y())
#         altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
#         vertical_margin = 50
#         altura_total += (len(paralelo.hijos) - 1) * vertical_margin
        
#         painter.drawLine(punto_inicial, comienzo_de_rama)
        
#         y_actual = punto_inicial.y() - altura_total / 2
#         puntos_finales = []
#         for hijo in paralelo.hijos:
#             punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2)
#             painter.drawLine(comienzo_de_rama, punto_final_rama_vertical)
#             punto_final_rama_actual = self.draw_connections(painter, hijo, punto_final_rama_vertical, True)
#             if punto_final_rama_actual is not None:
#                 puntos_finales.append(punto_final_rama_actual)
#             y_actual += hijo.alto() + vertical_margin
        
#         if not puntos_finales:
#             return punto_inicial

#         margen_horizontal_final = 30
#         max_x = max(point.x() for point in puntos_finales) + margen_horizontal_final
         
#         for end_point in puntos_finales:
#             painter.drawLine(end_point, QPointF(max_x, end_point.y()))
        
#         punto_de_reconexion = QPointF(max_x, punto_inicial.y())
        
#         painter.drawLine(QPointF(max_x, puntos_finales[0].y()), QPointF(max_x, puntos_finales[-1].y()))
        
#         painter.drawLine(QPointF(max_x, punto_inicial.y()), punto_de_reconexion)
        
#         return punto_de_reconexion 

#     def draw_microbloque_connection(self, painter, microbloque, punto_inicial, es_paralelo):
#         for mb in self.microbloques:
#             if mb.elemento_back == microbloque:
#                 if es_paralelo:
#                     punto_final = QPointF(mb.pos().x(), punto_inicial.y())
#                 else:
#                     punto_final = mb.pos() + QPointF(0, mb.height() / 2)
                
#                 if punto_inicial is not None and punto_final is not None:
#                     painter.drawLine(punto_inicial, punto_final)
                
#                 return mb.pos() + QPointF(mb.width(), mb.height() / 2)
        
#         return punto_inicial
    
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
#             new_microbloque = MicroBloque(nombre, color, funcion_transferencia, {}, self.modelo.topologia)

#             if relation == "serie_after_parallel":
#                 # Asegurarse de que el nuevo microbloque se agregue al final de la serie principal
#                 if isinstance(self.modelo.topologia, TopologiaSerie):
#                     self.modelo.topologia.hijos.append(new_microbloque)
#                 else:
#                     nueva_serie = TopologiaSerie()
#                     nueva_serie.hijos = [self.modelo.topologia, new_microbloque]
#                     self.modelo.topologia = nueva_serie
#             elif reference_microbloque and relation == "arriba":
#                 reference_microbloque.elemento_back.agregar_arriba(new_microbloque)
#             elif reference_microbloque and relation == "abajo":
#                 reference_microbloque.elemento_back.agregar_abajo(new_microbloque)
#             elif reference_microbloque and relation == "antes":
#                 reference_microbloque.elemento_back.agregar_antes(new_microbloque)
#             elif reference_microbloque and relation == "despues":
#                 reference_microbloque.elemento_back.agregar_despues(new_microbloque)
#             else:
#                 self.modelo.topologia.agregar_elemento(new_microbloque)
            
#             self.load_microbloques()
#             self.update()
#             self.hide_add_buttons()

#     def select_color(self, button):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             button.setStyleSheet(f"background-color: {color.name()};")
#             button.setProperty("selected_color", color)
            
#     def mousePressEvent(self, event):
#         super().mousePressEvent(event)

#         if not self.microbloques:
#             if hasattr(self, 'add_button_rect') and self.add_button_rect.contains(event.pos()):
#                 self.create_new_microbloque(self.add_button_rect.center())
#         else:
#             for microbloque in self.microbloques:
#                 if microbloque.geometry().contains(event.pos()):
#                     self.selected_microbloque = microbloque
#                     self.show_add_buttons(microbloque)
#                     break
#             else:
#                 if hasattr(self, 'add_button_after_parallel_rect') and self.add_button_after_parallel_rect.contains(event.pos()):
#                     self.create_new_microbloque(self.add_button_after_parallel_rect.center(), "serie_after_parallel")
#                 else:
#                     self.selected_microbloque = None
#                     self.hide_add_buttons()
        
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
#         if self.selected_microbloque:
#             if direction in ['arriba', 'abajo']:
#                 relation = direction
#             elif direction == 'izquierda':
#                 relation = 'antes'
#             else:  # derecha
#                 relation = 'despues'
            
#             self.create_new_microbloque(self.selected_microbloque.pos(), relation, self.selected_microbloque)

#     def contextMenuEvent(self, event):
#         for microbloque in self.microbloques:
#             if microbloque.geometry().contains(event.pos()):
#                 menu = QMenu(self)
#                 delete_action = menu.addAction("Eliminar")
#                 action = menu.exec_(self.mapToGlobal(event.pos()))
#                 if action == delete_action:
#                     self.delete_microbloque(microbloque)
#                 break

#     def delete_microbloque(self, microbloque):
#         self.microbloques.remove(microbloque)
#         self.modelo.topologia.borrar_elemento(microbloque.elemento_back)
#         microbloque.deleteLater()
#         self.load_microbloques()
#         self.update()

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         self.adjust_size()




from PyQt5.QtWidgets import QWidget, QMenu, QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QCursor
from PyQt5.QtCore import Qt, pyqtSignal, QPointF, QRectF, QPoint
from .micro_bloque import Microbloque
from .latex_editor import LatexEditor
from back.topologia.topologia_serie import TopologiaSerie, TopologiaParalelo, MicroBloque

class DrawingArea(QScrollArea):
    def __init__(self, parent=None, modelo=None):
        super().__init__(parent)
        self.canvas = Canvas(modelo)
        self.setWidget(self.canvas)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.canvas.adjust_size()

class Canvas(QWidget):
    def __init__(self, modelo=None):
        super().__init__()
        self.microbloques = []
        self.selected_microbloque = None
        self.modelo = modelo
        self.creating_microbloque = False
        self.new_microbloque_config = {}
        self.add_buttons = []
        self.button_size = 20
        self.add_buttons_after_parallel = []
        self.init_ui()
        
    def init_ui(self):
        self.setStyleSheet("background-color: white;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(2000, 1000)  # Tamaño inicial grande para permitir scroll
    
    def adjust_size(self):
        max_x = max([mb.pos().x() + mb.width() for mb in self.microbloques], default=0)
        max_y = max([mb.pos().y() + mb.height() for mb in self.microbloques], default=0)
        self.setMinimumSize(max(self.parent().width(), max_x + 200), max(self.parent().height(), max_y + 200))

    def load_microbloques(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.dibujar_topologia(self.modelo.topologia, QPointF(150, self.height() / 2))
        self.adjust_size()
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
        for hijo in serie.hijos:
            posicion_actual = self.dibujar_topologia(hijo, posicion_actual)
            posicion_actual.setX(posicion_actual.x() + 200)
        return posicion_actual

    def dibujar_paralelo(self, paralelo, posicion_inicial):
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
        vertical_margin = 50
        altura_total += (len(paralelo.hijos) - 1) * vertical_margin

        y_actual = posicion_inicial.y() - altura_total / 2
        max_x = posicion_inicial.x()
        for hijo in paralelo.hijos:
            centro_del_hijo = y_actual + hijo.alto() / 2
            posicion_del_hijo = QPointF(posicion_inicial.x(), centro_del_hijo)
            punto_final = self.dibujar_topologia(hijo, posicion_del_hijo)
            max_x = max(max_x, punto_final.x())
            y_actual += hijo.alto() + vertical_margin

        return QPointF(max_x, posicion_inicial.y())

    def create_microbloque(self, microbloque_back, pos):
        microbloque = Microbloque(self, microbloque_back)
        microbloque.setParent(self)
        microbloque.setPos(pos)
        self.microbloques.append(microbloque)
        microbloque.show()
        return QPointF(pos.x() + microbloque.width(), pos.y() + microbloque.height() / 2)
    
    def clear_all(self):
        for microbloque in self.microbloques:
            microbloque.deleteLater()
        self.microbloques.clear()
        self.modelo.reset_topologia()
        self.load_microbloques()
        self.update()
        self.hide_add_buttons()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
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
        entrada = QPointF(90, self.height() / 2)
        salida = QPointF(self.width() - 170, self.height() / 2)
        painter.drawLine(entrada, salida)
        
        center = QPointF((entrada.x() + salida.x()) / 2, self.height() / 2)
        self.draw_add_button(painter, center)
        
    def draw_add_button(self, painter, pos):
        button_size = 20
        button_rect = QRectF(pos.x() - button_size/2, pos.y() - button_size/2, button_size, button_size)
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
        punto_actual = punto_inicial
        for hijo in serie.hijos:
            punto_final = self.draw_connections(painter, hijo, punto_actual) 
            if isinstance(hijo, TopologiaParalelo):
                self.draw_add_button_after_parallel(painter, punto_final)
            punto_actual = punto_final

        return punto_actual

    def draw_paralelo_connections(self, painter, paralelo, punto_inicial):
        if punto_inicial is None:
            return None

        comienzo_de_rama = QPointF(punto_inicial.x() + 20, punto_inicial.y())
        altura_total = sum(hijo.alto() for hijo in paralelo.hijos)
        vertical_margin = 50
        altura_total += (len(paralelo.hijos) - 1) * vertical_margin
        
        painter.drawLine(punto_inicial, comienzo_de_rama)
        
        y_actual = punto_inicial.y() - altura_total / 2
        puntos_finales = []
        for hijo in paralelo.hijos:
            punto_final_rama_vertical = QPointF(comienzo_de_rama.x(), y_actual + hijo.alto() / 2)
            painter.drawLine(comienzo_de_rama, punto_final_rama_vertical)
            punto_final_rama_actual = self.draw_connections(painter, hijo, punto_final_rama_vertical, True)
            if punto_final_rama_actual is not None:
                puntos_finales.append(punto_final_rama_actual)
            y_actual += hijo.alto() + vertical_margin
        
        if not puntos_finales:
            return punto_inicial

        margen_horizontal_final = 30
        max_x = max(point.x() for point in puntos_finales) + margen_horizontal_final
         
        for end_point in puntos_finales:
            painter.drawLine(end_point, QPointF(max_x, end_point.y()))
        
        punto_de_reconexion = QPointF(max_x, punto_inicial.y())
        
        painter.drawLine(QPointF(max_x, puntos_finales[0].y()), QPointF(max_x, puntos_finales[-1].y()))
        
        painter.drawLine(QPointF(max_x, punto_inicial.y()), punto_de_reconexion)
        
        return punto_de_reconexion 

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
    
    def draw_add_button_after_parallel(self, painter, pos):
        button_size = 20
        button_rect = QRectF(pos.x() - button_size/2, pos.y() - button_size/2, button_size, button_size)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(button_rect)
        painter.drawText(button_rect, Qt.AlignCenter, "+")
        self.add_buttons_after_parallel.append(button_rect)

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

            if relation == "serie_after_parallel":
                self.agregar_microbloque_despues_de_paralelo(new_microbloque)
            elif reference_microbloque and relation == "arriba":
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

    def agregar_microbloque_despues_de_paralelo(self, new_microbloque):
        def agregar_a_serie_padre(topologia):
            if isinstance(topologia, TopologiaSerie):
                for i, hijo in enumerate(topologia.hijos):
                    if isinstance(hijo, TopologiaParalelo):
                        topologia.hijos.insert(i + 1, new_microbloque)
                        return True
                    elif isinstance(hijo, TopologiaSerie) or isinstance(hijo, TopologiaParalelo):
                        if agregar_a_serie_padre(hijo):
                            return True
            return False

        if not agregar_a_serie_padre(self.modelo.topologia):
            # Si no se encuentra una serie padre, se agrega al final de la topología principal
            if isinstance(self.modelo.topologia, TopologiaSerie):
                self.modelo.topologia.hijos.append(new_microbloque)
            else:
                nueva_serie = TopologiaSerie()
                nueva_serie.hijos = [self.modelo.topologia, new_microbloque]
                self.modelo.topologia = nueva_serie

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
                for button_rect in self.add_buttons_after_parallel:
                    if button_rect.contains(event.pos()):
                        self.create_new_microbloque(button_rect.center(), "serie_after_parallel")
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
            else:  # derecha
                relation = 'despues'
            
            self.create_new_microbloque(self.selected_microbloque.pos(), relation, self.selected_microbloque)

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
        self.modelo.topologia.borrar_elemento(microbloque.elemento_back)
        microbloque.deleteLater()
        self.load_microbloques()
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_size()