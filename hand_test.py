"""Test MediaPipe hand landmarks. Press Q to close the test window."""

from pathlib import Path
import time
from urllib.error import URLError
from urllib.request import urlretrieve

import cv2
import mediapipe as mp


CAMERA_INDEX = 0
MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/latest/hand_landmarker.task"
)
HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
)


def get_model_path():
    """Download the official pretrained model only on its first use."""
    if not MODEL_PATH.exists():
        print("Downloading MediaPipe's hand landmark model (first run only)...")
        try:
            urlretrieve(MODEL_URL, MODEL_PATH)
        except URLError as error:
            raise RuntimeError("Could not download the hand model. Check internet access.") from error
    return MODEL_PATH


def draw_hand_landmarks(frame, landmarks):
    height, width = frame.shape[:2]
    points = [(int(point.x * width), int(point.y * height)) for point in landmarks]
    for start, end in HAND_CONNECTIONS:
        cv2.line(frame, points[start], points[end], (0, 255, 0), 2)
    for point in points:
        cv2.circle(frame, point, 4, (0, 0, 255), -1)


def main():
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print(f"Could not open camera {CAMERA_INDEX}.")
        return

    try:
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(get_model_path())),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        hands = mp.tasks.vision.HandLandmarker.create_from_options(options)
    except RuntimeError as error:
        camera.release()
        print(error)
        return
    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read a frame from the camera.")
                break
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            results = hands.detect_for_video(mp_image, int(time.monotonic() * 1000))
            if results.hand_landmarks:
                for landmarks in results.hand_landmarks:
                    draw_hand_landmarks(frame, landmarks)
                message = "Hand detected"
            else:
                message = "Show your hand to the camera"
            cv2.putText(frame, message, (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, "Q = Quit", (20, 65), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("MediaPipe Hand Test", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break
    except KeyboardInterrupt:
        print("Hand test stopped with Ctrl+C.")
    finally:
        hands.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
