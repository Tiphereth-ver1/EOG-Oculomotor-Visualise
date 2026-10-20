from .trajectories import (
    circle,
    figure8,
    horizontal_sinusoid,
)

from PySide6.QtCore import Qt, QTimer, QObject, Signal
from datetime import datetime
from . import (Trial, Step_Prosaccade, Smooth_Pursuit, 
Overlap_Prosaccade, Gap_Prosaccade, Fixation)


TRIALS = {  # 《《《《《《《《《《《实验模块集中配置入口：修改名称、受试者提示语和刺激参数
    "fixation" : {
        "class": Fixation,  # 《《《《《《《《《《《此实验块对应的刺激实现类
        "name" : "注视",  # 《《《《《《《《《《《模块名称，中央标题和侧栏使用此文字
        "Description": "请注视白点，直到它消失。",  # 《《《《《《《《《《《受试者提示语，相邻字符串自动拼接，颜色修改后同步更新文字
        "params" : {
            "fixation_duration_s" : 1,  # 《《《《《《《《《《《单次注视持续时间，单位秒；检查间隔见fixation.py
            "reps" : 10,  # 《《《《《《《《《《《本实验块重复次数；顺序中出现多次的同名块各自执行这些次数
            "rest" : 1000  # 《《《《《《《《《《《重复后的空屏休息，单位毫秒；最后一次也会等待，与块间休息不同
                }
    },

    "smooth_pursuit" : {
        "class": Smooth_Pursuit,  # 《《《《《《《《《《《此实验块对应的刺激实现类
        "name" : "慢眼动跟随",  # 《《《《《《《《《《《模块名称，中央标题和侧栏使用此文字
        "Description": "请注视屏幕上的白点，并控制视线跟随屏幕上白点移动.",  # 《《《《《《《《《《《受试者提示语，相邻字符串自动拼接，颜色修改后同步更新文字
        "params" : {
            "fz" : 0.2,  # 《《《《《《《《《《《追踪频率Hz，0.2表示每周期5秒
            "test_duration_s" : 25,  # 《《《《《《《《《《《单次平滑追踪持续时间，单位秒
            "shift" : 600,  # 《《《《《《《《《《《目标偏移距离或追踪振幅，单位场景坐标，不是圆点直径
            "trajectory" : horizontal_sinusoid,  # 《《《《《《《《《《《追踪轨迹，可选horizontal_sinusoid、circle或figure8
            "reps" : 10,  # 《《《《《《《《《《《本实验块重复次数；顺序中出现多次的同名块各自执行这些次数
            "rest" : 5000  # 《《《《《《《《《《《重复后的空屏休息，单位毫秒；最后一次也会等待，与块间休息不同
                }
    },
    "gap_prosaccade" : {
        "class": Gap_Prosaccade,  # 《《《《《《《《《《《此实验块对应的刺激实现类
        "name" : "间隙眼跳",  # 《《《《《《《《《《《模块名称，中央标题和侧栏使用此文字
        "Description": "注视黄色圆点，当白色圆点出现时，将视线转向白色圆点。"  # 《《《《《《《《《《《受试者提示语，相邻字符串自动拼接，颜色修改后同步更新文字
                        "在白色圆点出现之前，黄色圆点会先消失。",
        "params" : {
            "fixation_min" : 500,  # 《《《《《《《《《《《随机中心注视时长下限，单位毫秒，包含此值
            "fixation_max" : 2000,  # 《《《《《《《《《《《随机中心注视时长上限，单位毫秒，不包含此值，必须大于下限
            "gap" : 200,  # 《《《《《《《《《《《中心点消失到外围目标出现的空屏时间，单位毫秒
            "target_duration" : 1000,  # 《《《《《《《《《《《外围目标点显示时长，单位毫秒
            "shift" : 400,  # 《《《《《《《《《《《目标偏移距离或追踪振幅，单位场景坐标，不是圆点直径
            "reps" : 15,  # 《《《《《《《《《《《本实验块重复次数；顺序中出现多次的同名块各自执行这些次数
        }
    },

    "step_prosaccade" : {
        "class": Step_Prosaccade,  # 《《《《《《《《《《《此实验块对应的刺激实现类；反向扫视也复用此类，仅提示语要求看相反方向
        "name" : "阶跃眼跳",  # 《《《《《《《《《《《模块名称，中央标题和侧栏使用此文字
        "Description": "注视黄色圆点，当白色圆点出现时，"  # 《《《《《《《《《《《受试者提示语，相邻字符串自动拼接，颜色修改后同步更新文字
                        "将视线转向白色圆点。",
        "params" : {
            "fixation_min" : 500,  # 《《《《《《《《《《《随机中心注视时长下限，单位毫秒，包含此值
            "fixation_max" : 2000,  # 《《《《《《《《《《《随机中心注视时长上限，单位毫秒，不包含此值，必须大于下限
            "target_duration" : 1000,  # 《《《《《《《《《《《外围目标点显示时长，单位毫秒
            "shift" : 400,  # 《《《《《《《《《《《目标偏移距离或追踪振幅，单位场景坐标，不是圆点直径
            "reps" : 15  # 《《《《《《《《《《《本实验块重复次数；顺序中出现多次的同名块各自执行这些次数
            }
    },

    "overlap_prosaccade" : {
        "class": Overlap_Prosaccade,  # 《《《《《《《《《《《此实验块对应的刺激实现类
        "name" : "重叠眼跳",  # 《《《《《《《《《《《模块名称，中央标题和侧栏使用此文字
        "Description": "注视黄色圆点，当白色圆点出现时，"  # 《《《《《《《《《《《受试者提示语，相邻字符串自动拼接，颜色修改后同步更新文字
                        "将视线转向白色圆点。 "
                        "黄色圆点不会消失。", 
        "params" : {
            "fixation_min" : 500,  # 《《《《《《《《《《《随机中心注视时长下限，单位毫秒，包含此值
            "fixation_max" : 2000,  # 《《《《《《《《《《《随机中心注视时长上限，单位毫秒，不包含此值，必须大于下限
            "target_duration" : 1000,  # 《《《《《《《《《《《外围目标点显示时长，单位毫秒
            "shift" : 400,  # 《《《《《《《《《《《目标偏移距离或追踪振幅，单位场景坐标，不是圆点直径
            "reps" : 15  # 《《《《《《《《《《《本实验块重复次数；顺序中出现多次的同名块各自执行这些次数
        }
    },

    "step_antisaccade" : {
        "class": Step_Prosaccade,  # 《《《《《《《《《《《此实验块对应的刺激实现类；反向扫视也复用此类，仅提示语要求看相反方向
        "name" : "阶跃反向眼跳",  # 《《《《《《《《《《《模块名称，中央标题和侧栏使用此文字
        "Description": "注视黄色圆点，当白色圆点出现时，"  # 《《《《《《《《《《《受试者提示语，相邻字符串自动拼接，颜色修改后同步更新文字
                        "将视线转向与白色圆点相反的方向。",
        "params" : {
            "fixation_min" : 500,  # 《《《《《《《《《《《随机中心注视时长下限，单位毫秒，包含此值
            "fixation_max" : 2000,  # 《《《《《《《《《《《随机中心注视时长上限，单位毫秒，不包含此值，必须大于下限
            "target_duration" : 1000,  # 《《《《《《《《《《《外围目标点显示时长，单位毫秒
            "shift" : 400,  # 《《《《《《《《《《《目标偏移距离或追踪振幅，单位场景坐标，不是圆点直径
            "reps" : 15  # 《《《《《《《《《《《本实验块重复次数；顺序中出现多次的同名块各自执行这些次数
        }
    },
}

EXPERIMENT_SEQUENCE = [  # 《《《《《《《《《《《实验块执行顺序，可增删重排；重复条目再次执行完整实验块
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
        self.countdown = True  # 《《《《《《《《《《《倒计时初始运行；暂停不控制刺激任务或singleShot等待
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
        self.current_trial += 1  # 《《《《《《《《《《《当前实验块完成后推进到下一个顺序条目

        # Experiment complete
        if self.current_trial >= len(self.trials):
            self.phase = "idle"
            self.disable_pause.emit()
            self.logger_message.emit("Experimental battery complete.")
            self.updating_exp.emit("Complete")  # 《《《《《《《《《《《全部实验结束后的侧栏状态文字
            self.updating_reps.emit(0, 0)
            self.show_title.emit("Complete")  # 《《《《《《《《《《《全部实验结束后的中央提示语
            self.experiment_complete.emit()  # 《《《《《《《《《《《通知日志器保存本轮JSON
            return


        self.rest_remaining = 30  # 《《《《《《《《《《《实验块之间休息30秒；最后一个块后直接结束

        self.updating_exp.emit("Rest")  # 《《《《《《《《《《《块间休息时的侧栏状态文字
        self.updating_reps.emit(0,0)
        self.show_title.emit(str(self.rest_remaining))
        self.logger_message.emit(f"{self.current_name} experiment completed.")
        self.enable_pause.emit()

        self.rest_timer.start(1000)  # 《《《《《《《《《《《休息倒计时每1000毫秒更新；改间隔须同步调整每次减1的逻辑
    

    def on_instructions_finished(self):
        self.rest_remaining = 3  # 《《《《《《《《《《《说明页面结束后准备倒计时3秒

        self.updating_exp.emit("Preparation")  # 《《《《《《《《《《《准备倒计时时的侧栏状态文字
        self.updating_reps.emit(0,0)
        self.show_title.emit(str(self.rest_remaining))

        self.test_timer.start(1000)  # 《《《《《《《《《《《准备倒计时每1000毫秒更新；改间隔须同步调整每次减1的逻辑

    
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

        config = TRIALS[EXPERIMENT_SEQUENCE[self.current_trial]]  # 《《《《《《《《《《《按执行顺序读取当前块配置
        self.current_name = config["name"]

        self.show_title.emit(self.current_name)

        QTimer.singleShot(
            2000,  # 《《《《《《《《《《《模块标题显示2000毫秒后进入说明页面
            lambda: self.show_instructions(config)
        )

    def show_instructions(self, config):
        self.show_instruction.emit(config["Description"])  # 《《《《《《《《《《《将配置中的受试者提示语发送到画布

        QTimer.singleShot(
            5000,  # 《《《《《《《《《《《受试者说明显示5000毫秒后进入准备倒计时
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
        trial.start(self.fixation, self.target)  # 《《《《《《《《《《《开始当前块的重复刺激任务
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

