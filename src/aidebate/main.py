import logging.config

from app.app import App, DefaultConfigLoader
from app.env import Env


if __name__ == "__main__":

    Env.init()

    config_loader = DefaultConfigLoader()

    logging.config.dictConfig(config_loader.load_logging_config())

    App(config_loader).run()
