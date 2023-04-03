from pydantic import BaseModel, Field

from allmeca.callbacks.manager import CallbackManager
from allmeca.environments.base import BaseEnvironment
from allmeca.processors.base import Processor
from allmeca.messages import Persistence
from allmeca.bot import MainBot


class RunContext(BaseModel):
    """Contains all the information needed in various places during a run
    of Allmecca.
    """

    environment: BaseEnvironment
    processor: Processor
    main_bot: MainBot
    callbacks: CallbackManager = Field(default_factory=CallbackManager)

    def inject_self(self):
        """Injects the run context into its components."""
        self.environment._ctx = self
        self.processor._ctx = self
        self.main_bot._ctx = self
        self.callbacks._ctx = self

    class Config:
        arbitrary_types_allowed = True
