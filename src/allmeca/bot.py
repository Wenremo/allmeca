from langchain.chat_models import ChatOpenAI

from allmeca.messages import Message, MessageList, Role
from allmeca.processors import reactions
from allmeca.logger import log


class MainBot:
    def __init__(self, *, prompt_set, processor, persistence, model="gpt-3.5-turbo"):
        self._persistence = persistence
        self._history = persistence.load()
        self._chat = ChatOpenAI(model_name=model, temperature=0)
        self._prompt_set = prompt_set
        if self._history.is_empty():
            self._history.add_many(self._prompt_set.init)
            self._persist()
        self._stop = False
        self._processor = processor

    def run(self, task):
        log.info("bot_started", task=task)
        content = f"This is your objective: {task}"
        self._history.add(Message(role=Role.system, content=content))
        while not self._stop:
            self.act()
        log.info("bot_stopped")

    def act(self):
        print("Thinking...")
        msg = self._get_completion()
        self._history.add(msg)
        for reaction in self._processor.process(msg):
            self._process_reaction(reaction)

    def _process_reaction(self, reaction):
        if isinstance(reaction, reactions.Response):
            log.info("bot_response", response=reaction.response)
            self._history.add(Message(role=Role.system, content=reaction.response))
        elif isinstance(reaction, reactions.Stop):
            self._stop = True
        elif isinstance(reaction, reactions.Noop):
            pass
        else:
            raise ValueError(f"Unknown reaction type: {type(reaction).__name__}")
        self._persist()

    def _get_completion(self):
        msg = self._chat(self._history.to_langchain(), stop=self._prompt_set.stop_words)
        return Message.from_langchain(msg)

    def _persist(self):
        self._persistence.save(self._history)
