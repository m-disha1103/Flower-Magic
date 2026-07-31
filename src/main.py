import cv2

from camera import Camera
from hand_tracker import HandTracker
from flower_brush import FlowerBrush
from renderer import Renderer
from gesture import Gesture
from effects import BloomEffect
from particles import ParticleSystem


FLOWER_IMAGE = "assets/flowers/flower.png"


def main():

    camera = Camera()
    tracker = HandTracker()

    brush = FlowerBrush(FLOWER_IMAGE)
    bloom = BloomEffect()
    particles = ParticleSystem()

    while True:

        frame = camera.read()

        if frame is None:
            break

        frame, hands = tracker.detect(frame)

        # Draw flowers
        brush.update(hands)

        # Bloom gesture
        for hand in hands:

            if Gesture.is_open_palm(hand):

                bloom.trigger()

                for flower in brush.flowers:
                    particles.emit(
                        flower.x,
                        flower.y,
                        6,
                    )

        # Animate bloom
        bloom.update(brush.flowers)

        # Update particles
        particles.update()

        # Render flowers
        frame = Renderer.draw(
            frame,
            brush.flowers,
        )

        # Draw particles
        for p in particles.particles:

            if p.life <= 0:
                continue

            cv2.circle(
                frame,
                (int(p.x), int(p.y)),
                2,
                (210, 210, 255),
                -1,
            )

        cv2.putText(
            frame,
            f"Flowers : {len(brush.flowers)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.imshow("Flower Magic", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            brush.clear()

        elif key == 27 or key == ord("q"):
            break

    tracker.close()
    camera.release()


if __name__ == "__main__":
    main()