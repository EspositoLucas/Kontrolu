from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import QRect,QCoreApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint

class MacroVista(QPushButton):
    def __init__(self, inicio, fin, modelo,main_window):
        super().__init__(main_window)
        self.setGeometry(QRect(inicio, fin, 121, 41))
        self.setCheckable(True)
        self.setObjectName("pushButton")
        self.setText(QCoreApplication.translate("Form",modelo.nombre))
        self.modelo = modelo

        self.show()
