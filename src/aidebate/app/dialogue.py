import copy
import logging
from typing import Callable, List

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.chat_models import HumanInputChatModel, ChatOllama, ChatAnthropic, \
    ChatBaichuan, BedrockChat, ChatCohere, ChatCoze, ChatDeepInfra, ErnieBotChat, ChatFireworks, \
    ChatFriendli, GigaChat as CommGigaChat, ChatGooglePalm, GPTRouter, ChatJavelinAIGateway, \
    MiniMaxChat, ChatMlflow, ChatMLflowAIGateway, ChatMLX, ChatHuggingFace, ChatHunyuan, \
    ChatKinetica, LlamaEdgeChatService, ChatLiteLLM, PaiEasChatEndpoint, ChatPerplexity, \
    ChatPremAI, QianfanChatEndpoint, ChatSparkLLM, ChatTongyi, ChatVertexAI, VolcEngineMaasChat, \
    ChatYandexGPT, ChatYuan2, ChatZhipuAI, FakeListChatModel as CommFakeListChatModel, JinaChat, \
    ChatMaritalk
from langchain_community.chat_models.azureml_endpoint import AzureMLChatOnlineEndpoint
from langchain_community.chat_models.dappier import ChatDappierAI
from langchain_community.chat_models.edenai import ChatEdenAI
from langchain_community.chat_models.fake import \
    FakeMessagesListChatModel as CommFakeMessagesListChatModel
from langchain_community.llms.gigachat import GigaChat as LLMGigaChat
from langchain_core.language_models import BaseChatModel, GenericFakeChatModel, \
    ParrotFakeChatModel, FakeListChatModel as CoreFakeListChatModel, \
    FakeMessagesListChatModel as CoreFakeMessagesListChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class DialogueAgent:
    def __init__(
            self,
            name: str,
            system_message: SystemMessage,
            model: BaseChatModel,
    ) -> None:
        self.name = name
        self.system_message = system_message
        self.model = model
        self.prefix = f"{self.name}: "
        self.message_history = []
        self.reset()

    def reset(self):
        self.message_history = ["Here is the conversation so far."]

    def speak(self) -> str:
        """
        Applies the chat model to the message history
        and returns the message string
        """
        message = self.model.invoke(
            [
                self.system_message,
                HumanMessage(content="\n".join(self.message_history + [self.prefix])),
            ]
        )
        return message.content

    def receive(self, name: str, message: str) -> None:
        """
        Concatenates {message} spoken by {name} into message history
        """
        self.message_history.append(f"{name}: {message}")


class DialogueAgentWithTools(DialogueAgent):
    def __init__(
            self,
            name: str,
            system_message: SystemMessage,
            model: BaseChatModel,
            tool_names: List[str],
            **tool_kwargs,
    ) -> None:
        super().__init__(name, system_message, model)
        self.tools = load_tools(tool_names, **tool_kwargs)

    def speak(self) -> str:
        """
        Applies the chat model to the message history
        and returns the message string
        """
        agent_chain = initialize_agent(
            self.tools,
            self.model,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=logger.isEnabledFor(logging.DEBUG),
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            ),
        )
        return agent_chain.run(
            input="\n".join(
                [self.system_message.content] + self.message_history + [self.prefix]
            )
        )


class DialogueSimulator:
    def __init__(
            self,
            agents: List[DialogueAgent],
            selection_function: Callable[[int, List[DialogueAgent]], int],
    ) -> None:
        self.agents = agents
        self._next = 0
        self.select_next_speaker = selection_function

    def reset(self):
        for agent in self.agents:
            agent.reset()

    def initiate(self, name: str, message: str):
        """
        Initiates the conversation with a {message} from {name}
        """
        for agent in self.agents:
            agent.receive(name, message)

        # increment time
        self._next += 1

    def next(self) -> tuple[str, str]:
        # 1. choose the next speaker
        speaker_idx = self.select_next_speaker(self._next, self.agents)
        speaker = self.agents[speaker_idx]

        # 2. next speaker sends message
        message = speaker.speak()

        # 3. everyone receives message
        for receiver in self.agents:
            receiver.receive(speaker.name, message)

        # 4. increment
        self._next += 1

        return speaker.name, message


DEFAULT_MODEL_PROVIDER = "openai"


class DialogueAgentProvider:
    def get_dialogue_agent(self,
                           name: str,
                           system_message: str,
                           tool_names: List[str],
                           tool_kwargs: dict[str, any],
                           model_kwargs: dict[str, any]) -> DialogueAgent:
        logger.debug(f"Creating dialogue agent: `{name}` with tools: {tool_names}")
        return self._create_dialogue_agent(
            name, system_message, tool_names, tool_kwargs, self.get_chat_model(**model_kwargs))

    def _create_dialogue_agent(self,
                               name: str,
                               system_message: str,
                               tool_names: List[str],
                               tool_kwargs: dict[str, any],
                               chat_model: BaseChatModel) -> DialogueAgent:
        logger.debug(f"Creating dialogue agent: {name}` with tools: {tool_names}")
        return DialogueAgentWithTools(
            name=name,
            system_message=SystemMessage(content=system_message),
            model=chat_model,
            tool_names=tool_names,
            **tool_kwargs)

    def get_chat_model(self, **kwargs) -> BaseChatModel:
        kwargs = {**kwargs}
        provider: str = kwargs.pop("provider", DEFAULT_MODEL_PROVIDER)
        logger.debug(f"Creating `{provider}` chat model with kwargs: {kwargs}")
        if provider not in _model_mappings.keys():
            raise NotImplementedError(f"Not implemented, chat model for {provider}")
        return _model_mappings[provider](**kwargs)


def get_chat_model_mappings() -> dict[str, any]:
    return copy.deepcopy(_model_mappings)


_model_mappings = {
    'anthropic': ChatAnthropic,  # Rather ChatAnthropic of `langchain-anthropic`
    'azuremlchatonlineendpoint': AzureMLChatOnlineEndpoint,
    'baichuan': ChatBaichuan,
    'bedrock': BedrockChat,  # Rather ChatBedrock of `langchain_aws`
    'cohere': ChatCohere,  # Rather use ChatCohere of `langchain_cohere`
    'coze': ChatCoze,
    'dappierai': ChatDappierAI,
    'deepinfra': ChatDeepInfra,
    'edenai': ChatEdenAI,
    'erniebot': ErnieBotChat,
    'fake.parrot': ParrotFakeChatModel,
    'fake-list': CoreFakeListChatModel,
    'fake-list.community': CommFakeListChatModel,
    'fake-messages-list': CoreFakeMessagesListChatModel,
    'fake-messages-list.community': CommFakeMessagesListChatModel,
    'fireworks': ChatFireworks,  # Rather use ChatFireworks of `langchain_fireworks`
    'friendli': ChatFriendli,
    'fake.generic': GenericFakeChatModel,
    'giga': CommGigaChat,
    'giga.llm': LLMGigaChat,
    'googlepalm': ChatGooglePalm,
    'gpt-router': GPTRouter,
    'javelinaigateway': ChatJavelinAIGateway,
    'jina': JinaChat,
    'maritalk': ChatMaritalk,
    'minimax': MiniMaxChat,
    'mlflow': ChatMlflow,
    'mlflowaigateway': ChatMLflowAIGateway,
    'mlx': ChatMLX,
    'huggingface': ChatHuggingFace,
    'human-input': HumanInputChatModel,
    'hunyuan': ChatHunyuan,
    'kinetica': ChatKinetica,
    'llamaedge': LlamaEdgeChatService,
    # Could not import litellm python package. Please install it with `pip install litellm`
    'litellm': ChatLiteLLM,
    'ollama': ChatOllama,
    'openai': ChatOpenAI,
    'paieas': PaiEasChatEndpoint,
    'pplx': ChatPerplexity,
    'premai': ChatPremAI,
    'qianfan': QianfanChatEndpoint,
    'sparkllm': ChatSparkLLM,
    'tongyi': ChatTongyi,
    'vertexai': ChatVertexAI,
    'volcenginemass': VolcEngineMaasChat,
    'yandexgpt': ChatYandexGPT,
    'yuan2': ChatYuan2,
    'zhipuai': ChatZhipuAI,
}
