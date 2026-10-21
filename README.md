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

## Editing the Interface with Qt Widgets Designer

Interface layout, dimensions, fonts, and colors are stored in `mainwindow.ui`
in the project root. `ui_mainwindow.py` loads this file directly at startup.
`mainwindow.py` handles button signals and control logic; `graphics_page.py`
handles stimulus movement and display of titles and instructions. Experiment
flow, serial communication, and logging remain in their respective modules.

Run this command in a Python environment with the project dependencies installed:

```powershell
pyside6-designer mainwindow.ui
```

Alternatively, use **File → Open** in Qt Widgets Designer to open `mainwindow.ui`.
Save changes and restart with `python -m app`. **Do not run `pyside6-uic` or
overwrite `ui_mainwindow.py` with generated code.**

### Layout, Size, and Colors

- Main window `MainWindow`: edit `geometry` for initial size and `windowTitle` for the title.
- Left dock `dock`: the movable dock uses `sidebar_layout` for buttons and information boxes.
  Reorder widgets in the layout and adjust spacing, margins, and spacers.
  Widget sizes depend on `minimumSize`, `maximumSize`, `sizePolicy`, and layout constraints.
- Information box `info` and log box `status_box`: both have a fixed width of 150.
  Change both minimum and maximum widths together, or relax these constraints for resizing.
- Colors and borders: edit the widget's `styleSheet`. The information box uses a grey
  background and white border. Example button style: `background-color: #364152; color: white;`.
- Labels `current_experiment` and `reps_count`: edit `font`, `alignment`, and `wordWrap`.

### Central Stimulus Canvas

`graphics` is a `QGraphicsView` promoted to the custom `Graphics_Page` widget.
Select it in Designer to edit these properties, including the dynamic properties:

| Property | Purpose | Default value |
| --- | --- | --- |
| `backgroundBrush` | Canvas background brush/color | Black |
| `sceneRect` | Scene coordinate rectangle | `(-600, -350, 1200, 700)` |
| `stimulusDiameter` | Fixation and target dot diameter | 24 |
| `fixationColor` | Fixation dot color | Yellow |
| `targetColor` | Target dot color | White |
| `titleFont` / `titleColor` | Title font/color | Arial 48, bold, white |
| `instructionsFont` / `instructionsColor` | Instruction font/color | Arial 36, white |
| `instructionsWidth` | Instruction wrapping width | 700 |
| `sceneTextDpi` | DPI used for scene text | 100, preserving the original rendered size |

Dots, titles, and instructions are runtime `QGraphicsItem` objects. Designer shows
only the canvas placeholder; run the application to inspect the rendered result.
Text is centered in the scene, and experimental trajectories control dot positions.
Changing `sceneRect` does not automatically change `Trial` trajectories, displacements,
or timing parameters.

Preserve widget `objectName` values, the `Graphics_Page` promotion, and the dynamic
property names above: the application relies on them to connect its logic.
The controller manages initial Debug log visibility, Pause button availability,
and text updates at runtime. Include `mainwindow.ui` when distributing the app;
its path is resolved relative to the Python module, independent of the working directory.

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
