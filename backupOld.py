import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 9
SQUARE_SIZE = WIDTH // GRID_SIZE
BACKGROUND_COLOR = (217, 185, 155)  # Beige
LINE_COLOR = (0, 0, 0)  # Black
FONT_COLOR = (0, 0, 0)  # Black
STONE_RADIUS = SQUARE_SIZE // 3

# Starting positions (black on top, white on bottom)
initial_setup = {
    'A1': 'black', 'B1': 'black', 'C1': 'black', 'D1': 'black', 'E1': 'black', 'F1': 'black', 'G1': 'black', 'H1': 'black', 'I1': 'black',
    'B2': 'black', 'H2': 'black', 'C3': 'black', 'G3': 'black', 'D4': 'black', 'F4': 'black',
    'A9': 'white', 'B9': 'white', 'C9': 'white', 'D9': 'white', 'E9': 'white', 'F9': 'white', 'G9': 'white', 'H9': 'white', 'I9': 'white',
    'B8': 'white', 'H8': 'white', 'C7': 'white', 'G7': 'white', 'D6': 'white', 'F6': 'white',
}

current_turn = 'white'  # 'white' starts the game
selected_stone = None # no stones selected at the beginning
previous_state = None # no previous state at the beginning


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fianco Game by Salvatore Pascarella")

def notation_to_coords(notation):
    """Convert chess notation to (row, col)."""
    if len(notation) < 2:
        return None
    col_letter, row_number = notation[0].upper(), notation[1:]
    if col_letter not in 'ABCDEFGHI' or row_number not in '123456789':
        return None
    col = ord(col_letter) - ord('A')
    row = 9 - int(row_number)  # Invert the row number for our coordinate system
    return (row, col)

def coords_to_notation(row, col):
    """Convert (row, col) to chess notation."""
    return f"{chr(ord('A') + col)}{GRID_SIZE - row}"

def draw_board():
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont(None, 24)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, BACKGROUND_COLOR, rect)  # Fill with beige color
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)  # Draw the border with black lines
            
            # Draw chess notation
            notation = f"{chr(ord('A') + col)}{GRID_SIZE - row}"
            label = font.render(notation, True, FONT_COLOR)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

            # Draw stones
            for pos, color in initial_setup.items():
                stone_row, stone_col = notation_to_coords(pos)
                if (row, col) == (stone_row, stone_col):
                    draw_stone(row, col, color)


def draw_stone(row, col, color):
    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.circle(screen, (0, 0, 0) if color == 'black' else (255, 255, 255), center, STONE_RADIUS)


def get_valid_moves_and_captures(player):
    """Generate all valid moves including captures for the current player and check for a winner."""

    valid_moves = []
    valid_captures = []
    
    for pos, color in initial_setup.items():
        if color == player:
            start_row, start_col = notation_to_coords(pos)

            # Depending on the player, determine the possible move directions
            if player == 'black':
                # Black moves forward (row decreases) or sideways (col changes by 1)
                possible_moves = [
                    (start_row - 1, start_col),  # Forward
                    (start_row, start_col - 1),  # Left
                    (start_row, start_col + 1),  # Right
                ]
                possible_captures = [
                    (start_row - 2, start_col - 2),  # Diagonally left forward capture
                    (start_row - 2, start_col + 2),  # Diagonally right forward capture
                ]
            elif player == 'white':
                # White moves forward (row increases) or sideways (col changes by 1)
                possible_moves = [
                    (start_row + 1, start_col),  # Forward
                    (start_row, start_col - 1),  # Left
                    (start_row, start_col + 1),  # Right
                ]
                possible_captures = [
                    (start_row + 2, start_col - 2),  # Diagonally left forward capture
                    (start_row + 2, start_col + 2),  # Diagonally right forward capture
                ]

            # Check if each possible capture is valid
            for capture_row, capture_col in possible_captures:
                if 0 <= capture_row < GRID_SIZE and 0 <= capture_col < GRID_SIZE:
                    end_pos = coords_to_notation(capture_row, capture_col)
                    mid_row, mid_col = (start_row + capture_row) // 2, (start_col + capture_col) // 2
                    mid_pos = coords_to_notation(mid_row, mid_col)

                    # Check if there's an opponent's stone to capture and the target cell is empty
                    opponent_color = 'white' if player == 'black' else 'black'
                    if initial_setup.get(end_pos) is None and initial_setup.get(mid_pos) == opponent_color:
                        valid_captures.append((pos, end_pos)) 
            if not valid_captures:  # If no captures are available, check for regular moves
                # Check if each possible move is within bounds and to an empty cell
                for move_row, move_col in possible_moves:
                    if 0 <= move_row < GRID_SIZE and 0 <= move_col < GRID_SIZE:
                        end_pos = coords_to_notation(move_row, move_col)
                        if initial_setup.get(end_pos) is None:  # Check if the target cell is empty
                            valid_moves.append((pos, end_pos))
            else:
                valid_moves = []

    # Check if the player has no valid moves or captures
    if not valid_moves and not valid_captures:
        opponent_color = 'white' if player == 'black' else 'black'
        print(f"{opponent_color} wins due to no valid moves for {player}!")
        return valid_moves, valid_captures, opponent_color  # Return opponent as winner
    
#TODO improve this next iteration by moving it up in the first one
    # Check if a player has won by reaching the last row or by eliminating all opponent's pieces
    for pos, color in initial_setup.items():
        row, _ = notation_to_coords(pos)
        if color == 'black' and row == 0:  # Black wins by reaching row 0
            return valid_moves, valid_captures, 'black'
        elif color == 'white' and row == 8:  # White wins by reaching row 8
            return valid_moves, valid_captures, 'white'

    if count_pieces('black') == 0:  # White wins if black has no pieces left
        return None, None, 'white'
    elif count_pieces('white') == 0:  # Black wins if white has no pieces left
        return None, None, 'black'

    return valid_moves, valid_captures, None  # No winner yet               

def restart():
    global initial_setup, selected_stone, current_turn
    initial_setup = {
        'A1': 'black', 'B1': 'black', 'C1': 'black', 'D1': 'black', 'E1': 'black', 'F1': 'black', 'G1': 'black', 'H1': 'black', 'I1': 'black',
        'B2': 'black', 'H2': 'black', 'C3': 'black', 'G3': 'black', 'D4': 'black', 'F4': 'black',
        'A9': 'white', 'B9': 'white', 'C9': 'white', 'D9': 'white', 'E9': 'white', 'F9': 'white', 'G9': 'white', 'H9': 'white', 'I9': 'white',
        'B8': 'white', 'H8': 'white', 'C7': 'white', 'G7': 'white', 'D6': 'white', 'F6': 'white',
    }
    selected_stone = None
    current_turn = 'white'
    if previous_state:
        previous_state = None
    if valid_moves:
        valid_moves = []
    if valid_captures:
        valid_captures = []
    print("Game restarted!")

def save_last_move():
    """Save the current state of the game for undo purposes."""
    global previous_state
    # Deep copy of the current game state (positions and turn)
    previous_state = (initial_setup.copy(), current_turn)

def undo_move():
    """Undo the last move."""
    global initial_setup, current_turn, previous_state
    if previous_state:
        # Restore the previous state
        initial_setup, current_turn = previous_state
        print("Move undone!")
    else:
        print("No move to undo!")

def count_pieces(player):
    """Count how many pieces a player has left."""
    return sum(1 for pos, color in initial_setup.items() if color == player)

def handle_input():
    """Handle the player's input for moving or capturing stones."""
    global selected_stone, current_turn

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Restart the game
                restart()
            elif event.key == pygame.K_u:  # Undo the last move
                undo_move()
            print(f"current_turn: {current_turn}")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            col = mouse_pos[0] // SQUARE_SIZE
            row = mouse_pos[1] // SQUARE_SIZE
            clicked_pos = coords_to_notation(row, col)

            # Get valid moves and captures for the current turn
            valid_moves, valid_captures, winner = get_valid_moves_and_captures(current_turn)
            
            if winner == 'black':
                print("Black wins!")
                return
            elif winner == 'white':
                print("White wins!")
                return  
            

            # If no stone is selected, check if the clicked cell contains the current player's stone
            if not selected_stone:
                if initial_setup.get(clicked_pos) == current_turn:
                    selected_stone = clicked_pos
                    print(f"Selected stone at {selected_stone}")
            else:
                # If valid captures exist, the player must capture
                if valid_captures:
                    for start, end in valid_captures:
                        if start == selected_stone and end == clicked_pos:
                            # Perform the capture
                            save_last_move()
                            initial_setup.pop(selected_stone)  # Remove the selected stone from its current position
                            initial_setup[clicked_pos] = current_turn  # Move the stone to the new position
                            
                            # Remove the captured stone
                            mid_row, mid_col = (notation_to_coords(selected_stone)[0] + notation_to_coords(clicked_pos)[0]) // 2, \
                                               (notation_to_coords(selected_stone)[1] + notation_to_coords(clicked_pos)[1]) // 2
                            mid_pos = coords_to_notation(mid_row, mid_col)
                            initial_setup.pop(mid_pos)  # Remove the captured stone
                            
                            selected_stone = None
                            current_turn = 'black' if current_turn == 'white' else 'white'  # Switch turn
                            print(f"{current_turn}'s turn")
                            return

                    # If the player clicked somewhere else and there are valid captures, deselect the stone
                    selected_stone = None
                    print("Capture required. Deselecting stone.")
                    return  # Prevent any further move if a capture is available but not made

                # If no captures exist, allow regular movement
                else:
                    for start, end in valid_moves:
                        if start == selected_stone and end == clicked_pos:
                            # Perform the move
                            save_last_move()
                            initial_setup.pop(selected_stone)  # Remove the selected stone from its current position
                            initial_setup[clicked_pos] = current_turn  # Move the stone to the new position
                            selected_stone = None
                            current_turn = 'black' if current_turn == 'white' else 'white'  # Switch turn
                            print(f"{current_turn}'s turn")
                            return

                # If the clicked position is invalid, deselect the stone
                selected_stone = None
                print("Invalid move, deselecting stone.")

    
# Main loop
running = True
while running:
    handle_input()
    # Draw everything
    screen.fill(BACKGROUND_COLOR)
    draw_board()
    pygame.display.flip()
