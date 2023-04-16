import chess
import random

from typing import Callable, List, Tuple

from utils import CHECK_MATE_VALUE, INF


class Search:

    @staticmethod
    def random_search(depth, board: chess.Board, eval_fn) -> List[Tuple[chess.Move, float]]:
        return [(move, float('nan')) for move in board.legal_moves]

    @staticmethod
    def alphabeta(depth: int, board: chess.Board, eval_fn) -> List[Tuple[chess.Move, float]]:
        # TODO: move ordering
        moves = list(board.legal_moves)

        # White is always maximizing, black is always minimizing
        sign = 1 if board.turn == chess.WHITE else -1

        move_values = []
        for move in moves:
            board.push(move)
            value = sign * Search.minimax(depth - 1, -INF, INF, board, -sign, eval_fn)
            board.pop()
            move_values.append((move, value))

        return move_values

    @staticmethod
    def minimax(depth: int, alpha: float, beta: float, board: chess.Board, sign, eval_fn) -> float:
        # Always from the point of view of white
        if depth == 0:
            return eval_fn(board)

        if board.is_checkmate():
            return -sign * CHECK_MATE_VALUE if board.turn == chess.WHITE else sign * CHECK_MATE_VALUE

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        best_move_value = -INF

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


