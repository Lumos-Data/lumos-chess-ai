import chess
import random


class Search:

    @staticmethod
    def random_search(board: chess.Board, eval_fn) -> chess.Move:
        return random.choice(list(board.legal_moves))

    @staticmethod
    def alphabeta(board: chess.Board, eval_fn) -> chess.Move:
        pass
