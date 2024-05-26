import logging.config
import unittest

from aidebate.app.app import App
from aidebate.app.config import DialogueConfig
from aidebate.app.debate import Debate

from test_config import TestConfigLoader
from test_dialogue import TestDialogueAgentProvider

logging.config.dictConfig(TestConfigLoader().load_logging_config())


class TestApp(App):
    @classmethod
    def _create_debate(cls, config: DialogueConfig) -> Debate:
        dialogue_agent_provider = TestDialogueAgentProvider()
        return super()._create_debate(config).with_dialogue_agent_provider(dialogue_agent_provider)


class AppTestCase(unittest.TestCase):
    @staticmethod
    def test_app_run():
        TestApp(TestConfigLoader()).run()


if __name__ == '__main__':
    unittest.main()
