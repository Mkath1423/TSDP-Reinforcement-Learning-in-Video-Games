from utilities import LoggerConfig, create_logger

from utilities import load_yaml, get_arg


config = {"name": "AI"}

if get_arg("config") is not None:
    config = load_yaml(get_arg("config"))["ai"]["logger"]

log = create_logger(LoggerConfig(config))
