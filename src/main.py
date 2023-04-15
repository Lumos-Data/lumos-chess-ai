from config import Config
from agent import Agent
from testing import Testing
from visualize import Visualize

from pyinstrument import Profiler


if __name__ == "__main__":

    config = Config()

    if config.main["profiling"]:
        profiler = Profiler()
        profiler.start()

    # Create an agent
    config.set_eval_function("dummy_evaluation")
    config.set_search_algorithm("alphabeta")
    agent = Agent(config)

    testing = Testing(config, agent)
    # testing.play_vs_stockfish(10, skill_levels=[2, 3, 4, 5])
    # testing.play_vs_stockfish(30, elos=[1400, 1500, 2500])

    config.set_eval_function("no_evaluation")
    config.set_search_algorithm("random")
    random_agent = Agent(config)
    testing.play_vs_other_agent(random_agent, 100)

    # testing.play_vs_stockfish(10, [100, 500, 1000])

    visualize = Visualize(config)
    visualize.plot()

    if config.main["profiling"]:
        profiler.stop()
        print(profiler.output_text(unicode=True, color=True))
        profiler.open_in_browser()

