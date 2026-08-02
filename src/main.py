import cv2

from camera import Camera
from hand_tracker import HandTracker
from gesture import Gesture

from flower_brush import FlowerBrush
from managers.flower_manager import FlowerManager

from renderer import Renderer
from particles import ParticleEngine
from effects import BloomEffect, WindEffect


def main():

    camera = Camera()
    tracker = HandTracker()

    manager = FlowerManager()
    brush = FlowerBrush(manager)

    renderer = Renderer()

    particles = ParticleEngine()

    bloom = BloomEffect()
    wind = WindEffect()

    bloom_triggered = False

    while True:

        frame = camera.read()

        if frame is None:
            break

        frame, hands = tracker.detect(frame)

        # Draw flowers
        brush.update(hands)

        # -------- Bloom Gesture --------

        open_palm = any(
            Gesture.is_open_palm(hand)
            for hand in hands
        )

        if open_palm and not bloom_triggered:

            bloom.trigger(manager.flowers)

            for flower in manager.flowers:

                particles.emit_petals(
                    flower.position,
                    count=6,
                )

                particles.emit_sparkles(
                    flower.position,
                    count=4,
                )

            bloom_triggered = True

        elif not open_palm:

            bloom_triggered = False

        # -------- Update --------

        bloom.update(manager.flowers)

        wind.update(manager.flowers)

        manager.update()

        particles.update()

        # Remove dead flowers
        manager.flowers = [
            flower
            for flower in manager.flowers
            if not flower.dead
        ]

        # -------- Render --------

        frame = renderer.draw(
            frame,
            manager,
            particles,
        )

        cv2.putText(
            frame,
            f"Flowers : {len(manager.flowers)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.imshow(
            "Flower Magic",
            frame,
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):

            brush.clear()
            particles.clear()

        elif key == ord("q") or key == 27:

            break

    tracker.close()
    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()