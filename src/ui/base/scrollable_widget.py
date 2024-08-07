from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
import math

class ScrollableWidget(QScrollArea):
    def __init__(self, widget):
        super().__init__()
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.addWidget(widget)
        self.setWidget(self.content_widget)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setFrameShape(QScrollArea.NoFrame)

    def wheelEvent(self, event):
        # Eliminamos la funcionalidad de zoom
        super().wheelEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjustScrollBars()
        
    def adjustScrollBars(self):
        content_rect = self.widget().childrenRect()
        margin = 100
        new_width = max(self.viewport().width(), math.ceil(content_rect.right() + margin))
        new_height = max(self.viewport().height(), math.ceil(content_rect.bottom() + margin))
        self.widget().setMinimumSize(QSize(new_width, new_height))
