import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QPushButton, QMainWindow, QToolBar, QWidget
from .drawing_area import DrawingArea
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QPen, QColor, QFont,QFontMetrics
from PyQt5.QtCore import Qt, QRectF


LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")
VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")
AMARILLO = QColor("#FFCC66")



class BotonSimular(QGraphicsRectItem):
    def __init__(self, pos,parent):
        self.parent = parent
        qrect = pos
        super().__init__(qrect)

        self.fondo_simular = VERDE
        self.borde_simular = VERDE.darker(150)
        self.fondo_claro = VERDE.lighter(150)
        self.color_texto = LETRA_COLOR

        self.hover_brush = QBrush(self.fondo_claro)  # Fondo aclarado al pasar el mouse
        self.default_brush = QBrush(self.fondo_simular)

        self.borde_pen = QPen(self.borde_simular, 4)  # Borde azul con grosor de 2px

        self.setBrush(self.default_brush)  # Fondo celeste suave
        self.setPen(self.borde_pen) # Borde azul con grosor de 2px
        self.setRect(qrect)  # Establecer el tamaño del rectángulo

        self.text = "SIMULAR | "
        self.icon = "\u25B6"

        self.font = QFont("Arial", 32, QFont.Bold)  # Estilo del texto
        self.font_icon = QFont("Arial", 64, QFont.Bold)  # Estilo del texto
        self.setAcceptHoverEvents(True)  


        

    def paint(self, painter, option, widget=None):
        # Dibujar un rectángulo con esquinas redondeadas
        painter.setRenderHint(painter.Antialiasing)
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Dibujar el texto centrado en el rectángulo
        painter.setFont(self.font)
        painter.setPen(self.color_texto)  # Color del texto
        text_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, self.text)
        painter.drawText(text_rect, Qt.AlignLeft, self.text)

        # Dibujar el icono a la derecha del texto
        painter.setFont(self.font_icon)
        icon_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, self.icon)
        icon_rect.moveLeft(text_rect.right() + 5)  # Mover el icono a la derecha del texto con un margen de 5px
        painter.drawText(icon_rect, Qt.AlignLeft, self.icon)
    

    def hoverEnterEvent(self, event):
        # Cambia el fondo al pasar el mouse sobre el rectángulo
        self.setBrush(self.hover_brush)
        self.update()  # Actualizar el rectángulo para que se vea el cambio

    def hoverLeaveEvent(self, event):
        # Restaura el fondo original cuando el mouse sale del rectángulo
        self.setBrush(self.default_brush)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Simular")
            self.parent.simular_button()

    def updateText(self):
        # Actualizar el texto del rectángulo
        self.text = self.modelo.nombre
        self.update()  # Actualizar el rectángulo para redibujar

    def update_nombre(self):
        self.updateText()
"""
    def click(self):
        self.ventana = QMainWindow()
        self.ventana.setWindowTitle(self.modelo.nombre)
        
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.ventana.setGeometry(screen)
        self.ventana.showMaximized()
        
        self.drawing_area = DrawingArea(self, self.ventana)
        self.ventana.setCentralWidget(self.drawing_area)
        
        self.init_tool_bar()
        self.ventana.show()
        self.ventana.setStyleSheet("background-color: #F1FAEE;")  # Color azul claro
        # Ruta de la imagen del logo
        path =  os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ventana.setWindowIcon(icon)
        
        QTimer.singleShot(100, self.drawing_area.load_microbloques)
"""