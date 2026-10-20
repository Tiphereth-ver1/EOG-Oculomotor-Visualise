import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import unittest
from unittest.mock import Mock
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QAbstractButton
from mainwindow import MainWindow
from Trial import Smooth_Pursuit
from Trial.trial_block import TRIALS
from graphics_page import Stimulus

app = QApplication.instance() or QApplication([])


class ControlsTests(unittest.TestCase):
    def test_space_toggle_and_completion_lock(self):
        window = MainWindow()
        try:
            window.show()
            window.activateWindow()
            window.experiment.toggle_pause = Mock()
            window.enable_pause()
            window.status_btn.setFocus()
            QTest.qWait(50)
            QTest.keyClick(window.status_btn, Qt.Key_Space)
            QTest.keyClick(window.status_btn, Qt.Key_Space)
            self.assertEqual(window.experiment.toggle_pause.call_count, 2)
            self.assertFalse(window.status)  # Space must not click the focused button.
            window.experiment.experiment_complete.disconnect(window.logger.save)
            window.experiment.experiment_complete.emit()
            self.assertTrue(all(not b.isEnabled() for b in window.findChildren(QAbstractButton)))
            self.assertFalse(window.pause_shortcut.isEnabled())
            window.enable_pause()
            window.countdowner()
            self.assertEqual(window.experiment.toggle_pause.call_count, 2)
            self.assertFalse(window.countdown_btn.isEnabled())
        finally:
            window.conn_thread.quit()
            window.conn_thread.wait()
            window.close()

    def test_five_left_and_five_right(self):
        trial = Smooth_Pursuit(**TRIALS["smooth_pursuit"]["params"])
        fixation, target = Stimulus(), Stimulus()
        directions = []
        events = []
        trial.event_generated.connect(events.append)
        try:
            self.assertEqual(trial.reps, 10)
            for index in range(1, 11):
                trial.current_reps = index
                trial.run(fixation, target)
                trial.timer.stop()
                directions.append(trial.initial_direction)
                x, y = trial.position_at(.01)
                self.assertGreater(x if trial.initial_direction == "right" else -x, 0)
            self.assertEqual(directions.count("right"), 5)
            self.assertEqual(directions.count("left"), 5)
            trial.start_time -= trial.test_duration_s + 1
            trial.update_position()
            self.assertEqual(events[-1]["parameters"]["initial_direction"], "left")
        finally:
            trial.cancel_callbacks()
            app.processEvents()


if __name__ == "__main__":
    unittest.main()
