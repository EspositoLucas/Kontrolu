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
    def __init__(self, source: QtCore.QPointF, destination: QtCore.QPointF, arrow_height=15, arrow_width=10, length_width=5, arrow=True, *args, **kwargs):
        super(Flecha, self).__init__(*args, **kwargs)
        self._sourcePoint = source
        self._destinationPoint = destination
        self._arrow_height = arrow_height
        self._arrow_width = arrow_width
        self._length_width = length_width
        self.arrow = arrow
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, False)
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        extra = 10
        points = [self._sourcePoint, self._destinationPoint]
        return QtCore.QRectF(QtCore.QPointF(min(p.x() for p in points), min(p.y() for p in points)),
                             QtCore.QPointF(max(p.x() for p in points), max(p.y() for p in points))).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        my_pen = QtGui.QPen()
        my_pen.setWidth(2)
        my_pen.setCosmetic(False)
        my_pen.setColor(QtGui.QColor(0, 0, 0))
        painter.setPen(my_pen)

        points = [self._sourcePoint, self._destinationPoint]

        if self.arrow:
            arrow_polygon = self.arrowCalc(points[0], points[1])
            if arrow_polygon is not None:
                painter.drawPolyline(QtGui.QPolygonF(points))
                painter.setBrush(QtGui.QColor(0, 0, 0))
                painter.drawPolygon(arrow_polygon)
        else:
            rectangle_polygon = self.rectangleCalc(points[0], points[1])
            if rectangle_polygon is not None:
                painter.drawPolyline(QtGui.QPolygonF(points))
                painter.setBrush(QtGui.QColor(0, 0, 0))
                painter.drawPolygon(rectangle_polygon)

    def arrowCalc(self, start_point, end_point):
        try:
            startPoint = start_point
            endPoint = end_point

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng

            perpX = -normY
            perpY = normX


            point2 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height * 5 + QtCore.QPointF(perpX, perpY) * self._arrow_width * 5
            point3 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height * 5 - QtCore.QPointF(perpX, perpY) * self._arrow_width * 5

            point4 = startPoint + QtCore.QPointF(perpX, perpY) * self._length_width
            point5 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height + QtCore.QPointF(perpX, perpY) * self._length_width
            point6 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height - QtCore.QPointF(perpX, perpY) * self._length_width
            point7 = startPoint - QtCore.QPointF(perpX, perpY) * self._length_width

            return QtGui.QPolygonF([point4, point5, point2, endPoint, point3, point6, point7])

        except (ZeroDivisionError, Exception):
            return None

    def rectangleCalc(self, start_point, end_point):
        try:
            startPoint = start_point
            endPoint = end_point

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng

            perpX = -normY
            perpY = normX

            point1 = startPoint + QtCore.QPointF(perpX, perpY) * self._length_width
            point2 = startPoint - QtCore.QPointF(perpX, perpY) * self._length_width
            point3 = endPoint - QtCore.QPointF(perpX, perpY) * self._length_width
            point4 = endPoint + QtCore.QPointF(perpX, perpY) * self._length_width

            return QtGui.QPolygonF([point1, point2, point3, point4])

        except (ZeroDivisionError, Exception):
            return None

    def hoverEnterEvent(self, event):
        self.setCursor(QtCore.Qt.CrossCursor)

    def hoverLeaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)