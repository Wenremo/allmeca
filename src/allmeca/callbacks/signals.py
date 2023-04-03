from typing import Optional

from pydantic import BaseModel


class Signal(BaseModel):
    pass


class SkipAction(Signal):
    reason: Optional[str] = None
