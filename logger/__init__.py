from .logger import create_logger
from .logger_config import LoggerConfig


config = {
    "name": "logger"
}

log = create_logger(LoggerConfig(config))
