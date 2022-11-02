from utilities import create_logger, LoggerConfig

from utilities import load_yaml, get_arg

config = {"name":"GAME"}

if get_arg("config") is not None:
    config = load_yaml(get_arg("config"))["game"]["logger"]

log = create_logger(LoggerConfig(config))
log.info("create game log")
