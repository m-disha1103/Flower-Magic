import math
import random
from pathlib import Path

import cv2


# ---------------------------------------------------
# Random values
# ---------------------------------------------------

def rand_scale():
    return random.uniform(0.55, 1.15)


def rand_rotation():
    return random.uniform(0, 360)


def rand_alpha():
    return random.uniform(0.85, 1.0)


def rand_brightness():
    return random.uniform(0.85, 1.15)


# ---------------------------------------------------
# Math
# ---------------------------------------------------

def distance(a, b):
    return math.hypot(
        a[0] - b[0],
        a[1] - b[1],
    )


def interpolate_points(start, end, spacing):
    dist = distance(start, end)

    if dist < spacing:
        return [end]

    steps = max(1, int(dist / spacing))

    points = []

    for i in range(1, steps + 1):
        t = i / steps

        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t

        points.append((int(x), int(y)))

    return points


# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FLOWERS_DIR = ASSETS_DIR / "flowers"


# ---------------------------------------------------
# Image Loading
# ---------------------------------------------------

def load_folder(folder):
    folder = Path(folder)

    images = []

    if not folder.exists():
        print(f"[FlowerMagic] Folder not found: {folder}")
        return images

    for file in sorted(folder.iterdir()):

        if file.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue

        image = cv2.imread(
            str(file),
            cv2.IMREAD_UNCHANGED,
        )

        if image is None:
            print(f"[FlowerMagic] Failed to load: {file.name}")
            continue

        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGRA)

        elif image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        images.append(image)

    print(f"[FlowerMagic] Loaded {len(images)} flower images.")

    return images


# ---------------------------------------------------
# Flower Assets
# ---------------------------------------------------

FLOWER_IMAGES = load_folder(FLOWERS_DIR)


def random_flower_image():
    if not FLOWER_IMAGES:
        return None

    return random.choice(FLOWER_IMAGES)


# ---------------------------------------------------
# Generic Helper
# ---------------------------------------------------

def random_image(images):
    if not images:
        return None

    return random.choice(images)