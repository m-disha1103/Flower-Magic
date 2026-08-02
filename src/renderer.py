import cv2
import numpy as np


class Renderer:

    def __init__(self):
        pass

    # -------------------------------------------------

    def _overlay(self, frame, image, x, y, alpha):

        h, w = image.shape[:2]

        if (
            x < 0
            or y < 0
            or x + w > frame.shape[1]
            or y + h > frame.shape[0]
        ):
            return

        roi = frame[y:y+h, x:x+w]

        mask = (image[:, :, 3].astype(np.float32) / 255.0) * alpha

        for c in range(3):

            roi[:, :, c] = (
                mask * image[:, :, c]
                + (1 - mask) * roi[:, :, c]
            )

        frame[y:y+h, x:x+w] = roi

    # -------------------------------------------------

    def draw_flower(self, frame, flower):

        img = flower.image.copy()

        # Brightness
        img = img.astype(np.float32)
        img[:, :, :3] *= flower.brightness
        img[:, :, :3] = np.clip(img[:, :, :3], 0, 255)
        img = img.astype(np.uint8)

        # Scale
        h, w = img.shape[:2]

        nw = max(8, int(w * flower.scale))
        nh = max(8, int(h * flower.scale))

        img = cv2.resize(
            img,
            (nw, nh),
            interpolation=cv2.INTER_AREA,
        )

        # Rotate
        h, w = img.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w / 2, h / 2),
            flower.rotation,
            1,
        )

        img = cv2.warpAffine(
            img,
            matrix,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_TRANSPARENT,
        )

        self._overlay(
            frame,
            img,
            int(flower.x - w / 2),
            int(flower.y - h / 2),
            flower.alpha,
        )

    # -------------------------------------------------

    def draw_particle(self, frame, particle):

        img = particle.image

        h, w = img.shape[:2]

        nw = max(4, int(w * particle.scale))
        nh = max(4, int(h * particle.scale))

        img = cv2.resize(
            img,
            (nw, nh),
            interpolation=cv2.INTER_AREA,
        )

        h, w = img.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w / 2, h / 2),
            particle.rotation,
            1,
        )

        img = cv2.warpAffine(
            img,
            matrix,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_TRANSPARENT,
        )

        self._overlay(
            frame,
            img,
            int(particle.x - w / 2),
            int(particle.y - h / 2),
            particle.alpha,
        )

    # -------------------------------------------------

    def draw(
        self,
        frame,
        manager,
        particles=None,
    ):

        # Flowers
        for flower in manager.flowers:
            self.draw_flower(frame, flower)

        # Particles
        if particles:

            for particle in particles.particles:
                self.draw_particle(
                    frame,
                    particle,
                )

        return frame