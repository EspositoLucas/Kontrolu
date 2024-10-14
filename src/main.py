import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from back.sesion import Sesion

def main():
    app = QApplication(sys.argv) 
    sesion = Sesion()
    main_window = MainWindow(sesion)
    # main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()