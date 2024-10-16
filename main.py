import random
from engine import FiancoEngine
from game import FiancoBoard
from constants import DEPTH, ALPHA, BETA
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    handlers=[
        logging.FileHandler("logs.log"),
    ]
)

def parse_move(move_str):
    """Convert a move in the format '0,0-0,1' to tuple of tuples ((start_row, start_col), (end_row, end_col))."""
    start_pos, end_pos = move_str.split('-')
    start = tuple(map(int, start_pos.split(',')))
    end = tuple(map(int, end_pos.split(',')))
    return (start, end)


def print_board(board):
    """Board print"""
    print("    " + " ".join(f" {i} " for i in range(len(board.board[0]))))  # Print column numbers
    print("  +" + "---+" * len(board.board[0]))  # Horizontal separator

    for i, row in enumerate(board.board):
        row_str = f"{i} |"  # Row number
        for cell in row:
            if cell == 0:
                row_str += " . |"  # Empty space
            elif cell == 1:
                row_str += " W |"  # White 
            elif cell == 2:
                row_str += " B |"  # Black stone
        print(row_str)
        print("  +" + "---+" * len(board.board[0]))  # Horizontal separator


def random_agent(board):
    """Select a random valid move for the current player."""
    valid_moves, valid_captures = board.get_valid_moves_and_captures(board.current_player)
    if valid_captures:  # Prioritize captures
        return random.choice(valid_captures)
    elif valid_moves:
        return random.choice(valid_moves)
    return None  # No valid moves available



def main():
    board = FiancoBoard()
    engine = FiancoEngine()
    game_over = False
    print("Initial board:")
    print_board(board)
    while not game_over:
        winner = board.is_winner()
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
            break
        if board.current_player == 1:  # Human player's turn (White)
            valid_moves, valid_captures = board.get_valid_moves_and_captures(board.current_player)
            print("Available captures for the human: ", valid_captures)
            print("Available moves for the human: ", valid_moves)
            print("Enter your move in the format '0,0-0,1':")
            
            move_input = input().strip()
            move = parse_move(move_input)
            if valid_captures:
                if move in valid_captures:
                    board.apply_move(move)
                    print(f"Black played {move}.")
                    print_board(board)
                else:
                    print("Invalid capture. Please try again.")
                    print("Valid captures: ", valid_captures)
                    continue
            else:
                if move in valid_moves:
                    board.apply_move(move)
                    print(f"Black played {move}.")
                    print_board(board)
                else:
                    print(f"Invalid move for the player {board.current_player}. Please try again.")
                    continue
        elif board.current_player == 2:  # AI plays for Black (Player 1)
            print("Black AI is thinking...")
            start = time.time() 
            _, best_move = engine.negamax(board, DEPTH, ALPHA, BETA, -1)            
            board.apply_move(best_move)
            end = time.time()
            print(f"Black AI played {best_move} in {(end - start)} seconds.")
            print_board(board)

if __name__ == "__main__":
    main()
    


'''
def main():
    board = FiancoBoard()
    engine = FiancoEngine()
    game_over = False
    print("Initial board:")
    print_board(board)
    while not game_over:
        winner = board.is_winner()
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
            break
        if board.current_player == 1:  # Human player's turn (White)
            valid_moves, valid_captures = board.get_valid_moves_and_captures(board.current_player)
            print("Available captures for the human: ", valid_captures)
            print("Available moves for the human: ", valid_moves)
            print("Enter your move in the format '0,0-0,1':")
            
            move_input = input().strip()
            move = parse_move(move_input)
            if valid_captures:
                if move in valid_captures:
                    board.apply_move(move)
                    print(f"White played {move}.")
                    print_board(board)
                else:
                    print("Invalid capture. Please try again.")
                    print("Valid captures: ", valid_captures)
                    continue
            else:
                if move in valid_moves:
                    board.apply_move(move)
                    print(f"White played {move}.")
                    print_board(board)
                else:
                    print("Invalid move. Please try again.")
                    continue
        elif board.current_player == 2:  # AI plays for black (Player 2)
            print("Black AI is thinking...")
            start = time.time()
            _, best_move = engine.negamax(board, DEPTH, ALPHA, BETA, -1)            
            board.apply_move(best_move)
            end = time.time()
            print(f"Black AI played {best_move} in {(end - start)} seconds.")
            print_board(board)

if __name__ == "__main__":
    main()
'''
