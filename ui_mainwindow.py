"""Load the Designer form without generating or overwriting Python code."""

from pathlib import Path

from PySide6.QtCore import QDir, QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDockWidget, QLabel, QPushButton, QTextEdit, QWidget, QLineEdit, QSpinBox, QComboBox

from graphics_page import Graphics_Page


class _MainWindowLoader(QUiLoader):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.registerCustomWidget(Graphics_Page)

    def createWidget(self, class_name, parent=None, name=""):
        # Populate the existing MainWindow so its signals and key events stay active.
        if parent is None:
            if class_name != "QMainWindow":
                raise ValueError("mainwindow.ui must have a QMainWindow root.")
            self.window.setObjectName(name)
            return self.window
        return super().createWidget(class_name, parent, name)


class Ui_MainWindow:
    def setupUi(self, window):
        ui_path = Path(__file__).resolve().with_name("mainwindow.ui")  # 《《《《《《《《《《《运行时直接加载此UI，修改界面无需生成Python代码
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Cannot open {ui_path}: {ui_file.errorString()}")

        loader = _MainWindowLoader(window)
        loader.setWorkingDirectory(QDir(str(ui_path.parent)))
        try:
            loaded_window = loader.load(ui_file)
        finally:
            ui_file.close()
        if loaded_window is None:
            raise RuntimeError(f"Cannot load {ui_path}: {loader.errorString()}")

        # These object names are the interface between the form and controller.
        controls = {
            "subject_group": QWidget,
            "subject_id_input": QLineEdit,
            "subject_name_input": QLineEdit,
            "age_input": QSpinBox,
            "cdr_input": QComboBox,
            "gender_input": QComboBox,
            "graphics": Graphics_Page,
            "dock": QDockWidget,
            "info": QWidget,
            "current_experiment": QLabel,
            "reps_count": QLabel,
            "expt_btn": QPushButton,
            "countdown_btn": QPushButton,
            "connect_btn": QPushButton,
            "status_btn": QPushButton,
            "status_box": QTextEdit,
        }
        for name, widget_type in controls.items():
            widget = window.findChild(widget_type, name)
            if widget is None:
                raise RuntimeError(f"{ui_path} is missing {widget_type.__name__} '{name}'.")
            setattr(self, name, widget)
            setattr(window, name, widget)

        self.graphics.apply_ui_properties()
