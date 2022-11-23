from typing import Sequence

from utilities.args import get_arg
from utilities.files import load_yaml


class Config:
    def __init__(self, d: dict, requirements: Sequence[str]):
        if d is None:
            return

        for requirement in requirements:
            if requirement not in d.keys():
                print(f"[UTILS ERROR] - requirement not met {requirement}, failed to create config.")
                return

        for k, v in d.items():
            self.__setattr__(k, v)

    def __str__(self):
        return vars(self).__str__()


class LoggerConfig(Config):
    requirements = (
        "name",
    )

    def __init__(self, config: dict):
        """
        Generates a LoggerConfig with the correct attributes

        :param config: the loaded configuration of this object
        """
        self.name: str = "new_logger"
        self.logger_level: str = "DEBUG"
        self.format: str = "[%(name)s %(levelname)s] %(asctime)s - %(message)s"
        self.use_file_handler: bool = False
        self.log_path: str = None
        self.log_file_level: str = "INFO"
        self.use_stream_handler: bool = True
        self.sep: str = ", "
        self.end: str = ""

        super().__init__(config, self.requirements)


class AgentConfig(Config):
    requirements = (
        "position",
    )

    def __init__(self, config: dict):
        """
        Generates a AgentConfig with the correct attributes

        :param config: the loaded configuration of this object
        """
        self.initial_state = config

        self.name: str = "new_agent"
        self.type: str = "Agent"

        self.color: Sequence[int] = (255, 0, 0)
        self.size: Sequence[int] = (50, 50)
        self.sprite: str = None  # path to sprite image file

        self.max_hp: int = 10
        self.shoot_cooldown: int = 1
        self.movement_speed: int = 10

        super().__init__(config, self.requirements)


class BulletConfig(Config):
    requirements = ()

    def __init__(self, config: dict):
        """
        Generates a BulletConfig with the correct attributes

        :param config: the loaded configuration of this object
        """
        self.initial_state = config

        self.damage: int = 1
        self.speed: int = 30
        self.size: int = 3

        super().__init__(config, self.requirements)


class LevelConfig(Config):
    requirements = ()

    def __init__(self, config: dict):
        """
        Generates a LoggerConfig with the correct attributes

        Only exists for type hinting

        :param config: the loaded configuration of this object
        """

        self.agents: Sequence[AgentConfig] = []
        self.bullet: BulletConfig = None

        self.tilemap: str = None  # TODO change this once decided

        # settings
        self.title: str = "TSDP"
        self.window_size: Sequence[int] = (1000, 800)
        self.fps: int = 60
        self.background_color: Sequence[int] = "black"

        # handle special cases of nested configs
        if config is None:
            self.bullet = BulletConfig({})
        else:
            config['bullet'] = BulletConfig(config.get("bullet", {}))

            if config.__contains__("agents"):
                config["agents"] = [AgentConfig(a) for a in config["agents"]]

        super().__init__(config, self.requirements)


class TrainerConfig(Config):
    requirements = ()

    def __init__(self, config: dict):
        """
        Generates a TrainerConfig with the correct attributes

        Only exists for type hinting

        :param config: the loaded configuration of this object
        """

        self.lr: float = 0.001
        self.gamma: float = 0.8
        self.epsilon: float = 0.8
        self.max_model_memory: int = 10000
        self.batch_size: int = 1000

        super().__init__(config, self.requirements)


class ModelConfig(Config):
    requirements = ("num_extra_inputs", "num_outputs")

    def __init__(self, config: dict):
        """
        Generates a ModelConfig with the correct attributes

        Only exists for type hinting

        :param config: the loaded configuration of this object
        """

        self.num_extra_inputs: int = -1
        self.num_outputs: int = -1

        self.load_path = None

        super().__init__(config, self.requirements)


_config: dict = None

if get_arg("config") is not None:
    _config: dict = load_yaml(get_arg("config"))


def get_config(*sub_dicts):
    out = _config

    for d in sub_dicts:
        if out is None or not out.__contains__(d):
            return None

        out = out[d]

    return out


if __name__ == "__main__":
    l = LoggerConfig({
        "name": "test"
    })

    print(l.logger_level)
