import math

WIDTH, HEIGHT = 800, 600 # Window size
GRID_SIZE = 9 # 9x9 grid
SQUARE_SIZE = HEIGHT // GRID_SIZE
BACKGROUND_COLOR = (217, 185, 155)  # Beige
LINE_COLOR = (0, 0, 0)  # Black
FONT_COLOR = (0, 0, 0)  # Black
STONE_RADIUS = SQUARE_SIZE // 3 # Radius of the stones


DEPTH = 5
ALPHA = -math.inf
BETA = math.inf
MAX_DEPTH = 10
MAX_TIME = 3
