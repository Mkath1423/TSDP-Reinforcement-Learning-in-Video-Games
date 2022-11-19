from utilities import LoggerConfig, create_logger, get_config
from utilities.config import ModelConfig, TrainerConfig

logger_config = get_config("ai", "logger")

if logger_config is None:
    logger_config = {"name", "AI"}

log = create_logger(LoggerConfig(logger_config))

model_config   = ModelConfig(get_config("ai", "model"))
trainer_config = TrainerConfig(get_config("ai", "trainer"))

log.info("model_config", vars(model_config))
log.info("trainer_config", vars(trainer_config))
