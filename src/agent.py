import chess
import chess.engine
from typing import Callable

from config import Config
from evaluation import Evaluation
from search import Search

evaluation_function_map = {
    "no_evaluation": Evaluation.no_evaluation,
    "dummy_evaluation": Evaluation.dummy_evaluation,
}

search_algorithm_map = {
    "random": Search.random_search,
    "minimax": Search.minimax,
    "alphabeta": Search.alphabeta,
}


class Agent:
    def __init__(self, config: Config):
        self.config_agent = config.agent

        self.evaluation_function_name = self.config_agent["evaluation_function"]
        self.search_algorithm_name = self.config_agent["search_algorithm"]

        self.eval: Callable[[chess.Board], float] = evaluation_function_map[self.evaluation_function_name]
        self.search: Callable[[chess.Board, Callable[[chess.Board], float]], chess.Move] = search_algorithm_map[
            self.search_algorithm_name]

    def play(self, board: chess.Board):
        # Get the best move
        best_move = self.search(board, self.eval)

        # Return the move
        return best_move
