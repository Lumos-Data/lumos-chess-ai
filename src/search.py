import chess
import random


class Search:

    @staticmethod
    def random_search(board: chess.Board, eval_fn) -> chess.Move:
        return random.choice(list(board.legal_moves))


    @staticmethod
    def alphabeta(depth: int, board: chess.Board, eval_fn) -> chess.Move:

        best_move = -float("inf")

        moves = list(board.legal_moves)
        best_move_found = moves[0]

        for move in moves:
            board.push(move)

            value = Search.minimax(depth-1, -float("inf"), float("inf"), board, False)
            board.pop()

            if value > best_move:
                best_move_found = move
                best_move = value


    @staticmethod
    def minimax(depth: int, alpha: float, beta: float, board: chess.Board, is_maximizing_player: bool) -> float:
        if board.turn == chess.WHITE:
            agent_color = "W"
        else:

        if board.is_checkmate():


