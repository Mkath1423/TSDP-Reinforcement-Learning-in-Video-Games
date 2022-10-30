from .logger import create_logger

from .logger_config import LoggerConfig


config = {
    "name": "utilities"
}

log = create_logger(LoggerConfig(config))
