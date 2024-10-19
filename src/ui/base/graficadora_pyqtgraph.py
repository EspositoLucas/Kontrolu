import sys
import random
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class RealTimePlot(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Real-Time Plot')

        # Create a plot widget
        self.plot_widget = PlotWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        # Initialize the plot data
        self.x_data = []
        self.y_data = []
        self.curve = self.plot_widget.plot(self.x_data, self.y_data, pen='y')


    def update_plot(self,x,y):
        self.x_data.append(float(x))
        self.y_data.append(float(y))
        print(self.x_data)
        print(self.y_data)
        # Update the plot
        self.curve.setData(self.x_data, self.y_data)