import pygame
import sys
from constants import *
from game import FiancoBoard
from engine import FiancoEngine

class FiancoGUI:
    def __init__(self, board):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fianco Game by Salvatore Pascarella")
        self.font = pygame.font.Font(None, 36)
        self.notation_font = pygame.font.Font(None, 18)  # Smaller font for notation
        self.board = board  
        self.selected_player1 = "Human"  # Default Player 1 (white) selection
        self.selected_player2 = "Human"  # Default Player 2 (black) selection

        self.selected_piece = None  # Coordinates of the selected piece
        self.valid_moves = []  # List of valid moves for the selected piece


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
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            # Vertical lines
            pygame.draw.line(self.screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT))
            # Horizontal lines
            pygame.draw.line(self.screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE))

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
                #if self.board.board[r, c] == 0:
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

    def handle_click(self, position):
        '''Handle the mouse click events on the board.'''
        x, y = position  # Get the x, y coordinates of the mouse click
        col = x // SQUARE_SIZE  # Calculate the column
        row = y // SQUARE_SIZE  # Calculate the row
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:
            piece = self.board.board[row, col]  # Get the piece at the clicked position
            if self.selected_piece is None:
                # No piece selected yet
                if piece == self.board.current_player:
                    # Select the piece and get its valid moves and captures
                    self.selected_piece = (row, col)
                    print("Selected piece:", self.selected_piece)
                    valid_moves, captures = self.board.get_valid_moves_and_captures(self.board.current_player)
                    moves = captures if captures else valid_moves
                    print("Valid moves:", moves)
                    # Filter moves starting from the selected piece
                    self.valid_moves = [move for move in moves if move[0] == self.selected_piece]
            else:
                print("Selected piece:", self.selected_piece)
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


if __name__ == "__main__":
    board = FiancoBoard()
    gui = FiancoGUI(board)
    engine = FiancoEngine()
    player1, player2 = gui.player_selection()
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

            # Handle mouse clicks for human players
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player1 == "Human" and player2 == "Human":
                    position = event.pos
                    gui.handle_click(position)
                elif player1 == "Human" and player2 == "Negamax":
                    if board.current_player == 1:
                        position = event.pos
                        gui.handle_click(position)
                elif player1 == "Negamax" and player2 == "Human":
                    if board.current_player == 2:
                        position = event.pos
                        gui.handle_click(position)

        # Process AI moves outside the event loop
        if not running:
            break  # Exit the loop if the game is over

        if player1 == "Negamax" and board.current_player == 1:
            print("Player 1 (AI) is thinking...")
            score, best_move = engine.negamax(board, DEPTH, ALPHA, BETA, 1)
            board.apply_move(best_move)

        elif player2 == "Negamax" and board.current_player == 2:
            print("Player 2 (AI) is thinking...")
            _, best_move = engine.negamax(board, DEPTH, ALPHA, BETA, -1)
            if best_move:
                board.apply_move(best_move)


        gui.draw_board()
        gui.draw_stones()
        pygame.display.flip()
