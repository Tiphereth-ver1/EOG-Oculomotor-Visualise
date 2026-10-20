# EOG Oculomotor Visualisation and Experimental Framework

A Python-based experimental stimulus presentation framework for designing and running oculomotor tasks for Electrooculography (EOG) research.

The project provides a modular interface for presenting controlled visual stimuli, executing structured eye movement paradigms, and logging experimental events for later analysis.

---

## Overview

This project was developed to support research investigating eye movement biomarkers associated with neurological conditions. It provides a configurable framework for implementing common oculomotor assessments, including:

- Fixation stability tasks
- Step prosaccades
- Gap prosaccades
- Overlap prosaccades
- Antisaccade paradigms
- Smooth pursuit tracking

The framework is designed around modular trial classes, allowing experimental protocols to be modified without requiring changes to the underlying GUI or execution engine.

---

## Features

### Modular Trial Architecture

Each experimental task is implemented as an independent `Trial` module.

Each trial is responsible for:

- Generating visual stimuli
- Managing repetitions
- Controlling stimulus timing
- Emitting completion events
- Reporting experiment events

---

### Configurable Experiment Protocols

Experiments are defined through a central protocol dictionary:

```python
TRIALS = {
    "step_prosaccade": {
        "class": Step_Prosaccade,
        "name": "Step Prosaccade",
        "Description": "...",
        "params": {
            "fixation_min": 1000,
            "fixation_max": 1500,
            "target_duration": 1000,
            "shift": 400,
            "reps": 60
        }
    }
}
```
## Installation
### Requirements
- Python 3.x
- PySide6
- NumPy
### Setup

Clone repository:

```
git clone <repository-url>
cd EOG-Oculomotor-Visualise
```

Create virtual environment:

```
python -m venv .venv
```

Activate environment:

Windows:

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run application:

```
python -m app
```

## 使用 Qt Widgets Designer 编辑界面

界面的布局、尺寸、字体和颜色统一保存在项目根目录的 `mainwindow.ui` 中。
`ui_mainwindow.py` 在启动时直接加载这个文件，`mainwindow.py` 保留按钮的信号连接和控制逻辑，
`graphics_page.py` 保留刺激移动及标题、说明文字的显示逻辑。
实验流程、串口通信和日志输出仍由原来的模块负责。

在安装了项目依赖的 Python 环境中运行：

```powershell
pyside6-designer mainwindow.ui
```

也可以在 Qt Widgets Designer 中选择 **File → Open**，打开 `mainwindow.ui`。
编辑并保存后，重新运行 `python -m app` 即可看到修改，**不需要运行 `pyside6-uic`，
也不要用生成的代码覆盖 `ui_mainwindow.py`**。

### 布局、大小和颜色

- 主窗口 `MainWindow`：通过 `geometry` 修改初始窗口尺寸，通过 `windowTitle` 修改标题。
- 左侧面板 `dock`：保留原有可移动的停靠面板；按钮和信息框的排列由 `sidebar_layout` 管理。
  在布局中拖动控件可以调整顺序，通过布局的 `spacing`、边距和伸缩项调整间距。
  布局中的控件尺寸受 `minimumSize`、`maximumSize`、`sizePolicy` 和布局约束共同控制。
- 信息框 `info` 和日志框 `status_box`：当前宽度固定为 150。
  修改宽度时，请同时修改 `minimumSize.width` 和 `maximumSize.width`；若希望自动伸缩，可以放宽这些约束。
- 颜色和边框：选择控件，编辑 `styleSheet`。信息框原有灰色背景和白色边框已经放入该属性。
  例如，按钮可设置 `background-color: #364152; color: white;`。
- 信息标签 `current_experiment` 和 `reps_count`：通过 `font`、`alignment`、`wordWrap` 等属性编辑。

### 中央刺激画布

`graphics` 是由 `QGraphicsView` 提升为 `Graphics_Page` 的自定义控件。
在 Designer 中选中它，可以编辑以下属性；动态属性位于属性编辑器的动态属性区域：

| 属性 | 用途 | 原有值 |
| --- | --- | --- |
| `backgroundBrush` | 画布背景画刷/颜色 | 黑色 |
| `sceneRect` | 场景坐标范围 | `(-600, -350, 1200, 700)` |
| `stimulusDiameter` | 注视点和目标点的直径 | 24 |
| `fixationColor` | 注视点颜色 | 黄色 |
| `targetColor` | 目标点颜色 | 白色 |
| `titleFont` / `titleColor` | 标题字体/颜色 | Arial 48，加粗，白色 |
| `instructionsFont` / `instructionsColor` | 说明文字字体/颜色 | Arial 36，白色 |
| `instructionsWidth` | 说明文字的换行宽度 | 700 |
| `sceneTextDpi` | 场景文字使用的字体 DPI | 100，保持原有文字实际尺寸 |

圆点、标题和说明是运行时创建的 `QGraphicsItem`，Designer 中只显示画布占位控件，
实际绘制效果需要启动程序查看。文字继续按原逻辑在场景中心对齐，圆点的位置继续由实验轨迹控制。
`sceneRect` 修改场景范围，不会自动修改 `Trial` 中的轨迹、位移或时间参数。

请保留原控件的 `objectName`、`Graphics_Page` 提升设置和上述动态属性名称，
程序用这些名称连接原有逻辑。Debug 日志框初始隐藏、Pause 按钮的状态，以及运行时的文字更新由控制逻辑负责。
分发程序时需要一并保留 `mainwindow.ui`；加载路径根据 Python 文件所在目录确定，不依赖启动目录。

## Configuration

Experimental batteries are defined in the experiment protocol configuration.

The sequence of trials can be modified through:

```python
EXPERIMENT_SEQUENCE = [
    "fixation",
    "step_prosaccade",
    "gap_prosaccade",
    "overlap_prosaccade",
    "step_antisaccade",
    "smooth_pursuit"
]
```

Trial parameters can be modified independently:

```python
"reps": 60
"target_duration": 1000
"fixation_min": 1000
"fixation_max": 1500
```
## Adding New Experiments

New paradigms can be added by creating a new Trial subclass.

Example:

```python
class NewTrial(Trial):

    def run(self, fixation, target):
        pass
```
The new trial can then be registered in the experiment configuration:

```python
"new_trial": {
    "class": NewTrial,
    "name": "New Trial",
    "Description": "Instructions shown to participant.",
    "params": {}
}
```
## Logging

During an active task, click **Pause** to hide the stimuli and stop the current
trial. Click **Resume** to skip that interrupted trial and start the next one.
If the interrupted trial was the last repetition, the block finishes normally.
Rest pauses freeze the remaining rest time and do not create trial pause events.

The session JSON stores each task pause as an event with `type: "trial pause"`,
`start_time`, `end_time`, `task_key`, `block` (1-based), and `trial` (1-based).
The text log also records `trial pause start` and `trial pause end`.

The framework provides event-based logging for:

- Experiment start/end
- Trial start/end
- Trial repetitions
- Stimulus events
- Timing information

Example:

```
[14:31:12] Step Prosaccade experiment started.
[14:31:14] Duration: 1458ms, Direction: Down
[14:33:29] Step Prosaccade experiment completed.
```

This framework is intended as a research prototype for investigating whether EOG-derived oculomotor measurements can provide accessible assessments of neurological function.

The design prioritises:

- Reproducible stimulus presentation
- Modular experimental design
- Accurate event timing
- Expandable research workflows
