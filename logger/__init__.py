import logging

from .logger import Logger
from .logger_config import LoggerConfig

config = {
    "name": "logger"
}

log = Logger(LoggerConfig(config))
