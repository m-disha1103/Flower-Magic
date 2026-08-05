import cv2
import mediapipe as mp

from config import (
    MAX_NUM_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE,
    SMOOTHING_FACTOR,
)


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.drawer = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
            model_complexity=1,
        )

        self.previous = {
            "Left": {},
            "Right": {},
        }

    def _smooth(self, label, idx, x, y):
        prev = self.previous[label]

        if idx in prev:
            px, py = prev[idx]
            x = int(px + (x - px) * SMOOTHING_FACTOR)
            y = int(py + (y - py) * SMOOTHING_FACTOR)

        prev[idx] = (x, y)
        return x, y

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False

        results = self.hands.process(rgb)

        rgb.flags.writeable = True

        hands_data = []

        if not results.multi_hand_landmarks:
            self.previous["Left"].clear()
            self.previous["Right"].clear()
            return frame, hands_data

        h, w = frame.shape[:2]

        seen = {"Left": False, "Right": False}

        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks,
            results.multi_handedness,
        ):
            mp_label = handedness.classification[0].label

            label = "Right" if mp_label == "Left" else "Left"

            if seen[label]:
                label = mp_label

            seen[label] = True

            landmarks = []

            for idx, lm in enumerate(hand_landmarks.landmark):
                x = int(lm.x * w)
                y = int(lm.y * h)

                x, y = self._smooth(label, idx, x, y)
                landmarks.append((x, y))

            self.drawer.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.drawer.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2,
                    circle_radius=2,
                ),
                self.drawer.DrawingSpec(
                    color=(255, 170, 120),
                    thickness=2,
                ),
            )

            xs = [p[0] for p in landmarks]
            ys = [p[1] for p in landmarks]

            center = (
                int(sum(xs) / len(xs)),
                int(sum(ys) / len(ys)),
            )

            hands_data.append(
                {
                    "label": label,
                    "landmarks": landmarks,
                    "center": center,
                    "index_tip": landmarks[8],
                    "thumb_tip": landmarks[4],
                    "middle_tip": landmarks[12],
                    "ring_tip": landmarks[16],
                    "pinky_tip": landmarks[20],
                    "wrist": landmarks[0],
                }
            )

        if not seen["Left"]:
            self.previous["Left"].clear()

        if not seen["Right"]:
            self.previous["Right"].clear()

        return frame, hands_data

    def close(self):
        self.hands.close()