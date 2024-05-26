from pyu.io.yaml_loader import YamlLoader

from aidebate.app.config import AppConfig, ConfigLoader


class TestConfigLoader(ConfigLoader):
    def load_app_config(self) -> AppConfig:
        config: dict = YamlLoader(
            "src/resources/config", suffix=".config").load_app_config()
        return AppConfig(config)

    def load_logging_config(self) -> dict:
        return {
            'version': 1,
            'formatters': {'simple': {'format': '%(asctime)s %(name)s %(levelname)s %(message)s'}},
            'handlers': {'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG', 'formatter': 'simple'}},
            'loggers': {'aidebate': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False}}
        }
