import time


class BloomEffect:

    def __init__(self):
        self.active = False
        self.start = 0
        self.duration = 1.2

    def trigger(self):
        if not self.active:
            self.active = True
            self.start = time.time()

    def update(self, flowers):

        if not self.active:
            return False

        t = (time.time() - self.start) / self.duration

        if t >= 1:
            self.active = False
            flowers.clear()
            return False

        scale = 1 + 0.5 * t

        for flower in flowers:
            flower.scale *= 1.003
            flower.rotation += 0.4
            flower.alpha = max(0.0, 1 - t)

        return True