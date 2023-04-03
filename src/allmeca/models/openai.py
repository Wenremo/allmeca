from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.openai_info import OpenAICallbackHandler
import click

from allmeca.models.openai_utils import NonabstractBaseCallbackHandler
from allmeca.messages import Message, MessageList, Role
from allmeca.logger import log


class TokenStreamCallbackHandler(NonabstractBaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        click.echo(click.style(token, fg="green"), nl=False)


# Workaround until https://github.com/hwchase17/langchain/pull/1924 is fixed
class CountTokensCallbackHandler(NonabstractBaseCallbackHandler):
    def __init__(self):
        self.tokens = 0

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens += 1


class OpenAIChat:
    def __init__(self, model: str, temperature: float = 0, stream=True):
        self._stream = stream
        self._callback_manager = CallbackManager([])
        # self._openai_info = OpenAICallbackHandler()
        # self._callback_manager.add_handler(self._openai_info)
        self._count_tokens = CountTokensCallbackHandler()
        self._callback_manager.add_handler(self._count_tokens)
        if stream:
            self._callback_manager.add_handler(TokenStreamCallbackHandler())

        self._chat = ChatOpenAI(
            model_name=model,
            temperature=temperature,
            callback_manager=self._callback_manager,
            streaming=True,
            verbose=True,
        )

    def generate(self, history: MessageList, stop: list[str] = []):
        if len(stop) == 0:
            stop = None

        msg = self._chat(history.to_langchain(), stop=stop)
        if self._stream:
            click.echo("\n")
        log.debug(
            "openai_info",
            total_tokens=self._count_tokens.tokens,
            # total_cost=self.total_cost,
            # total_tokens=self._openai_info.total_tokens,
            # prompt_tokens=self._openai_info.prompt_tokens,
            # completion_tokens=self._openai_info.completion_tokens,
        )
        return Message.from_langchain(msg)

    @property
    def total_cost(self):
        return self._openai_info.total_cost
