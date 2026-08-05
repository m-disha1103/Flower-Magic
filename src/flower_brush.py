from config import (
    FLOWER_SPACING,
    MAX_FLOWERS,
)

from flower import Flower
from utils import (
    distance,
    interpolate_points,
    random_flower_image,
)


class FlowerBrush:
    """
    Converts fingertip movement into flower placement.
    Supports both hands.
    """

    def __init__(self, flowers):

        self.flowers = flowers

        self.spacing = FLOWER_SPACING

        self.last_points = {
            "Left": None,
            "Right": None,
        }

    # --------------------------------------------------

    def update(self, hands):

        active = set()

        for hand in hands:
            label = hand["label"]
            point = hand["index_tip"]
            active.add(label)
            last = self.last_points[label]
            # First flower
            if last is None:
                self.add_flower(point)
                self.last_points[label] = point
                continue
            # Ignore tiny movement
            if distance(last, point) < self.spacing:
                continue
            # Fill gaps smoothly
            points = interpolate_points(
                last,
                point,
                self.spacing,
            )
            for p in points:
                self.add_flower(p)
            self.last_points[label] = point
        # Reset missing hands
        for label in self.last_points:
            if label not in active:
                self.last_points[label] = None
    # --------------------------------------------------
    def add_flower(self, position):
        image = random_flower_image()
        if image is None:
            return
        self.flowers.append(
            Flower(
                image=image,
                position=position,
            )
        )
        # Keep newest flowers
        if len(self.flowers) > MAX_FLOWERS:
            self.flowers[:] = self.flowers[-MAX_FLOWERS:]
    # --------------------------------------------------
    def clear(self):
        self.flowers.clear()
        self.last_points = {
            "Left": None,
            "Right": None,
        }