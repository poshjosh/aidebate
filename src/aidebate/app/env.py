import logging
import os

APP_DIALOGUE_MODEL_API_KEY: str = "APP_DIALOGUE_MODEL_API_KEY"
APP_DIALOGUE_MODEL_PROVIDER: str = "APP_DIALOGUE_MODEL_PROVIDER"
APP_DIALOGUE_MODEL: str = "APP_DIALOGUE_MODEL"
APP_DIALOGUE_MODEL_TEMPERATURE: str = "APP_DIALOGUE_MODEL_TEMPERATURE"
APP_DIALOGUE_MAX_TURNS: str = "APP_DIALOGUE_MAX_TURNS"
APP_DIALOGUE_MODERATOR: str = "APP_DIALOGUE_MODERATOR"
APP_DIALOGUE_PERSONAS: str = "APP_DIALOGUE_PERSONAS"
APP_DIALOGUE_TOPIC: str = "APP_DIALOGUE_TOPIC"
APP_DIALOGUE_WORD_LIMIT: str = "APP_DIALOGUE_WORD_LIMIT"
LANGCHAIN_ENDPOINT: str = "LANGCHAIN_ENDPOINT"
LANGCHAIN_PROJECT: str = "LANGCHAIN_PROJECT"
LANGCHAIN_TRACING_V2: str = "LANGCHAIN_TRACING_V2"

logger = logging.getLogger(__name__)


class Env:
    @staticmethod
    def init():
        Env.set_value_if_none(APP_DIALOGUE_MAX_TURNS, 6)
        Env.set_value_if_none(APP_DIALOGUE_MODERATOR, "Moderator")
        Env.set_value_if_none(APP_DIALOGUE_WORD_LIMIT, 50)

        # Ensure these are set
        Env.get_app_dialogue_personas()
        Env.get_app_dialogue_topic()

    @staticmethod
    def get_app_dialogue_moderator() -> str:
        return os.environ[APP_DIALOGUE_MODERATOR].strip()

    @staticmethod
    def get_app_dialogue_topic() -> str:
        return os.environ[APP_DIALOGUE_TOPIC].strip()

    @staticmethod
    def get_app_dialogue_word_limit() -> int:
        return int(os.environ.get(APP_DIALOGUE_WORD_LIMIT, 50))

    @staticmethod
    def get_app_dialogue_personas() -> [str]:
        return [e.strip() for e in os.environ[APP_DIALOGUE_PERSONAS].split(",")]

    @staticmethod
    def get_app_dialogue_max_turns() -> int:
        return int(os.environ[APP_DIALOGUE_MAX_TURNS])

    @staticmethod
    def is_langchain_tracing() -> bool:
        return os.environ[LANGCHAIN_TRACING_V2] == "true"

    @staticmethod
    def set_value_if_none(key: str, value: any) -> str:
        existing = os.environ.get(key, None)
        if existing is None:
            os.environ[key] = None if value is None else str(value)
        return existing
