import cv2
import random


class Flower:
    def __init__(self, image, position):

        self.original = image

        self.x, self.y = position

        self.scale = random.uniform(0.8, 1.2)
        self.rotation = random.uniform(-30, 30)
        self.alpha = random.uniform(0.85, 1.0)

        self.image = None
        self.update()

    def update(self):

        h, w = self.original.shape[:2]

        img = cv2.resize(
            self.original,
            (
                int(w * self.scale),
                int(h * self.scale),
            ),
            interpolation=cv2.INTER_AREA,
        )

        h, w = img.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w // 2, h // 2),
            self.rotation,
            1,
        )

        self.image = cv2.warpAffine(
            img,
            matrix,
            (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_TRANSPARENT,
        )