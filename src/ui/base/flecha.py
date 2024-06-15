from PyQt5 import QtWidgets, QtCore, QtGui
import math

#  draw an arrow like this
#                           |\
#                ___   _____| \
#    length_width |   |        \  _____
#                _|_  |_____   /    |
#                           | /     | arrow_width
#                           |/    __|__
#
#                           |<->|
#                        arrow_height 

class Flecha(QtWidgets.QGraphicsItem):
    def __init__(self, source: QtCore.QPointF, destination: QtCore.QPointF, arrow_height, arrow_width, length_width, *args, **kwargs):
        super(Flecha, self).__init__(*args, **kwargs)
        self._sourcePoint = source
        self._destinationPoint = destination
        self._arrow_height = arrow_height
        self._arrow_width = arrow_width
        self._length_width = length_width

    def boundingRect(self):
        extra = 10
        return QtCore.QRectF(self._sourcePoint, QtCore.QSizeF(self._destinationPoint.x() - self._sourcePoint.x(),
                                                              self._destinationPoint.y() - self._sourcePoint.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        my_pen = QtGui.QPen()
        my_pen.setWidth(1)
        my_pen.setCosmetic(False)
        my_pen.setColor(QtGui.QColor(255, 0, 0, 100))
        painter.setPen(my_pen)

        arrow_polygon = self.arrowCalc()
        if arrow_polygon is not None:
            painter.drawPolygon(arrow_polygon)

    def arrowCalc(self, start_point=None, end_point=None):
        try:
            startPoint = start_point if start_point else self._sourcePoint
            endPoint = end_point if end_point else self._destinationPoint

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize
            
            perpX = -normY
            perpY = normX
            
            point2 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height + QtCore.QPointF(perpX, perpY) * self._arrow_width
            point3 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height - QtCore.QPointF(perpX, perpY) * self._arrow_width

            point4 = startPoint + QtCore.QPointF(perpX, perpY) * self._length_width
            point5 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height + QtCore.QPointF(perpX, perpY) * self._length_width
            point6 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height - QtCore.QPointF(perpX, perpY) * self._length_width
            point7 = startPoint - QtCore.QPointF(perpX, perpY) * self._length_width

            return QtGui.QPolygonF([point4, point5, point2, endPoint, point3, point6, point7])

        except (ZeroDivisionError, Exception):
            return None
