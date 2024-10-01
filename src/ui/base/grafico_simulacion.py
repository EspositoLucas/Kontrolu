import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class Graficadora(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, False)  # Evita que la ventana se cierre automáticamente
        self.setWindowTitle("Gráfico de Simulación en Tiempo Real")
        self.setGeometry(100, 100, 800, 600)

        # Widget principal para la disposición
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Crear un layout horizontal
        self.layout = QHBoxLayout(self.central_widget)

        # Crear el gráfico de Matplotlib
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        # Añadir el gráfico al layout
        self.layout.addWidget(self.canvas)

        # Crear el panel lateral con checkboxes
        self.controls_layout = QVBoxLayout()
        self.layout.addLayout(self.controls_layout)

        self.datos = {}
        self.lineas = {}
        self.checkboxes = {}

    def agregar_datos(self, nuevos_datos):
        for clave, valor in nuevos_datos.items():
            if clave not in self.datos:
                self.datos[clave] = []
                self.lineas[clave], = self.ax.plot([], [], label=clave)
                self.checkboxes[clave] = QCheckBox(clave)
                self.checkboxes[clave].setChecked(True)
                self.checkboxes[clave].stateChanged.connect(self.actualizar_grafico)
                self.controls_layout.addWidget(self.checkboxes[clave])
            
            valor_numerico = self.convertir_a_numerico(valor)
            self.datos[clave].append(valor_numerico)

        self.actualizar_grafico()


    def convertir_a_numerico(self, valor):
        if isinstance(valor, (int, float)):
            return valor
        elif isinstance(valor, dict):
            for key in ['valor', 'prioridad', 'minimo']:
                if key in valor and isinstance(valor[key], (int, float)):
                    return valor[key]
            return 0
        else:
            try:
                return float(str(valor))
            except ValueError:
                return 0

    def actualizar_grafico(self):
        self.ax.clear()  # Limpiar el gráfico antes de actualizarlo
        for clave, linea in self.lineas.items():
            if clave != 'tiempo' and self.checkboxes[clave].isChecked():
                self.ax.plot(self.datos['tiempo'], self.datos[clave], label=clave)

        self.ax.legend()
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Valor')
        self.canvas.draw()

    def closeEvent(self, event):
        event.ignore()  # Ignora el evento de cierre
        self.hide()  # Oculta la ventana en lugar de cerrarla

    def procesar_eventos(self):
        QApplication.processEvents()