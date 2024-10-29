from PyQt5.QtWidgets import  QApplication
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from io import BytesIO
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import ( QApplication, 
                              QDialog, QVBoxLayout, QTabWidget, QLabel)
from PyQt5.QtSvg import QSvgRenderer, QGraphicsSvgItem
from PyQt5.QtCore import Qt
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify,DiracDelta


class SVGView(QGraphicsSvgItem):
    def __init__(self, macro, parent=None):
        super().__init__(parent)
        self.macro = macro
        self.laplace = "Y(s) = " + self.macro.obtener_fdt_con_entrada_latex()
        self.tiempo = "y(t) = " + self.macro.obtener_fdt_con_entrada_latex_tiempo()
        self.total_laplace = "\\frac{Y(s)}{R(s)} = " + self.macro.obtener_fdt_global_latex()
        self.total_tiempo = "\\frac{y(s)}{r(t)} = " + self.macro.obtener_fdt_global_latex_tiempo()
        self.global_laplace = "G(s) = " + self.macro.obtener_fdt_global_latex()
        self.global_tiempo = "g(t) = " + self.macro.obtener_fdt_global_latex_tiempo()

        self.fdt_sympy_laplace = self.macro.obtener_fdt_con_entrada_simpy()
        self.fdt_sympy_tiempo = self.macro.obtener_fdt_con_entrada_tiempo()
        self.fdt_sympy_laplace_total = self.macro.obtener_fdt_global_simpy()
        self.fdt_sympy_tiempo_total = self.macro.obtener_fdt_global_tiempo()
        self.fdt_sympy_global_laplace = self.macro.obtener_fdt_global_simpy()
        self.fdt_sympy_global_tiempo = self.macro.obtener_fdt_global_tiempo()

        # Configurar matplotlib para usar la fuente Computer Modern
        plt.rc('mathtext', fontset='cm')
        
        # Generar el SVG a partir de la fórmula LaTeX
        bytess_laplace = self.tex2svg(self.laplace)
        bytess_tiempo = self.tex2svg(self.tiempo)
        bytess_laplace_total = self.tex2svg(self.total_laplace)
        bytess_tiempo_total = self.tex2svg(self.total_tiempo)
        bytess_global_laplace = self.tex2svg(self.global_laplace)
        bytess_global_tiempo = self.tex2svg(self.global_tiempo)
        
        # Cargar el SVG en el renderer
        self.renderer_laplace = QSvgRenderer(bytess_laplace)
        self.renderer_tiempo = QSvgRenderer(bytess_tiempo)
        self.renderer_laplace_total = QSvgRenderer(bytess_laplace_total)
        self.renderer_tiempo_total = QSvgRenderer(bytess_tiempo_total)
        self.renderer_global_laplace = QSvgRenderer(bytess_global_laplace)
        self.renderer_global_tiempo = QSvgRenderer(bytess_global_tiempo)

        self.laplace_mode = 0
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
            self.open_graph_window(self.laplace_mode)
        if event.button() == Qt.RightButton:
            print("Clic derecho detectado en SVG.")
            if self.laplace_mode == 0:
                self.laplace_mode = 1
                self.setSharedRenderer(self.renderer_tiempo)
            elif self.laplace_mode == 1:
                self.laplace_mode = 2
                self.setSharedRenderer(self.renderer_laplace_total)
            elif self.laplace_mode == 2:
                self.laplace_mode = 3
                self.setSharedRenderer(self.renderer_tiempo_total)
            elif self.laplace_mode == 3:
                self.laplace_mode = 4
                self.setSharedRenderer(self.renderer_global_laplace)
            elif self.laplace_mode == 4:
                self.laplace_mode = 5
                self.setSharedRenderer(self.renderer_global_tiempo)
            elif self.laplace_mode == 5:
                self.laplace_mode = 0
                self.setSharedRenderer(self.renderer_laplace)
        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)

    def open_graph_window(self, cual):
        dialog = QDialog()
        dialog.setWindowTitle("Dominio de Laplace y Dominio de Tiempo")
        layout = QVBoxLayout()

        tab_widget = QTabWidget()

        # Crear la pestaña para el dominio de Laplace
        laplace_tab = QLabel()
        laplace_pixmap = self.get_plot_pixmap(self.plot_laplace(self.fdt_sympy_laplace))
        laplace_tab.setPixmap(laplace_pixmap)
        tab_widget.addTab(laplace_tab, "Y(s)")

        # Crear la pestaña para el dominio de tiempo
        tiempo_tab = QLabel()
        tiempo_pixmap = self.get_plot_pixmap(self.plot_tiempo(self.fdt_sympy_tiempo))
        tiempo_tab.setPixmap(tiempo_pixmap)
        tab_widget.addTab(tiempo_tab, "y(t)")

        # Crear la pestaña para el dominio de Laplace
        laplace_tab = QLabel()
        laplace_pixmap = self.get_plot_pixmap(self.plot_laplace(self.fdt_sympy_laplace_total))
        laplace_tab.setPixmap(laplace_pixmap)
        tab_widget.addTab(laplace_tab, "Y(s)/R(s)")

        # Crear la pestaña para el dominio de tiempo
        tiempo_tab = QLabel()
        tiempo_pixmap = self.get_plot_pixmap(self.plot_tiempo(self.fdt_sympy_tiempo_total))
        tiempo_tab.setPixmap(tiempo_pixmap)
        tab_widget.addTab(tiempo_tab, "y(t)/r(t)")

        laplace_tab = QLabel()
        laplace_pixmap = self.get_plot_pixmap(self.plot_laplace(self.fdt_sympy_global_laplace))
        laplace_tab.setPixmap(laplace_pixmap)
        tab_widget.addTab(laplace_tab, "G(s)")

        # Crear la pestaña para el dominio de tiempo
        tiempo_tab = QLabel()
        tiempo_pixmap = self.get_plot_pixmap(self.plot_tiempo(self.fdt_sympy_global_tiempo))
        tiempo_tab.setPixmap(tiempo_pixmap)
        tab_widget.addTab(tiempo_tab, "g(t)")

        # Seleccionar la pestaña activa dependiendo del valor de `cual`
        tab_widget.setCurrentIndex(cual)

        layout.addWidget(tab_widget)
        dialog.setLayout(layout)
        dialog.exec_()

    def get_plot_pixmap(self, figure):
        """Convierte una figura de matplotlib en un QPixmap."""
        buf = BytesIO()
        figure.savefig(buf, format="png")
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        buf.close()
        return pixmap
        
    def plot_laplace(self,fdt):
        """Generar y mostrar el gráfico del dominio de Laplace."""
        s = symbols('s')
        f_laplace = sympify(fdt)  # Asegúrate de que `self.fdt_sympy_laplace` esté definida
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

    def plot_tiempo(self,fdt):
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