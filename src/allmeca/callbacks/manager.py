from collections.abc import Iterable

from allmeca.logger import log


class CallbackManager:
    def __init__(self):
        self._handlers = set()

    def register(self, handler):
        self._handlers.add(handler)

    def unregister(self, handler):
        self._handlers.discard(handler)

    def emit(self, event, **kwargs):
        log.debug("emit_event", event_name=event, kwargs=list(kwargs.keys()))
        return list(self._emit(event, **kwargs))

    def _emit(self, event, **kwargs):
        for handler in self._handlers:
            if hasattr(handler, f"on_{event}"):
                callback = getattr(handler, f"on_{event}")
                yield from self._call_callback(callback, **kwargs)

    def _call_callback(self, callback, **kwargs):
        result = callback(**kwargs)
        if isinstance(result, Iterable):
            yield from result
        elif result is not None:
            yield result
