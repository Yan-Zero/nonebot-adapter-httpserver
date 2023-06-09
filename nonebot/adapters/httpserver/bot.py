""" HTTP Server Bot """

from typing import Any, Union
from nonebot.typing import overrides

from nonebot.adapters.onebot.v11.bot import Bot as BaseBot

from .event import Event
from .message import Message, MessageSegment


class Bot(BaseBot):
    @overrides(BaseBot)
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs,
    ) -> Any:
        ...
