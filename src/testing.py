import chess
import chess.engine
import pandas as pd
import numpy as np
import time
from config import Config
from agent import Agent


class Testing:
    def __init__(self, config: Config, agent: Agent):
        self.config_agent = config.agent
        self.config_testing = config.testing
        self.agent = agent

        self.output_dir = f'{config.root}/{self.config_testing["output_dir"]}'

    # Method that plays n_games against stockfish for each skill level or elo provided
    def play_vs_stockfish(self, n_games, skill_levels=None, elos=None):

        assert skill_levels is None or elos is None, "Provide either skill_levels or elos, not both"

        print(f'Playing {n_games * (len(skill_levels) if skill_levels is not None else 1 if elos is None else len(elos))} games against stockfish')
        # Create a stockfish engine
        engine = chess.engine.SimpleEngine.popen_uci(self.config_testing["stockfish_path"])
        results = {
            'agent_plays_white': [],
            'param': [],
            'result': [],
            'game': []
        }

        to_iterate = skill_levels if skill_levels is not None else (elos if elos is not None else [None])

        for x in to_iterate:
            if skill_levels is not None:
                engine.configure({'Skill Level': x})
            elif x is not None:
                engine.configure({"UCI_LimitStrength": "true", "UCI_Elo": x})

            # Play n_games
            for i in range(n_games):

                # Create a board
                board = chess.Board()

                # Half of the games, the agent plays white
                if i < n_games / 2:
                    # Get the best move
                    best_move = self.agent.play(board)
                    assert board.is_legal(best_move)
                    board.push(best_move)

                while True:

                    # Get the best move from the engine
                    engine_move = engine.play(board, chess.engine.Limit(time=1 / 1e10)).move

                    # Make the move
                    assert board.is_legal(engine_move)
                    board.push(engine_move)

                    # Check if the game is over
                    if board.is_game_over():
                        break

                    # Get the best move
                    best_move = self.agent.play(board)

                    # Make the move
                    assert board.is_legal(best_move)
                    board.push(best_move)

                    # Check if the game is over
                    if board.is_game_over():
                        break

                results['agent_plays_white'].append(i < n_games / 2)
                results['param'].append(x)
                results['result'].append(board.result())
                results['game'].append(chess.Board().variation_san(board.move_stack))
        engine.quit()

        results = pd.DataFrame(results)
        # Calculate the whether it was a win, loss, or draw
        results['agent_win'] = results.apply(
            lambda x: x['result'] == '1-0' if x['agent_plays_white'] else x['result'] == '0-1', axis=1)
        results['agent_loss'] = results.apply(
            lambda x: x['result'] == '0-1' if x['agent_plays_white'] else x['result'] == '1-0', axis=1)
        results['agent_draw'] = results['result'] == '1/2-1/2'

        # Calculate the win, loss, and draw percentages by depth
        agg = results.groupby('param').agg({'agent_win': 'mean', 'agent_loss': 'mean', 'agent_draw': 'mean'})
        agg.index.names = ['skill_level' if skill_levels is not None else ('elo' if elos is not None else 'index')]
        print(agg)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        results.to_csv(f'{self.output_dir}/{timestamp}_vs_stockfish.csv')

    def play_vs_other_agent(self, other_agent, n_games):
        print(f'Playing {n_games} games against {other_agent.__class__.__name__}')
        col_names = ['agent_plays_white', 'result', 'agent_time_to_move', 'other_agent_time_to_move', 'n_moves', 'game',
                     'top_moves']
        results = {col_name: [] for col_name in col_names}

        # Play n_games
        for i in range(n_games):

            # Half of the games, the agent plays white
            if i < n_games / 2:
                game_info = self.play_game(self.agent, other_agent)
                time_a = game_info['avg_time_1']
                time_o = game_info['avg_time_2']
                top_moves = game_info['top_moves_1']
                # game_result, time_a, time_o, n_moves, board = self.play_game(self.agent, other_agent)
            else:
                game_info = self.play_game(other_agent, self.agent)
                time_a = game_info['avg_time_2']
                time_o = game_info['avg_time_1']
                top_moves = game_info['top_moves_2']
                # game_result, time_o, time_a, n_moves, board = self.play_game(other_agent, self.agent)

            results['agent_plays_white'].append(i < n_games / 2)
            results['result'].append(game_info['board_result'])
            results['agent_time_to_move'].append(time_a)
            results['other_agent_time_to_move'].append(time_o)
            results['n_moves'].append(game_info['n_moves'])
            results['game'].append(chess.Board().variation_san(game_info['board'].move_stack))
            results['top_moves'].append('//'.join(top_moves))

        results = pd.DataFrame(results)
        results['agent_win'] = results.apply(
            lambda x: x['result'] == '1-0' if x['agent_plays_white'] else x['result'] == '0-1', axis=1)
        results['agent_loss'] = results.apply(
            lambda x: x['result'] == '0-1' if x['agent_plays_white'] else x['result'] == '1-0', axis=1)
        results['agent_draw'] = results['result'] == '1/2-1/2'
        agg = results.agg({'agent_win': 'mean', 'agent_loss': 'mean', 'agent_draw': 'mean',
                           'agent_time_to_move': 'mean', 'other_agent_time_to_move': 'mean', 'n_moves': 'mean'})

        print(agg)
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        results.to_csv(f'{self.output_dir}/{timestamp}_vs_agent.csv')

    @staticmethod
    def play_game(agent_1: Agent, agent_2: Agent, max_moves=1000) -> dict:
        avg_time_1, avg_time_2 = 0, 0
        # Create a board
        board = chess.Board()

        m1, m2 = 0, 0
        top_moves_1 = []
        top_moves_2 = []
        while m1 + m2 < max_moves:
            avg_time_1, m1 = Testing.play_move(agent_1, avg_time_1, board, m1, top_moves_1)

            if board.is_game_over():
                break

            avg_time_2, m2 = Testing.play_move(agent_2, avg_time_2, board, m2, top_moves_2)

            if board.is_game_over():
                break

        results = {
            'board_result': board.result() if board.is_game_over() else '1/2-1/2',
            'avg_time_1': round(avg_time_1, 4),
            'avg_time_2': round(avg_time_2, 4),
            'n_moves': m1 + m2,
            'board': board,
            'top_moves_1': top_moves_1,
            'top_moves_2': top_moves_2
        }

        return results

    @staticmethod
    def play_move(agent, avg_time, board, m, top_moves):
        a = time.time()
        move, move_scores = agent.play_and_evaluate(board)

        top_moves.append(move_scores)
        avg_time = (avg_time * m + (time.time() - a)) / (m + 1)
        board.push(move)
        return avg_time, m + 1
