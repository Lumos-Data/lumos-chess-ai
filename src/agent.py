import chess
import chess.engine
from typing import Callable, List, Tuple

from config import Config
from evaluation import Evaluation
from search import Search

evaluation_function_map = {
    "no_evaluation": Evaluation.no_evaluation,
    "baseline_evaluation": Evaluation.baseline_evaluation,
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
        self.search: Callable[[int, chess.Board, Callable[[chess.Board], float]], List[Tuple[chess.Move, int]]] = \
            search_algorithm_map[self.search_algorithm_name]

    def play(self, board: chess.Board):
        # Get the best move
        move_values = self.search(self.config_agent['search_depth'], board, self.eval)
        best_move = max(move_values, key=lambda x: x[1])[0]
        # Return the move
        return best_move

    def play_and_evaluate(self, board: chess.Board):
        # Get the best move
        move_values = self.search(self.config_agent['search_depth'], board, self.eval)
        # Sort the moves by their evaluation
        move_values.sort(key=lambda x: x[1], reverse=True)
        # Five best moves and their scores go to a string
        top_moves = ','.join(f'{move} - {score}' for move, score in move_values[:5])
        # Return the move and the evaluation
        return move_values[0][0], top_moves
