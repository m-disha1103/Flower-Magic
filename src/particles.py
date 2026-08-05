import random
from pathlib import Path

from utils import load_folder, random_image


class Particle:
    def __init__(self, image, position):

        self.image = image

        self.x = float(position[0])
        self.y = float(position[1])

        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-5.5, -2.5)

        self.scale = random.uniform(0.25, 0.75)

        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-8, 8)

        self.alpha = 1.0

        self.gravity = 0.18

        self.life = random.randint(55, 90)

        self.dead = False

    # ---------------------------------------------

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += self.gravity

        self.rotation += self.rotation_speed

        self.alpha *= 0.985

        self.life -= 1

        if self.life <= 0 or self.alpha < 0.03:
            self.dead = True


# =====================================================


class ParticleEngine:

    def __init__(self):

        self.petal_images = load_folder(
            Path("assets/petals")
        )

        self.sparkle_images = load_folder(
            Path("assets/sparkle")
        )

        self.particles = []

        self.max_particles = 300

    # ---------------------------------------------

    def emit_petals(self, position, count=8):

        for _ in range(count):

            image = random_image(self.petal_images)

            if image is None:
                continue

            self.particles.append(
                Particle(image, position)
            )

    # ---------------------------------------------

    def emit_sparkles(self, position, count=6):

        for _ in range(count):

            image = random_image(self.sparkle_images)

            if image is None:
                continue

            p = Particle(image, position)

            p.scale *= 0.6
            p.life = 40

            self.particles.append(p)

    # ---------------------------------------------

    def update(self):

        alive = []

        for particle in self.particles:

            particle.update()

            if not particle.dead:
                alive.append(particle)

        self.particles = alive[-self.max_particles:]

    # ---------------------------------------------

    def clear(self):

        self.particles.clear()