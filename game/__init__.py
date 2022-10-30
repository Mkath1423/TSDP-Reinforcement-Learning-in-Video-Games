from utilities import create_logger, LoggerConfig

from utilities import load_yaml, get_arg

config = load_yaml(get_arg("config"))["game"]

log = create_logger(LoggerConfig(config["logger"]))
log.info("create game log")
