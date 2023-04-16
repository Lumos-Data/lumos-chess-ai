import chess
import random


class Search:

    CHECK_MATE_VALUE = 1e8
    INF = float("inf")

    @staticmethod
    def random_search(depth, board: chess.Board, eval_fn) -> chess.Move:
        return random.choice(list(board.legal_moves))

    @staticmethod
    def alphabeta(depth: int, board: chess.Board, eval_fn) -> chess.Move:
        # TODO: move ordering
        moves = list(board.legal_moves)

        # White is always maximizing, black is always minimizing
        sign = 1 if board.turn == chess.WHITE else -1

        best_move_value = sign * -Search.INF
        best_move_found = moves[0]

        for move in moves:
            board.push(move)
            value = sign * Search.minimax(depth-1, -Search.INF, Search.INF, board, -sign, eval_fn)
            board.pop()

            if value > best_move_value:
                best_move_value = value
                best_move_found = move

        return best_move_found

    @staticmethod
    def minimax(depth: int, alpha: float, beta: float, board: chess.Board, sign, eval_fn) -> float:
        # Always from the point of view of white
        if depth == 0:
            return eval_fn(board)

        if board.is_checkmate():
            return -sign * Search.CHECK_MATE_VALUE if board.turn == chess.WHITE else sign * Search.CHECK_MATE_VALUE

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        best_move_value = -Search.INF

        # TODO: move ordering
        moves = list(board.legal_moves)
        for move in moves:
            board.push(move)
            value = sign * Search.minimax(depth - 1, -beta, -alpha, board, -sign, eval_fn)
            best_move_value = max(best_move_value, value)
            board.pop()

            if sign > 0:
                alpha = max(alpha, best_move_value)
            else:
                beta = min(beta, best_move_value)

            if alpha >= beta:
                return best_move_value

        return best_move_value


