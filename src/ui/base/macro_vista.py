import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar, QWidget
from .drawing_area import DrawingArea
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor, QFont,QFontMetrics
from PyQt5.QtCore import Qt, QRectF
from ..base.boton_circulo import QGraphicCircleItem



class MacroVista(QGraphicsRectItem):
    def __init__(self, elementoBack,  pos):
        qrect = pos
        super().__init__(qrect)
        self.modelo = elementoBack
        self.default_brush = QBrush(QColor("#A8DADC"))  # Fondo celeste suave
        self.hover_brush = QBrush(QColor("#F1FAEE"))  # Fondo aclarado al pasar el mouse
        self.setBrush(QBrush(QColor("#A8DADC")))  # Fondo celeste suave
        self.setPen(QPen(QColor("#457B9D"), 4))  # Borde azul con grosor de 2px
        self.setRect(qrect)  # Establecer el tamaño del rectángulo

        # Agregar texto centrado
        # Texto que se mostrará en el rectángulo
        self.text = self.modelo.nombre
        self.font = QFont("Arial", 16, QFont.Bold)  # Estilo del texto
        self.setAcceptHoverEvents(True)  


        

    def paint(self, painter, option, widget=None):
        # Dibujar un rectángulo con esquinas redondeadas
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Dibujar el texto centrado en el rectángulo
        painter.setFont(self.font)
        painter.setPen(QColor("#2B2D42"))  # Color del texto
        text_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, self.text)
        painter.drawText(text_rect, Qt.AlignCenter, self.text)
    

    def hoverEnterEvent(self, event):
        # Cambia el fondo al pasar el mouse sobre el rectángulo
        self.setBrush(self.hover_brush)
        self.update()  # Actualizar el rectángulo para que se vea el cambio

    def hoverLeaveEvent(self, event):
        # Restaura el fondo original cuando el mouse sale del rectángulo
        self.setBrush(self.default_brush)
        self.update()

    def updateText(self):
        # Actualizar el texto del rectángulo
        self.text = self.modelo.nombre
        self.update()  # Actualizar el rectángulo para redibujar

    def update_nombre(self):
        self.updateText()
    
    def click(self):
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle(self.modelo.nombre)
        
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.ventana.setGeometry(screen)
        self.ventana.showMaximized()
        
        self.drawing_area = DrawingArea(self, self.ventana)
        self.ventana.setCentralWidget(self.drawing_area)
        
        #self.init_tool_bar()
        self.ventana.show()

        self.ventana.setStyleSheet("background-color: #F1FAEE;")  # Color azul claro
        # Ruta de la imagen del logo
        path =  os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ventana.setWindowIcon(icon)
        
        QTimer.singleShot(100, self.drawing_area.load_microbloques)
        
    def init_tool_bar(self):
        
        return
        toolbar = QToolBar("Herramientas", self.ventana)
        self.ventana.addToolBar(Qt.LeftToolBarArea, toolbar)

        button_style = """
            QPushButton {
                background-color: #808080; /* Color gris */
                color: white;
                font-size: 14px;
                padding: 5px;
                border-radius: 3px;
            }

            QPushButton:hover {
                background-color: #696969; /* Un gris más oscuro para el hover */
            }
            """
        
        # Botón de borrar todo
        delete_button = QPushButton('Borrar todo', self.drawing_area)
        delete_button.clicked.connect(self.drawing_area.clear_all)
        delete_button.setStyleSheet(button_style)
        toolbar.addWidget(delete_button)

        # Espaciador
        spacer = QWidget()
        spacer.setFixedSize(50, 5)  # Ajusta el tamaño del espaciador (ancho x alto)
        spacer.setStyleSheet("background-color: #333;")  # Establece el color de fondo
        toolbar.addWidget(spacer)

        # Botón de seleccionar varios
        self.seleccion_multiple = QPushButton('Seleccionar varios', self.drawing_area)
        self.seleccion_multiple.setCheckable(True)
        self.seleccion_multiple.toggled.connect(self.drawing_area.set_seleccion_multiple)
        self.seleccion_multiple.setStyleSheet(button_style + """
        QPushButton:checked {
            background-color: #505050; /* Color gris más oscuro cuando está seleccionado */
        }
        """)
        toolbar.addWidget(self.seleccion_multiple)

        # Espaciador
        spacer = QWidget()
        spacer.setFixedSize(50, 5)  # Ajusta el tamaño del espaciador (ancho x alto)
        spacer.setStyleSheet("background-color: #333;")  # Establece el color de fondo
        toolbar.addWidget(spacer)

        # Botón de seleccionar varios
        self.edicion_json = QPushButton('Edicion Json', self.drawing_area)
        self.edicion_json.clicked.connect(self.drawing_area.vista_json)
        self.edicion_json.setStyleSheet(button_style)
        toolbar.addWidget(self.edicion_json)

        # Espaciador
        spacer = QWidget()
        spacer.setFixedSize(50, 5)  # Ajusta el tamaño del espaciador (ancho x alto)
        spacer.setStyleSheet("background-color: #333;")  # Establece el color de fondo
        toolbar.addWidget(spacer)

        # Boton de ayuda
        help_button = QPushButton('Ayuda',self.drawing_area)
        help_button.clicked.connect(self.drawing_area.show_help)
        help_button.setStyleSheet(button_style + """
        QPushButton {
                background-color: #808080; /* Color gris */
                color: white;
                font-size: 14px;
                padding: 5px;
                border-radius: 3px;
            }

            QPushButton:hover {
                background-color: #696969; /* Un gris más oscuro para el hover */
            }
        """)
        help_button.setToolTip("Mostrar ayuda")
        toolbar.addWidget(help_button)

        toolbar.setStyleSheet("QToolBar { background-color: #333; }")  # Establece el color de fondo de la barra de herramientas

    def configure_microbloque(self):
        self.drawing_area.create_new_microbloque()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click()

    def hoverMoveEvent(self, event):
        # Cambia el cursor a una mano al pasar el mouse sobre el rectángulo
        self.setCursor(Qt.PointingHandCursor)