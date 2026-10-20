import json
import os
from pathlib import Path
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication, QMainWindow
from data_logger import Data_Logger
from ui_mainwindow import Ui_MainWindow

app = QApplication.instance() or QApplication([])


class SubjectRecordsTests(unittest.TestCase):
    def test_form_loads_and_inputs_work(self):
        window = QMainWindow()
        Ui_MainWindow().setupUi(window)
        window.subject_id_input.setText("01")
        window.subject_name_input.setText("Zhang San")
        window.age_input.setValue(65)
        window.cdr_input.setCurrentText("0.5")
        window.gender_input.setCurrentText("女")
        window.show()
        app.processEvents()
        self.assertTrue(window.subject_group.isVisible())
        self.assertEqual(window.subject_id_input.text(), "01")
        self.assertEqual(window.subject_name_input.text(), "Zhang San")
        self.assertEqual(window.cdr_input.currentText(), "0.5")
        window.close()

    def test_header_filename_and_metadata(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as folder:
            logger = Data_Logger()
            self.assertIsNone(logger.file)
            logger.output_dir = Path(folder)
            info = {"subject_id": "01", "subject_name": "Zhang San", "age": 65, "cdr": 0.5, "gender": "女"}
            logger.init_main_data(info)
            logger.write_message("Experimental battery started.")
            logger.save()
            logger.close_logger()
            self.assertRegex(logger.txt_path.name, r"^Subject01-\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.txt$")
            lines = logger.txt_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], "被试编号: 01 | 姓名（英文）: Zhang San | 年龄: 65 | CDR等级: 0.5 | 性别: 女")
            self.assertIn("Experimental battery started.", lines[1])
            session = json.loads(logger.json_path.read_text(encoding="utf-8"))["session"]
            for key, value in info.items():
                self.assertEqual(session[key], value)


if __name__ == "__main__":
    unittest.main()
