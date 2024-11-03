from PyQt5.QtWidgets import  QApplication
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from io import BytesIO
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import ( QApplication, 
                              QDialog, QVBoxLayout, QTabWidget, QLabel)
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import os
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify,DiracDelta,latex
ESTILO = """
    QDialog {
        background-color: #B0B0B0;  /* Gris pastel oscuro para el fondo */
        border-radius: 15px;  /* Bordes redondeados */
        padding: 20px;  /* Espaciado interior */
        border: 2px solid #505050;  /* Borde gris más oscuro */
    }

    QPushButton {
        background-color: #707070;  /* Un gris más oscuro para mayor contraste */
        color: white;  /* Texto en blanco */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;  /* Texto en negrita */
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
    }


    QLineEdit {
        background-color: #FAF8F6;  /* Fondo gris claro */
        border: 2px solid #505050;  /* Borde gris oscuro */
        border-radius: 10px;
        padding: 8px;
        color: #2B2D42;  /* Texto gris oscuro */
        font-size: 14px;  /* Tipografía más grande */
        font-family: "Segoe UI", "Arial", sans-serif;
    }
    
    QTextEdit {
        background-color: #FAF8F6;  /* Fondo blanco pastel */
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

    QTabWidget::pane {
        border: 2px solid #505050;
        border-radius: 10px;
        background-color: #FAF8F6;
        padding: 10px;
    }
    QTabBar::tab {
        background-color: #D0D0D0;
        color: #2B2D42;
        border: 2px solid #505050;
        border-radius: 5px;
        padding: 12px 20px;  /* Aumentamos el padding horizontal a 20px */
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-weight: bold;
        min-width: 80px;  /* Ancho mínimo para las tabs */
        margin-right: 2px;  /* Pequeño espacio entre tabs */
    }

    QTabBar::tab:selected {
        background-color: #808080;  /* Fondo gris oscuro al seleccionar */
        color: white;  /* Texto en blanco en la pestaña seleccionada */
    }

    QTabBar::tab:hover {
        background-color: #606060;  /* Fondo gris más oscuro al pasar el cursor */
        color: white;  /* Texto en blanco al pasar el cursor */
    }


    QTableWidget {
        background-color: #FAF8F6;  /* Color de fondo del área sin celdas */
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        gridline-color: #505050;  /* Color de las líneas de la cuadrícula */
    }

    QTableWidget::item {
        background-color: #D0D0D0;  /* Color de fondo de las celdas */
        border: none;
    }

    QHeaderView::section {
        background-color: #808080;
        color: white;
        padding: 5px;
        border: 1px solid #505050;
    }

    QTableCornerButton::section {
        background-color: #808080;  /* Color del botón de esquina */
        border: 1px solid #505050;
    }


    QListWidget {
        background-color: #D0D0D0;
        border: 2px solid #505050;
        border-radius: 10px;
        color: #2B2D42;
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
    }

    QListWidget::item:selected {
        background-color: #808080;
        color: white;
    }
"""

class SVGView(QGraphicsSvgItem):
    def __init__(self, macro,x,y, padre, fdts,parent=None):
        self.padre = padre
        super().__init__(parent)
        self.pos_x = x
        self.pos_y = y
        self.macro = macro

        plt.rc('mathtext', fontset='cm')

        self.funciones = []

        self.graficos = []


        self.fdt_sympy_laplace, self.fdt_latex_laplace, self.fdt_sympy_laplace_total, self.fdt_latex_laplace_total, self.fdt_sympy_global_laplace, self.fdt_latex_global_laplace, self.fdt_sympy_global_unitaria, self.fdt_latex_global_unitaria, self.realimentacion, self.realimentacion_latex  = fdts
        
        
        self.laplace = "\\theta_{o}(s) = " + self.fdt_latex_laplace
        bytess_laplace = self.tex2svg(self.laplace)
        self.renderer_laplace = QSvgRenderer(bytess_laplace)
        self.funciones.append(self.renderer_laplace)
        self.graficos.append((self.fdt_sympy_laplace,True,"Salida","\\theta_{o}(s)"))

        
        self.total_laplace = "G_{g}(s) = " + self.fdt_latex_laplace_total
        bytess_laplace_total = self.tex2svg(self.total_laplace)
        self.renderer_laplace_total = QSvgRenderer(bytess_laplace_total)
        self.funciones.append(self.renderer_laplace_total)
        self.graficos.append((self.fdt_sympy_laplace_total,True,"Directo","G_{g}(s)"))


        self.global_laplace = "G_{t}(s) = " + self.fdt_latex_global_laplace
        bytess_global_laplace = self.tex2svg(self.global_laplace)
        self.renderer_global_laplace = QSvgRenderer(bytess_global_laplace)
        self.funciones.append(self.renderer_global_laplace)
        self.graficos.append((self.fdt_sympy_global_laplace,True,"Total","G_{t}(s)"))

        
        self.global_unitaria = "G_{0}(s) = " + self.fdt_latex_global_unitaria
        bytess_global_unitaria = self.tex2svg(self.global_unitaria)
        self.renderer_global_unitaria = QSvgRenderer(bytess_global_unitaria)
        self.funciones.append(self.renderer_global_unitaria)      
        self.graficos.append((self.fdt_sympy_global_unitaria,True,"Unitaria","G_{0}(s)"))

        self.realimentacion_latex_completa = "H(s) = " + self.realimentacion_latex
        bytess_realimentacion = self.tex2svg(self.realimentacion_latex_completa)
        self.renderer_realimentacion = QSvgRenderer(bytess_realimentacion)
        self.funciones.append(self.renderer_realimentacion)      
        self.graficos.append((self.realimentacion,True,"Realimentación","H(s)"))

        self.laplace_mode = 0
        if len(self.funciones) > 0:
            self.setSharedRenderer(self.funciones[0])
            # Permitir eventos de hover
            self.setAcceptHoverEvents(True)
            self.setSize()

    def setSize(self):

        max_x = 560
        max_y = 250

        render = self.funciones[self.laplace_mode]

        rect = render.viewBoxF()

        # Calcular la escala necesaria para ajustar el SVG al tamaño máximo
        scale_x = max_x / rect.width()
        scale_y = max_y / rect.height()
        scale = min(scale_x, scale_y,1)
        
        # Aplicar la escala al QGraphicsSvgItem
        self.setTransform(QTransform().scale(scale, scale))

        # Calcular la nueva posición para centrar el SVG
        # Obtener el tamaño escalado
        scaled_width = rect.width() * scale
        scaled_height = rect.height() * scale

        pos_x = self.pos_x -(scaled_width/2)
        pos_y = self.pos_y -(scaled_height/2)

        # Establecer la nueva posición
        self.setPos(pos_x, pos_y)

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
        
        # Verificar si el clic fue con el botón izquierdo
        if event.button() == Qt.LeftButton:
            self.open_graph_window(self.laplace_mode)
        if event.button() == Qt.RightButton:

            self.laplace_mode += 1

            if self.laplace_mode >= len(self.funciones):
                self.laplace_mode = 0
            self.setSharedRenderer(self.funciones[self.laplace_mode])
            self.setSize()
        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)

    def open_graph_window(self, cual):
        dialog = QDialog()
        dialog.setWindowTitle("Dominio de Laplace")
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
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

        for fdt, is_laplace, title, output in self.graficos:
            # Crear la pestaña para el dominio de Laplace
            laplace_tab = QLabel()
            if is_laplace:
                laplace_pixmap = self.get_plot_pixmap(self.plot_laplace(fdt,title,output))
            else:
                laplace_pixmap = self.get_plot_pixmap(self.plot_tiempo(fdt,title))
            laplace_tab.setPixmap(laplace_pixmap)
            tab_widget.addTab(laplace_tab, title)

        # Seleccionar la pestaña activa dependiendo del valor de `cual`
        tab_widget.setCurrentIndex(cual)

        layout.addWidget(tab_widget)
        dialog.setLayout(layout)
        dialog.exec_()
        
    def mostrar_ayuda(self):
        help_dialog = QtWidgets.QDialog()
        help_dialog.setWindowTitle("Ayuda - Visualización del Sistema")
        help_dialog.setStyleSheet(ESTILO)
        help_dialog.setMinimumWidth(500)
        help_dialog.setWindowFlags(help_dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Configurar el icono
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'imgs', 'logo.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        help_dialog.setWindowIcon(icon)
        
        layout = QtWidgets.QVBoxLayout()
        
        titulo = QtWidgets.QLabel("Guía de Visualización del Sistema de Control")
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
            ("<b>Visualización del Sistema:</b>", 
            "Esta ventana permite analizar el sistema de control de múltiples formas, mostrando diferentes representaciones "
            "en el dominio de Laplace."),
            
            ("<b>Representaciones Disponibles:</b>",
            "<ul>"
            "<li><b>Y(s):</b> Salida del sistema en el dominio de Laplace</li>"
            "<li><b>Y(s)/R(s):</b> Función de transferencia total del sistema en Laplace</li>"
            "<li><b>G(s):</b> Función de transferencia global en Laplace</li>"
            "<li><b>G_{0}(s):</b> Función de transferencia total unitaria en Laplace</li>"
            "</ul>"),
            
            ("<b>Interpretación de Gráficos:</b>",
            "<ul>"
            "<li><b>Dominio de Laplace:</b> Muestra la magnitud de la función vs. la frecuencia</li>"
            "<li><b>Ejes:</b> Las unidades dependen de la magnitud física representada</li>"
            "<li><b>Cuadrícula:</b> Facilita la lectura de valores específicos</li>"
            "</ul>"),
            
            ("<b>Navegación e Interacción:</b>",
            "<ul>"
            "<li><b>Clic Derecho:</b> Cambia entre las diferentes representaciones en el siguiente orden:"
            "<br>Y(s) → Y(s)/R(s) → G(s) → G_{0}(s)"
            "<li><b>Clic Izquierdo:</b> Abre la ventana de gráficos detallados</li>"
            "<li><b>Pestañas:</b> Permiten alternar entre diferentes vistas del sistema</li>"
            "</ul>"),

            ("<b>Análisis del Sistema:</b>",
            "<ul>"
            "<li><b>Respuesta en Frecuencia:</b> Analizar G(s) para entender el comportamiento frecuencial</li>"
            "<li><b>Relación E/S:</b> Y(s)/R(s) muestra cómo el sistema procesa la entrada</li>"
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
        
    def plot_laplace(self, fdt, title, output):
        """Generar y mostrar el gráfico del dominio de Laplace con la ecuación en LaTeX."""
        s = symbols('s')
        f_laplace = sympify(fdt)
        F_laplace = lambdify(s, f_laplace, 'numpy')

        # Crear figura
        fig = plt.figure(figsize=(10, 6))
        
        ax = plt.subplot2grid((1,1), (0,0))
        
        s_vals = np.linspace(0, 10, 100)
        F_s = F_laplace(s_vals)
        
        # Si F_s es un valor constante, extiéndelo
        if np.isscalar(F_s):
            F_s = np.full_like(s_vals, F_s)

        # Graficar
        plt.plot(s_vals, F_s)
        plt.title(title)
        plt.xlabel("S")
        plt.ylabel(f"${output}$")
        plt.grid(True)
        
        # Convertir la función a LaTeX usando el output proporcionado
        latex_expr = f"{output} = {latex(f_laplace)}"
        
        # Agregar la ecuación en LaTeX debajo del gráfico con tamaño de fuente aumentado
        fig.text(0.5, 0.08, f"${latex_expr}$", 
                horizontalalignment='center', 
                fontsize=30)  # Aumentado de 12 a 16
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.25)
        
        return fig

    def plot_tiempo(self,fdt,title):
        """Generar y mostrar el gráfico del dominio del tiempo, con manejo especial para DiracDelta."""
        t = symbols('t')
        f_tiempo = sympify(fdt)  # Supone que `self.fdt_sympy_tiempo` esté definida
        
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
        plt.title(title)
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