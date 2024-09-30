import inspect
from typing import (
    Any,
    Callable,
    Mapping,
    Protocol,
    Type,
    Union,
    get_args,
    get_origin,
    get_overloads,
    get_type_hints,
)

from src.api.v1.handlers.command.base import QT, RT, Command, CommandProtocol
from .proxy import AwaitableProxy, CommandType


class CommandMediatorProtocol(Protocol):
    # there you should add an overload for your command
    # it need to auto registry your command and also typing in routes

    # default one, should leave unchanged at the bottom of the protocol
    def send(self, query: QT, **kwargs: Any) -> AwaitableProxy[CommandType, RT]:
        ...


def _retrieve_command_params(command: CommandProtocol) -> Mapping[str, Any]:
    return {k: v.annotation for k, v in inspect.signature(command).parameters.items()}


def get_register_commands() -> (
    Mapping[Type[Any], Union[Callable[[], CommandProtocol], CommandProtocol]]
):
    commands = {}
    overloads = get_overloads(CommandMediatorProtocol.send)
    for send in overloads:
        hints = get_type_hints(send)
        query, proxy = hints.get("query"), hints.get("return")

        if not query or not proxy:
            raise TypeError(
                "Did you forget to annotate your overloads? "
                "It should contain :query: param and :return: AwaitableProxy generic"
            )
        origin = get_origin(proxy)
        if origin is not AwaitableProxy:
            raise TypeError("Return type must be a type of AwaitableProxy.")

        args = get_args(proxy)

        if len(args) < 2:
            raise TypeError("AwaitableProxy must have two generic parameters")

        command = args[0]
        if not issubclass(command, Command):
            raise TypeError("command must inherit from base Command class.")

        commands[query] = {"command": command, **_retrieve_command_params(command)}

    return commands
