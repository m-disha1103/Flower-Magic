from utils import distance, interpolate_points


class FlowerBrush:
    """
    Responsible only for converting fingertip movement
    into flower placement requests.
    """

    def __init__(self, manager):

        self.manager = manager

        self.spacing = 18

        self.last_points = {
            "Left": None,
            "Right": None,
        }

    def update(self, hands):

        active = set()

        for hand in hands:

            label = hand["label"]
            point = hand["index_tip"]

            active.add(label)

            last = self.last_points[label]

            # First flower
            if last is None:

                self.manager.add(point)
                self.last_points[label] = point
                continue

            # Ignore tiny movements
            if distance(last, point) < self.spacing:
                continue

            # Fill gaps when moving fast
            points = interpolate_points(
                last,
                point,
                self.spacing,
            )

            for p in points:
                self.manager.add(p)

            self.last_points[label] = point

        # Reset hands that disappeared
        for label in self.last_points:

            if label not in active:
                self.last_points[label] = None

    def clear(self):

        self.manager.clear()

        for hand in self.last_points:
            self.last_points[hand] = None