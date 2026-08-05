import cv2

from camera import Camera
from hand_tracker import HandTracker
from gesture import Gesture

from flower_brush import FlowerBrush
from renderer import Renderer
from particles import ParticleEngine


def main():

    camera = Camera()
    tracker = HandTracker()

    flowers = []

    brush = FlowerBrush(flowers)

    renderer = Renderer()

    particles = ParticleEngine()

    bloom_triggered = False

    while True:

        frame = camera.read()

        if frame is None:
            break

        frame, hands = tracker.detect(frame)

        # Draw flowers
        brush.update(hands)

        # Bloom Gesture
        open_palm = any(
            Gesture.is_open_palm(hand)
            for hand in hands
        )

        if open_palm and not bloom_triggered:

            for flower in flowers:

                flower.start_bloom()

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

        # Update flowers
        alive = []

        for flower in flowers:

            flower.update()

            if not flower.dead:
                alive.append(flower)

        # IMPORTANT:
        # Keep the same list object so FlowerBrush, Renderer,
        # and the bloom system all reference the same list.
        flowers[:] = alive

        particles.update()

        frame = renderer.draw(
            frame,
            flowers,
            particles,
        )

        cv2.putText(
            frame,
            f"Flowers : {len(flowers)}",
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

            flowers.clear()
            particles.clear()
            brush.clear()

        elif key == ord("q") or key == 27:

            break

    tracker.close()
    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()