from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel, QMessageBox, QPushButton, QHBoxLayout, QToolButton
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from sympy import sympify, Symbol, SympifyError,Expr
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
        symbols = ["\\frac{}{}", "^2", "^3", "\sqrt[n]{x}","\\frac{d}{dx}", "∫","\int_{inf}^{sup}", "log","ln", "e","\lim_{x \\to 0}","sin","cos","tan","cot","cst","sec","∞", "π", "θ", ">", "<", "≥", "≤", "⋅", "÷", "×", "∑", "∏", "()", "[]","\{  \}"]
        for symbol in symbols:
            button = QToolButton()
            if symbol == "\\frac{}{}":
                button.setText("a/b")
            elif symbol == "\\sqrt[n]{x}":
                button.setText("√ₙ(x)")
            elif symbol == "\\int_{inf}^{sup}":
                button.setText("∫ definida")
            elif symbol == "\\frac{d}{dx}":
                button.setText("d/dx")
            elif symbol == "\lim_{x \\to 0}":
                button.setText("lim")
            elif symbol == "\{  \}":
                button.setText("{}")
            else:
                button.setText(symbol)
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
        
        # Reemplazar símbolos problemáticos
        latex = latex.replace('\\frac', '')  # eliminar \frac
        latex = re.sub(r'\{([^}]*)\}\{([^}]*)\}', r'((\1)/(\2))', latex)  # convertir fracciones
        latex = latex.replace('^', '**')  # cambiar exponentes
        latex = latex.replace('()', '(x)')  # reemplazar paréntesis vacíos
        latex = latex.replace('[]', '[x]')  # reemplazar corchetes vacíos
        latex = latex.replace('{}', '{x}')  # reemplazar llaves vacías
        
        s = Symbol('s')
        try:
            expr = sympify(latex, locals={'s': s})
            
            if isinstance(expr, (dict, list, tuple)):
                return False
            
            if not isinstance(expr, Expr):
                return False
            
            if 's' not in latex and not expr.is_constant():
                return False
            
            return True
        except (SympifyError, TypeError, ValueError):
            return False