# tests/test_main.py
import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.ui.main_window import MainWindow

class TestWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        self.main_window = MainWindow()
        self.main_window.show()
    
    def tearDown(self):
        self.main_window.close()
    
    def test_window_initialization(self):
        self.assertTrue(self.main_window.isVisible())

if __name__ == '__main__':
    unittest.main()