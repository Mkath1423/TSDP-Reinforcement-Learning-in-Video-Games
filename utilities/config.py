import logging


class Config:
    requirements = (

    )

    defaults = (

    )

    def __init__(self, d: dict):
        for requirement in self.requirements:
            if requirement not in d.keys():
                logging.error(f"requirement not met {requirement}, failed to create config.")
                return

        for default in self.defaults:
            self.__setattr__(default[0], default[1])

        for k, v in d.items():
            self.__setattr__(k, v )

