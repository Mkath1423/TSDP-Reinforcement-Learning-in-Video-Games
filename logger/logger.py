import logging


class Logger:
    def __init__(self, config):
        formatter = logging.Formatter(config.format)

        self.logger = logging.getLogger(config.name)
        self.logger.setLevel(config.level)

        if config.use_file_handler:
            file_handler = logging.FileHandler(config.log_path)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(config.log_file_level)

            self.logger.addHandler(file_handler)

        if config.use_stream_handler:
            self.logger.addHandler(logging.StreamHandler())


