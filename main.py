import cv2

from camera import Camera
from hand_tracker import HandTracker
from utils.smoother import PointSmoother


def main():

    camera = Camera()
    tracker = HandTracker()

    left_smoother = PointSmoother(alpha=0.22)
    right_smoother = PointSmoother(alpha=0.22)

    print("===================================")
    print(" Flower Magic Started")
    print(" Press ESC to Exit")
    print("===================================")

    while True:

        frame = camera.read()

        if frame is None:
            break

        frame, hands = tracker.process(frame)

        left_found = False
        right_found = False

        for hand in hands:

            tip = hand["landmarks"][8]

            if hand["label"] == "Left":

                smooth_tip = left_smoother.update(tip)
                left_found = True

                cv2.circle(
                    frame,
                    smooth_tip,
                    10,
                    (255, 0, 255),
                    -1,
                )

            else:

                smooth_tip = right_smoother.update(tip)
                right_found = True

                cv2.circle(
                    frame,
                    smooth_tip,
                    10,
                    (0, 255, 255),
                    -1,
                )

        if not left_found:
            left_smoother.reset()

        if not right_found:
            right_smoother.reset()

        cv2.imshow("Flower Magic", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    tracker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()