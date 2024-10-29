from PyQt5.QtWidgets import  QApplication
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from io import BytesIO
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import ( QApplication, 
                              QDialog, QVBoxLayout, QTabWidget, QLabel)
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify,DiracDelta
import os

ESTILO = """
    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #808080;  /* Botones en gris oscuro pastel */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;  /* Tamaño de botón más grande */
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;  /* Tipografía moderna */
    }

    QPushButton:hover {
        background-color: #606060;  /* Gris aún más oscuro al pasar el cursor */
    }

    QLineEdit {
        background-color: #D0D0D0;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QLabel {
        color: #2B2D42;  /* Texto gris oscuro */
        background-color: transparent;
        font-size: 16px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox {
        background-color: #D0D0D0;  /* Fondo gris claro */
        color: #2B2D42;  /* Texto gris oscuro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 5px;
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QComboBox QAbstractItemView {
        background-color: #D0D0D0;  /* Fondo de la lista desplegable */
        border: 2px solid #505050;  /* Borde gris oscuro */
        selection-background-color: #808080;  /* Selección gris oscuro */
        color: #2B2D42;  /* Texto blanco en selección */
    }

    QVBoxLayout {
        margin: 10px;  /* Márgenes en el layout */
        spacing: 10px;  /* Espaciado entre widgets */
    }
"""

class SVGView(QGraphicsSvgItem):
    def __init__(self, macro, parent=None):
        super().__init__(parent)
        self.macro = macro
        self.laplace = "F(s) = " + self.macro.obtener_fdt_latex()
        self.tiempo = "f(t) = " + self.macro.obtener_fdt_tiempo_latex()
        self.fdt_sympy_laplace = self.macro.obtener_fdt_simpy()
        self.fdt_sympy_tiempo = self.macro.obtener_fdt_tiempo()

        # Configurar matplotlib para usar la fuente Computer Modern
        plt.rc('mathtext', fontset='cm')
        
        # Generar el SVG a partir de la fórmula LaTeX
        bytess_laplace = self.tex2svg(self.laplace)
        bytess_tiempo = self.tex2svg(self.tiempo)
        
        # Cargar el SVG en el renderer
        self.renderer_laplace = QSvgRenderer(bytess_laplace)
        self.renderer_tiempo = QSvgRenderer(bytess_tiempo)
        self.laplace_mode = True
        self.setSharedRenderer(self.renderer_laplace)

        # Permitir eventos de hover
        self.setAcceptHoverEvents(True)

    def tex2svg(self, formula, fontsize=50, dpi=300):
        """Render TeX formula to SVG."""
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

        output = BytesIO()
        fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                    bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)

        output.seek(0)
        return output.read()

    def mousePressEvent(self, event):
        # Obtener la posición del clic
        pos = event.pos()
        print(f"Clic en posición: {pos.x()}, {pos.y()}")  # Mostrar la posición en la consola
        
        # Verificar si el clic fue con el botón izquierdo
        if event.button() == Qt.LeftButton:
            print("Clic izquierdo detectado en SVG.")
            self.open_graph_window(self.laplace)
        if event.button() == Qt.RightButton:
            print("Clic derecho detectado en SVG.")
            if self.laplace:
                self.setSharedRenderer(self.renderer_tiempo)
                self.laplace = False
            else:
                self.setSharedRenderer(self.renderer_laplace)
                self.laplace = True

        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)

    def open_graph_window(self, cual):
        
        dialog = QDialog()
        dialog.setWindowTitle("Dominio de Laplace y Dominio de Tiempo")
        dialog.setStyleSheet(ESTILO)
        
        # Configurar el icono
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(QtGui.QIcon(icon))
        
        layout = QVBoxLayout()
        
        # Agregar botón de ayuda
        help_button = QtWidgets.QPushButton("?")
        help_button.setFixedSize(30, 30)
        help_button.move(50, 50)  # Posición del botón en la ventana
        # help_button.setMaximumWidth(30)
        help_button.clicked.connect(self.mostrar_ayuda)
        layout.addWidget(help_button, alignment=Qt.AlignRight)
        help_button.setStyleSheet("""
            QPushButton {
                background-color: #808080;
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #606060;
            }
        """)

        tab_widget = QTabWidget()

        # Crear la pestaña para el dominio de Laplace
        laplace_tab = QLabel()
        laplace_pixmap = self.get_plot_pixmap(self.plot_laplace())
        laplace_tab.setPixmap(laplace_pixmap)
        tab_widget.addTab(laplace_tab, "Dominio de Laplace")

        # Crear la pestaña para el dominio de tiempo
        tiempo_tab = QLabel()
        tiempo_pixmap = self.get_plot_pixmap(self.plot_tiempo())
        tiempo_tab.setPixmap(tiempo_pixmap)
        tab_widget.addTab(tiempo_tab, "Dominio Tiempo")

        # Seleccionar la pestaña activa dependiendo del valor de `cual`
        if cual:
            tab_widget.setCurrentIndex(0)  # Activa la primera pestaña (Dominio de Laplace)
        else:
            tab_widget.setCurrentIndex(1)  # Activa la segunda pestaña (Dominio Tiempo)

        layout.addWidget(tab_widget)
        dialog.setLayout(layout)
        dialog.exec_()
        
    def mostrar_ayuda(self):
        help_dialog = QtWidgets.QDialog()  # Quitamos el self como padre
        help_dialog.setWindowTitle("Ayuda - Visualización de Funciones de Transferencia")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)
        
        # Configurar el icono
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        help_dialog.setWindowIcon(icon)
        
        layout = QtWidgets.QVBoxLayout()
        
        titulo = QtWidgets.QLabel("Guía de Visualización de Funciones")
        titulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2B2D42;
                padding: 10px;
            }
        """)
        layout.addWidget(titulo)
        
        contenido = [
            ("<b>Visualización de Funciones:</b>", 
            "Esta ventana permite visualizar la respuesta del sistema en dos dominios diferentes:"),
            
            ("<b>Dominio de Laplace (F(s)):</b>",
            "<ul>"
            "<li><b>Eje X:</b> Parte real de la variable compleja s</li>"
            "<li><b>Eje Y:</b> Magnitud de la función de transferencia</li>"
            "<li><b>Interpretación:</b> Muestra el comportamiento del sistema en el dominio de la frecuencia</li>"
            "</ul>"),
            
            ("<b>Dominio del Tiempo (f(t)):</b>",
            "<ul>"
            "<li><b>Eje X:</b> Tiempo en segundos</li>"
            "<li><b>Eje Y:</b> Amplitud de la respuesta</li>"
            "<li><b>Interpretación:</b> Muestra la respuesta temporal del sistema</li>"
            "</ul>"),
            
            ("<b>Interacción:</b>",
            "<ul>"
            "<li><b>Clic Derecho:</b> Alterna entre visualización en tiempo y Laplace</li>"
            "<li><b>Clic Izquierdo:</b> Abre la ventana de gráficos detallados</li>"
            "<li><b>Cursor:</b> El cursor cambia al pasar sobre la función indicando interactividad</li>"
            "</ul>")
        ]
        
        for titulo, texto in contenido:
            seccion = QtWidgets.QLabel()
            seccion.setText(f"{titulo}<br>{texto}")
            seccion.setWordWrap(True)
            seccion.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #2B2D42;
                    padding: 5px;
                    background-color: #D0D0D0;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            layout.addWidget(seccion)
        
        cerrar_btn = QtWidgets.QPushButton("Cerrar")
        cerrar_btn.clicked.connect(help_dialog.close)
        layout.addWidget(cerrar_btn)
        
        help_dialog.setLayout(layout)
        help_dialog.exec_()

    def get_plot_pixmap(self, figure):
        """Convierte una figura de matplotlib en un QPixmap."""
        buf = BytesIO()
        figure.savefig(buf, format="png")
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        buf.close()
        return pixmap
        
    def plot_laplace(self):
        """Generar y mostrar el gráfico del dominio de Laplace."""
        s = symbols('s')
        f_laplace = sympify(self.fdt_sympy_laplace)  # Asegúrate de que `self.fdt_sympy_laplace` esté definida
        F_laplace = lambdify(s, f_laplace, 'numpy')

        s_vals = np.linspace(0, 10, 100)
        
        # Evaluar la función en s_vals
        F_s = F_laplace(s_vals)
        
        # Si F_s es un valor constante, extiéndelo para que tenga la misma longitud que s_vals
        if np.isscalar(F_s):  # Verifica si F_s es un número (escalar)
            F_s = np.full_like(s_vals, F_s)  # Crea un array con el mismo valor y longitud que s_vals

        plt.figure()
        plt.plot(s_vals, F_s)
        plt.title("Dominio de Laplace")
        plt.xlabel("Re(s)")
        plt.ylabel("F(s)")
        plt.grid(True)
        return plt.gcf()

    def plot_tiempo(self):
        """Generar y mostrar el gráfico del dominio del tiempo, con manejo especial para DiracDelta."""
        t = symbols('t')
        f_tiempo = sympify(self.fdt_sympy_tiempo)  # Supone que `self.fdt_sympy_tiempo` esté definida
        
        # Verificar si hay una DiracDelta en la función
        if f_tiempo.has(DiracDelta(t)):
            # Crear un array para simular la DiracDelta: un valor alto en t=0, y 0 en los demás puntos
            t_vals = np.linspace(0, 10, 100)
            f_t_vals = np.zeros_like(t_vals)
            # Aproximamos la DiracDelta con un pico alto en el primer punto
            f_t_vals[0] = 1e10  # Representa la intensidad del impulso en t=0
        else:
            # Si no hay DiracDelta, crear la función normalmente
            f_t = lambdify(t, f_tiempo, 'numpy')
            t_vals = np.linspace(0, 10, 100)
            f_t_vals = f_t(t_vals)

            # Si f_t_vals es un valor constante, extiéndelo para que tenga la misma longitud que t_vals
            if np.isscalar(f_t_vals):  # Verifica si f_t_vals es un número (escalar)
                f_t_vals = np.full_like(t_vals, f_t_vals)  # Crea un array con el mismo valor y longitud que t_vals

        plt.figure()
        plt.plot(t_vals, f_t_vals)
        plt.title("Dominio de Tiempo")
        plt.xlabel("Tiempo (t)")
        plt.ylabel("f(t)")
        plt.grid(True)
        return plt.gcf()
    
    def hoverEnterEvent(self, event):
        # Cambiar el cursor al formato de clic
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Restaurar el cursor al estado predeterminado
        QApplication.restoreOverrideCursor()
        super().hoverLeaveEvent(event)