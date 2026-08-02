import random


class BloomEffect:
    def __init__(self):

        self.active = False

    def trigger(self, flowers):

        if self.active:
            return

        self.active = True

        for flower in flowers:
            flower.start_bloom()

    def update(self, flowers):

        if not self.active:
            return

        alive = False

        for flower in flowers:

            flower.update()

            if not flower.dead:
                alive = True

        if not alive:
            self.active = False


class WindEffect:

    def __init__(self):

        self.speed = 0.15

    def update(self, flowers):

        for flower in flowers:

            if flower.dead:
                continue

            flower.x += random.uniform(
                -self.speed,
                self.speed,
            )

            flower.y += random.uniform(
                -0.05,
                0.05,
            )