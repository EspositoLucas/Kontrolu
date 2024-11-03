import os
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import  QMainWindow,  QWidget
from .drawing_area import DrawingArea
from PyQt5.QtWidgets import  QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt
from .floating_buttons import FloatingButtons

CELESTE_SUAVE = QColor("#A8DADC")
AZUL = QColor("#457B9D")
ACLARADO = QColor("#F1FAEE")

VERDE_FONDO = QColor("#D5E8D4")       # Fondo verde pastel suave
VERDE_BORDE_OSCURO = QColor("#6B9D8F")  # Verde oscuro para bordes
VERDE_HOVER = QColor("#BCE2D0")         # Verde intermedio para el efecto hover



class MacroVista(QGraphicsRectItem):
    def __init__(self, elementoBack=None,  pos=100,padre=None,nombre=None):
        self.clickeable = True
        qrect = pos
        self.padre = padre
        super().__init__(qrect)
        self.modelo = elementoBack
        self.default_brush = QBrush(QColor("#A8DADC"))  # Fondo celeste suave
        self.hover_brush = QBrush(QColor("#F1FAEE"))  # Fondo aclarado al pasar el mouse
        self.borde = QPen(QColor("#457B9D"), 4)  # Borde azul con grosor de 2px
        if elementoBack==None:
            self.nombre = nombre
            self.clickeable = False
            self.default_brush = QBrush(VERDE_FONDO)  # Fondo verde pastel suave
            self.hover_brush = QBrush(VERDE_HOVER)
            self.borde = QPen(VERDE_BORDE_OSCURO, 4)


        self.setBrush(self.default_brush)  # Fondo celeste suave
        self.setPen(self.borde)  # Borde azul con grosor de 2px
        self.setRect(qrect)  # Establecer el tamaño del rectángulo

        # Agregar texto centrado
        # Texto que se mostrará en el rectángulo
        if self.modelo == None:
            self.text = self.nombre
        else:
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
        if self.modelo == None:
            self.text = self.modelo.nombre
        else:
            self.text = self.nombre
        self.update()  # Actualizar el rectángulo para redibujar

    def update_nombre(self):
        self.updateText()
    
    def update_fdt(self):
        self.padre.update_funciones()
    
    def click(self):
        if self.clickeable:
            self.macro_vista_window = MacroVistaMainWindow(self, self.modelo)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.click()

    def hoverMoveEvent(self, event):
        # Cambia el cursor a una mano al pasar el mouse sobre el rectángulo
        self.setCursor(Qt.PointingHandCursor)




class MacroVistaMainWindow(QMainWindow):
    def __init__(self,padre,modelo):
        super().__init__()
        self.floating_ellipses_view = None
        self.padre = padre
        self.modelo = modelo

        self.setWindowTitle(self.modelo.nombre)

        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.showMaximized()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        

        self.drawing_area = DrawingArea(self.padre, self.central_widget)
        self.drawing_area.setGeometry(screen)
        #self.setCentralWidget(self.drawing_area)

        # Crear la segunda QGraphicsView que contendrá los elipses
        self.floating_ellipses_view = FloatingButtons(self.central_widget,padre=self.drawing_area)
        self.floating_ellipses_view.raise_()

        # Establecer la posición de la vista de elipses flotantes en la esquina inferior izquierda
        
        self.floating_ellipses_view.setGeometry(0,screen.height()-350, 600, 150)

        self.show()

        # Ruta de la imagen del logo
        path =  os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        QTimer.singleShot(100, self.drawing_area.load_microbloques)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.floating_ellipses_view:
            height = self.size().height()
            self.floating_ellipses_view.setGeometry(0, height-200, 600, 150)