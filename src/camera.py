import cv2

from config import (
    CAMERA_ID,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    TARGET_FPS,
)


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, TARGET_FPS)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open camera.")

    def read(self):
        ok, frame = self.cap.read()
        if not ok:
            return None

        return cv2.flip(frame, 1)

    def size(self):
        return (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

    def fps(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return int(fps) if fps > 0 else TARGET_FPS

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

        cv2.destroyAllWindows()