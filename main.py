from engine import FiancoEngine
from game import FiancoBoard 
from constants import DEPTH,ALPHA,BETA
import time


def parse_move(move_str):
    """Convert a move in the format '0,0-0,1' to tuple of tuples ((start_row, start_col), (end_row, end_col))."""
    start_pos, end_pos = move_str.split('-')
    start = tuple(map(int, start_pos.split(',')))
    end = tuple(map(int, end_pos.split(',')))
    return (start, end)


def main():
    board = FiancoBoard()
    engine = FiancoEngine()
    game_over = False
    print("Initial board:")
    print(board.board)
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
                    print("Board after white's move:")
                    print(board.board)
                    board.current_player = 2
                else:
                    print("Invalid capture. Please try again.")
                    print("Valid captures: ", valid_captures)
                    continue
            else:
                if move in valid_moves:
                    board.apply_move(move)
                    print("Board after white's move:")
                    print(board.board)
                    board.current_player = 2
                else:
                    print("Invalid move. Please try again.")
                    continue
        elif board.current_player == 2:  # AI plays for black (Player 2)
            print("Black AI is thinking...")
            start = time.time()
            move = engine.get_ai_move(board, 3)
            board.apply_move(move)
            end = time.time()
            print(f"Black AI played {move} in {(end - start)} seconds.")
            print(board.board)
            board.current_player = 1

if __name__ == "__main__":
    main()