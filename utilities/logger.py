import logging


def create_logger(config):
        formatter = logging.Formatter(config.format)

        logger = logging.getLogger(config.name)
        logger.setLevel(config.logger_level)

        if config.use_file_handler:
            file_handler = logging.FileHandler(config.log_path)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(config.log_file_level)

            logger.addHandler(file_handler)

        if config.use_stream_handler:
            logger.addHandler(logging.StreamHandler())

        return logger


