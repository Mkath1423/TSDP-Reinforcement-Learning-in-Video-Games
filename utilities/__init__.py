from logger import create_logger, LoggerConfig

from .config import *

config = {
    "name": "utilities"
}

log = create_logger(LoggerConfig(config))
