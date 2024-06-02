# tests/test_drawing_area.py
import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QPoint

# Agregar la ruta del módulo src a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.ui.drawing_area import DrawingArea

class TestDrawingArea(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        self.drawing_area = DrawingArea()
        self.drawing_area.show()
    
    def tearDown(self):
        self.drawing_area.close()
    
    # Agregar Tests de DrawingArea

if __name__ == '__main__':
    unittest.main()
