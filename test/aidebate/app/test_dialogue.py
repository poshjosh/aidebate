import logging
from typing import List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage

from aidebate.app.dialogue import DialogueAgentProvider, DialogueAgent

logger = logging.getLogger(__name__)


class TestDialogueAgentProvider(DialogueAgentProvider):
    def _create_dialogue_agent(self,
                               name: str,
                               system_message: str,
                               tool_names: List[str],
                               tool_kwargs: dict[str, any],
                               chat_model: BaseChatModel) -> DialogueAgent:
        logger.debug(f"Creating test dialogue agent: {name}` with tools: {tool_names}")
        if name.lower().startswith('test_'):
            return DialogueAgent(
                name=name,
                system_message=SystemMessage(content=system_message),
                model=chat_model)
        else:
            return super()._create_dialogue_agent(
                name, system_message, tool_names, tool_kwargs, chat_model)
