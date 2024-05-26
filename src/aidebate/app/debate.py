import logging
from typing import Union, List

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage

from .config import DialogueConfig
from .dialogue import DialogueAgent, DialogueAgentProvider, DialogueSimulator
from .env import Env

logger = logging.getLogger(__name__)


class DebateListener:
    def on_spoken(self, speaker: str, message: str):
        logger.info(f"({speaker}):\n{message}\n")


class Debate:
    @staticmethod
    def of(config: DialogueConfig) -> 'Debate':
        return Debate(config,
                      Env.get_app_dialogue_topic(),
                      Env.get_app_dialogue_personas(),
                      Env.get_app_dialogue_moderator(),
                      Env.get_app_dialogue_max_turns())

    def __init__(self, config: DialogueConfig,
                 topic: str,
                 personas: [str],
                 moderator: str = "Moderator",
                 max_turns: int = 5,
                 dialogue_agent_provider: Union[DialogueAgentProvider, None] = None):
        self.__config: DialogueConfig = config
        self.__topic: str = topic
        self.__personas: str = personas
        self.__moderator: str = moderator
        self.__turns: int = 0
        self.__max_turns: int = max_turns
        self.__dialogue_agent_provider: DialogueAgentProvider = DialogueAgentProvider() \
            if dialogue_agent_provider is None else dialogue_agent_provider
        self.__paused: bool = False
        self.__default_tools: [str] = config.agent_config.tool_config.names
        self.__persona_tools: dict[str, [str]] = \
            {} if not personas else {e: self.__default_tools for e in personas}
        self.__dialogue_simulator: Union[DialogueSimulator, None] = None

    def with_dialogue_agent_provider(self,
                                     dialogue_agent_provider: DialogueAgentProvider) -> 'Debate':
        return Debate(self.__config, self.__topic, self.__personas,
                      self.__moderator, self.__max_turns, dialogue_agent_provider)

    def add_persona(self, persona: str, tools: Union[tuple[str], None] = None) \
            -> 'Debate':
        self.__persona_tools[persona] = self.__default_tools if not tools else tools
        logger.debug(f"Added dialogue participant `{persona}` "
                     f"with tools: {self.__persona_tools[persona]}")
        return self

    def start(self, listener: Union[DebateListener, None] = None):

        logger.debug(f"Starting {self.__print_basics()}")

        if listener is None:
            listener = DebateListener()

        if self.__dialogue_simulator is None:
            model_kwargs: dict[str, any] = \
                {**self.__config.agent_config.chat_model, "temperature": 1.0}
            chat_model = self.__dialogue_agent_provider.get_chat_model(**model_kwargs)

            topic: str = self._ask_ai_to_update_topic(chat_model)
            participants: [DialogueAgent] = self._create_participants(chat_model)

            logger.debug(f"Initializing simulator for {self.__print_basics()}")
            self.__dialogue_simulator = self._init_simulator(topic, self.__moderator, participants)

            listener.on_spoken(self.__moderator, topic)

        while self.__paused is False and self.__turns < self.__max_turns:
            name, message = self.__dialogue_simulator.next()
            listener.on_spoken(name, message)
            self.__turns += 1

    def stop(self):
        self.__turns = 0
        self.pause()

    def pause(self):
        logger.debug(f"Starting {self.__print_basics()}")
        self.__paused = True

    def is_paused(self) -> bool:
        return self.__paused

    @staticmethod
    def _init_simulator(topic: str, moderator: str, participants: [DialogueAgent]) \
            -> DialogueSimulator:
        def select_next_speaker(step: int, agents: List[DialogueAgent]) -> int:
            return step % len(agents)

        simulator = DialogueSimulator(agents=participants, selection_function=select_next_speaker)
        simulator.reset()
        simulator.initiate(moderator, topic)
        return simulator

    def __print_basics(self):
        return (f"Debate{{moderator: '{self.__moderator}', "
                f"personas: {self.__personas}, topic: '{self.__topic}'}}")

    def _ask_ai_to_update_topic(self, chat_model: BaseChatModel) -> str:
        logger.debug(f"Asking ai to update topic: {self.__topic}")
        updated_topic = self._ask_ai(
            chat_model,
            self.__config.topic_config.prompt_config.system,
            self.__config.topic_config.prompt_config.human)

        logger.debug(f"\nOriginal topic: {self.__topic}\nDetailed topic: {updated_topic}")

        return updated_topic

    def _create_participants(self, chat_model: BaseChatModel) -> [DialogueAgent]:
        logger.debug(f"Creating participating agents from personas: {self.__personas}")

        persona_tools: dict = self.__require_min_length("personas", self.__persona_tools)

        persona_system_messages = {}
        for persona, tools in persona_tools.items():
            description = self._ask_ai_to_update_persona_description(chat_model, persona)
            persona_system_messages[persona] = self._get_persona_system_message(
                persona, description)

        for persona, system_message in persona_system_messages.items():
            logger.debug(f"{persona}\n{system_message}")
            
        return [
            self.__dialogue_agent_provider.get_dialogue_agent(
                persona, system_message, tools, 
                self.__config.agent_config.tool_config.args,
                self.__config.agent_config.chat_model)
            for (persona, tools), system_message in zip(
                persona_tools.items(), persona_system_messages.values()
            )
        ]

    def _get_persona_system_message(self, persona, description):
        return self.__config.agent_config.prompt_config.system.replace(
            "%%persona%%", persona).replace("%%persona_description%%", description)

    def _ask_ai_to_update_persona_description(self, chat_model: BaseChatModel, persona) -> str:
        logger.debug(f"Asking ai to update persona description for: {persona}")
        agent_description_prompt = self.__config.agent_config.description_config.prompt_config
        system_msg = agent_description_prompt.system
        human_msg = agent_description_prompt.human.replace("%%persona%%", persona)
        return self._ask_ai(chat_model, system_msg, human_msg)

    @staticmethod
    def _ask_ai(chat_model: BaseChatModel, system_msg: str, human_msg: str) -> str:
        prompt = [SystemMessage(content=system_msg), HumanMessage(content=human_msg)]
        return chat_model(prompt).content

    @staticmethod
    def __require_min_length(name: str, value):
        if len(value) < 2:
            raise ValueError(f"At least 2 {name} must be specified.")
        return value
