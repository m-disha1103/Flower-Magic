import cv2
import mediapipe as mp


class HandTracker:
    """
    Detects up to two hands and returns all 21 landmarks for each hand.
    """

    def __init__(
        self,
        max_num_hands=2,
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
        Returns:
            frame
            hands_data

        hands_data = [
            {
                "label": "Left" or "Right",
                "landmarks": [(x, y), ...]
            }
        ]
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        hands_data = []

        if (
            results.multi_hand_landmarks
            and results.multi_handedness
        ):

            h, w, _ = frame.shape

            for hand_landmarks, hand_info in zip(
                results.multi_hand_landmarks,
                results.multi_handedness,
            ):

                label = hand_info.classification[0].label

                landmarks = []

                for lm in hand_landmarks.landmark:

                    x = int(lm.x * w)
                    y = int(lm.y * h)

                    landmarks.append((x, y))

                # Draw landmarks
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
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

                # Display Left / Right label
                cv2.putText(
                    frame,
                    label,
                    (landmarks[0][0], landmarks[0][1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                )

                hands_data.append(
                    {
                        "label": label,
                        "landmarks": landmarks,
                    }
                )

        return frame, hands_data

    def close(self):
        self.hands.close()