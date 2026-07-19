from mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys
import time

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("EOG Oculomotor Visualise")
window.show()
sys.exit(app.exec())
