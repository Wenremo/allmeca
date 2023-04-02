from langchain.chat_models import ChatOpenAI

from allmeca.messages import Message, MessageList, Role
from allmeca.prompts import load_prompt_set


class MainBot:
    def __init__(self, *, processor, model="gpt-3.5-turbo"):
        self._history = MessageList()
        self._chat = ChatOpenAI(model_name=model, temperature=0)
        self.prompt_set = load_prompt_set("default")
        self._history.add_many(self.prompt_set.init)
        self._finished = False
        self._processor = processor

    def run(self, task):
        self._history.add(Message(role="human", content=task))
        while not self._finished:
            self.act()

    def act(self):
        print("Thinking...")
        msg = self._get_response()
        self._history.add(msg)
        print("Processing...")
        response = self._processor.process(msg)
        self._history.add(Message(role=Role.human, content=response))

    def _get_response(self):
        msg = self._chat(self._history.to_langchain(), stop=["/execute"])
        return Message.from_langchain(msg)
