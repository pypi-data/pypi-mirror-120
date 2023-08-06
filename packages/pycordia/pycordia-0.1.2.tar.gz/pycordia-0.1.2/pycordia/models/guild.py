import typing
import aiohttp
from typing import List, Union, Optional
from .user import User


class Member:
    def __init__(self, data: dict):
        self.user: User = User(data.get("user", {}))
        self.nick: Union[str, None] = data.get("nick")
        self.roles: list = data.get("roles", [])
        self.joined_at: Union[str, None] = data.get("joined_at")
        self.premium_since: Union[str, None] = data.get("premium_since")
        self.deaf: Union[bool, None] = data.get("deaf")
        self.mute: Union[bool, None] = data.get("mute")
        self.pending: Union[bool, None] = data.get("pending")
        self.permissions: Union[str, None] = data.get("permissions")

    def __repr__(self):
        return f"<GuildMember id={self.user.user_id} username='{self.user.username}'>"


class PartialGuild:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: str = data.get("icon")
        self.owner: bool = bool(data.get("owner"))
        self.permissions_integer = data.get("permissions")
        self.features: typing.List[str] = data.get("features", [])

    def __repr__(self):
        return f"<PartialGuild - id={self.id} name={self.name}>"


class Role:
    def __init__(self, data: dict):
        self.role_id: Union[str, None] = data.get("id")
        self.role_name: Union[str, None] = data.get("name")

        self.color: Union[int, None] = data.get("color")
        self.colour = self.color

        self.hoist: Union[bool, None] = data.get("hoist")
        self.position: Union[int, None] = data.get("position")
        self.permissions: Union[str, None] = data.get("permissions")
        self.managed: Union[bool, None] = data.get("managed")
        self.mentionable: Union[bool, None] = data.get("mentionable")

        self.tags = data.get("tags")
