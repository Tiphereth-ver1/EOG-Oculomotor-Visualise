# EOG Modules and Configuration Guide

Configurable locations are marked with `CONFIG:` comments: Python uses `#`, and
UI XML uses `<!-- ... -->`. Search for this marker in the IDE to find settings.
The English translation changes text only; experimental parameters and execution
logic remain unchanged.

## 1. Module Responsibilities

| File | Responsibility | Common changes |
| --- | --- | --- |
| `app.py` | Create the Qt application and main window; run the event loop | Normal or full-screen display |
| `mainwindow.ui` | Configure interface layout and appearance | Window size, widget order, colors, fonts, initial button text, dot diameter |
| `ui_mainwindow.py` | Load the UI at runtime, bind widget names, apply canvas properties | UI path; do not replace with generated code |
| `mainwindow.py` | Connect buttons, experiment, canvas, logger, and serial worker; handle shortcuts | Start, pause, Debug display, dynamic button text, E artefact marker |
| `graphics_page.py` | Create dots, titles, and instructions; update display | Text position and alignment, dot size and color |
| `Trial/trial_block.py` | Define trial configuration and schedule all blocks | Duration, repetitions, displacement, instructions, block order, countdowns |
| `Trial/trial.py` | Base repetition logic, directions, and completion signals | Direction list and repetition completion |
| `Trial/fixation.py` | Central white-dot fixation task | Completion check interval and central position |
| `Trial/step_prosaccade.py` | Show the peripheral target as central fixation disappears | Step stimulus transitions and target position; also used for antisaccades |
| `Trial/gap_prosaccade.py` | Hide fixation, wait for the gap, then show the target | Blank interval and stimulus transitions |
| `Trial/overlap_prosaccade.py` | Keep fixation visible when the peripheral target appears | Simultaneous display of both dots |
| `Trial/smooth_pursuit.py` | Move the white target along a trajectory | Position update interval, timing, repetition rest |
| `Trial/trajectories.py` | Horizontal sinusoid, circle, and figure-eight functions | Mathematical movement paths |
| `data_logger.py` | Write text logs and event JSON | Subject details, filenames, paths, timestamps, sampling-rate metadata |
| `Connection/bluetooth.py` | Serial connection and marker transmission using pyserial | COM port, baud rate, timeout, messages, marker bytes |
| Package `__init__.py` files | Export classes for other modules | Maintain exports when adding modules |

## 2. Size, Colors, and Layout

Edit `mainwindow.ui` in Qt Widgets Designer or directly as XML, then restart the
application. Running `pyside6-uic` is unnecessary.

| Setting | Location/property | Value or action |
| --- | --- | --- |
| Initial window size | `MainWindow` → `geometry` | Width 1400, height 800 |
| Window title | `MainWindow` → `windowTitle` | EOG Oculomotor Visualise |
| Sidebar order | `sidebar_layout` items | Reorder items; adjust spacing and margins |
| Info and Debug box width | `info`, `status_box` → `minimumSize`, `maximumSize` | Fixed width 150; change both constraints together |
| Info background and border | `info` → `styleSheet` | Grey background, white border; add `color` for text |
| Button size and colors | Corresponding `QPushButton` | Set minimum/maximum size, font, and styleSheet |
| Sidebar experiment font | `current_experiment` → `font` | Arial 16 pt |
| Repetition font | `reps_count` → `font` | Arial 20 pt bold |
| Canvas background | `graphics` → `backgroundBrush` | RGB(0,0,0), black |
| Scene rectangle | `graphics` → `sceneRect` | x=-600, y=-350, width=1200, height=700 |
| Shared dot diameter | `stimulusDiameter` | 24 scene units |
| Saccade fixation color | `fixationColor` | RGB(255,255,0), yellow |
| Peripheral, fixation-task, and pursuit target color | `targetColor` | RGB(255,255,255), white |
| Central title/countdown font and color | `titleFont`, `titleColor` | Arial 48 pt bold, white |
| Central instruction font and color | `instructionsFont`, `instructionsColor` | Arial 36 pt, white |
| Instruction wrapping width | `instructionsWidth` | 700 |
| Text size conversion | `sceneTextDpi` | 100; usually change font size first |

Dot size and displacement use scene coordinates, usually corresponding to view
pixels without scaling; these are not visual degrees. Dot size and color are
shared globally. Set individual sizes at `stimulus.setRect(...)` in
`graphics_page.py` if needed.

`sceneRect` does not change trajectories. Vertical saccade `shift=400` exceeds the
initial y range of -350 to 350. Visibility also depends on window size, view, and
scrolling. Coordinate window size, scene bounds, and shift, allowing for dot radius.
Preserve `objectName` values, `Graphics_Page` promotion, and dynamic property names;
the loader and controller depend on them.

## 3. Instruction Content and Position

- Participant instructions: `Trial/trial_block.py` → `TRIALS` → `Description`.
  Adjacent strings concatenate; use `\n` for explicit line breaks. Update white/yellow
  references when changing dot colors.
- Block names: `name` in the same configuration, used for the title and sidebar.
- Instruction position: `graphics_page.py` → `show_instruction()` → `setPos(...)`.
  Coordinates `-rect.width()/2`, `-rect.height()/2` center the text box. Adding 100
  to y moves it down 100 scene units.
- Title/countdown position: `show_title()` → `self.title.setPos(...)`; adjust x/y offsets.
- Paragraph alignment: `block_format.setAlignment(...)`, currently `AlignCenter`.
  This controls text inside the box independently of the box position.
- Initial button text: each widget's `text` property in `mainwindow.ui`.
  The controller updates Pause/Resume text at runtime.
- Rest, Preparation, Complete: `updating_exp.emit(...)` in `trial_block.py`;
  the central completion message uses `show_title.emit("Complete")`.
- Serial messages: `connection_status.emit(...)` in `Connection/bluetooth.py`, shown in Debug.

## 4. Experiment Parameters and Timing

Edit `TRIALS` in `Trial/trial_block.py`; stimulus constructors receive these
parameters. Durations ending in `_s` use seconds. `fixation_min/max`,
`target_duration`, `gap`, `rest`, and QTimer intervals use milliseconds.

| Task | Parameters | Approximate stimulus time per block, excluding title, instructions, preparation, and block rest |
| --- | --- | --- |
| Fixation | `fixation_duration_s=1`, `reps=10`, `rest=1000` | 20 seconds |
| Smooth Pursuit | `fz=0.2`, `test_duration_s=25`, `shift=600`, horizontal sinusoid, `reps=10`, `rest=5000` | 300 seconds |
| Gap Prosaccade | Fixation 500–1999 ms, `gap=200`, target 1000 ms, `shift=400`, `reps=15` | 25.5–48 seconds |
| Step Prosaccade | Fixation 500–1999 ms, target 1000 ms, `shift=400`, `reps=15` | 22.5–45 seconds |
| Overlap Prosaccade | Fixation 500–1999 ms, target 1000 ms, `shift=400`, `reps=15` | 22.5–45 seconds |
| Step Antisaccade | Step stimulus class, fixation 500–1999 ms, target 1000 ms, `shift=400`, `reps=15` | 22.5–45 seconds |

Fixation and pursuit wait for `rest` after the last repetition before completing
the block. Saccade tasks have no additional repetition rest. Overlap keeps the
central dot visible until both dots are cleared. Antisaccades use the same visual
stimulus as Step; instructions require looking in the opposite direction. The
program does not assess whether the participant follows this instruction.

Fixation checks completion every 1000 ms in `fixation.py`, so a configured duration
of 1.5 seconds need not end at exactly 1.5 seconds. Pursuit updates every 16 ms,
approximately 62.5 times per second. Qt timers and system scheduling affect timing.

Trajectory functions take time in seconds, amplitude, and frequency in Hz.
Figure-eight vertical amplitude is half the horizontal amplitude at twice the
frequency. Saccade directions are sampled randomly from four directions without
guaranteed balance. Update `randint(0,4)` in all three saccade classes if changing
the length of `DIRECTIONS`.

## 5. Experiment Flow

`EXPERIMENT_SEQUENCE` contains ten blocks:

`Fixation → Step → Step → Gap → Gap → Overlap → Overlap → Antisaccade → Antisaccade → Smooth Pursuit`

Each repeated sequence entry runs its full configured repetition count.

1. `app.py` creates the window; `mainwindow.py` connects experiment signals, canvas, logger, and serial worker.
2. Experiment validates subject details, initializes the logger, and calls `Experiment.start()`.
3. `start_next_trial()` displays the configured block title for 2 seconds.
4. `show_instructions()` displays `Description` for 5 seconds.
5. `on_instructions_finished()` starts a 3-second preparation countdown.
6. `begin_trial()` clears text and starts all repetitions of the current task.
7. `Trial.check_repeat()` continues until `reps` is reached and emits `finished`.
8. `on_trial_finished()` advances the block index; if another block remains, rest for 30 seconds and return to step 3.
9. After the last block, display Complete and signal the logger to save JSON.

Edit the 2000/5000 ms `QTimer.singleShot` arguments for title/instruction duration.
Edit the initial `rest_remaining` values of 3 and 30 for preparation/block rest.
Changing the 1000 ms countdown interval also requires adjusting the decrement.
Each block adds about 10 seconds for title, instructions, and preparation; ten
blocks add about 100 seconds, and nine rests add 270 seconds.

During an active task, Pause hides stimuli and stops the current repetition;
Resume skips the interrupted repetition and starts the next. Rest pauses freeze
the remaining rest time. Title, instruction, and preparation phases disable pause.
The Experiment button is disabled after starting, and completion locks the controls.

## 6. Logging and Device Connection

- Subject details are entered before starting. Logs are written under `promptrecords`
  beside `data_logger.py`, with matching `Subject<ID>-YYYY-MM-DD_HH-MM-SS.txt` and
  `.json` filenames. Text files use exclusive creation to avoid overwriting existing records.
- Text headers and JSON session metadata record subject ID, English name, age,
  CDR rating, and gender. Relative timing resets when subject records are initialized.
- `sampling_rate=500` is JSON metadata; the code does not continuously read serial
  EOG samples or configure a hardware sampling rate.
- `add_event()` stores incoming dictionaries in `type`, except trial pause events,
  whose fields are also copied to the event. Analysis must follow the saved structure.
- Press E to record motion artefacts. Before initialization, event/message logging returns without writing.
- Serial configuration: COM3, 9600 baud, 8 data bits, one stop bit, no parity,
  one-second timeout. Update the connection message when changing the port.
- `marker_high()` and `marker_low()` send `111111` and `000000` bytes. The main
  controller does not connect these methods to stimulus events; connecting a device
  does not automatically send experimental markers.

## 7. Common Changes

- Five-second fixation, six repetitions: set `fixation_duration_s=5`, `reps=6`
  in `TRIALS["fixation"]["params"]`.
- Sixty-second block rests: set `self.rest_remaining=60` in `on_trial_finished()`.
  A task's `rest` parameter controls repetition rest instead.
- Eight-second instructions: set the first `QTimer.singleShot` argument in
  `show_instructions()` to 8000.
- Move saccade targets closer: reduce `shift`, for example from 400 to 250.
  Update Step, Gap, Overlap, and Antisaccade configurations as required.
- Circular pursuit: set the pursuit `trajectory` to `circle` and check that the
  amplitude fits the canvas height.
- Red target: set `targetColor` to RGB(255,0,0) and update each affected `Description`.
- Button styling: select the button in Designer and edit `styleSheet`, for example
  `background-color: #364152; color: white;`.

## 8. Verification Notes

The original annotation pass compared Python abstract syntax trees and UI XML
elements, attributes, and values before and after its changes. That pass did not
launch the GUI or connect hardware because its environment lacked PySide6, NumPy,
and pyserial. English translation also changes visible strings and test expectations;
its verification is reported separately with the change.
