from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
import numpy as np
import csv

class Graficadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setWindowTitle("Gráfico de Simulación en Tiempo Real")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        self.layout.addLayout(graph_layout, 3)

        self.controls_layout = QVBoxLayout()
        self.layout.addLayout(self.controls_layout, 1)

        self.datos = {}
        self.lineas = {}
        self.checkboxes = {}
        self.colores = plt.cm.get_cmap('Set1')(np.linspace(0, 1, 10))

        self.export_manager = ExportManager(self)

        self.setup_controls()

    def setup_controls(self):
        export_button = QPushButton("Exportar Datos")
        export_button.clicked.connect(self.export_manager.export_data)
        self.controls_layout.addWidget(export_button)

    def agregar_datos(self, nuevos_datos):
        for clave, valor in nuevos_datos.items():
            if clave not in self.datos:
                self.datos[clave] = []
                color = self.colores[len(self.lineas) % len(self.colores)]
                self.lineas[clave], = self.ax.plot([], [], label=clave, color=color)
                if clave != 'tiempo':
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
        self.ax.clear()
        for clave, linea in self.lineas.items():
            if clave != 'tiempo':
                if self.checkboxes[clave].isChecked():
                    self.ax.plot(self.datos['tiempo'], self.datos[clave], label=clave)
                    # Añadir esta línea para mostrar el último valor
                    if len(self.datos[clave]) > 0:
                        ultimo_valor = self.datos[clave][-1]
                        self.ax.annotate(f'{ultimo_valor:.2f}', 
                                        (self.datos['tiempo'][-1], ultimo_valor),
                                        textcoords="offset points", 
                                        xytext=(0,10), 
                                        ha='center')

        self.ax.legend()
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Valor')
        self.canvas.draw()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def procesar_eventos(self):
        QApplication.processEvents()


class ExportManager:
    def __init__(self, graficadora):
        self.graficadora = graficadora

    def export_data(self):
        filename, _ = QFileDialog.getSaveFileName(self.graficadora, "Guardar datos", "", "CSV Files (*.csv)")
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.graficadora.datos.keys())
                for i in range(len(self.graficadora.datos['tiempo'])):
                    row = [self.graficadora.datos[key][i] for key in self.graficadora.datos.keys()]
                    writer.writerow(row)