from game import FiancoBoard
import copy

class FiancoEngine():
    def __init__(self):
        pass    

    def negamaxAlgorithm(self, board: FiancoBoard, depth, alpha, beta, color):
        # Negamax algorithm with alpha-beta pruning
        if depth == 0 or board.is_winner() is not None:
            return color * board.evaluate()

        max_score = -float('inf')
        valid_moves, captures = board.get_valid_moves_and_captures(board.current_player)
        moves = captures if captures else valid_moves  # Prioritize captures if any
        print(f"Valid moves: {moves}")

        for move in moves:
            board_copy = FiancoBoard()
            board_copy.board = copy.deepcopy(board.board)
            board_copy.current_player = board.current_player
            board_copy.apply_move(move)

            score = -self.negamaxAlgorithm(board_copy, depth - 1, -beta, -alpha, -color)
            
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                print(f"Pruned at depth {depth} with alpha: {alpha}, beta: {beta}")
                break

        return max_score


    def get_ai_move(self, board: FiancoBoard, depth):
        # Get the best move for the AI
        best_move = None
        best_score = float('-inf')
        valid_moves, captures = board.get_valid_moves_and_captures(board.current_player)
        moves = captures if captures else valid_moves  # AI prioritizes captures
        print(f"AI valid moves: {moves}")  # Debugging

        for move in moves:
            print(f"Trying move: {move}")
            board_copy = FiancoBoard()
            board_copy.board = copy.deepcopy(board.board)
            board_copy.current_player = board.current_player
            board_copy.apply_move(move)
            
            score = -self.negamaxAlgorithm(board_copy, depth - 1, float('-inf'), float('inf'), -1)
            
            if score > best_score:
                best_score = score
                best_move = move
                print(f"Best move: {best_move}, Score: {best_score}")

        return best_move
