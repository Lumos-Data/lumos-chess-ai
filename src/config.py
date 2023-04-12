import yaml
from pathlib import Path


class Config:
    def __init__(self):
        # Find root of the project
        self.root = Path(__file__).parent.parent
        self.config_path = self.root / "config.yaml"

        # Read config.yaml from the root of the project
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        self.agent = config["agent"]
        self.testing = config["testing"]
        self.visual = config["visual"]
