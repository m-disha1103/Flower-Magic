import math
import random
from pathlib import Path

import cv2
import numpy as np


# ---------- Math ----------

def distance(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1],
    )


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_point(p1, p2, t):
    return (
        lerp(p1[0], p2[0], t),
        lerp(p1[1], p2[1], t),
    )


def interpolate_points(start, end, spacing):

    d = distance(start, end)

    if d < spacing:
        return []

    count = int(d // spacing)

    points = []

    for i in range(1, count + 1):

        t = (i * spacing) / d

        points.append(
            lerp_point(start, end, t)
        )

    return points


# ---------- Image ----------

_image_cache = {}


def load_png(path):

    path = str(path)

    if path not in _image_cache:

        img = cv2.imread(
            path,
            cv2.IMREAD_UNCHANGED,
        )

        if img is None:
            raise FileNotFoundError(path)

        if img.shape[-1] != 4:
            raise ValueError(
                f"{path} must contain alpha channel."
            )

        _image_cache[path] = img

    return _image_cache[path].copy()


def load_folder(folder):

    folder = Path(folder)

    images = []

    for file in sorted(folder.glob("*.png")):

        images.append(
            load_png(file)
        )

    if not images:
        raise RuntimeError(
            f"No PNGs found in {folder}"
        )

    return images


def random_image(images):
    return random.choice(images).copy()


# ---------- Color ----------

def adjust_brightness(image, factor):

    img = image.astype(np.float32)

    img[:, :, :3] *= factor

    img[:, :, :3] = np.clip(
        img[:, :, :3],
        0,
        255,
    )

    return img.astype(np.uint8)


# ---------- Random ----------

def rand_scale():

    return random.uniform(
        0.75,
        1.25,
    )


def rand_rotation():

    return random.uniform(
        -25,
        25,
    )


def rand_alpha():

    return random.uniform(
        0.85,
        1.0,
    )


def rand_brightness():

    return random.uniform(
        0.85,
        1.15,
    )