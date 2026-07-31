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
        )

        # Store previous landmarks separately for each hand
        self.previous = {
            "Left": {},
            "Right": {},
        }

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        hands_data = []

        if not result.multi_hand_landmarks or not result.multi_handedness:
            self.previous["Left"].clear()
            self.previous["Right"].clear()
            return frame, hands_data

        h, w = frame.shape[:2]

        for hand_landmarks, handedness in zip(
            result.multi_hand_landmarks,
            result.multi_handedness,
        ):
            label = handedness.classification[0].label

            landmarks = []

            for idx, lm in enumerate(hand_landmarks.landmark):
                x = int(lm.x * w)
                y = int(lm.y * h)

                prev = self.previous[label]

                if idx in prev:
                    px, py = prev[idx]
                    x = int(px + (x - px) * SMOOTHING_FACTOR)
                    y = int(py + (y - py) * SMOOTHING_FACTOR)

                prev[idx] = (x, y)
                landmarks.append((x, y))

            self.drawer.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
            )

            hands_data.append(
                {
                    "label": label,
                    "landmarks": landmarks,
                    "index_tip": landmarks[8],
                    "thumb_tip": landmarks[4],
                    "middle_tip": landmarks[12],
                    "ring_tip": landmarks[16],
                    "pinky_tip": landmarks[20],
                    "wrist": landmarks[0],
                }
            )

        return frame, hands_data

    def close(self):
        self.hands.close()