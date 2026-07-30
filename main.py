import cv2

from camera import Camera
from hand_tracker import HandTracker


def main():

    camera = Camera()
    tracker = HandTracker()

    print("Flower Magic Started")
    print("Press ESC to Exit")

    while True:

        frame = camera.read()

        if frame is None:
            break

        frame, landmarks = tracker.process(frame)

        # Draw index fingertip (landmark 8)
        if landmarks:

            index_tip = landmarks[8]

            cv2.circle(
                frame,
                index_tip,
                10,
                (255, 0, 255),
                -1,
            )

        cv2.imshow("Flower Magic", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    tracker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()