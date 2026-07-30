import cv2


class Camera:
    def __init__(self, camera_index=0, width=1280, height=720):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open webcam.")

        # Camera settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def read(self):
        success, frame = self.cap.read()

        if not success:
            return None

        # Mirror view
        frame = cv2.flip(frame, 1)

        return frame

    def release(self):
        if self.cap.isOpened():
            self.cap.release()