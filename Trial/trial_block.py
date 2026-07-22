from .trajectories import (
    circle,
    figure8,
    horizontal_sinusoid,
)

from PySide6.QtCore import Qt, QTimer, QObject, Signal
from . import (Trial, Step_Prosaccade, Smooth_Pursuit, 
Overlap_Prosaccade, Gap_Prosaccade, Fixation)


TRIALS = {
    "fixation" : {
        "class": Fixation,
        "name" : "Fixation", 
        "Description": "Focus on the white dot while it is on screen.",
        "params" : {
            "fixation_duration_s" : 10,
            "reps" : 4,
            "rest" : 5000
                }
    },

    "smooth_pursuit" : {
        "class": Smooth_Pursuit,
        "name" : "Smooth Pursuit", 
        "Description": "Follow the white dot while it is on screen.",
        "params" : {
            "fz" : 0.2,
            "test_duration_s" : 25,
            "shift" : 400,
            "trajectory" : horizontal_sinusoid,
            "reps" : 4,
            "rest" : 5000
                }
    },
    "gap_prosaccade" : {
        "class": Gap_Prosaccade,
        "name" : "Gap Prosaccade", 
        "Description": "Focus on the yellow dot, and "
                        "look at the white dot when it appears. "
                        "The yellow dot will disappear before the white dot.",
        "params" : {
            "fixation_min" : 500,
            "fixation_max" : 2000,
            "gap" : 200,
            "target_duration" : 1000,
            "shift" : 400,
            "reps" : 60,
        }
    },

    "step_prosaccade" : {
        "class": Step_Prosaccade,
        "name" : "Step Prosaccade", 
        "Description": "Focus on the yellow dot, and "
                        "look at the white dot when it appears. ",
        "params" : {
            "fixation_min" : 500,
            "fixation_max" : 2000,
            "target_duration" : 1000,
            "shift" : 400,
            "reps" : 60
            }
    },

    "overlap_prosaccade" : {
        "class": Overlap_Prosaccade,
        "name" : "Overlap Prosaccade", 
        "Description": "Focus on the yellow dot, and look at "
                        "the white dot when it appears. "
                        "The yellow dot will not disappear.",
        "params" : {
            "fixation_min" : 500,
            "fixation_max" : 2000,
            "target_duration" : 1000,
            "shift" : 400,
            "reps" : 60
        }
    },

    "step_antisaccade" : {
        "class": Step_Prosaccade,
        "name" : "Step Antisaccade", 
        "Description": "Focus on the yellow dot, and look in the opposite "
                        "direction to the white dot when it appears.",
        "params" : {
            "fixation_min" : 500,
            "fixation_max" : 2000,
            "target_duration" : 1000,
            "shift" : 400,
            "reps" : 40
        }
    },
}

EXPERIMENT_SEQUENCE = [
    "fixation",
    "step_prosaccade",
    "gap_prosaccade",
    "overlap_prosaccade",
    "step_antisaccade",
    "smooth_pursuit"
]

class Experiment(QObject):
    logger_message = Signal(str)
    show_title = Signal(str)
    show_instruction = Signal(str)
    clear_text = Signal()
    def __init__(self):
        super().__init__()
        self.trials : list[Trial]= []
        self.current_trial = 0
        self.current_name = ""

        for trial_name in EXPERIMENT_SEQUENCE:
            config = TRIALS[trial_name]
            trial = config["class"](**config["params"])
            self.trials.append(trial)
            trial.finished.connect(self.on_trial_finished)
            trial.sent_message.connect(self.relay_message)
    
    def start(self, fixation, target):
        self.fixation = fixation
        self.target = target

        self.current_trial = 0
        self.start_next_trial()
    
    def on_trial_finished(self):
        self.current_trial += 1
        QTimer.singleShot(
            60000,
            self.start_next_trial
        )
        self.logger_message.emit(f"{self.current_name} experiment completed.")
        self.show_title.emit("Rest")
    
    
    def relay_message(self, message : str):
        self.logger_message.emit(message)
        print("pinged")
        pass

    def start_next_trial(self):
        if self.current_trial >= len(self.trials):
            self.logger_message.emit("Experimental battery complete.")
            return

        config = TRIALS[EXPERIMENT_SEQUENCE[self.current_trial]]
        self.current_name = config["name"]

        self.show_title.emit(self.current_name)

        QTimer.singleShot(
            3000,
            lambda: self.show_instructions(config)
        )

    def show_instructions(self, config):
        self.show_instruction.emit(config["Description"])

        QTimer.singleShot(
            7000,
            self.begin_trial
        )

    def begin_trial(self):
        self.clear_text.emit()
        trial = self.trials[self.current_trial]
        self.logger_message.emit(f"{self.current_name} experiment started.")
        trial.start(self.fixation, self.target)
