# src/ui/drawing_area.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QPolygonF, QColor
from PyQt5.QtCore import Qt, QPoint, QRectF, QLineF, QPointF
import math

class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.shapes = []
        self.current_shape = None
        self.current_arrow = None
        self.drawing_shape = False
        self.shape_type = None
        self.start_point = None

    def set_shape(self, shape_type):
        self.shape_type = shape_type

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.shape_type:
            self.start_point = event.pos()
            if self.shape_type in ['square', 'rectangle', 'circle']:
                self.drawing_shape = True
            elif self.shape_type == 'arrow':
                self.current_arrow = {'type': 'arrow', 'start': self.start_point, 'end': self.start_point}
                self.shapes.append(self.current_arrow)

    def mouseMoveEvent(self, event):
        if self.drawing_shape:
            if self.shape_type == 'square':
                self.current_shape = self.create_square(self.start_point, event.pos())
            else:
                self.current_shape = {'type': self.shape_type, 'start': self.start_point, 'end': event.pos()}
            self.update()
        elif self.current_arrow:
            self.current_arrow['end'] = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing_shape:
            if self.current_shape:
                self.shapes.append(self.current_shape)
            self.current_shape = None
            self.drawing_shape = False
            self.update()
        elif self.current_arrow:
            if not self.valid_arrow(self.current_arrow):
                self.shapes.remove(self.current_arrow)
            else:
                self.current_arrow = self.adjust_arrow(self.current_arrow)
            self.current_arrow = None
            self.update()

    def valid_arrow(self, arrow):
        start_connected = any(
            shape['type'] in ['square', 'rectangle', 'circle'] and 
            self.point_in_shape(arrow['start'], shape)
            for shape in self.shapes
        )
        end_connected = any(
            shape['type'] in ['square', 'rectangle', 'circle'] and 
            self.point_in_shape(arrow['end'], shape)
            for shape in self.shapes
        )
        return start_connected and end_connected

    def point_in_shape(self, point, shape):
        if shape['type'] in ['square', 'rectangle']:
            rect = QRectF(shape['start'], shape['end'])
            return rect.contains(point)
        elif shape['type'] == 'circle':
            center = (shape['start'] + shape['end']) / 2
            radius = (shape['start'] - shape['end']).manhattanLength() / 2
            return (point - center).manhattanLength() <= radius
        return False

    def create_square(self, start, end):
        side_length = min(abs(end.x() - start.x()), abs(end.y() - start.y()))
        end_point = QPoint(start.x() + side_length, start.y() + side_length)
        if end.x() < start.x():
            end_point.setX(start.x() - side_length)
        if end.y() < start.y():
            end_point.setY(start.y() - side_length)
        return {'type': 'square', 'start': start, 'end': end_point}

    def adjust_arrow(self, arrow):
        adjusted_arrow = arrow.copy()
        for shape in self.shapes:
            if shape['type'] in ['square', 'rectangle', 'circle']:
                if self.point_in_shape(adjusted_arrow['start'], shape):
                    adjusted_arrow['start'] = self.get_edge_point(shape, adjusted_arrow['end'])
                if self.point_in_shape(adjusted_arrow['end'], shape):
                    adjusted_arrow['end'] = self.get_edge_point(shape, adjusted_arrow['start'])
        return adjusted_arrow

    def get_edge_point(self, shape, outside_point):
        if shape['type'] in ['square', 'rectangle']:
            rect = QRectF(shape['start'], shape['end'])
            center = rect.center()
        elif shape['type'] == 'circle':
            center = (shape['start'] + shape['end']) / 2

        line = QLineF(center, outside_point)
        if shape['type'] in ['square', 'rectangle']:
            rect = QRectF(shape['start'], shape['end'])
            points = [
                QPointF(rect.left(), rect.top()),
                QPointF(rect.right(), rect.top()),
                QPointF(rect.right(), rect.bottom()),
                QPointF(rect.left(), rect.bottom())
            ]
            for i in range(4):
                edge = QLineF(points[i], points[(i + 1) % 4])
                intersect_point = QPointF()
                if line.intersect(edge, intersect_point) == QLineF.BoundedIntersection:
                    return intersect_point
        elif shape['type'] == 'circle':
            radius = (shape['start'] - shape['end']).manhattanLength() / 2
            dx = outside_point.x() - center.x()
            dy = outside_point.y() - center.y()
            length = math.sqrt(dx * dx + dy * dy)
            return QPointF(center.x() + dx / length * radius, center.y() + dy / length * radius)

        return outside_point

    def draw_arrow(self, painter, start, end):
        painter.drawLine(start, end)

        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 10

        arrow_p1 = end + QPointF(math.cos(angle + math.pi / 6) * arrow_size,
                                 math.sin(angle + math.pi / 6) * arrow_size)
        arrow_p2 = end + QPointF(math.cos(angle - math.pi / 6) * arrow_size,
                                 math.sin(angle - math.pi / 6) * arrow_size)

        arrow_head = QPolygonF([end, arrow_p1, arrow_p2])
        painter.setBrush(Qt.black)
        painter.drawPolygon(arrow_head)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        for shape in self.shapes:
            if shape and shape['type'] == 'square':
                painter.drawRect(QRectF(shape['start'], shape['end']))
            elif shape and shape['type'] == 'rectangle':
                painter.drawRect(QRectF(shape['start'], shape['end']))
            elif shape and shape['type'] == 'circle':
                center = (shape['start'] + shape['end']) / 2
                radius = (shape['start'] - shape['end']).manhattanLength() / 2
                painter.drawEllipse(center, radius, radius)
            elif shape and shape['type'] == 'arrow':
                self.draw_arrow(painter, shape['start'], shape['end'])

        if self.current_shape:
            if self.current_shape['type'] == 'square':
                painter.drawRect(QRectF(self.current_shape['start'], self.current_shape['end']))
            elif self.current_shape['type'] == 'rectangle':
                painter.drawRect(QRectF(self.current_shape['start'], self.current_shape['end']))
            elif self.current_shape['type'] == 'circle':
                center = (self.current_shape['start'] + self.current_shape['end']) / 2
                radius = (self.current_shape['start'] - self.current_shape['end']).manhattanLength() / 2
                painter.drawEllipse(center, radius, radius)

        if self.current_arrow:
            self.draw_arrow(painter, self.current_arrow['start'], self.current_arrow['end'])

    def clear(self):
        self.shapes = []
        self.update()
