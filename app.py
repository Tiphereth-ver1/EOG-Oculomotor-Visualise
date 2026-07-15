from mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys
import time

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("Ringo Music")
window.show()

from PySide6.QtCore import QTimer

# timer = QTimer()
# timer.timeout.connect(window.send_signal)
# timer.start(50000)
# window.send_signal()
sys.exit(app.exec())
