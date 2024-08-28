# CMD Recorder

**Terminal Recorder** is a Python script for recording the contents of a terminal or console window. It allows you to capture images from a specified window and save them in GIF or MP4 format. You can customize the recording duration, frame interval, scaling, and maximum number of frames.

## Features

- Record a terminal or console window
- Save recorded frames in GIF or MP4 formats
- Customize the recording duration, frame interval, and scaling
- Ability to set the maximum number of frames to record

## Installation

1. Clone the repository or download the source code:

```bash
git clone https://github.com/Craxti/cmd-recorder.git
cd terminal-recorder
```

2. Install the necessary dependencies. You can use `pip`:

```bash
pip install pygetwindow pyautogui Pillow moviepy numpy argparse
```

3. To use the MP4 video functionality, you also need to install `ffmpeg`. Follow the [ffmpeg installation instructions](https://ffmpeg.org/download.html) for your operating system.

## Usage

### Running the Script

Run the script using Python, specifying the required parameters:

```bash
python terminal_recorder.py --output output.gif --duration 10 --interval 0.5 --scale 1.0 --format gif --window-title "Terminal" --max-frames 100
```

### Command Line Arguments
```
--output (default output.gif): The name of the output file (GIF or MP4).
--duration (default 10): Duration of recording in seconds.
--interval (default 0.5): Interval between frames in seconds.
--scale (default 1.0): Frame scaling factor.
--format (default gif): Saving format (gif or mp4).
--window-title (default empty): Window title to record. If not specified, a list of standard titles will be used.
--max-frames (default None): Maximum number of frames to record. If not specified, recording will continue until time expires.
```

Examples:
Recording a window with the title "Terminal" to GIF format with a 5-second recording:

```python terminal_recorder.py --output terminal.gif --duration 5 --format gif --window-title "Terminal"```

Recording a window with a maximum of 50 frames to MP4 format:

```python terminal_recorder.py --output terminal.mp4 --max-frames 50 --format mp4 --window-title "Terminal"```
## Known issues
You may need permission from the operating system to capture windows.
On some systems, there may be problems with window focus.
Contributing to the project
Your suggestions for improvements or bug fixes are welcome! To contribute to the project, please create a pull request or report bugs via Issues.

## License
This project is licensed under the MIT License.
