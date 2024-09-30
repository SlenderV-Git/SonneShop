from typing import Generator, Generic, TypeVar, cast

from src.api.v1.handlers.command.base import RT, CommandProtocol


CommandType = TypeVar("CommandType", bound=CommandProtocol)


class AwaitableProxy(Generic[CommandType, RT]):
    __slots__ = ("_command", "_kw")

    def __init__(self, command: CommandType, **kwargs):
        self._command = command
        self._kw = kwargs

    def __await__(self) -> Generator[None, None, RT]:
        result = yield from self._command(**self._kw).__await__()
        return cast(RT, result)
