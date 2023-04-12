from config import Config
from agent import Agent
from testing import Testing

from pyinstrument import Profiler


if __name__ == "__main__":
    profiler = Profiler()
    profiler.start()

    # config = {
    #     "evaluation_function": "no_evaluation",
    #     "search_algorithm": "random",
    # }
    config = Config()

    # Create an agent
    agent = Agent(config)

    testing = Testing(config, agent)
    testing.play_vs_stockfish(100, skill_levels=[2, 3, 4, 5])
    # testing.play_vs_stockfish(100, elos=[1400, 1500, 2500])

    testing.play_vs_other_agent(agent, 10)

    # testing.play_vs_stockfish(10, [100, 500, 1000])

    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))
    profiler.open_in_browser()

