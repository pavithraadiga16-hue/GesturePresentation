# Smart Gesture-Controlled Media & Presentation System

This beginner project uses your laptop webcam to detect one hand with MediaPipe.
It watches the wrist landmark moving sideways and sends a single keyboard arrow
key to PowerPoint: swipe right for the next slide, and swipe left for the
previous slide. No dataset or model training is needed.

## Files

- `main.py` - the complete gesture presentation controller.
- `camera_test.py` - checks that OpenCV can open your webcam.
- `hand_test.py` - checks that MediaPipe can detect and draw hand landmarks.
- `requirements.txt` - packages the project needs.

## Windows setup in VS Code

Open the VS Code terminal in this project folder and run these commands:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell says that scripts are disabled, run this once in the same terminal,
then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

After activation, VS Code should show `(.venv)` at the beginning of the terminal
line. In VS Code, also select this environment through **Python: Select
Interpreter** if prompted.

## Test each part

On the first run of `hand_test.py` or `main.py`, the program downloads
`hand_landmarker.task`, MediaPipe's official pretrained hand-landmark model, to
this project folder. This is not a dataset and involves no training; leave the
file in place after it is downloaded.

First test the webcam:

```powershell
python camera_test.py
```

You should see a mirror-like live video window. Press `Q` while that window is
selected to close it.

Then test hand landmarks:

```powershell
python hand_test.py
```

Show an open hand to the camera. Green landmark dots and connecting lines should
appear. Press `Q` to close it.

Finally run the controller:

```powershell
python main.py
```

## Use with PowerPoint

1. Open your presentation and begin Slide Show mode (`F5` is common).
2. Keep the slideshow as the focused window if possible. The program sends the
   left/right keys to whichever app Windows considers active.
3. Start `main.py`. A separate camera preview appears.
4. Keep your hand visible and move it clearly across the frame:
   - Move from the left side toward the right: **next slide**.
   - Move from the right side toward the left: **previous slide**.
5. Pause briefly between swipes. The program has a one-second cooldown to stop
   accidental multiple changes.
6. Click the camera preview and press `Q` to stop the program safely.

The overlay reports whether it is tracking, ready, or has recognized a swipe.
If arrow keys go to the wrong application, click the PowerPoint slideshow before
making a gesture. Some systems may bring the OpenCV camera preview to the front;
click PowerPoint again after starting the program.

## Common problems

| Problem | Fix |
| --- | --- |
| `py` or `python` is not recognized | Install Python from python.org and tick **Add Python to PATH**, then restart VS Code. |
| Camera cannot open | Close Teams, Zoom, Camera, and browser tabs using the webcam. Check Windows Camera privacy permission. Try changing `CAMERA_INDEX = 0` to `1`. |
| No landmarks appear | Use good lighting, show one whole hand, and stand slightly farther from the camera. |
| Swipes trigger too easily | Increase `SWIPE_THRESHOLD` in `main.py`, for example to `0.28`. |
| Swipes do not trigger | Make a clearer, faster sideways movement, or reduce `SWIPE_THRESHOLD` to `0.15`. |
| PowerPoint does not change slides | Start Slide Show mode and make sure PowerPoint is the active window before swiping. |
| `ModuleNotFoundError` | Activate `.venv` and run `pip install -r requirements.txt` again. |
| `module 'mediapipe' has no attribute 'solutions'` | This project now supports your MediaPipe 1.x installation. Use the updated project files and do not copy old `mp.solutions` tutorial code into them. |
| Model download fails | Check your internet connection, then run `python hand_test.py` again. |

## Safety

The script only presses one arrow key after a recognized swipe, never holds a
key down, and waits one second before allowing another gesture. Press `Q` in the
camera window to stop it. PyAutoGUI also has its standard emergency failsafe:
move the mouse to the top-left corner of the screen if required.

## Viva explanation

MediaPipe provides 21 predefined hand landmarks. Landmark `0` is the wrist. The
program stores several recent normalized wrist x-coordinates. If the newest
position is far enough to the right of the oldest one, it is a right swipe; if
it is far enough to the left, it is a left swipe. PyAutoGUI converts that result
into the right or left arrow key that PowerPoint understands.
