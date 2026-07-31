import random


class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.dx = random.uniform(-2, 2)
        self.dy = random.uniform(-4, -1)

        self.life = 60

    def update(self):

        self.x += self.dx
        self.y += self.dy

        self.dy += 0.03
        self.life -= 1


class ParticleSystem:

    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=10):

        for _ in range(count):
            self.particles.append(
                Particle(x, y)
            )

    def update(self):

        for p in self.particles[:]:

            p.update()

            if p.life <= 0:
                self.particles.remove(p)