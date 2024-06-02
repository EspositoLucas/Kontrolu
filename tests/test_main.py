# tests/test_main.py
import unittest
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow
import sys

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()

    def test_window_title(self):
        self.assertEqual(self.main_window.windowTitle(), 'Diagramador')

if __name__ == "__main__":
    unittest.main()