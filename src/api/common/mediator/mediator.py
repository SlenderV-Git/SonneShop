from typing import Any, Callable, Mapping, Optional, Type, Union

from src.api.common.exceptions import CommandNotFoundError
from src.api.v1.handlers.command.base import QT, RT, CommandProtocol
from .proxy import AwaitableProxy
from .register import get_register_commands


class CommandMediator:
    def __init__(self) -> None:
        self.commands: Mapping[
            Type[Any], Union[Callable[[], CommandProtocol], CommandProtocol]
        ] = {}

    def _resolve_factory(
        self, command_or_factory: Union[Callable[[], CommandProtocol], CommandProtocol]
    ) -> CommandProtocol:
        if isinstance(command_or_factory, CommandProtocol):
            return command_or_factory

        return command_or_factory()

    def add(
        self,
        query: Type[QT],
        command_or_factory: Union[Callable[[], CommandProtocol], CommandProtocol],
    ):
        self.commands[query] = command_or_factory

    def _predict_dependency_or_raise(
        self,
        actual: Mapping[str, Any],
        expectable: Mapping[str, Any],
        non_checkable: Optional[set[str]] = None,
    ) -> Mapping[str, Any]:
        if not non_checkable:
            non_checkable = set()

        missing = [k for k in actual if k not in expectable and k not in non_checkable]
        if missing:
            details = ", ".join(f"`{k}`:`{actual[k]}`" for k in missing)
            raise TypeError(f"Did you forget to set dependency for {details}?")

        return {k: value if (value := expectable.get(k)) else actual[k] for k in actual}

    def _create_command_lazy(
        self,
        command: Type[CommandProtocol],
        **dependencies: Union[Callable[[], Any], Any],
    ) -> Callable[[], CommandProtocol]:
        def _create() -> CommandProtocol:
            return command(
                **{k: v() if callable(v) else v for k, v in dependencies.items()}
            )

        return _create

    def setup(self, **kwargs: Any) -> None:
        for query, command_or_factory in get_register_commands().items():
            self.add(
                query=query,
                command_or_factory=self._create_command_lazy(
                    **self._predict_dependency_or_raise(
                        command_or_factory, kwargs, {"command"}
                    )
                ),
            )

    def send(self, query: QT, **kwargs: Any) -> AwaitableProxy[CommandProtocol, RT]:
        handler = self.commands.get(type(query))
        if not handler:
            raise CommandNotFoundError(f"Not found handlers from {type(query)} command")

        return AwaitableProxy(self._resolve_factory(handler), query=query, **kwargs)
