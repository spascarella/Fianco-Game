from constants import *
import numpy as np
import copy

class FiancoBoard:
    def __init__(self):
        self.board = self.setup_board()
        self.current_player = 1  # 1 for white, 2 for black
        self.move_history = []  # To store history of moves
        self.move_list = []

    def setup_board(self):
        board = np.zeros((9, 9), dtype=int)      

        # Black
        board[0, :] = 2
        board[1, (1, 7)] = 2
        board[2, (2, 6)] = 2
        board[3, (3, 5)] = 2

        # White
        board[8, :] = 1
        board[7, (1, 7)] = 1
        board[6, (2, 6)] = 1
        board[5, (3, 5)] = 1

        return board
    
    def get_valid_moves_and_captures(self, player):
        valid_moves = []
        captures = []
        direction = -1 if player == 1 else 1 # White moves down, Black moves up
        last_row = 0 if player == 1 else 8  # The opponent's last row

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
        
        # 1. Check if there is any capture that reaches the opponent's last row
        captures_to_last_row = [capture for capture in captures if capture[1][0] == last_row]
        if captures_to_last_row:
            # If there's a capture to the last row, return only that capture and no valid moves
            return [], captures_to_last_row

        # 2. If no captures to the last row, check if any valid move reaches the opponent's last row
        moves_to_last_row = [move for move in valid_moves if move[1][0] == last_row]
        if moves_to_last_row:
            # Return only the moves to the last row and no captures
            return moves_to_last_row, []

        # 3. If neither captures nor moves reach the last row, return all valid moves and captures
        return valid_moves, captures

    def apply_move(self, move):
        """Apply a move on the board."""
        start, end = move
        self.save_state()

        # Calculate the row/column differences to determine if it's a capture
        row_diff = abs(end[0] - start[0])
        col_diff = abs(end[1] - start[1])

        # Capture move
        if row_diff == 2 and col_diff == 2:
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            captured_piece = self.board[middle_row, middle_col]
            
            if captured_piece != 0 and captured_piece != self.current_player:
                self.board[end] = self.board[start]  # Move the stone to the new location
                self.board[start] = 0  # Clear the starting position
                self.board[middle_row, middle_col] = 0  # Remove the captured piece
            else:
                print("Invalid capture. No enemy stone to capture.")
        # Regular move
        elif row_diff <= 1 and col_diff <= 1:
            self.board[end] = self.board[start]
            self.board[start] = 0
        else:
            print("Invalid move or capture.")
        
        #self.move_list.append((start, end)) # Add the move to the move list

        
        # Switch player after a valid move
        self.current_player = 3 - self.current_player
        
    
    def is_winner(self): # Check if there is a winner
        if np.any(self.board[0, :] == 1): # Black wins if any black stone is in row 0
            return 1
        if np.any(self.board[8, :] == 2):  # White wins if any white stone is in row 8
            return 2
        elif np.sum(self.board == 1) == 0: # Black wins if no white stones are left
            return 2
        elif np.sum(self.board == 2) == 0: # White wins if no black stones are left
            return 1
        else:
            # Check if the opponent has no valid moves
            valid_moves, captures = self.get_valid_moves_and_captures(self.current_player)
            if not valid_moves and not captures:
                return 3 - self.current_player  # The opponent wins if there are no valid moves or captures for the current player
        return None
    
    def save_state(self):
        """Save the current state of the board and player to history."""
        self.move_history.append((copy.deepcopy(self.board), self.current_player))

    def undo(self):
        """Undo the last move."""
        if self.move_history:
            # Restore the last state
            self.board, self.current_player = self.move_history.pop()
        else:
            print("No moves to undo.")

    
    def evaluate(self):
        white_score = 0
        black_score = 0
        winner = self.is_winner()
        if winner == 1:
            return 100000
        elif winner == 2:
            return -100000
        # 1. Count stones and weight them
        white_stones = np.sum(self.board == 1)
        black_stones = np.sum(self.board == 2)
        score_diff = (white_stones - black_stones) * 100

        # 2. Weight the board based on position
        blackWeightMap = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2],
            [4, 4, 4, 4, 4, 4, 4, 4, 4],
            [6, 6, 6, 6, 6, 6, 6, 6, 6],
            [8, 8, 8, 8, 8, 8, 8, 8, 8],
            [10, 10, 10, 10, 10, 10, 10, 10, 10],
            [12, 12, 12, 12, 12, 12, 12, 12, 12],
            [14, 14, 14, 14, 14, 14, 14, 14, 14],
            [16, 16, 16, 16, 16, 16, 16, 16, 16]
        ]
        whiteWeightMap = blackWeightMap[::-1]

        white_score += np.where(self.board == 1, whiteWeightMap, 0).sum()
        black_score += np.where(self.board == 2, blackWeightMap, 0).sum()

        # 4. Penalize for opponent's stones in your half
        opponent_in_white_half = (np.sum(self.board[5:9, :] == 2)) * 5  # Black stones in white's half
        opponent_in_black_half = np.sum(self.board[0:5, :] == 1) * 5  # White stones in black's half
        white_score -= opponent_in_white_half
        black_score -= opponent_in_black_half

        # Final score is white's advantage minus black's advantage
        total_score = (white_score - black_score) + score_diff
        return total_score