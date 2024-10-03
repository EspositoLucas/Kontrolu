from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QColorDialog, QDialog,QComboBox,QHBoxLayout, QMessageBox, QGraphicsItem,QTabWidget,QGridLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF
from .latex_editor import LatexEditor
from back.topologia.configuraciones import Configuracion,TipoError
from .crear_microbloque import CrearMicroBloque
class Microbloque(QGraphicsItem):
    def __init__(self, microbloque_back=None):
        super().__init__()
        self.elemento_back = microbloque_back
        self.nombre = microbloque_back.nombre
        self.color = microbloque_back.color or QColor(255, 255, 0)
        self.funcion_transferencia = microbloque_back.funcion_transferencia or ""
        self.configuracion_entrada = microbloque_back.configuracion_entrada
        self.configuracion_salida = microbloque_back.configuracion_salida
        self.esta_selecionado = False
        
        self.entrada_unidad_color = Qt.red
        self.salida_unidad_color = Qt.red
        
        if microbloque_back.validar_entrada():
            self.entrada_unidad_color = Qt.green
        if microbloque_back.validar_salida():
            self.salida_unidad_color = Qt.green
        
        

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(1)
    
    def boundingRect(self):
        return QRectF(0, 0, self.elemento_back.ancho(), self.elemento_back.alto())

    def es_color_claro(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        return r * 0.299 + g * 0.587 + b * 0.114 > 186

    def calcular_color(self, color):
        fondo_color = color
        es_claro = self.es_color_claro(fondo_color)
        color_texto = "black" if es_claro else "white"
        return color_texto

    def setPos(self, pos):
        super().setPos(pos)

    def height(self):
        return self.boundingRect().height()
    
    def width(self):
        return self.boundingRect().width()

    def setSeleccionado(self, seleccionado):
        self.esta_selecionado = seleccionado
        self.update()
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.esta_selecionado:
            painter.setPen(QPen(Qt.red, 3))
        else:
            painter.setPen(QPen(Qt.black, 2))
        
        painter.setBrush(self.color)
        rect = self.boundingRect()
        painter.drawRect(rect)
        
        font = QFont("Arial", max(1, round(10)), QFont.Bold)
        painter.setFont(font)
        
        color_texto = self.calcular_color(self.color)
        painter.setPen(QPen(QColor(color_texto)))
        
        text_rect = rect.adjusted(5, 5, -5, -5)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.nombre)

        # Dibujar unidades
        units_font = QFont("Arial", max(1, round(12)), QFont.Bold)
        painter.setFont(units_font)

        # Unidad de entrada
        entrada_text = f"({self.configuracion_entrada.unidad})"
        entrada_rect = painter.fontMetrics().boundingRect(entrada_text)
        painter.setPen(QPen(self.entrada_unidad_color, 2))
        painter.drawText(QPointF(rect.left(), rect.top() - entrada_rect.height() / 2), entrada_text)

        # Unidad de salida
        salida_text = f"({self.configuracion_salida.unidad})"
        salida_rect = painter.fontMetrics().boundingRect(salida_text)
        painter.setPen(QPen(self.salida_unidad_color, 2))
        painter.drawText(QPointF(rect.right() - salida_rect.width(), rect.top() - salida_rect.height() / 2), salida_text)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.edit_properties()


    def edit_properties(self):
        self.scene().views()[0].window()

        unidad_vieja_entrada = self.elemento_back.configuracion_entrada.unidad
        unidad_vieja_salida = self.elemento_back.configuracion_salida.unidad

        micro = CrearMicroBloque(self.elemento_back, self.scene().parent().modelo.tipo, self.scene().parent(),1)
        result = micro.exec_()

        if result == QDialog.Accepted:
            if unidad_vieja_entrada != self.elemento_back.configuracion_entrada.unidad or unidad_vieja_salida != self.elemento_back.configuracion_salida.unidad:
                self.scene().parent().actualizar_colores_unidades()               
                
            self.update()
    
    def select_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
            button.setStyleSheet(f"background-color: {color.name()};")

    def get_center(self):
        return self.pos() + QPointF(self.width() / 2, self.height() / 2)

    def set_center(self, point):
        new_pos = point - QPointF(self.width() / 2, self.height() / 2)
        self.move(new_pos.toPoint())

    def __str__(self):
        return f"Microbloque(nombre={self.nombre}, color={self.color.name()}, funcion_transferencia={self.funcion_transferencia})"

    def __repr__(self):
        return self.__str__()
    
    def actualizar_color_unidades(self):
        color_entrada = Qt.red
        color_salida = Qt.red

        if self.elemento_back.validar_entrada():
            color_entrada = Qt.green
        if self.elemento_back.validar_salida():
            color_salida = Qt.green
        
        if self.entrada_unidad_color != color_entrada or self.salida_unidad_color != color_salida:
            self.entrada_unidad_color = color_entrada
            self.salida_unidad_color = color_salida
            self.update()
