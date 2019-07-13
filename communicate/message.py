from abc import ABC, abstractmethod
from enum import Enum

from spade.message import Message
from spade.template import Template

from settings import get_xmpp_username, users


class AgentType(Enum):
    COORDINATOR = "coordinator"
    DECISION = "decision"
    FUNDAMENTAL = "fundamental"
    PUBLISHER = "publisher"
    TECHNICAL = "technical"
    STREAM_AGENT = "stream_agent"
    ORACLE = "oracle"
    PATTERN = "pattern"


def get_template(agent: AgentType):
    temp = Template()
    to = agent.value
    if to in users:
        to = users[to]
        temp.to = get_xmpp_username(to['username'])
    temp.set_metadata("stream", agent.value)
    return temp


class AbsMessageBuilder(ABC):

    @property
    @abstractmethod
    def message(self) -> None:
        pass

    @abstractmethod
    def to(self, to) -> None: pass

    @abstractmethod
    def meta_data(self, key, value) -> None: pass

    @abstractmethod
    def body(self, body) -> None: pass

    @abstractmethod
    def stream_name(self, name) -> None: pass


class MessageBuilder(AbsMessageBuilder):

    @property
    def message(self):
        return self.__message

    def to(self, to):
        if to in users:
            to = users[to]
            self.__message.to = get_xmpp_username(to['username'])
            return self
        raise Exception("Username is not found in users")

    def meta_data(self, key, value):
        self.__message.set_metadata(key, value)
        return self

    def stream_name(self, name):
        return self.meta_data("stream", name)

    def body(self, body):
        self.__message.body = body
        return self

    def __init__(self, to_agent: AgentType = AgentType.COORDINATOR) -> None:
        self.__message = Message()
        self.stream_name(to_agent.value)
        self.to(to_agent.value)
