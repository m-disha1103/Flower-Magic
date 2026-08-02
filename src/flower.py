import random

from utils import (
    rand_alpha,
    rand_brightness,
    rand_rotation,
    rand_scale,
)


class Flower:
    """
    Lightweight flower object.

    Rendering is handled by renderer.py
    Animation is handled by effects.py
    Placement is handled by flower_brush.py
    """

    def __init__(self, image, position):

        # Original PNG (RGBA)
        self.image = image

        # Position
        self.x = float(position[0])
        self.y = float(position[1])

        # Random appearance
        self.scale = rand_scale()
        self.rotation = rand_rotation()
        self.alpha = rand_alpha()
        self.brightness = rand_brightness()

        # Animation state
        self.glow = 0.0
        self.blooming = False
        self.dead = False

        # Motion (used later for petals / wind)
        self.vx = 0.0
        self.vy = 0.0

        # Lifetime
        self.age = 0

    def start_bloom(self):
        """Trigger bloom animation."""
        self.blooming = True

    def update(self):

        self.age += 1

        if self.blooming:

            # Smooth growth
            self.scale *= 1.012

            # Gentle rotation
            self.rotation += 0.6

            # Glow intensity
            self.glow = min(1.0, self.glow + 0.04)

            # Fade away
            self.alpha -= 0.010

            if self.alpha <= 0:

                self.alpha = 0
                self.dead = True

        else:

            # Keep glow fading naturally
            self.glow *= 0.96

    @property
    def position(self):
        return (self.x, self.y)