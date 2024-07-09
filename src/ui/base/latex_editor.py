from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

class LatexEditor(QWidget):
    latex_changed = pyqtSignal(str)

    def __init__(self, initial_latex="", parent=None):
        super().__init__(parent)
        self.init_ui(initial_latex)

    def init_ui(self, initial_latex):
        layout = QVBoxLayout()

        self.preview_label = QLabel("Funcion de Transferencia")
        layout.addWidget(self.preview_label)

        self.web_view = QWebEngineView()
        channel = QWebChannel()
        self.web_view.page().setWebChannel(channel)
        channel.registerObject("latex_editor", self)
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS_HTML"></script>
            <script>
                MathJax.Hub.Config({
                    tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
                });
                new QWebChannel(qt.webChannelTransport, function (channel) {
                    window.latex_editor = channel.objects.latex_editor;
                });
                function updateLatex(latex) {
                    document.getElementById('latex-content').innerHTML = latex;
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
                }
            </script>
        </head>
        <body>
            <div id="latex-content"></div>
        </body>
        </html>
        """
        self.web_view.setHtml(html_content)
        layout.addWidget(self.web_view)

        self.editor = QTextEdit()
        self.editor.setText(initial_latex)
        self.editor.textChanged.connect(self.update_preview)
        layout.addWidget(self.editor)

        self.setLayout(layout)

        self.update_preview()

    def update_preview(self):
        latex = self.editor.toPlainText()
        self.web_view.page().runJavaScript(f"updateLatex('${latex}$');")
        self.latex_changed.emit(latex)

    def get_latex(self):
        return self.editor.toPlainText()

    def set_latex(self, latex):
        self.editor.setText(latex)