import cv2
import numpy as np


class Renderer:

    def __init__(self):
        pass

    def draw_flower(self, frame, flower):

        img = flower.image.copy()

        # ---------- Brightness ----------
        img = img.astype(np.float32)
        img[:, :, :3] *= flower.brightness
        img[:, :, :3] = np.clip(img[:, :, :3], 0, 255)
        img = img.astype(np.uint8)

        # ---------- Scale ----------
        h, w = img.shape[:2]

        nw = max(8, int(w * flower.scale))
        nh = max(8, int(h * flower.scale))

        img = cv2.resize(
            img,
            (nw, nh),
            interpolation=cv2.INTER_AREA,
        )

        # ---------- Rotation ----------
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

        if img.shape[2] != 4:
            return

        x = int(flower.x - w / 2)
        y = int(flower.y - h / 2)

        if (
            x < 0
            or y < 0
            or x + w > frame.shape[1]
            or y + h > frame.shape[0]
        ):
            return

        roi = frame[y:y + h, x:x + w]

        alpha = (
            img[:, :, 3].astype(np.float32) / 255.0
        ) * flower.alpha

        for c in range(3):
            roi[:, :, c] = (
                alpha * img[:, :, c]
                + (1 - alpha) * roi[:, :, c]
            )

        frame[y:y + h, x:x + w] = roi

        # ---------- Glow ----------
        if flower.glow > 0:

            radius = int(max(w, h) * 0.7)

            glow = np.zeros_like(frame)

            cv2.circle(
                glow,
                (int(flower.x), int(flower.y)),
                radius,
                (220, 240, 255),
                -1,
                cv2.LINE_AA,
            )

            frame[:] = cv2.addWeighted(
                frame,
                1.0,
                glow,
                flower.glow * 0.18,
                0,
            )

    def draw(self, frame, manager):

        for flower in manager.flowers:
            self.draw_flower(frame, flower)

        return frame