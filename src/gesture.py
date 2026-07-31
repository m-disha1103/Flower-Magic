import math


class Gesture:

    @staticmethod
    def distance(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    @staticmethod
    def is_open_palm(hand):

        tips = [
            hand["thumb_tip"],
            hand["index_tip"],
            hand["middle_tip"],
            hand["ring_tip"],
            hand["pinky_tip"],
        ]

        wrist = hand["wrist"]

        count = 0

        for tip in tips:
            if Gesture.distance(tip, wrist) > 110:
                count += 1

        return count >= 4

    @staticmethod
    def is_pinching(hand):

        return (
            Gesture.distance(
                hand["thumb_tip"],
                hand["index_tip"],
            )
            < 35
        )