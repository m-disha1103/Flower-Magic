import cv2
import mediapipe as mp


class HandTracker:
    """
    Detects a single hand and returns all 21 landmarks.
    """

    def __init__(
        self,
        max_num_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7,
    ):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process(self, frame):
        """
        Processes a BGR frame.

        Returns:
            frame: frame with landmarks drawn
            landmarks: list of 21 (x, y) pixel coordinates or None
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        landmarks = None

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            h, w, _ = frame.shape

            landmarks = []

            for lm in hand.landmark:

                x = int(lm.x * w)
                y = int(lm.y * h)

                landmarks.append((x, y))

            # Draw hand skeleton
            self.mp_draw.draw_landmarks(
                frame,
                hand,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_draw.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=2,
                    circle_radius=3,
                ),
                self.mp_draw.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2,
                ),
            )

        return frame, landmarks

    def close(self):
        self.hands.close()