# # from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QPushButton
# # from PyQt5.QtCore import pyqtSignal, QTimer
# # from PyQt5.QtWebEngineWidgets import QWebEngineView
# # from PyQt5.QtWebChannel import QWebChannel
# # from sympy import sympify, Symbol, SympifyError
# # import re


# # class LatexEditor(QWidget):
# #     latex_changed = pyqtSignal(str)

# #     def __init__(self, initial_latex="", parent=None):
# #         super().__init__(parent)
# #         self.init_ui(initial_latex)
# #         self.connect_web_signals()

# #     def init_ui(self, initial_latex):
# #         layout = QVBoxLayout()

# #         self.preview_label = QLabel("Vista previa:")
# #         layout.addWidget(self.preview_label)

# #         self.web_view = QWebEngineView()
# #         self.web_view.setFixedHeight(35)
# #         channel = QWebChannel()
# #         self.web_view.page().setWebChannel(channel)
# #         channel.registerObject("latex_editor", self)
        
# #         html_content = """
# # <!DOCTYPE html>
# # <html>
# # <head>
# #     <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML"></script>
# #     <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
# #     <script>
# #         var latex_editor;

# #         MathJax.Hub.Config({
# #             tex2jax: {
# #                 inlineMath: [['$','$'], ['\\(','\\)']],
# #                 processEscapes: true
# #             },
# #             TeX: {
# #                 equationNumbers: { autoNumber: "AMS" },
# #                 extensions: ["AMSmath.js", "AMSsymbols.js"]
# #             },
# #             messageStyle: "none"
# #         });

# #         function updateLatex(latex) {
# #             console.log("updateLatex called with:", latex);
# #             var content = document.getElementById('latex-content');
# #             if (content) {
# #                 content.innerHTML = '$$' + latex + '$$';
# #                 MathJax.Hub.Queue(["Typeset", MathJax.Hub, content]);
# #             } else {
# #                 console.error("Element 'latex-content' not found");
# #             }
# #         }

# #         function initWebChannel() {
# #             new QWebChannel(qt.webChannelTransport, function (channel) {
# #                 latex_editor = channel.objects.latex_editor;
# #                 console.log("QWebChannel initialized");
# #                 if (latex_editor && typeof latex_editor.get_latex === 'function') {
# #                     latex_editor.get_latex(function(initialLatex) {
# #                         console.log("Initial LaTeX:", initialLatex);
# #                         updateLatex(initialLatex);
# #                     });
# #                 } else {
# #                     console.error("latex_editor or get_latex not available");
# #                 }
# #             });
# #         }

# #         document.addEventListener("DOMContentLoaded", initWebChannel);

# #         // Make updateLatex globally accessible
# #         window.updateLatex = updateLatex;
# #     </script>
# # </head>
# # <body>
# #     <div id="latex-content" style="font-size: 16px;"></div>
# # </body>
# # </html>
# #         """
# #         self.web_view.setHtml(html_content)
# #         layout.addWidget(self.web_view)

# #         self.editor = QTextEdit()
# #         self.editor.setFixedHeight(35)
# #         self.editor.setText(initial_latex)
# #         self.editor.textChanged.connect(self.update_preview)
# #         layout.addWidget(self.editor)
        
# #         self.validate_button = QPushButton("Validar Función")
# #         self.validate_button.clicked.connect(self.validar_funcion)
# #         layout.addWidget(self.validate_button)

# #         self.setLayout(layout)

# #     def update_preview(self):
# #         latex = self.editor.toPlainText()
# #         escaped_latex = latex.replace('\\', '\\\\').replace("'", "\\'")
# #         js_code = f"if(window.updateLatex) {{ window.updateLatex('{escaped_latex}'); }} else {{ console.error('updateLatex not available'); }}"
# #         self.web_view.page().runJavaScript(js_code)
# #         self.latex_changed.emit(latex)
        
# #     def connect_web_signals(self):
# #         self.web_view.loadFinished.connect(self.on_load_finished)

# #     def on_load_finished(self, ok):
# #         if ok:
# #             print("Web page loaded successfully")
# #             QTimer.singleShot(500, self.update_preview)  # Delay the initial update
# #         else:
# #             print("Failed to load web page")

# #     def get_latex(self):
# #         return self.editor.toPlainText()

# #     def set_latex(self, latex):
# #         self.editor.setText(latex)
# #         self.update_preview()

# #     def validar_funcion(self):
# #         latex = self.editor.toPlainText()
# #         if self.es_funcion_valida(latex):
# #             self.update_preview()
# #             self.latex_changed.emit(latex)
# #         else:
# #             QMessageBox.warning(self, "Función inválida", "Por favor ingresar una función en el dominio de Laplace.")
# #             self.editor.undo()  

# #     def es_funcion_valida(self, latex):
# #         latex = latex.replace(' ', '').lower()
        
# #         if not latex or latex.count('{') != latex.count('}'):
# #             return False
        
# #         if latex.replace('.', '').isdigit():
# #             return True
        
# #         latex = latex.replace('\\frac', '')  # eliminar \frac
# #         latex = re.sub(r'\{([^}]*)\}\{([^}]*)\}', r'((\1)/(\2))', latex)  # convertir fracciones
# #         latex = latex.replace('^', '**')  # cambiar exponentes
        
# #         s = Symbol('s') # intentar parsear con SymPy
# #         try:
# #             expr = sympify(latex)
            
# #             if 's' not in latex and not expr.is_constant(): # verificar que 's' está en la expresión o es un número constante
# #                 return False
# #             return True
# #         except (SympifyError, TypeError, ValueError):
# #             return False


# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QPushButton
# from PyQt5.QtCore import pyqtSignal, QTimer
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtWebChannel import QWebChannel
# from sympy import sympify, Symbol, SympifyError
# import re


# class LatexEditor(QWidget):
#     latex_changed = pyqtSignal(str)

#     def __init__(self, initial_latex="", parent=None):
#         super().__init__(parent)
#         self.init_ui(initial_latex)
#         self.connect_web_signals()
#         self.validation_timer = QTimer(self)
#         self.validation_timer.setSingleShot(True)
#         self.validation_timer.timeout.connect(self.delayed_validation)

#     def init_ui(self, initial_latex):
#         layout = QVBoxLayout()

#         self.preview_label = QLabel("Vista previa:")
#         layout.addWidget(self.preview_label)

#         self.web_view = QWebEngineView()
#         self.web_view.setFixedHeight(35)
#         channel = QWebChannel()
#         self.web_view.page().setWebChannel(channel)
#         channel.registerObject("latex_editor", self)
        
#         html_content = """
# <!DOCTYPE html>
# <html>
# <head>
#     <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML"></script>
#     <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
#     <script>
#         var latex_editor;

#         MathJax.Hub.Config({
#             tex2jax: {
#                 inlineMath: [['$','$'], ['\\(','\\)']],
#                 processEscapes: true
#             },
#             TeX: {
#                 equationNumbers: { autoNumber: "AMS" },
#                 extensions: ["AMSmath.js", "AMSsymbols.js"]
#             },
#             messageStyle: "none"
#         });

#         function updateLatex(latex) {
#             console.log("updateLatex called with:", latex);
#             var content = document.getElementById('latex-content');
#             if (content) {
#                 content.innerHTML = '$$' + latex + '$$';
#                 MathJax.Hub.Queue(["Typeset", MathJax.Hub, content]);
#             } else {
#                 console.error("Element 'latex-content' not found");
#             }
#         }

#         function initWebChannel() {
#             new QWebChannel(qt.webChannelTransport, function (channel) {
#                 latex_editor = channel.objects.latex_editor;
#                 console.log("QWebChannel initialized");
#                 if (latex_editor && typeof latex_editor.get_latex === 'function') {
#                     latex_editor.get_latex(function(initialLatex) {
#                         console.log("Initial LaTeX:", initialLatex);
#                         updateLatex(initialLatex);
#                     });
#                 } else {
#                     console.error("latex_editor or get_latex not available");
#                 }
#             });
#         }

#         document.addEventListener("DOMContentLoaded", initWebChannel);

#         // Make updateLatex globally accessible
#         window.updateLatex = updateLatex;
#     </script>
# </head>
# <body>
#     <div id="latex-content" style="font-size: 16px;"></div>
# </body>
# </html>
#         """
#         self.web_view.setHtml(html_content)
#         layout.addWidget(self.web_view)

#         self.editor = QTextEdit()
#         self.editor.setFixedHeight(35)
#         self.editor.setText(initial_latex)
#         self.editor.textChanged.connect(self.update_preview)
#         layout.addWidget(self.editor)
        
#         self.editor.textChanged.connect(self.start_validation_timer)
        
#         self.validation_label = QLabel("")
#         self.validation_label.setStyleSheet("font-weight: bold;")
#         layout.addWidget(self.validation_label)

#         self.setLayout(layout)
        
#     def start_validation_timer(self):
#         self.validation_timer.start(1000)  # 1000 ms = 1 segundo de delay

#     def delayed_validation(self):
#         latex = self.editor.toPlainText()
#         if self.es_funcion_valida(latex):
#             self.validation_label.setText("Función válida")
#             self.validation_label.setStyleSheet("color: green; font-weight: bold;")
#             self.update_preview()
#             self.latex_changed.emit(latex)
#         else:
#             self.validation_label.setText("Función inválida")
#             self.validation_label.setStyleSheet("color: red; font-weight: bold;")

#     def update_preview(self):
#         latex = self.editor.toPlainText()
#         escaped_latex = latex.replace('\\', '\\\\').replace("'", "\\'")
#         js_code = f"if(window.updateLatex) {{ window.updateLatex('{escaped_latex}'); }} else {{ console.error('updateLatex not available'); }}"
#         self.web_view.page().runJavaScript(js_code)
#         self.latex_changed.emit(latex)
        
#     def connect_web_signals(self):
#         self.web_view.loadFinished.connect(self.on_load_finished)

#     def on_load_finished(self, ok):
#         if ok:
#             print("Web page loaded successfully")
#             QTimer.singleShot(500, self.update_preview)  # Delay the initial update
#         else:
#             print("Failed to load web page")

#     def get_latex(self):
#         return self.editor.toPlainText()

#     def set_latex(self, latex):
#         self.editor.setText(latex)
#         self.update_preview()

#     def validar_funcion(self):
#         latex = self.editor.toPlainText()
#         if self.es_funcion_valida(latex):
#             self.update_preview()
#             self.latex_changed.emit(latex)
#         else:
#             QMessageBox.warning(self, "Función inválida", "Por favor ingresar una función en el dominio de Laplace.")
#             self.editor.undo()  

#     def es_funcion_valida(self, latex):
#         latex = latex.replace(' ', '').lower()
        
#         if not latex or latex.count('{') != latex.count('}'):
#             return False
        
#         if latex.replace('.', '').isdigit():
#             return True
        
#         latex = latex.replace('\\frac', '')  # eliminar \frac
#         latex = re.sub(r'\{([^}]*)\}\{([^}]*)\}', r'((\1)/(\2))', latex)  # convertir fracciones
#         latex = latex.replace('^', '**')  # cambiar exponentes
        
#         s = Symbol('s') # intentar parsear con SymPy
#         try:
#             expr = sympify(latex)
            
#             if 's' not in latex and not expr.is_constant(): # verificar que 's' está en la expresión o es un número constante
#                 return False
#             return True
#         except (SympifyError, TypeError, ValueError):
#             return False

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QPushButton, QHBoxLayout, QToolButton
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from sympy import sympify, Symbol, SympifyError
import re

class LatexEditor(QWidget):
    latex_changed = pyqtSignal(str)

    def __init__(self, initial_latex="", parent=None):
        super().__init__(parent)
        self.init_ui(initial_latex)
        self.connect_web_signals()
        self.validation_timer = QTimer(self)
        self.validation_timer.setSingleShot(True)
        self.validation_timer.timeout.connect(self.delayed_validation)

    def init_ui(self, initial_latex):
        layout = QVBoxLayout()

        self.preview_label = QLabel("Vista previa:")
        layout.addWidget(self.preview_label)

        self.web_view = QWebEngineView()
        self.web_view.setFixedHeight(75)
        channel = QWebChannel()
        self.web_view.page().setWebChannel(channel)
        channel.registerObject("latex_editor", self)
        
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML"></script>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
        var latex_editor;

        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [['$','$'], ['\\(','\\)']],
                processEscapes: true
            },
            TeX: {
                equationNumbers: { autoNumber: "AMS" },
                extensions: ["AMSmath.js", "AMSsymbols.js"]
            },
            messageStyle: "none"
        });

        function updateLatex(latex) {
            console.log("updateLatex called with:", latex);
            var content = document.getElementById('latex-content');
            if (content) {
                content.innerHTML = '$$' + latex + '$$';
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, content]);
            } else {
                console.error("Element 'latex-content' not found");
            }
        }

        function initWebChannel() {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                latex_editor = channel.objects.latex_editor;
                console.log("QWebChannel initialized");
                if (latex_editor && typeof latex_editor.get_latex === 'function') {
                    latex_editor.get_latex(function(initialLatex) {
                        console.log("Initial LaTeX:", initialLatex);
                        updateLatex(initialLatex);
                    });
                } else {
                    console.error("latex_editor or get_latex not available");
                }
            });
        }

        document.addEventListener("DOMContentLoaded", initWebChannel);

        window.updateLatex = updateLatex;
    </script>
</head>
<body>
    <div id="latex-content" style="font-size: 16px;"></div>
</body>
</html>
        """
        self.web_view.setHtml(html_content)
        layout.addWidget(self.web_view)

        self.editor = QTextEdit()
        self.editor.setFixedHeight(35)
        self.editor.setText(initial_latex)
        self.editor.textChanged.connect(self.update_preview)
        layout.addWidget(self.editor)
        
        self.editor.textChanged.connect(self.start_validation_timer)
        
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.validation_label)

        # Add symbol selector
        symbol_layout = QHBoxLayout()
        symbols = ["\\frac{}{}", "^2", "^3", "√", "∛", "∫", "log", "π", "θ", "∞", "∫", "≥", "≤", "⋅", "÷", "×", "∑", "∏", "()", "[]", "{}"]
        for symbol in symbols:
            button = QToolButton()
            button.setText(symbol if symbol != "\\frac{}{}" else "a/b")
            button.clicked.connect(lambda checked, s=symbol: self.insert_symbol(s))
            symbol_layout.addWidget(button)
        layout.addLayout(symbol_layout)

        self.setLayout(layout)

    def insert_symbol(self, symbol):
        cursor = self.editor.textCursor()
        if symbol == "\\frac{}{}":
            cursor.insertText("\\frac{numerador}{denominador}")
            # Seleccionar "numerador" para que el usuario pueda reemplazarlo fácilmente
            cursor.movePosition(cursor.Left, cursor.KeepAnchor, 9)
        else:
            cursor.insertText(symbol)
        self.editor.setFocus()

    def start_validation_timer(self):
        self.validation_timer.start(1000)  # 1000 ms = 1 segundo de delay

    def delayed_validation(self):
        latex = self.editor.toPlainText()
        if self.es_funcion_valida(latex):
            self.validation_label.setText("Función válida")
            self.validation_label.setStyleSheet("color: green; font-weight: bold;")
            self.update_preview()
            self.latex_changed.emit(latex)
        else:
            self.validation_label.setText("Función inválida")
            self.validation_label.setStyleSheet("color: red; font-weight: bold;")

    def update_preview(self):
        latex = self.editor.toPlainText()
        escaped_latex = latex.replace('\\', '\\\\').replace("'", "\\'")
        js_code = f"if(window.updateLatex) {{ window.updateLatex('{escaped_latex}'); }} else {{ console.error('updateLatex not available'); }}"
        self.web_view.page().runJavaScript(js_code)
        self.latex_changed.emit(latex)
        
    def connect_web_signals(self):
        self.web_view.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            print("Web page loaded successfully")
            QTimer.singleShot(500, self.update_preview)  # Delay the initial update
        else:
            print("Failed to load web page")

    def get_latex(self):
        return self.editor.toPlainText()

    def set_latex(self, latex):
        self.editor.setText(latex)
        self.update_preview()

    def es_funcion_valida(self, latex):
        latex = latex.replace(' ', '').lower()
        
        if not latex or latex.count('{') != latex.count('}'):
            return False
        
        if latex.replace('.', '').isdigit():
            return True
        
        latex = latex.replace('\\frac', '')  # eliminar \frac
        latex = re.sub(r'\{([^}]*)\}\{([^}]*)\}', r'((\1)/(\2))', latex)  # convertir fracciones
        latex = latex.replace('^', '**')  # cambiar exponentes
        
        s = Symbol('s') # intentar parsear con SymPy
        try:
            expr = sympify(latex)
            
            if 's' not in latex and not expr.is_constant(): # verificar que 's' está en la expresión o es un número constante
                return False
            return True
        except (SympifyError, TypeError, ValueError):
            return False