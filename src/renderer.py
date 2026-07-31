import cv2


class Renderer:

    @staticmethod
    def draw(frame, flowers):

        for flower in flowers:

            flower.update()

            img = flower.image

            if img is None:
                continue

            if img.shape[2] != 4:
                continue

            h, w = img.shape[:2]

            x = int(flower.x - w / 2)
            y = int(flower.y - h / 2)

            if (
                x < 0
                or y < 0
                or x + w > frame.shape[1]
                or y + h > frame.shape[0]
            ):
                continue

            roi = frame[y:y+h, x:x+w]

            alpha = (
                img[:, :, 3] / 255.0
            ) * flower.alpha

            for c in range(3):
                roi[:, :, c] = (
                    alpha * img[:, :, c]
                    + (1 - alpha) * roi[:, :, c]
                )

            frame[y:y+h, x:x+w] = roi

        return frame