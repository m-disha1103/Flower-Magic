from pathlib import Path

from flower import Flower
from utils import load_folder, random_image


class FlowerManager:

    def __init__(self):

        self.images = load_folder(
            Path("assets/flowers")
        )

        self.flowers = []

        self.max_flowers = 3000

    # -------------------------------------

    def add(self, position):

        if len(self.flowers) >= self.max_flowers:
            self.flowers.pop(0)

        flower = Flower(
            random_image(self.images),
            position,
        )

        self.flowers.append(flower)

    # -------------------------------------

    def update(self):

        alive = []

        for flower in self.flowers:

            flower.update()

            if not flower.dead:
                alive.append(flower)

        self.flowers = alive

    # -------------------------------------

    def bloom(self):

        for flower in self.flowers:
            flower.start_bloom()

    # -------------------------------------

    def clear(self):

        self.flowers.clear()

    # -------------------------------------

    def __len__(self):

        return len(self.flowers)