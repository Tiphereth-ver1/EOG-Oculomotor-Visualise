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
            "fixation_duration_s" : 1,
            "reps" : 4,
            "rest" : 1000
                }
    },

    "smooth_pursuit" : {
        "class": Smooth_Pursuit,
        "name" : "Smooth Pursuit", 
        "Description": "Follow the white dot while it is on screen.",
        "params" : {
            "fz" : 0.2,
            "test_duration_s" : 25,
            "shift" : 600,
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
            "reps" : 30,
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
            "reps" : 30
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
            "reps" : 40
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
            "reps" : 20
        }
    },
}

EXPERIMENT_SEQUENCE = [
    "fixation",
    "step_prosaccade",
    "step_prosaccade",
    "gap_prosaccade",
    "gap_prosaccade",
    "overlap_prosaccade",
    "overlap_prosaccade",
    "step_antisaccade",
    "step_antisaccade",
    "smooth_pursuit"
]

class Experiment(QObject):
    event_sent = Signal(dict)
    logger_message = Signal(str)
    show_title = Signal(str)
    show_instruction = Signal(str)
    updating_reps = Signal(int, int)
    updating_exp = Signal(str)
    enable_pause = Signal()
    disable_pause = Signal()
    clear_text = Signal()
    experiment_complete = Signal()
    def __init__(self):
        super().__init__()
        self.trials : list[Trial]= []
        self.current_trial = 0
        self.current_name = ""
        self.countdown = True
        self.rest_timer = QTimer()
        self.rest_timer.timeout.connect(self.update_rest)
        self.test_timer = QTimer()
        self.test_timer.timeout.connect(self.update_test)


        for trial_name in EXPERIMENT_SEQUENCE:
            config = TRIALS[trial_name]
            trial = config["class"](**config["params"])
            self.trials.append(trial)
            trial.finished.connect(self.on_trial_finished)
            trial.sent_message.connect(self.relay_message)
            trial.update_reps.connect(self.update_reps)
            trial.event_generated.connect(self.event_received)
    
    def start(self, fixation, target):
        self.fixation = fixation
        self.target = target

        self.current_trial = 0
        self.start_next_trial()
    
    def on_trial_finished(self):
        self.current_trial += 1

        # Experiment complete
        if self.current_trial >= len(self.trials):
            self.logger_message.emit("Experimental battery complete.")
            self.updating_exp.emit("Complete")
            self.updating_reps.emit(0, 0)
            self.show_title.emit("Complete")
            self.experiment_complete.emit()
            return


        self.rest_remaining = 30

        self.updating_exp.emit("Rest")
        self.updating_reps.emit(0,0)
        self.show_title.emit(str(self.rest_remaining))
        self.logger_message.emit(f"{self.current_name} experiment completed.")
        self.enable_pause.emit()

        self.rest_timer.start(1000)    
    

    def on_instructions_finished(self):
        self.rest_remaining = 3

        self.updating_exp.emit("Preparation")
        self.updating_reps.emit(0,0)
        self.show_title.emit(str(self.rest_remaining))

        self.test_timer.start(1000)    

    
    def relay_message(self, message : str):
        self.logger_message.emit(message)
        print("pinged")
        pass

    def event_received(self, parameters: dict):
        self.event_sent.emit({
            "type" : "STIMULUS",
            "task" : self.current_name,
            "parameters" : parameters
        })


    def start_next_trial(self):
        if self.current_trial >= len(self.trials):
            self.logger_message.emit("Experimental battery complete.")
            return

        config = TRIALS[EXPERIMENT_SEQUENCE[self.current_trial]]
        self.current_name = config["name"]

        self.show_title.emit(self.current_name)

        QTimer.singleShot(
            2000,
            lambda: self.show_instructions(config)
        )

    def show_instructions(self, config):
        self.show_instruction.emit(config["Description"])

        QTimer.singleShot(
            5000,
            self.on_instructions_finished
        )

    def update_reps(self, current, total):
        self.updating_reps.emit(current,total)

    def begin_trial(self):
        self.clear_text.emit()
        trial = self.trials[self.current_trial]
        self.logger_message.emit(f"{self.current_name} experiment started.")
        self.updating_exp.emit(self.current_name)
        trial.start(self.fixation, self.target)
        self.disable_pause.emit()

    def update_rest(self):
        if self.countdown == True:
            self.rest_remaining -= 1

        self.show_title.emit(str(self.rest_remaining))

        if self.rest_remaining == 0:
            self.rest_timer.stop()
            self.start_next_trial()

    def update_test(self):
        if self.countdown == True:
            self.rest_remaining -= 1

        self.show_title.emit(str(self.rest_remaining))

        if self.rest_remaining == 0:
            self.test_timer.stop()
            self.begin_trial()

