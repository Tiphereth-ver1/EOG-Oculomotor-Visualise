from .trajectories import (
    circle,
    figure8,
    horizontal_sinusoid,
)

from PySide6.QtCore import Qt, QTimer, QObject, Signal
from datetime import datetime
from . import (Trial, Step_Prosaccade, Smooth_Pursuit, 
Overlap_Prosaccade, Gap_Prosaccade, Fixation)


TRIALS = {  # CONFIG: Central experiment configuration: edit names, participant instructions, and stimulus parameters here.
    "fixation" : {
        "class": Fixation,  # CONFIG: Stimulus implementation class for this block.
        "name" : "Fixation",  # CONFIG: Block name displayed in the central title and sidebar.
        "Description": "Please look at the white dot until it disappears.",  # CONFIG: Participant instructions; adjacent strings concatenate automatically. Update color references when changing colors.
        "params" : {
            "fixation_duration_s" : 1,  # CONFIG: Fixation duration per repetition in seconds; see fixation.py for the check interval.
            "reps" : 10,  # CONFIG: Repetitions per block; each occurrence of a repeated block runs this many repetitions.
            "rest" : 1000  # CONFIG: Blank-screen rest after each repetition in milliseconds, including the last; separate from rest between blocks.
                }
    },

    "smooth_pursuit" : {
        "class": Smooth_Pursuit,  # CONFIG: Stimulus implementation class for this block.
        "name" : "Smooth Pursuit",  # CONFIG: Block name displayed in the central title and sidebar.
        "Description": "Please look at the white dot on the screen and follow it with your eyes as it moves.",  # CONFIG: Participant instructions; adjacent strings concatenate automatically. Update color references when changing colors.
        "params" : {
            "fz" : 0.2,  # CONFIG: Pursuit frequency in Hz; 0.2 means a five-second cycle.
            "test_duration_s" : 25,  # CONFIG: Smooth pursuit duration per repetition in seconds.
            "shift" : 600,  # CONFIG: Target displacement or pursuit amplitude in scene units, rather than dot diameter.
            "trajectory" : horizontal_sinusoid,  # CONFIG: Pursuit trajectory: horizontal_sinusoid, circle, or figure8.
            "reps" : 10,  # CONFIG: Repetitions per block; each occurrence of a repeated block runs this many repetitions.
            "rest" : 5000  # CONFIG: Blank-screen rest after each repetition in milliseconds, including the last; separate from rest between blocks.
                }
    },
    "gap_prosaccade" : {
        "class": Gap_Prosaccade,  # CONFIG: Stimulus implementation class for this block.
        "name" : "Gap Prosaccade",  # CONFIG: Block name displayed in the central title and sidebar.
        "Description": "Look at the yellow dot. When the white dot appears, look toward it. "  # CONFIG: Participant instructions; adjacent strings concatenate automatically. Update color references when changing colors.
                        "The yellow dot will disappear before the white dot appears.",
        "params" : {
            "fixation_min" : 500,  # CONFIG: Inclusive lower bound for random central fixation duration in milliseconds.
            "fixation_max" : 2000,  # CONFIG: Exclusive upper bound for random central fixation duration in milliseconds; must exceed the lower bound.
            "gap" : 200,  # CONFIG: Blank interval between central fixation offset and peripheral target onset in milliseconds.
            "target_duration" : 1000,  # CONFIG: Peripheral target display duration in milliseconds.
            "shift" : 400,  # CONFIG: Target displacement or pursuit amplitude in scene units, rather than dot diameter.
            "reps" : 15,  # CONFIG: Repetitions per block; each occurrence of a repeated block runs this many repetitions.
        }
    },

    "step_prosaccade" : {
        "class": Step_Prosaccade,  # CONFIG: Stimulus class for this block; antisaccades reuse this class with instructions to look in the opposite direction.
        "name" : "Step Prosaccade",  # CONFIG: Block name displayed in the central title and sidebar.
        "Description": "Look at the yellow dot. When the white dot appears, "  # CONFIG: Participant instructions; adjacent strings concatenate automatically. Update color references when changing colors.
                        "look toward the white dot.",
        "params" : {
            "fixation_min" : 500,  # CONFIG: Inclusive lower bound for random central fixation duration in milliseconds.
            "fixation_max" : 2000,  # CONFIG: Exclusive upper bound for random central fixation duration in milliseconds; must exceed the lower bound.
            "target_duration" : 1000,  # CONFIG: Peripheral target display duration in milliseconds.
            "shift" : 400,  # CONFIG: Target displacement or pursuit amplitude in scene units, rather than dot diameter.
            "reps" : 15  # CONFIG: Repetitions per block; each occurrence of a repeated block runs this many repetitions.
            }
    },

    "overlap_prosaccade" : {
        "class": Overlap_Prosaccade,  # CONFIG: Stimulus implementation class for this block.
        "name" : "Overlap Prosaccade",  # CONFIG: Block name displayed in the central title and sidebar.
        "Description": "Look at the yellow dot. When the white dot appears, "  # CONFIG: Participant instructions; adjacent strings concatenate automatically. Update color references when changing colors.
                        "look toward the white dot. "
                        "The yellow dot will remain visible.",
        "params" : {
            "fixation_min" : 500,  # CONFIG: Inclusive lower bound for random central fixation duration in milliseconds.
            "fixation_max" : 2000,  # CONFIG: Exclusive upper bound for random central fixation duration in milliseconds; must exceed the lower bound.
            "target_duration" : 1000,  # CONFIG: Peripheral target display duration in milliseconds.
            "shift" : 400,  # CONFIG: Target displacement or pursuit amplitude in scene units, rather than dot diameter.
            "reps" : 15  # CONFIG: Repetitions per block; each occurrence of a repeated block runs this many repetitions.
        }
    },

    "step_antisaccade" : {
        "class": Step_Prosaccade,  # CONFIG: Stimulus class for this block; antisaccades reuse this class with instructions to look in the opposite direction.
        "name" : "Step Antisaccade",  # CONFIG: Block name displayed in the central title and sidebar.
        "Description": "Look at the yellow dot. When the white dot appears, "  # CONFIG: Participant instructions; adjacent strings concatenate automatically. Update color references when changing colors.
                        "look in the direction opposite to the white dot.",
        "params" : {
            "fixation_min" : 500,  # CONFIG: Inclusive lower bound for random central fixation duration in milliseconds.
            "fixation_max" : 2000,  # CONFIG: Exclusive upper bound for random central fixation duration in milliseconds; must exceed the lower bound.
            "target_duration" : 1000,  # CONFIG: Peripheral target display duration in milliseconds.
            "shift" : 400,  # CONFIG: Target displacement or pursuit amplitude in scene units, rather than dot diameter.
            "reps" : 15  # CONFIG: Repetitions per block; each occurrence of a repeated block runs this many repetitions.
        }
    },
}

EXPERIMENT_SEQUENCE = [  # CONFIG: Block execution order; add, remove, or reorder entries. Repeated entries run the entire block again.
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
    pause_changed = Signal(bool)
    def __init__(self):
        super().__init__()
        self.trials : list[Trial]= []
        self.current_trial = 0
        self.current_name = ""
        self.phase = "idle"
        self.paused = False
        self.pause_event = None
        self.countdown = True  # CONFIG: Start with the countdown running; task pauses are handled separately from this flag.
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
        self.countdown = True
        self.paused = False
        self.pause_changed.emit(False)
        self.fixation = fixation
        self.target = target

        self.current_trial = 0
        self.start_next_trial()
    
    def on_trial_finished(self):
        self.phase = "rest"
        self.current_trial += 1  # CONFIG: Advance to the next sequence entry after the current block finishes.

        # Experiment complete
        if self.current_trial >= len(self.trials):
            self.phase = "idle"
            self.disable_pause.emit()
            self.logger_message.emit("Experimental battery complete.")
            self.updating_exp.emit("Complete")  # CONFIG: Sidebar status text after all experiments finish.
            self.updating_reps.emit(0, 0)
            self.show_title.emit("Complete")  # CONFIG: Central message after all experiments finish.
            self.experiment_complete.emit()  # CONFIG: Notify the logger to save the session JSON.
            return


        self.rest_remaining = 30  # CONFIG: Rest for 30 seconds between blocks; finish immediately after the last block.

        self.updating_exp.emit("Rest")  # CONFIG: Sidebar status text during rest between blocks.
        self.updating_reps.emit(0,0)
        self.show_title.emit(str(self.rest_remaining))
        self.logger_message.emit(f"{self.current_name} experiment completed.")
        self.enable_pause.emit()

        self.rest_timer.start(1000)  # CONFIG: Update the rest countdown every 1000 ms; adjust the one-second decrement if changing this interval.
    

    def on_instructions_finished(self):
        self.rest_remaining = 3  # CONFIG: Run a three-second preparation countdown after the instruction page.

        self.updating_exp.emit("Preparation")  # CONFIG: Sidebar status text during the preparation countdown.
        self.updating_reps.emit(0,0)
        self.show_title.emit(str(self.rest_remaining))

        self.test_timer.start(1000)  # CONFIG: Update the preparation countdown every 1000 ms; adjust the one-second decrement if changing this interval.

    
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
        self.phase = "instructions"
        self.disable_pause.emit()
        if self.current_trial >= len(self.trials):
            self.logger_message.emit("Experimental battery complete.")
            return

        config = TRIALS[EXPERIMENT_SEQUENCE[self.current_trial]]  # CONFIG: Read the current block configuration from the execution sequence.
        self.current_name = config["name"]

        self.show_title.emit(self.current_name)

        QTimer.singleShot(
            2000,  # CONFIG: Show the block title for 2000 ms before displaying instructions.
            lambda: self.show_instructions(config)
        )

    def show_instructions(self, config):
        self.show_instruction.emit(config["Description"])  # CONFIG: Send participant instructions from the configuration to the canvas.

        QTimer.singleShot(
            5000,  # CONFIG: Show participant instructions for 5000 ms before the preparation countdown.
            self.on_instructions_finished
        )

    def update_reps(self, current, total):
        self.updating_reps.emit(current,total)

    def begin_trial(self):
        self.phase = "task"
        self.clear_text.emit()
        trial = self.trials[self.current_trial]
        self.logger_message.emit(f"{self.current_name} experiment started.")
        self.updating_exp.emit(self.current_name)
        trial.start(self.fixation, self.target)  # CONFIG: Start the repeated stimulus task for the current block.
        self.enable_pause.emit()

    def toggle_pause(self):
        if self.phase == "task":
            trial = self.trials[self.current_trial]
            if not self.paused:
                if trial.phase not in ("active", "rest"):
                    return
                if trial.phase == "active":
                    self.pause_event = {
                        "type": "trial pause",
                        "task": self.current_name,
                        "task_key": EXPERIMENT_SEQUENCE[self.current_trial],
                        "block": self.current_trial + 1,
                        "trial": trial.current_reps,
                        "start_time": datetime.now().isoformat(timespec="milliseconds"),
                    }
                    self.logger_message.emit(
                        f"trial pause start: {self.current_name}, trial {trial.current_reps}")
                trial.pause()
                self.clear_text.emit()
                self.paused = True
                self.pause_changed.emit(True)
            else:
                if self.pause_event is not None:
                    self.pause_event["end_time"] = datetime.now().isoformat(timespec="milliseconds")
                    self.event_sent.emit(self.pause_event)
                    self.logger_message.emit(
                        f"trial pause end: {self.current_name}, trial {trial.current_reps}")
                    self.pause_event = None
                self.paused = False
                self.pause_changed.emit(False)
                trial.resume()
        elif self.phase == "rest":
            self.countdown = not self.countdown
            self.pause_changed.emit(not self.countdown)

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

