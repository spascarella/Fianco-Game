import math

WIDTH, HEIGHT = 800, 600 
GRID_SIZE = 9 
SQUARE_SIZE = HEIGHT // GRID_SIZE
BACKGROUND_COLOR = (217, 185, 155)  
LINE_COLOR = (0, 0, 0)  
FONT_COLOR = (0, 0, 0)  
STONE_RADIUS = SQUARE_SIZE // 3 # 


DEPTH = 5
ALPHA = -math.inf
BETA = math.inf
MAX_DEPTH = 10
MAX_TIME = 3
