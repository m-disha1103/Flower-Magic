from pathlib import Path
from flower import Flower
from utils import load_folder, random_image


class FlowerManager:
    def __init__(self):

        self.images = load_folder(
            Path("assets/flowers")
        )

        self.flowers = []

    def add(self, position):

        flower = Flower(
            random_image(self.images),
            position,
        )

        self.flowers.append(flower)

    def draw(self, renderer, frame):

        for flower in self.flowers:
            renderer.draw_flower(frame, flower)

    def bloom(self):

        for flower in self.flowers:
            flower.bloom()

    def update(self):

        alive = []

        for flower in self.flowers:

            flower.update()

            if flower.alpha > 0.02:
                alive.append(flower)

        self.flowers = alive

    def clear(self):

        self.flowers.clear()