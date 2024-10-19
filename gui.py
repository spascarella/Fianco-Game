import pygame
import sys
from constants import *
from game import FiancoBoard
from engine import FiancoEngine
import time

#TODO: 
# Improve Iterative Deepening Search
# Implement killer moves
# Implement Transposition Table
## PRIORITY: IDS, Killer Moves, Transposition Table


class FiancoGUI:
    def __init__(self, board):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fianco Game by Salvatore Pascarella")
        self.font = pygame.font.Font(None, 36)
        self.notation_font = pygame.font.Font(None, 18)  # Smaller font for notation
        self.timer_font = pygame.font.Font(None, 28)  # Font for displaying the timers
        self.board = board  
        self.selected_player1 = "Human"  # Default Player 1 (white) selection
        self.selected_player2 = "Human"  # Default Player 2 (black) selection

        self.selected_piece = None  # Coordinates of the selected piece
        self.valid_moves = []  # List of valid moves for the selected piece
        self.last_move = None  # Last move made by the players

        # Player timers (in seconds) and a variable to track the start time
        self.white_time = 600  # 10 minutes in seconds
        self.black_time = 600  # 10 minutes in seconds
        self.start_time = time.time()  # Keep track of when the player's turn started

    def draw_timers(self):
        """Draw the timers for both players with White on top of Black at the bottom-right corner."""
        padding = 10
        white_timer_text = self.timer_font.render(f"White: {self.format_time(self.white_time)}", True, FONT_COLOR)
        black_timer_text = self.timer_font.render(f"Black: {self.format_time(self.black_time)}", True, FONT_COLOR)

        # Calculate positions for the timers, placing white above black
        white_timer_position = (WIDTH - white_timer_text.get_width() - padding, HEIGHT - black_timer_text.get_height() - white_timer_text.get_height() - (padding * 2))
        black_timer_position = (WIDTH - black_timer_text.get_width() - padding, HEIGHT - black_timer_text.get_height() - padding)

        # Draw the timers on the screen
        self.screen.blit(white_timer_text, white_timer_position)
        self.screen.blit(black_timer_text, black_timer_position)

    def format_time(self, seconds):
        """Convert seconds to a MM:SS format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes):02}:{int(seconds):02}"

    def update_timers(self, current_player):
        """Update the timer for the current player."""
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if current_player == 1:
            self.white_time -= elapsed_time
            if self.white_time <= 0:
                self.white_time = 0
                print("White ran out of time! Black wins!")
                pygame.quit()
                sys.exit()
        else:
            self.black_time -= elapsed_time
            if self.black_time <= 0:
                self.black_time = 0
                print("Black ran out of time! White wins!")
                pygame.quit()
                sys.exit()

        # Reset the start time to the current time
        self.start_time = current_time

    def reset_timers(self):
        """Reset the timers for both players."""
        self.white_time = 600  # Reset white timer to 10 minutes
        self.black_time = 600  # Reset black timer to 10 minutes
        self.start_time = time.time()  # Reset start time

    def draw_homescreen(self):
        '''Draw the homescreen with player selection options.'''
        self.screen.fill(BACKGROUND_COLOR)  # Set the background color to beige
        title = self.font.render("Fianco", True, FONT_COLOR)
        # Center the title
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw Player 1 selection
        self.draw_player_selection("Player 1 (White):  ", 200, self.selected_player1)

        # Draw Player 2 selection
        self.draw_player_selection("Player 2 (Black): ", 300, self.selected_player2)

        # Start button
        self.draw_start_button()

    def draw_player_selection(self, text, y_pos, selected_option):
        '''Draw the player selection options on the homescreen.'''
        label = self.font.render(text, True, FONT_COLOR)
        # Adjust the label position to add more horizontal padding
        self.screen.blit(label, (WIDTH // 2 - 250, y_pos))  # Center the label with more padding

        options = ["Human", "Negamax"]  # Two options: Human and Negamax AI
        for i, option in enumerate(options):
            # Set color red for the selected option
            color = (255, 0, 0) if selected_option == option else FONT_COLOR
            option_text = self.font.render(option, True, color)
            # Reduce spacing between options and add more padding to center them better
            self.screen.blit(option_text, (WIDTH // 2 - 50 + (i * 150), y_pos))  # Adjusted to better center options

    def draw_start_button(self):
        '''Draw the start button on the homescreen.'''
        button_text = self.font.render("Start Game", True, FONT_COLOR)
        self.screen.blit(button_text, (WIDTH // 2 - button_text.get_width() // 2, 410))  # Center the button text

    def handle_homescreen_events(self, event):
        '''Handle the events on the homescreen.'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Player 1 selection
            if WIDTH // 2 - 50 < x < WIDTH // 2 + 100 and 200 < y < 250:  # Human option for Player 1
                self.selected_player1 = "Human"
            elif WIDTH // 2 + 100 < x < WIDTH // 2 + 250 and 200 < y < 250:  # Negamax option for Player 1
                self.selected_player1 = "Negamax"

            # Player 2 selection
            if WIDTH // 2 - 50 < x < WIDTH // 2 + 100 and 300 < y < 350:  # Human option for Player 2
                self.selected_player2 = "Human"
            elif WIDTH // 2 + 100 < x < WIDTH // 2 + 250 and 300 < y < 350:  # Negamax option for Player 2
                self.selected_player2 = "Negamax"

            # Start game button
            if WIDTH // 2 - 150 < x < WIDTH // 2 + 150 and 400 < y < 460:
                if self.selected_player1 and self.selected_player2:
                    return True  # Start the game if both players are selected
        return False

    def player_selection(self):
        '''Display the player selection screen and return the selected players.'''
        running = True
        while running:
            self.draw_homescreen()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.handle_homescreen_events(event):
                    return self.selected_player1, self.selected_player2
    
    def draw_board(self):
        '''Draw the board grid and chess notation.'''
        # Clear the entire screen
        self.screen.fill(BACKGROUND_COLOR)

        # Draw board area background (optional, if you want a different color)
        board_area = pygame.Rect(0, 0, GRID_SIZE * SQUARE_SIZE, HEIGHT)
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, board_area)

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            # Vertical lines
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (i * SQUARE_SIZE, 0),
                (i * SQUARE_SIZE, HEIGHT)
            )
            # Horizontal lines
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (0, i * SQUARE_SIZE),
                (GRID_SIZE * SQUARE_SIZE, i * SQUARE_SIZE)
            )

        # Draw notation only on the board area
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        numbers = [str(i) for i in range(9, 0, -1)]  # Ranks from '9' down to '1'

        # Loop over each cell to draw the notation in the center
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                # Calculate the notation
                notation = letters[c] + numbers[r]
                # Calculate the center position of the cell
                x = c * SQUARE_SIZE + SQUARE_SIZE // 2
                y = r * SQUARE_SIZE + SQUARE_SIZE // 2

                # Render the notation text using the smaller font
                notation_text = self.notation_font.render(notation, True, FONT_COLOR)
                text_rect = notation_text.get_rect(center=(x, y))

                # If the cell is empty, draw the notation
                if self.board.board[r, c] == 0:
                    self.screen.blit(notation_text, text_rect)

    def draw_stones(self):
        '''Draw the stones on the board.'''
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                piece = self.board.board[r, c]
                if piece == 1:
                    # White stone
                    color = (255, 255, 255)  # White
                elif piece == 2:
                    # Black stone
                    color = (0, 0, 0)  # Black
                else:
                    continue  # Empty square, skip

                # Calculate the center of the square
                x = c * SQUARE_SIZE + SQUARE_SIZE // 2
                y = r * SQUARE_SIZE + SQUARE_SIZE // 2

                # Draw the stone
                pygame.draw.circle(self.screen, color, (x, y), STONE_RADIUS)

                # Draw a black outline around the stone for visibility
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), STONE_RADIUS, 1)

    def draw_move_log(self):
        '''Draw the last performed move in the dedicated log area.'''
        # Define the area for the move log
        log_area = pygame.Rect(GRID_SIZE * SQUARE_SIZE, 0, WIDTH - GRID_SIZE * SQUARE_SIZE, HEIGHT)
        pygame.draw.rect(self.screen, (200, 200, 200), log_area)  # Light gray background

        # Draw a vertical line to separate the board and the move log
        pygame.draw.line(
            self.screen, LINE_COLOR,
            (GRID_SIZE * SQUARE_SIZE, 0),
            (GRID_SIZE * SQUARE_SIZE, HEIGHT),
            2  # Line thickness
        )

        # Display the last move
        padding = 10
        y_offset = padding

        if self.last_move:
            move_text = self.font.render("Last Move:", True, FONT_COLOR)
            self.screen.blit(move_text, (GRID_SIZE * SQUARE_SIZE + padding, y_offset))
            y_offset += move_text.get_height() + 5

            player, start_notation, end_notation = self.last_move
            move_detail = f"{player}: {start_notation} to {end_notation}"
            move_detail_text = self.notation_font.render(move_detail, True, FONT_COLOR)
            self.screen.blit(move_detail_text, (GRID_SIZE * SQUARE_SIZE + padding, y_offset))

    def position_to_notation(self, position):
        """Convert board coordinates to notation."""
        row, col = position
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        numbers = [str(i) for i in range(9, 0, -1)]  # '9' down to '1'
        notation = letters[col] + numbers[row]
        return notation

    def handle_click(self, position):
        '''Handle the mouse click events on the board.'''
        x, y = position  # Get the x, y coordinates of the mouse click
        # Check if click is within the board area
        if x >= GRID_SIZE * SQUARE_SIZE:
            return  # Click is outside the board area
        col = x // SQUARE_SIZE  # Calculate the column
        row = y // SQUARE_SIZE  # Calculate the row
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            piece = self.board.board[row, col]  # Get the piece at the clicked position
            if self.selected_piece is None:
                # No piece selected yet
                if piece == self.board.current_player:
                    # Select the piece and get its valid moves and captures
                    self.selected_piece = (row, col)
                    valid_moves, captures = self.board.get_valid_moves_and_captures(self.board.current_player)
                    moves = captures if captures else valid_moves
                    # Filter moves starting from the selected piece
                    self.valid_moves = [move for move in moves if move[0] == self.selected_piece]
            else:
                # A piece is already selected
                if piece == self.board.current_player:
                    # Change selection to the new piece
                    self.selected_piece = (row, col)
                    valid_moves, captures = self.board.get_valid_moves_and_captures(self.board.current_player)
                    moves = captures if captures else valid_moves
                    # Filter moves starting from the new selected piece
                    self.valid_moves = [move for move in moves if move[0] == self.selected_piece]
                else:
                    move = (self.selected_piece, (row, col))
                    if move in self.valid_moves:
                        # Apply the move
                        self.board.apply_move(move)
                        # Update the last move
                        player = 'White' if self.board.current_player == 2 else 'Black'  # current_player has switched
                        start_notation = self.position_to_notation(self.selected_piece)
                        end_notation = self.position_to_notation((row, col))
                        self.last_move = (player, start_notation, end_notation)
                        # Clear the selection
                        self.selected_piece = None
                        self.valid_moves = []
                    else:
                        # Invalid move or click, deselect the piece
                        self.selected_piece = None
                        self.valid_moves = []
        else:
            # Click outside the board, deselect
            self.selected_piece = None
            self.valid_moves = []

# Main game loop as per previous instructions

if __name__ == "__main__":
    board = FiancoBoard()
    gui = FiancoGUI(board)
    engine = FiancoEngine()
    player1, player2 = gui.player_selection()
    gui.draw_board()
    gui.draw_stones()
    gui.draw_move_log()  # Draw the last move in the log area
    gui.draw_timers()  # Draw the timers for the players
    pygame.display.flip()

    running = True
    while running:
        winner = board.is_winner()
        if winner is not None:
            print(f"Player {winner} wins!")
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle pressing the "Q" key to quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    player1, player2 = gui.player_selection()
                    board = FiancoBoard()
                    gui = FiancoGUI(board)
                    engine = FiancoEngine()
                    gui.reset_timers()  # Reset the timers when restarting

            # Handle mouse clicks for human players
            if event.type == pygame.MOUSEBUTTONDOWN:
                gui.update_timers(board.current_player)  # Update the timer for the current player
                if player1 == "Human" and player2 == "Human":
                    position = event.pos
                    gui.handle_click(position)
                    gui.draw_board()
                    gui.draw_stones()
                    gui.draw_move_log()  # Draw the last move in the log area
                    gui.draw_timers()  # Draw the updated timers
                    pygame.display.flip()
                elif player1 == "Human" and player2 == "Negamax":
                    if board.current_player == 1:
                        position = event.pos
                        gui.handle_click(position)
                        gui.draw_board()
                        gui.draw_stones()
                        gui.draw_move_log()  # Draw the last move in the log area
                        gui.draw_timers()  # Draw the updated timers
                        pygame.display.flip()
                elif player1 == "Negamax" and player2 == "Human":
                    if board.current_player == 2:
                        position = event.pos
                        gui.handle_click(position)
                        gui.draw_board()
                        gui.draw_stones()
                        gui.draw_move_log()  # Draw the last move in the log area
                        gui.draw_timers()  # Draw the updated timers
                        pygame.display.flip()

        # Process AI moves outside the event loop
        if not running:
            break  # Exit the loop if the game is over

        if player1 == "Negamax" and board.current_player == 1:
            # Update the AI player timer just before and after making the move
            gui.update_timers(board.current_player)
            best_move = None
            start_time = time.time()
            for depth in range(1, MAX_DEPTH + 1):
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time > MAX_TIME:
                    break
                score, move = engine.negamax(board, depth, ALPHA, BETA, 1)
                if move:
                    best_move = move
                else:
                    break  # No valid moves
            if best_move:
                print(f"Best move: {best_move} found at depth {depth} with score {score} in {elapsed_time:.2f} seconds.")
                board.apply_move(best_move)
                gui.update_timers(board.current_player)  # Update the timer for the current player
                gui.start_time = time.time()  # Reset start time after each move
                # Update the last move
                player = 'White'
                start_pos, end_pos = best_move
                start_notation = gui.position_to_notation(start_pos)
                end_notation = gui.position_to_notation(end_pos)
                gui.last_move = (player, start_notation, end_notation)
            else:
                running = False  # No valid moves, game over

        elif player2 == "Negamax" and board.current_player == 2:
            # Update the AI player timer just before and after making the move
            gui.update_timers(board.current_player)
            best_move = None
            start_time = time.time()
            for depth in range(1, MAX_DEPTH + 1):
                current_time = time.time()
                elapsed_time = current_time - start_time
                if elapsed_time > MAX_TIME:
                    break
                score, move = engine.negamax(board, depth, ALPHA, BETA, -1)
                if move:
                    best_move = move
                else:
                    break  # No valid moves
            if best_move:
                print(f"Best move: {best_move} found at depth {depth} with score {score}")
                board.apply_move(best_move)
                gui.update_timers(board.current_player)  # Update the timer for the current player
                gui.start_time = time.time()  # Reset start time after each move
                # Update the last move
                player = 'Black'
                start_pos, end_pos = best_move
                start_notation = gui.position_to_notation(start_pos)
                end_notation = gui.position_to_notation(end_pos)
                gui.last_move = (player, start_notation, end_notation)
            else:
                running = False  # No valid moves, game over

        gui.draw_board()
        gui.draw_stones()
        gui.draw_move_log()  # Draw the last move in the log area
        gui.draw_timers()  # Draw the updated timers
        pygame.display.flip()