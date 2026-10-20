import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest
from datetime import datetime
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest

from graphics_page import Stimulus
from Trial import Experiment, Fixation, Step_Prosaccade, Gap_Prosaccade, Overlap_Prosaccade, Smooth_Pursuit
from Trial.trajectories import horizontal_sinusoid
from data_logger import Data_Logger

app = QApplication.instance() or QApplication([])


class PauseTests(unittest.TestCase):
    def setUp(self):
        self.experiments = []

    def tearDown(self):
        for exp in self.experiments:
            for trial in exp.trials:
                trial.cancel_callbacks()
        QTest.qWait(1)

    def make_experiment(self, trial):
        exp = Experiment()
        self.experiments.append(exp)
        exp._configured_trials = exp.trials
        exp.trials = [trial]
        exp.current_name = "test task"
        exp.fixation, exp.target = Stimulus(), Stimulus()
        exp.phase = "task"
        trial.finished.connect(exp.on_trial_finished)
        trial.start(exp.fixation, exp.target)
        return exp

    def test_all_tasks_skip_and_cancel_old_callbacks(self):
        factories = [
            lambda: Fixation(10, 30, 100),
            lambda: Step_Prosaccade(10, 11, 10, 100, 30),
            lambda: Gap_Prosaccade(10, 11, 10, 10, 100, 30),
            lambda: Overlap_Prosaccade(10, 11, 10, 100, 30),
            lambda: Smooth_Pursuit(.2, 10, 100, horizontal_sinusoid, 30, 100),
        ]
        for factory in factories:
            with self.subTest(task=factory):
                trial = factory()
                exp = self.make_experiment(trial)
                events = []
                exp.event_sent.connect(events.append)
                trial.current_reps = 21
                exp.toggle_pause()
                self.assertFalse(exp.fixation.isVisible())
                self.assertFalse(exp.target.isVisible())
                QTest.qWait(80)
                self.assertEqual(trial.current_reps, 21)
                self.assertFalse(exp.fixation.isVisible())
                self.assertFalse(exp.target.isVisible())
                exp.toggle_pause()
                self.assertEqual(trial.current_reps, 22)
                self.assertEqual(len(events), 1)
                self.assertEqual(events[0]["type"], "trial pause")
                self.assertEqual(events[0]["trial"], 21)
                self.assertLessEqual(events[0]["start_time"], events[0]["end_time"])
                trial.cancel_callbacks()

    def test_saccade_target_and_gap_phases(self):
        for trial, wait in [(Step_Prosaccade(1, 2, 500, 100, 3), 30),
                            (Gap_Prosaccade(1, 2, 500, 500, 100, 3), 30),
                            (Overlap_Prosaccade(1, 2, 500, 100, 3), 30)]:
            exp = self.make_experiment(trial)
            QTest.qWait(wait)
            exp.toggle_pause()
            QTest.qWait(550)
            self.assertEqual(trial.current_reps, 1)
            self.assertFalse(exp.target.isVisible())
            exp.toggle_pause()
            self.assertEqual(trial.current_reps, 2)
            trial.cancel_callbacks()

    def test_rest_pause_has_no_event_and_preserves_next_trial(self):
        trial = Fixation(10, 3, 80)
        exp = self.make_experiment(trial)
        trial.timer.stop()
        trial.clean_graphics()
        events = []
        exp.event_sent.connect(events.append)
        exp.toggle_pause()
        QTest.qWait(120)
        self.assertEqual(trial.current_reps, 1)
        exp.toggle_pause()
        QTest.qWait(120)
        self.assertEqual(trial.current_reps, 2)
        self.assertEqual(events, [])
        trial.cancel_callbacks()
        exp.phase = "rest"
        exp.rest_remaining = 30
        exp.toggle_pause()
        exp.update_rest()
        self.assertEqual(exp.rest_remaining, 30)
        exp.toggle_pause()
        exp.update_rest()
        self.assertEqual(exp.rest_remaining, 29)
        self.assertEqual(events, [])

    def test_last_trial_completes_and_logger_keeps_interval(self):
        trial = Fixation(10, 1, 80)
        exp = self.make_experiment(trial)
        logger = Data_Logger.__new__(Data_Logger)
        logger.start = datetime.now()
        logger.main_data = {"events": []}
        exp.event_sent.connect(logger.add_event)
        completed = []
        exp.experiment_complete.connect(lambda: completed.append(True))
        exp.toggle_pause()
        exp.toggle_pause()
        self.assertEqual(completed, [True])
        self.assertEqual(exp.phase, "idle")
        event = logger.main_data["events"][0]
        self.assertEqual(event["type"], "trial pause")
        self.assertIn("start_time", event)
        self.assertIn("end_time", event)


if __name__ == "__main__":
    unittest.main()
