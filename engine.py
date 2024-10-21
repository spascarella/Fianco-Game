class FiancoEngine:
    def __init__(self):
        # Initialize the killer move table with two slots per depth (adjust size as needed)
        self.killer_moves = [[None, None] for _ in range(100)]
        pass

    def negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or board.is_winner() is not None:
            return board.evaluate() * color, None

        best_score = -float("inf")
        best_move = None
        normal_moves, captures = board.get_valid_moves_and_captures(board.current_player)
        moves = captures if captures else normal_moves

        # If only one capture or move is available, choose it without recursion
        if len(moves) == 1:
            single_move = moves[0]
            board.apply_move(single_move)
            score = board.evaluate() * color
            board.undo()
            return score, single_move

        # Apply killer moves at the current depth first
        killer_moves_at_depth = [move for move in self.killer_moves[depth] if move in moves] # Only consider moves that are still valid
        for killer_move in killer_moves_at_depth:
            moves.remove(killer_move)  # Remove it from moves so it doesn't get processed twice
        moves = killer_moves_at_depth + moves  # Put killer moves first
        print(f"Killer moves at depth {depth}: {killer_moves_at_depth}")
        first_move = True
        change = 0 if captures else 1  # Quiet search if no captures

        for move in moves:
            board.apply_move(move)

            if first_move:
                # Full alpha-beta search for the first move (principal variation)
                score = -self.negamax(board, depth - change, -beta, -alpha, -color)[0]
                first_move = False
            else:
                # Null-window search for all other moves
                score = -self.negamax(board, depth - change, -alpha - 1, -alpha, -color)[0]

                # Re-search with full alpha-beta window if null-window search failed
                if alpha < score < beta:
                    score = -self.negamax(board, depth - change, -beta, -alpha, -color)[0]

            board.undo()

            if score > best_score:
                best_score = score
                best_move = move

            # Update alpha and check for beta-cutoff
            alpha = max(alpha, score)
            if alpha >= beta:
                # Store the killer move in the killer table for this depth
                if move not in self.killer_moves[depth]:
                    # Insert the move into the killer moves list, replacing the least recent if needed
                    if self.killer_moves[depth][0] is None:
                        self.killer_moves[depth][0] = move
                    else:
                        self.killer_moves[depth][1] = move
                break  # Beta cutoff

        return best_score, best_move