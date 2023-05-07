""" HTTP 服务器配置类。 """

from typing import Set, Dict, Optional

from pydantic import Field, AnyUrl, BaseModel


class Config(BaseModel):
    """HTTP 服务器配置类。"""

    class Config:
        extra = "ignore"
