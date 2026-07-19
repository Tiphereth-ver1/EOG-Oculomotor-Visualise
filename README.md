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
