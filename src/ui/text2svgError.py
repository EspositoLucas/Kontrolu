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
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import os
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, lambdify,DiracDelta,N,latex

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
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);  /* Sombra de texto para resaltar */
        cursor: pointer;
    }

    QPushButton:hover {
        background-color: #606060;  /* Color un poco más claro al pasar el cursor */
        cursor: pointer;
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
        padding: 12px 30px;  /* Aumentar el padding para más espacio */
        min-width: 140px;   /* Tamaño mínimo para evitar solapamiento */
        font-size: 14px;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-weight: bold;  /* Texto en negrita */
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

class SVGViewError(QGraphicsSvgItem):
    def __init__(self, macro, padre, parent=None):
        super().__init__(parent)
        self.padre = padre
        self.macro = macro

        plt.rc('mathtext', fontset='cm')

        self.renders =[]
        self.graficos = []

        self.error_estado_estable = self.macro.calcular_error_en_estado_estable()
        if self.error_estado_estable.is_real:
            #limitar cantidad de decimales
            self.error_estado_estable = N(self.error_estado_estable, 2)
        self.error_estado_estable_texto = 'e_{ss} = ' + latex(self.error_estado_estable)
        bytess_error_estado_estable = self.tex2svg(self.error_estado_estable_texto)
        self.renderer_error_estado_estable = QSvgRenderer(bytess_error_estado_estable)

        self.renders.append(self.renderer_error_estado_estable)

        self.calculo_simpy = self.macro.obtener_calculo_error_en_estado_estable_simpy()
        if self.calculo_simpy != None:
            self.calculo = self.macro.obtener_calculo_error_en_estado_estable_latex()
            self.calculo_texto = 'lim_{s \\to 0}' + self.calculo + ' = ' + latex(self.error_estado_estable)
            bytess_calculo = self.tex2svg(self.calculo_texto)
            self.renderer_calculo = QSvgRenderer(bytess_calculo)
            self.renders.append(self.renderer_calculo)
            self.graficos.append((self.calculo_simpy,True,'lim_{s \\to 0}'))

        
        
        #self.calculo_tiempo_simpy = self.macro.obtener_calculo_error_en_estado_estable_tiempo()
        self.calculo_tiempo_simpy = None
        if self.calculo_tiempo_simpy != None:
            self.calculo_tiempo = self.macro.obtener_calculo_error_en_estado_estable_latex_tiempo()
            self.calculo_tiempo_texto = 'lim_{t \\to \\infty}' + self.calculo_tiempo + ' = ' + latex(self.error_estado_estable)
            bytess_calculo_tiempo = self.tex2svg(self.calculo_tiempo_texto)
            self.renderer_calculo_tiempo = QSvgRenderer(bytess_calculo_tiempo)
            self.renders.append(self.renderer_calculo_tiempo)
            self.graficos.append((self.calculo_tiempo_simpy,False,'lim_{t \\to \\infty}'))



        if len(self.renders) > 0:
            self.setSharedRenderer(self.renders[0])
            self.elegir = 0
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
        if event.button() == Qt.RightButton:
            self.elegir += 1
            if self.elegir >= len(self.renders):
                self.elegir = 0
            self.setSharedRenderer(self.renders[self.elegir])
            self.padre.error_update_pos()


        if event.button() == Qt.LeftButton:
            self.open_graph_window(self.elegir)
        # Llamar al método base para manejar otros eventos
        super().mousePressEvent(event)

    def open_graph_window(self, cual):
        if len(self.graficos) == 0:
            return
        
        dialog = QDialog()
        dialog.setWindowTitle("Dominio de Laplace")
        dialog.setStyleSheet(ESTILO)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Configurar el icono
        path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(path, 'base','imgs', 'logo.png')
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
                cursor: pointer;
            }
        """)
        

        tab_widget = QTabWidget()

        for fdt, is_laplace, title in self.graficos:
            # Crear la pestaña para el dominio de Laplace
            laplace_tab = QLabel()
            if is_laplace:
                laplace_pixmap = self.get_plot_pixmap(self.plot_laplace(fdt))
            else:
                laplace_pixmap = self.get_plot_pixmap(self.plot_tiempo(fdt))
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
        image_path = os.path.join(path, 'base','imgs', 'logo.png')
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
            ("<b>Visualización del Error en Estado Estable:</b>",
         "Esta ventana permite analizar el error en estado estable del sistema de control en el dominio de Laplace."),
        
        ("<b>Representaciones Disponibles:</b>",
         "<ul>"
         "<li><b>e_ss:</b> Error en estado estable en el dominio de Laplace</li>"
         "<li><b>lim_{s->0} (G(s)):</b> Representación algebraica del error en estado estable en Laplace</li>"
         "</ul>"),
        
        ("<b>Interpretación de Gráficos:</b>",
         "<ul>"
         "<li><b>Dominio de Laplace:</b> Muestra el valor del error en estado estable y su cálculo algebraico</li>"
         "</ul>"),
        
        ("<b>Navegación e Interacción:</b>",
         "<ul>"
         "<li><b>Clic Derecho:</b> Alterna entre las diferentes representaciones del error en estado estable</li>"
         "<li><b>Clic Izquierdo:</b> Abre una ventana con gráficos detallados de las representaciones</li>"
         "<li><b>Pestañas:</b> Permiten cambiar entre las diferentes vistas de la visualización</li>"
         "</ul>"),
        
        ("<b>Análisis del Error en Estado Estable:</b>",
         "<ul>"
         "<li><b>Valor Numérico:</b> Consultar el valor exacto del error en estado estable</li>"
         "<li><b>Cálculo Algebraico:</b> Examinar la expresión matemática que define el error</li>"
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