from mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys
import time

app = QApplication(sys.argv)
window = MainWindow()
window.show()  # CONFIG: Show a normal window; use window.showFullScreen() for full screen.
sys.exit(app.exec())
