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
    engine = FiancoEngine()  # Ensure you have the AI engine instantiated
    game_over = False
    print("Initial board:\n")
    print_board(board)  # Use the new print function

    while not game_over:
        winner = board.is_winner()
        if winner:
            print(f"Player {winner} wins!")
            game_over = True
            break

        if board.current_player == 1:  # AI plays for white (Player 1)
            print("White AI is thinking...")
            start = time.time()
            # AI decides on the best move
            best_score, best_move = engine.negamax(board, DEPTH, ALPHA, BETA, 1)
            board.apply_move(best_move)
            end = time.time()
            print(f"White AI played {best_move} with a score of {best_score} in {(end - start)} seconds.")
            logging.debug(f"White AI played {best_move} with a score of {best_score} in {(end - start)} seconds.")
            print_board(board)

        elif board.current_player == 2:  # Random agent plays for black (Player 2)
            print("Black random agent is thinking...")
            move = random_agent(board)  # Get a random valid move
            if move:
                board.apply_move(move)
                print(f"Black random agent played {move}.")
                logging.debug(f"Black random agent played {move}.")
            else:
                print("No valid moves available for the black random agent.")
            print_board(board)

if __name__ == "__main__":
    main()


            


