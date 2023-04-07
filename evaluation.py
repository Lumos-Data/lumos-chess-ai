import chess


class Evaluation:
    @staticmethod
    def no_evaluation(board: chess.Board) -> float:
        return 0

    @staticmethod
    def dummy_evaluation(board: chess.Board) -> float:
        pass

    @staticmethod
    def neural_network_evaluation(board: chess.Board) -> float:
        pass

