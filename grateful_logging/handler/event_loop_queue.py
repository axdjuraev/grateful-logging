import asyncio
from .queue import QueueHandler


class EventLoopQueue(QueueHandler):
    def __init__(self, *args, loop: "asyncio.AbstractEventLoop | None" = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._loop = loop or asyncio.new_event_loop()

    def _shutup(self):
        self._loop.close()
        return super()._shutup()
