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
class Flecha(QtWidgets.QGraphicsPathItem):
    def __init__(self, source: QtCore.QPointF, destination: QtCore.QPointF, arrow_height, arrow_width, length_width, *args, **kwargs):
        super(Flecha, self).__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination

        self._arrow_height = arrow_height
        self._arrow_width = arrow_width
        self._length_width = length_width

    def arrowCalc(self, start_point=None, end_point=None):  # calculates the point where the arrow should be drawn

        try:
            startPoint, endPoint = start_point, end_point

            if start_point is None:
                startPoint = self._sourcePoint

            if endPoint is None:
                endPoint = self._destinationPoint

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize
            
            # parallel vector (normX, normY)
            # perpendicular vector (perpX, perpY)
            perpX = -normY
            perpY = normX
            
            
            #           p2
            #           |\
            #    p4____p5 \
            #     |        \ endpoint
            #    p7____p6  /
            #           | /
            #           |/
            #          p3
            point2 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height + QtCore.QPointF(perpX, perpY) * self._arrow_width
            point3 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height - QtCore.QPointF(perpX, perpY) * self._arrow_width

            point4 = startPoint + QtCore.QPointF(perpX, perpY) * self._length_width
            point5 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height + QtCore.QPointF(perpX, perpY) * self._length_width
            point6 = endPoint + QtCore.QPointF(normX, normY) * self._arrow_height - QtCore.QPointF(perpX, perpY) * self._length_width
            point7 = startPoint - QtCore.QPointF(perpX, perpY) * self._length_width

            return QtGui.QPolygonF([point4, point5, point2, endPoint, point3, point6, point7])

        except (ZeroDivisionError, Exception):
            return None

    def paint(self, painter: QtGui.QPainter, option, widget=None) -> None:
        painter.setRenderHint(painter.Antialiasing)

        my_pen = QtGui.QPen()
        my_pen.setWidth(1)
        my_pen.setCosmetic(False)
        my_pen.setColor(QtGui.QColor(255, 0, 0, 100))
        painter.setPen(my_pen)

        arrow_polygon = self.arrowCalc()
        if arrow_polygon is not None:
            # painter.drawPolyline(arrow_polygon)
            painter.drawPolygon(arrow_polygon)


def main():
    app = QtWidgets.QApplication([])



    scene = QtWidgets.QGraphicsScene()

    view = QtWidgets.QGraphicsView(scene)

    view.show()

    arrow = Flecha(QtCore.QPointF(0, 0), QtCore.QPointF(0, 100), 10, 30, 10)
    scene.addItem(arrow)
    arrow = Flecha(QtCore.QPointF(100, 0), QtCore.QPointF(100, 100), 10, 30, 10)
    scene.addItem(arrow)

    app.exec_()
if __name__ == "__main__":
    main()