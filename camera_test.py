"""Simple webcam test. Press Q to close the test window."""

import cv2


CAMERA_INDEX = 0


def main():
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print(f"Could not open camera {CAMERA_INDEX}.")
        return

    print("Camera works if you can see video. Press Q to quit.")
    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read a frame from the camera.")
                break
            cv2.imshow("Camera Test", cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
                break
    except KeyboardInterrupt:
        print("Camera test stopped with Ctrl+C.")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
