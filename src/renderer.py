import cv2
import numpy as np


class Renderer:
    """
    Renders flowers and particles.
    """

    # --------------------------------------------------

    @staticmethod
    def overlay(frame, image, x, y, alpha=1.0):

        if image is None:
            return

        if len(image.shape) != 3:
            return

        if image.shape[2] != 4:
            return

        h, w = image.shape[:2]
        fh, fw = frame.shape[:2]

        x1 = max(0, x)
        y1 = max(0, y)

        x2 = min(fw, x + w)
        y2 = min(fh, y + h)

        if x1 >= x2 or y1 >= y2:
            return

        sx1 = x1 - x
        sy1 = y1 - y
        sx2 = sx1 + (x2 - x1)
        sy2 = sy1 + (y2 - y1)

        overlay = image[sy1:sy2, sx1:sx2]

        alpha_mask = (
            overlay[:, :, 3].astype(np.float32) / 255.0
        ) * alpha

        alpha_mask = alpha_mask[..., None]

        roi = frame[y1:y2, x1:x2].astype(np.float32)

        rgb = overlay[:, :, :3].astype(np.float32)

        blended = rgb * alpha_mask + roi * (1.0 - alpha_mask)

        frame[y1:y2, x1:x2] = blended.astype(np.uint8)

    # --------------------------------------------------

    @staticmethod
    def rotate_rgba(image, angle):

        h, w = image.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w / 2, h / 2),
            angle,
            1.0,
        )

        channels = cv2.split(image)

        rotated = []

        for channel in channels:

            rotated.append(
                cv2.warpAffine(
                    channel,
                    matrix,
                    (w, h),
                    flags=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=0,
                )
            )

        return cv2.merge(rotated)

    # --------------------------------------------------

    def draw_flower(self, frame, flower):

        if flower.image is None:
            return

        img = flower.image.copy().astype(np.float32)

        img[:, :, :3] *= flower.brightness

        img[:, :, :3] = np.clip(
            img[:, :, :3],
            0,
            255,
        )

        img = img.astype(np.uint8)

        h, w = img.shape[:2]

        scale = max(0.15, flower.scale * 0.18)

        nw = max(24, int(w * scale))
        nh = max(24, int(h * scale))

        img = cv2.resize(
            img,
            (nw, nh),
            interpolation=cv2.INTER_AREA,
        )

        img = self.rotate_rgba(
            img,
            flower.rotation,
        )

        h, w = img.shape[:2]

        self.overlay(
            frame,
            img,
            int(flower.x - w / 2),
            int(flower.y - h / 2),
            flower.alpha,
        )

    # --------------------------------------------------

    def draw_particle(self, frame, particle):

        if particle.image is None:
            return

        img = particle.image.copy()

        h, w = img.shape[:2]

        nw = max(6, int(w * particle.scale))
        nh = max(6, int(h * particle.scale))

        img = cv2.resize(
            img,
            (nw, nh),
            interpolation=cv2.INTER_AREA,
        )

        img = self.rotate_rgba(
            img,
            particle.rotation,
        )

        h, w = img.shape[:2]

        self.overlay(
            frame,
            img,
            int(particle.x - w / 2),
            int(particle.y - h / 2),
            particle.alpha,
        )

    # --------------------------------------------------

    def draw(self, frame, flowers, particles=None):

        for flower in flowers:
            self.draw_flower(frame, flower)

        if particles is not None:

            for particle in particles.particles:
                self.draw_particle(
                    frame,
                    particle,
                )

        return frame