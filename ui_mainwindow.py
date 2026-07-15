from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
from graphics_page import Graphics_Page

class Ui_MainWindow(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.graphics_page = Graphics_Page(self)
        self.layout.addWidget(self.graphics_page)