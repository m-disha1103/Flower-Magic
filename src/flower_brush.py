import cv2
import math

from flower import Flower
from config import MIN_FLOWER_DISTANCE


class FlowerBrush:
    def __init__(self, flower_path):
        self.template = cv2.imread(
            flower_path,
            cv2.IMREAD_UNCHANGED,
        )

        if self.template is None:
            raise FileNotFoundError(flower_path)

        self.flowers = []

        self.last = {
            "Left": None,
            "Right": None,
        }

    def update(self, hands):

        for hand in hands:

            label = hand["label"]
            point = hand["index_tip"]

            last = self.last[label]

            if last is None:
                self.flowers.append(
                    Flower(self.template, point)
                )
                self.last[label] = point
                continue

            dist = math.hypot(
                point[0] - last[0],
                point[1] - last[1],
            )

            if dist >= MIN_FLOWER_DISTANCE:
                self.flowers.append(
                    Flower(self.template, point)
                )
                self.last[label] = point

    def clear(self):
        self.flowers.clear()

        self.last = {
            "Left": None,
            "Right": None,
        }