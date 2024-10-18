class FiancoEngine:
    def __init__(self):
        pass
    
    def negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or board.is_winner() is not None:
            return board.evaluate() * color, None

        best_score = -float("inf")
        best_move = None
        normal_moves,captures = board.get_valid_moves_and_captures(board.current_player)
        moves = captures if captures else normal_moves
        change = 1
        if captures:
            change = 0
        moves = captures if captures else normal_moves
        for move in moves:
            board.apply_move(move)
            score = -self.negamax(board, depth-change, -beta, -alpha, -color)[0]
            board.undo()

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break  

        return best_score, best_move