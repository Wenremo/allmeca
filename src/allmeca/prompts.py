from pathlib import Path
import yaml
from pydantic import BaseModel
from allmeca.messages import Message, MessageList

propts_dir = Path(__file__).parent.parent.parent / "prompts"


class PromptSet(BaseModel):
    init: MessageList


def load_prompt_set(name):
    with open(propts_dir / f"{name}.yml") as f:
        obj = yaml.safe_load(f)
        return PromptSet(init=MessageList(messages=obj["init"]))
