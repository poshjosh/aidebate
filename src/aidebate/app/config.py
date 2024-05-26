import os
from typing import Callable

from .env import APP_DIALOGUE_MODEL, APP_DIALOGUE_MODEL_API_KEY, \
                 APP_DIALOGUE_MODEL_PROVIDER, APP_DIALOGUE_MODEL_TEMPERATURE, \
                 LANGCHAIN_ENDPOINT, LANGCHAIN_PROJECT


class Config:
    def __init__(self, config: dict[str, any]):
        if config is None:
            raise ValueError("config is required")
        self.__config: dict[str, any] = config

    def update_from_env(self,
                        env_name: str,
                        config_key: str,
                        transform_value: Callable[[str, any], any] = lambda k, v: v) -> any:
        env_value: str = os.environ.get(env_name, None)
        if env_value is not None:
            self.__config[config_key] = transform_value(config_key, env_value)
        return self.__config.get(config_key, None)

    def create(self, construct) -> any:
        return construct(self.__config)

    def require(self, key: str) -> any:
        return self.__config[key]

    @property
    def as_dict(self) -> dict[str, any]:
        """Returns a copy of the config as a dictionary."""
        return {**self.__config}


class PromptConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["prompt"])

    @property
    def system(self) -> str:
        return self.require("system")

    @property
    def human(self) -> str:
        return self.require("human")


class TopicConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["topic"])
        self.__prompt_config = self.create(PromptConfig)

    @property
    def prompt_config(self) -> PromptConfig:
        return self.__prompt_config


class AgentDescriptionConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["description"])
        self.__prompt_config = self.create(PromptConfig)

    @property
    def prompt_config(self) -> PromptConfig:
        return self.__prompt_config


class ChatModelConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["chat_model"])

    __provider = "provider"
    __model = "model"
    __temperature = "temperature"

    def update_all_from_env(self):
        self.update_from_env(APP_DIALOGUE_MODEL_PROVIDER, self.__provider)
        self.update_from_env(APP_DIALOGUE_MODEL, self.__model)
        self.update_from_env(APP_DIALOGUE_MODEL_TEMPERATURE,
                             self.__temperature, lambda k, v: None if v is None else float(v))
        self.update_from_env(APP_DIALOGUE_MODEL_API_KEY, f'{self.provider}_api_key')

    @property
    def provider(self) -> str:
        return self.require(self.__provider)

    @property
    def model(self) -> str:
        return self.require(self.__model)

    @property
    def temperature(self) -> float:
        return float(self.require(self.__temperature))


class AgentToolConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["tool"])

    @property
    def names(self) -> [str]:
        return self.require("names")

    @property
    def args(self) -> dict[str, any]:
        return self.require("args")


class AgentConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["agent"])
        self.__chat_model_config = self.create(ChatModelConfig)
        self.__description_config = self.create(AgentDescriptionConfig)
        self.__tool_config = self.create(AgentToolConfig)
        self.__prompt_config = self.create(PromptConfig)

    @property
    def chat_model(self) -> dict[str, any]:
        return self.__chat_model_config.as_dict

    @property
    def chat_model_config(self) -> ChatModelConfig:
        return self.__chat_model_config

    @property
    def description_config(self) -> AgentDescriptionConfig:
        return self.__description_config

    @property
    def tool_config(self) -> AgentToolConfig:
        return self.__tool_config

    @property
    def prompt_config(self) -> PromptConfig:
        return self.__prompt_config


class DialogueConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["dialogue"])
        self.__topic_config = self.create(TopicConfig)
        self.__agent_config = self.create(AgentConfig)

    @property
    def description(self) -> str:
        return self.require("description")

    @property
    def topic_config(self) -> TopicConfig:
        return self.__topic_config

    @property
    def agent_config(self) -> AgentConfig:
        return self.__agent_config


class LangchainConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config["langchain"])

    def update_env(self):
        os.environ[LANGCHAIN_ENDPOINT] = self.endpoint
        os.environ[LANGCHAIN_PROJECT] = self.project

    @property
    def endpoint(self) -> str:
        return self.require("endpoint")

    @property
    def project(self) -> str:
        return self.require("project")


class AppConfig(Config):
    def __init__(self, config: dict[str, any]):
        super().__init__(config)
        self.__dialogue_config = self.create(DialogueConfig)
        self.__langchain_config = self.create(LangchainConfig)

    def sync_with_env(self):
        self.__langchain_config.update_env()
        self.__dialogue_config.agent_config.chat_model_config.update_all_from_env()

    @property
    def dialogue_config(self) -> DialogueConfig:
        return self.__dialogue_config

    @property
    def langchain_config(self) -> LangchainConfig:
        return self.__langchain_config


class ConfigLoader:
    def load_app_config(self) -> AppConfig:
        """Subclasses should implement this method to load the app config."""
        raise NotImplementedError("Implement this method to load the app config.")

    def load_logging_config(self) -> dict[str, any]:
        """Subclasses should implement this method to load the logging config."""
        raise NotImplementedError("Implement this method to load the logging config.")
