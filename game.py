from constants import *
import numpy as np
import copy


#TODO: Find out why the AI is not playing correctly - always the same moves 
    
class FiancoBoard:
    def __init__(self):
        self.board = self.setup_board()
        self.current_player = 1  # 1 for white, 2 for black
        self.board_history = []  # Stores the history of board states

    def setup_board(self):
        board = np.zeros((9, 9), dtype=int)
        # White
        board[0, :] = 1
        board[1, (1, 7)] = 1
        board[2, (2, 6)] = 1
        board[3, (3, 5)] = 1
        # Black
        board[8, :] = 2
        board[7, (1, 7)] = 2
        board[6, (2, 6)] = 2
        board[5, (3, 5)] = 2
        return board
    
    def get_valid_moves_and_captures(self, player):
        valid_moves = []
        captures = []
        direction = -1 if player == 2 else 1  # White moves forward (-1), Black moves forward (1)

        for r in range(9):
            for c in range(9):
                if self.board[r, c] == player:
                    # Debug statement
                    #print(f"Checking moves for stone at ({r}, {c})")

                    # Forward move
                    if 0 <= r + direction < 9 and self.board[r + direction, c] == 0:
                        valid_moves.append(((r, c), (r + direction, c)))
                        #print(f"Added forward move: {((r, c), (r + direction, c))}")
                    
                    # Left move
                    if c > 0 and self.board[r, c - 1] == 0:
                        valid_moves.append(((r, c), (r, c - 1)))
                        #print(f"Added left move: {((r, c), (r, c - 1))}")
                    
                    # Right move
                    if c < 8 and self.board[r, c + 1] == 0:
                        valid_moves.append(((r, c), (r, c + 1)))
                        #print(f"Added right move: {((r, c), (r, c + 1))}")
                    
                    # Capture forward-left
                    if 0 <= r + direction < 9 and c > 0:
                        if self.board[r + direction, c - 1] != player and self.board[r + direction, c - 1] != 0:
                            if 0 <= r + 2 * direction < 9 and c - 2 >= 0 and self.board[r + 2 * direction, c - 2] == 0:
                                captures.append(((r, c), (r + 2 * direction, c - 2)))
                                #print(f"Added forward-left capture: {((r, c), (r + 2 * direction, c - 2))}")
                    
                    # Capture forward-right
                    if 0 <= r + direction < 9 and c < 8:
                        if self.board[r + direction, c + 1] != player and self.board[r + direction, c + 1] != 0:
                            if 0 <= r + 2 * direction < 9 and c + 2 <= 8 and self.board[r + 2 * direction, c + 2] == 0:
                                captures.append(((r, c), (r + 2 * direction, c + 2)))
                                #print(f"Added forward-right capture: {((r, c), (r + 2 * direction, c + 2))}")
        
        return valid_moves, captures
    
    def save_board_state(self):
        """Store a copy of the current board in history before making a move."""
        self.board_history.append(copy.deepcopy(self.board))  # Add a deep copy of the board
        return self.board_history

    def apply_move(self, move):

        self.save_board_state()

        start = move[0]
        end = move[1]

        
        # Calculate the row/column differences to determine if it's a capture
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])

        # Logic for a capture (diagonal jump over an enemy piece)
        if row_diff == 2 and col_diff == 2:  # Check for jump (capture)
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            captured_piece = self.board[middle_row, middle_col]
            
            if captured_piece != 0 and captured_piece != self.current_player:
                # Perform the capture
                self.board[end] = self.board[start]  # Move the stone to the new location
                self.board[start] = 0  # Clear the starting position
                self.board[middle_row, middle_col] = 0  # Remove the captured piece
                #print(f"Captured piece at ({middle_row}, {middle_col}): {captured_piece}")
            else:
                print("Invalid capture. No enemy stone to capture.")
        
        # Logic for a regular move (one step forward or sideways)
        elif row_diff <= 1 and col_diff <= 1:  # Check for normal move (adjacent cell)
            self.board[end] = self.board[start]  # Move the stone to the new location
            self.board[start] = 0  # Clear the starting position
            #print(f"Moved from {start} to {end}")
        
        # If neither a valid move nor capture, it's invalid
        else:
            print("Invalid move or capture.")

    def undo_move(self, move, captured_piece):
        """Undo a move on the board and restore the captured piece if any."""
        start, end = move
        self.board[start] = self.board[end]
        self.board[end] = 0  # Clear the destination

        if captured_piece is not None:
            # Restore the captured piece
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            self.board[middle_row, middle_col] = captured_piece


    def restart(self):
        """Restart the game."""
        self.board = self.setup_board()
        self.current_player = 1
    
    def is_winner(self): # Check if there is a winner
        if np.any(self.board[0, :] == 2): # Black wins if any black stone is in row 0
            return 2
        if np.any(self.board[8, :] == 1):  # White wins if any white stone is in row 8
            return 1
        elif np.sum(self.board == 1) == 0: # Black wins if no white stones are left
            return 2
        elif np.sum(self.board == 2) == 0: # White wins if no black stones are left
            return 1
        elif not self.get_valid_moves_and_captures(self.current_player): # Player wins if the opponent has no valid moves
            return 3 - self.current_player
        return None

    def evaluate(self):
        """Evaluate the board state."""

        white_score = 0
        black_score = 0

        winner = self.is_winner()

        if winner == self.current_player:
            return 1500
        elif winner == 3 - self.current_player:
            return -1500

        # Add points for each stone, with a bonus for stones closer to the opponent's back row
        for r in range(9):
            for c in range(9):
                if self.board[r, c] == 1:  # White
                    white_score += 10 + (8 - r)  # Bonus for being closer to row 8
                elif self.board[r, c] == 2:  # Black
                    black_score += 10 + r  # Bonus for being closer to row 0

        # Optionally, give bonuses for having more valid moves (mobility)
        white_moves, white_captures = self.get_valid_moves_and_captures(1)
        black_moves, black_captures = self.get_valid_moves_and_captures(2)
        white_score += len(white_moves) + 5 * len(white_captures)
        black_score += len(black_moves) + 5 * len(black_captures)

        # Final evaluation is black score minus white score
        return black_score - white_score if self.current_player == 2 else white_score - black_score



def parse_move(move_str):
    """Convert a move in the format '0,0-0,1' to tuple of tuples ((start_row, start_col), (end_row, end_col))."""
    start_pos, end_pos = move_str.split('-')
    start = tuple(map(int, start_pos.split(',')))
    end = tuple(map(int, end_pos.split(',')))
    return (start, end)

'''
def play_game():
    board = FiancoBoard()
    game_over = False

    while not game_over:
        winner = board.is_winner()
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
            break
        
        if board.current_player == 1:  # Human player's turn (White)
            valid_moves, valid_captures = board.get_valid_moves_and_captures(1)
            print("Captures: ", valid_captures)
            print("Moves: ", valid_moves)
            print("Before white human's move:")
            print(board.board)
            print("Enter your move in the format '0,0-0,1':")
            
            move_input = input().strip()
            move = parse_move(move_input)
            if valid_captures:
                if move in valid_captures:
                    board.apply_move(move)
                    board.current_player = 2
                    print("Board after white's move:")
                    print(board.board)
                else:
                    print("Invalid capture. Please try again.")
                    print("Valid captures: ", valid_captures)
                    continue
            else:
                if move in valid_moves:
                    board.apply_move(move)
                    board.current_player = 2
                    print("Board after white's move:")
                    print(board.board)
                else:
                    print("Invalid move. Please try again.")
                    continue

        elif board.current_player == 2:  # AI plays for black (Player 2)
        
            print("Black AI is thinking...")
            _, best_move = board.negamax(depth=5, alpha=-math.inf, beta=math.inf, color=-1)
            if best_move:
                board.apply_move(best_move)
                board.current_player = 1
                print(f"Black AI played {best_move}")
                print(board.board)
            else:
                print("No valid moves for Black AI.")
                game_over = True
                break
        
        


        if board.current_player == 1:  # Human player's turn (White)
            valid_moves, valid_captures = board.get_valid_moves_and_captures(1)
            print("Captures: ", valid_captures)
            print("Moves: ", valid_moves)
            print("Before white human's move:")
            print(board.board)
            print("Enter your move in the format '0,0-0,1':")
            
            move_input = input().strip()
            move = parse_move(move_input)
            if valid_captures:
                if move in valid_captures:
                    board.apply_move(move)
                    board.current_player = 2
                    print("Board after white's move:")
                    print(board.board)
                else:
                    print("Invalid capture. Please try again.")
                    print("Valid captures: ", valid_captures)
                    continue
            else:
                if move in valid_moves:
                    board.apply_move(move)
                    board.current_player = 2
                    print("Board after white's move:")
                    print(board.board)
                else:
                    print("Invalid move. Please try again.")
                    continue
        '''




'''
def play_game():
    board = FiancoBoard()
    game_over = False

    while not game_over:
        winner = board.is_winner()
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
            break

        if board.current_player == 1:  # Human player's turn (White)
            valid_moves, valid_captures = board.get_valid_moves_and_captures(1)
            print("Captures: ", valid_captures)
            print("Moves: ", valid_moves)
            print("Before white human's move:")
            print(board.board)
            print("Enter your move in the format '0,0-0,1':")
            
            move_input = input().strip()
            move = parse_move(move_input)
            if valid_captures:
                if move in valid_captures:
                    board.apply_move(move)
                    board.current_player = 2
                    print("Board after white's move:")
                    print(board.board)
                else:
                    print("Invalid capture. Please try again.")
                    print("Valid captures: ", valid_captures)
                    continue
            else:
                if move in valid_moves:
                    board.apply_move(move)
                    board.current_player = 2
                    print("Board after white's move:")
                    #print(f"Evaluation score: {board.evaluate()}")  # <-- This line
                    print(board.board)
                else:
                    print("Invalid move. Please try again.")
                    continue
        elif board.current_player == 2:  # AI player's turn (Black)
            print("AI is thinking...")
            _, best_move = board.negamax(depth=5, alpha=-math.inf, beta=math.inf, color=1)
            if best_move:
                board.apply_move(best_move)
                board.current_player = 1
                print(f"AI played {best_move}")
                print(board.board)

# Run the game
play_game()
'''


'''
def play_game():
    board = FiancoBoard()
    game_over = False

    while not game_over:
        winner = board.is_winner()
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
            break

        if board.current_player == 1:  # Human player's turn (White)
            valid_moves, _ = board.get_valid_moves_and_captures(1)
            print("Before white human's move:")
            print(board.board)
            print("Enter your move in the format '0,0-0,1':")
            
            move_input = input().strip()
            move = parse_move(move_input)
            
            if move in valid_moves + _:
                board.apply_move(move)
                board.current_player = 2
                print("Board after white's move:")
                print(board.board)
            else:
                print("Invalid move. Please try again.")
        else:
            valid_moves, _ = board.get_valid_moves_and_captures(2)
            print("Before Black Human's move:")
            print(board.board)
            print("Enter your move in the format '0,0-0,1':")
            move_input = input().strip()
            move = parse_move(move_input)
            
            # Validate the move
            if move in valid_moves + _:
                board.apply_move(move)
                board.current_player = 1
                # Print the board after the move
                print("Board after Black Human's move:")
                print(board.board)
            else:
                print("Invalid move. Please try again.")
play_game()
'''

    