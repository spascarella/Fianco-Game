import math

WIDTH, HEIGHT = 600, 600 # Window size
GRID_SIZE = 9 # 9x9 grid
SQUARE_SIZE = WIDTH // GRID_SIZE
BACKGROUND_COLOR = (217, 185, 155)  # Beige
LINE_COLOR = (0, 0, 0)  # Black
FONT_COLOR = (0, 0, 0)  # Black
STONE_RADIUS = SQUARE_SIZE // 3 # Radius of the stones


DEPTH = 5
ALPHA = -math.inf
BETA = math.inf

WHITE_PLAYER = "AI"
BLACK_PLAYER = "Human"