import random
import math

from config import (
    BLOOM_SCALE_SPEED,
    BLOOM_ROTATION_SPEED,
    BLOOM_FADE_SPEED,
)

from utils import (
    rand_alpha,
    rand_brightness,
    rand_rotation,
    rand_scale,
)


class Flower:
    """
    Animated flower object.
    Rendering is handled by renderer.py.
    """

    def __init__(self, image, position):

        self.image = image

        self.x = float(position[0])
        self.y = float(position[1])

        # ---------------- Appearance ----------------

        self.target_scale = rand_scale()

        # Start tiny for bloom animation
        self.scale = self.target_scale * 0.15

        self.rotation = rand_rotation()

        self.alpha = rand_alpha()

        self.brightness = rand_brightness()

        self.glow = 1.0

        # ---------------- Animation ----------------

        self.age = 0

        self.dead = False

        self.blooming = True

        self.bloom_progress = 0.0

        # ---------------- Floating Motion ----------------

        self.float_offset = random.uniform(0, math.pi * 2)

        self.float_speed = random.uniform(0.015, 0.035)

        self.float_strength = random.uniform(0.15, 0.5)

        self.vx = random.uniform(-0.05, 0.05)

        self.vy = random.uniform(-0.05, 0.05)

    # -----------------------------------------------------

    @property
    def position(self):
        return (self.x, self.y)

    # -----------------------------------------------------

    def start_bloom(self):
        self.blooming = True

    # -----------------------------------------------------

    def update(self):

        self.age += 1

        # Gentle floating
        self.float_offset += self.float_speed

        self.x += self.vx
        self.y += self.vy + math.sin(self.float_offset) * self.float_strength

        # ---------------- Spawn Bloom ----------------

        if self.blooming:

            self.bloom_progress = min(
                1.0,
                self.bloom_progress + 0.08,
            )

            ease = (
                1.0
                - (1.0 - self.bloom_progress)
                * (1.0 - self.bloom_progress)
            )

            self.scale = (
                self.target_scale * ease
            )
            self.rotation += BLOOM_ROTATION_SPEED
            self.glow = max(
                0.0,
                self.glow - 0.03,
            )
            if self.bloom_progress >= 1.0:
                self.blooming = False
        # ---------------- Explosion Bloom ----------------
        else:
            self.scale = (
                self.scale * 0.999
                + self.target_scale * 0.001
            )
        # If flower alpha is already reduced externally,
        # fade naturally until removed.
        if self.alpha < 1.0:
            self.alpha -= BLOOM_FADE_SPEED
            if self.alpha <= 0.0:
                self.alpha = 0.0
                self.dead = True