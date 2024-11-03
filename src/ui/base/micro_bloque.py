from PyQt5.QtWidgets import QColorDialog, QDialog,QGraphicsItem
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QPointF, QRectF
from .crear_microbloque import CrearMicroBloque


LETRA_COLOR = QColor("#2B2D42")
TEXTO_BLANCO = QColor("#FFFDF5")
VERDE = QColor("#55AA55")
ROJO = QColor("#CC6666")

class Microbloque(QGraphicsItem):
    def __init__(self, microbloque_back=None):
        super().__init__()
        self.elemento_back = microbloque_back
        self.nombre = microbloque_back.nombre
        self.funcion_transferencia = microbloque_back.funcion_transferencia or ""
        self.configuracion_entrada = microbloque_back.configuracion_entrada
        self.configuracion_salida = microbloque_back.configuracion_salida
        self.esta_selecionado = False
        
        self.entrada_unidad_color = ROJO
        self.salida_unidad_color = ROJO
        
        if microbloque_back.validar_entrada():
            self.entrada_unidad_color = VERDE
        if microbloque_back.validar_salida():
            self.salida_unidad_color = VERDE
        
        self.calcular_colores()
        
        self.setAcceptHoverEvents(True)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(1)

    def calcular_colores(self):
        self.color = self.elemento_back.color or QColor(255, 255, 0)

        self.default_brush = self.color  # Fondo

        self.hover_color = self.color.lighter(150) 

        self.border_color = self.color.darker(150)

        self.selected_color = self.border_color.darker(150)

        self.texto_color = self.calcular_color(self.color)

    def boundingRect(self):
        return QRectF(0, 0, self.elemento_back.ancho(), self.elemento_back.alto())

    def es_color_claro(self, color):
        r, g, b = color.red(), color.green(), color.blue()
        return r * 0.299 + g * 0.587 + b * 0.114 > 186

    def calcular_color(self, color):
        fondo_color = color
        es_claro = self.es_color_claro(fondo_color)
        color_texto = LETRA_COLOR if es_claro else TEXTO_BLANCO
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
        self.option = option
        self.painter = painter
        self.widget = widget

        painter.setRenderHint(painter.Antialiasing)
        
        if self.esta_selecionado:
            painter.setPen(QPen(self.selected_color, 5))
        else:
            painter.setPen(QPen(self.border_color, 4))
        
        painter.setBrush(self.color)
        rect = self.boundingRect()
        painter.drawRoundedRect(rect, 10, 10)
        
        font = QFont("Arial", max(1, round(10)), QFont.Bold)
        painter.setFont(font)
        
        painter.setPen(QPen(self.texto_color))
        
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
            self.actualizar()
            self.scene().parent().update_fdt()
            if unidad_vieja_entrada != self.elemento_back.configuracion_entrada.unidad or unidad_vieja_salida != self.elemento_back.configuracion_salida.unidad:
                self.scene().parent().actualizar_colores_unidades() 

            try:
                self.elemento_back.color = micro.color
                self.color = micro.color
            except:
                pass        
                
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
        color_entrada = ROJO
        color_salida = ROJO

        if self.elemento_back.validar_entrada():
            color_entrada = VERDE
        if self.elemento_back.validar_salida():
            color_salida = VERDE
        
        if self.entrada_unidad_color != color_entrada or self.salida_unidad_color != color_salida:
            self.entrada_unidad_color = color_entrada
            self.salida_unidad_color = color_salida
            self.update()

    def actualizar(self):
        self.calcular_colores()
        self.nombre = self.elemento_back.nombre
        self.funcion_transferencia = self.elemento_back.funcion_transferencia or ""
        self.configuracion_entrada = self.elemento_back.configuracion_entrada
        self.configuracion_salida = self.elemento_back.configuracion_salida

    
    def hoverEnterEvent(self, event):
        self.color = self.hover_color
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.color = self.default_brush
        self.update()
        super().hoverLeaveEvent(event)
    
    def hoverMoveEvent(self, event):
        # Cambia el cursor a una mano al pasar el mouse sobre el rectángulo
        self.setCursor(Qt.PointingHandCursor)
