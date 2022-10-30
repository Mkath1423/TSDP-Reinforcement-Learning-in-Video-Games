from utilities import LoggerConfig, create_logger

from utilities import load_yaml, get_arg

config = load_yaml(get_arg("config"))["ai"]

log = create_logger(LoggerConfig(config["logger"]))
