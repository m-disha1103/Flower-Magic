# ==========================================================
# Flower Magic Configuration
# ==========================================================

# ---------------- Camera ----------------

CAMERA_ID = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

TARGET_FPS = 60

WINDOW_NAME = "Flower Magic"


# ---------------- Hand Tracking ----------------

MAX_NUM_HANDS = 2

DETECTION_CONFIDENCE = 0.75
TRACKING_CONFIDENCE = 0.75

SMOOTHING_FACTOR = 0.45


# ---------------- Brush ----------------

FLOWER_SPACING = 14
MIN_FLOWER_DISTANCE = 12


# ---------------- Flower ----------------

FLOWER_MIN_SCALE = 0.70
FLOWER_MAX_SCALE = 1.20

FLOWER_MIN_ROTATION = -30
FLOWER_MAX_ROTATION = 30

FLOWER_MIN_ALPHA = 220
FLOWER_MAX_ALPHA = 255

FLOWER_MIN_BRIGHTNESS = 0.90
FLOWER_MAX_BRIGHTNESS = 1.15


# ---------------- Bloom ----------------

BLOOM_DURATION = 1.2
BLOOM_SCALE_SPEED = 1.012
BLOOM_ROTATION_SPEED = 0.8
BLOOM_FADE_SPEED = 0.01


# ---------------- Butterflies ----------------

MAX_BUTTERFLIES = 25
BUTTERFLY_SCALE = 0.55
BUTTERFLY_SPEED = 2.4
BUTTERFLY_FLAP_FPS = 18


# ---------------- Petals ----------------

PETAL_LIFETIME = 45
PETAL_SPEED_MIN = 1.0
PETAL_SPEED_MAX = 3.5
PETAL_ROTATION_SPEED = 6


# ---------------- Sparkles ----------------

SPARKLE_LIFETIME = 25
SPARKLE_SPEED_MIN = 0.8
SPARKLE_SPEED_MAX = 2.2


# ---------------- Particles ----------------

MAX_PARTICLES = 1200

PETALS_PER_FLOWER = 6
SPARKLES_PER_FLOWER = 4


# ---------------- Performance ----------------

MAX_FLOWERS = 3000
MAX_TRAIL_POINTS = 5000


# ---------------- Colors ----------------

GLOW_COLOR = (255, 180, 255)