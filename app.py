from mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys
import time

app = QApplication(sys.argv)
window = MainWindow()
window.show()  # 《《《《《《《《《《《普通窗口显示，如需全屏可改为window.showFullScreen()
sys.exit(app.exec())
