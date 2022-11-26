from utilities import create_logger, get_config, LoggerConfig, LevelConfig

logger_config = get_config("game", "logger")

if logger_config is None:
    logger_config = {"name": "GAME"}

log = create_logger(LoggerConfig(logger_config))
log.info("create game log")

level_config = LevelConfig(get_config("game", "level"))
