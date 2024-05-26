import logging
from typing import Union

from pyu.io.yaml_loader import YamlLoader

from .config import AppConfig, ConfigLoader, DialogueConfig
from .debate import Debate
from .env import Env, LANGCHAIN_TRACING_V2

logger = logging.getLogger(__name__)


class DefaultConfigLoader(ConfigLoader):
    def __init__(self):
        self.__yaml_loader = YamlLoader(['resources', 'config'], suffix='.config')

    def load_app_config(self) -> AppConfig:
        return AppConfig(self.__yaml_loader.load_app_config())

    def load_logging_config(self) -> dict:
        return self.__yaml_loader.load_logging_config()


class App:
    def __init__(self, config_loader: Union[ConfigLoader, None] = None) -> None:

        config_loader = DefaultConfigLoader() if config_loader is None else config_loader

        app_config: AppConfig = config_loader.load_app_config()

        Env.set_value_if_none(LANGCHAIN_TRACING_V2, logger.isEnabledFor(logging.DEBUG))

        app_config.sync_with_env()

        self.__debate = self._create_debate(app_config.dialogue_config)

    @classmethod
    def _create_debate(cls, config: DialogueConfig) -> Debate:
        return Debate.of(config)

    def run(self):
        self.__debate.start()
