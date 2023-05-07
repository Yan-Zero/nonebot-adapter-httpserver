"""OneBot v11 适配器。

FrontMatter:
    sidebar_position: 1
    description: onebot.v11.adapter 模块
"""
import hmac
import json
import asyncio
import inspect
import contextlib
from typing import Any, Dict, List, Type, Union, Callable, Optional, Generator, cast

from nonebot.typing import overrides
from nonebot.exception import WebSocketClosed
from nonebot.utils import DataclassEncoder, escape_tag
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter
from nonebot.adapters.onebot.collator import Collator
from nonebot.adapters.onebot.store import ResultStore
from nonebot.adapters.onebot.utils import get_auth_bearer

from . import event
from .bot import Bot
from .config import Config
from .event import Event
from .message import Message, MessageSegment

RECONNECT_INTERVAL = 3.0
DEFAULT_MODELS: List[Type[Event]] = []
for model_name in dir(event):
    model = getattr(event, model_name)
    if not inspect.isclass(model) or not issubclass(model, Event):
        continue
    DEFAULT_MODELS.append(model)


class Adapter(BaseAdapter):
    event_models = Collator(
        "Simple HTTP Server",
        DEFAULT_MODELS,
        (
            "post_type",
            ("message_type", "notice_type", "request_type", "meta_event_type"),
            "sub_type",
        ),
    )

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.onebot_config: Config = Config(**self.config.dict())
        """ HTTP Server 适配器配置 """

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        """适配器名称: `HTTP Server`"""
        return "HTTP Server"

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        raise NotImplementedError
