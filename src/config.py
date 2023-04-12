import yaml


class Config:
    def __init__(self):
        # Read config.yaml from the root of the project
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        self.agent = config["agent"]
        self.testing = config["testing"]
