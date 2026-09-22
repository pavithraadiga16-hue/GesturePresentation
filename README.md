# Smart Gesture-Controlled Media & Presentation System 🖥️✋

An AI-powered computer vision project that lets you control Microsoft PowerPoint presentations hands-free using real-time webcam hand gestures. Swipe your hand in the air to flip through your slides seamlessly!

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [System Architecture](#-system-architecture)
3. [Gestures & Logic](#-gestures--logic)
4. [Installation & Setup (Windows)](#-installation--setup-windows)
5. [How to Run & Test](#-how-to-run--test)
6. [How to Connect with PowerPoint](#-how-to-connect-with-powerpoint)
7. [Troubleshooting & Common Errors](#-troubleshooting--common-errors)

---

## 🔍 Project Overview
This project allows a user to control slide presentations without touching a keyboard or mouse. Instead of training a heavy custom Machine Learning model or gathering thousands of training images, this system uses **Google's MediaPipe** pre-trained framework to find a hand and tracks its movement using simple mathematical rules.

### Core Technologies:
* **Python:** The programming language used to tie everything together.
* **OpenCV:** Captures the live video feed from your laptop webcam and displays the window.
* **MediaPipe:** Instantly tracks 21 distinct coordinate points (landmarks) on your hand.
* **NumPy:** Handles numerical math calculations smoothly.
* **PyAutoGUI:** Emulates actual keyboard keypresses (`Left` and `Right` arrows) to control PowerPoint.

---

## ⚙️ System Architecture

```text
Laptop Webcam 📷
      │
      ▼
OpenCV Frame Capture (Flipped horizontally like a mirror)
      │
      ▼
BGR to RGB Color Conversion
      │
      ▼
MediaPipe Processing (Finds 21 Hand Landmarks)
      │
      ▼
Wrist Tracking (Focuses on Landmark 0 X-coordinate)
      │
      ▼
Movement History Check (Ensures movement is continuous)
      │
      ▼
PyAutoGUI Keystroke Simulation (Left or Right Arrow)
      │
      ▼
PowerPoint Slide Changes! 📑
```

---

## ✋ Gestures & Logic
The system tracks the **Wrist (Landmark 0)**. It monitors its normalized `X-coordinate` (which ranges from `0.0` on the far left of the camera screen to `1.0` on the far right).

Instead of comparing just two frames (which creates jittery glitches), the program saves a small history of your wrist positions:

1. **Swipe Right (Next Slide):** 
   * If your wrist positions steadily increase (e.g., `0.25 → 0.35 → 0.48 → 0.60`), the system triggers a **Right Arrow** keypress.
2. **Swipe Left (Previous Slide):** 
   * If your wrist positions steadily decrease (e.g., `0.75 → 0.62 → 0.49 → 0.35`), the system triggers a **Left Arrow** keypress.

*A built-in **Cooldown system** stops the program from registering multiple swipes immediately, giving you time to bring your hand back down safely.*

---

## 🛠️ Installation & Setup (Windows)

Follow these exact steps inside your **VS Code Terminal** to set up a clean isolation box (Virtual Environment) for your project:

### Step 1: Create a Virtual Environment
This prevents project dependencies from clashing with other Python programs on your computer.
```bash
python -m venv venv
```

### Step 2: Activate the Virtual Environment
```bash
.\venv\Scripts\activate
```
*(You will know it worked when you see `(venv)` appear at the very beginning of your terminal prompt line).*

### Step 3: Install the Requirements
```bash
pip install -r requirements.txt
```

---

## 🎮 How to Run & Test

We have broken the project down into 3 easy stages so you can verify your hardware step-by-step:

### Test 1: Is your Camera Working?
Run the camera test script to ensure OpenCV can access your laptop's webcam:
```bash
python camera_test.py
```
* **Expectation:** A window opens showing your live video. Press **`q`** to close it.

### Test 2: Is MediaPipe Detecting Your Hand?
Run the hand tracking script to verify point mapping:
```bash
python hand_test.py
```
* **Expectation:** You should see a red/green digital skeletal mesh drawn on top of your hand tracking 21 unique nodes. Press **`q`** to close it.

### Test 3: Run the Complete Presentation System
Run the main controller:
```bash
python main.py
```
* **Expectation:** The camera feed opens displaying visual status text overlays at the top ("Status: Idle", "Swipe Left = Prev", etc.).

---

## How to Connect with PowerPoint
1. Launch the **`main.py`** script.
2. Open your target **PowerPoint Presentation** file.
3. Start **Slide Show Mode** (Press **F5**).
4. **Crucial:** Ensure PowerPoint is your active, highlighted window on your screen.
5. Stand or sit **2 to 4 feet away** from the camera, raise your hand, and perform smooth, deliberate horizontal sweeps.

---

## 🚨 Troubleshooting & Common Errors

#### 1. Error: `ModuleNotFoundError: No module named 'cv2'` or `'mediapipe'`
* **Cause:** You either forgot to activate your virtual environment or ran the install command outside of it.
* **Fix:** Run `.\venv\Scripts\activate` and then re-run `pip install -r requirements.txt`.

#### 2. Error: PowerPoint isn't flipping slides, but the terminal logs say "Swipe Detected"
* **Cause:** PowerPoint is not the active window. PyAutoGUI sends keys to whatever application is currently focused.
* **Fix:** Click your mouse once inside your PowerPoint presentation slideshow to bring it to the front focus.

#### 3. Issue: The slides skip 3 or 4 pages at a single time
* **Cause:** Your swipe motion is too slow or the cooldown is set too low.
* **Fix:** Adjust the `SWIPE_COOLDOWN` constant near the top of `main.py` to a higher number (e.g., `1.5` seconds).
