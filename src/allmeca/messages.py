from pydantic import BaseModel
from enum import Enum
from langchain.schema import AIMessage, HumanMessage, SystemMessage, ChatMessage
from pathlib import Path


class Role(str, Enum):
    human = "human"
    ai = "ai"
    system = "system"


class Message(BaseModel):
    role: Role
    content: str
    sticky: bool = False

    def to_langchain(self):
        if self.role == "human":
            return HumanMessage(content=self.content)
        elif self.role == "ai":
            return AIMessage(content=self.content)
        elif self.role == "system":
            return SystemMessage(content=self.content)
        else:
            return ChatMessage(content=self.content, role=self.role)

    @classmethod
    def from_langchain(cls, message):
        return cls(role=message.type, content=message.content)


class MessageList(BaseModel):
    messages: list[Message] = []

    def add(self, message: Message):
        self.messages.append(message)

    def add_many(self, messages: list[Message]):
        for message in messages:
            self.add(message)

    def to_langchain(self):
        return [m.to_langchain() for m in self.messages]

    def __iter__(self):
        return iter(self.messages)

    def is_empty(self):
        return len(self.messages) == 0


class Persistence:
    def save(self, message_list: MessageList):
        raise NotImplementedError

    def load(self) -> MessageList:
        raise NotImplementedError


class NullPersistence(Persistence):
    def save(self, message_list: MessageList):
        pass

    def load(self) -> MessageList:
        return MessageList()


class FilePersistence(Persistence):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, message_list: MessageList):
        with self.path.open("w") as f:
            f.write(message_list.json())

    def load(self) -> MessageList:
        if not self.path.exists():
            return MessageList()
        with self.path.open("r") as f:
            return MessageList.parse_raw(f.read())
