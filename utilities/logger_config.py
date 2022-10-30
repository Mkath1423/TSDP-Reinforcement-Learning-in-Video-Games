from utilities.config import Config


class LoggerConfig(Config):
    requirements = (
        "name",
    )
    defaults = (
        ("logger_level", "WARNING"),
        ("format", "[%(levelname)s] %(asctime)s - %(message)s"),
        ("use_file_handler", False),
        ("log_path", None),
        ("log_file_level", "INFO"),
        ("use_stream_handler", True),
        ("sep", ", "),
        ("end", "")
    )

    def __init__(self, config: dict):
        self.logger_level       : int  = None
        self.format             : str  = None
        self.use_file_handler   : bool = None
        self.log_path           : str  = None
        self.log_file_level     : int  = None
        self.use_stream_handler : bool = None
        super().__init__(config)


if __name__ == "__main__":
    l = LoggerConfig({
        "name": "test"
    })

    print(l.logger_level)
