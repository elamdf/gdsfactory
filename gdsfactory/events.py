from __future__ import annotations

from typing import Any, Callable

# TODO this should have a type parameter other than "Any"
Handler = Callable[[Any], Any]


class Event:
    def __init__(self) -> None:
        """Initialize the object."""
        self._handlers: list[Handler] = []

    def __iadd__(self, handler: Handler) -> Event:
        """Add item."""
        self.add_handler(handler)
        return self

    def __isub__(self, handler: Handler) -> Event:
        """Subtract item."""
        self._handlers.remove(handler)
        return self

    def add_handler(self, handler: Handler) -> None:
        """Adds a handler that will be executed when this event is fired.

        Args:
            handler: a function which matches the signature fired by this event

        """
        self._handlers.append(handler)

    def clear_handlers(self) -> None:
        """Clear all handlers."""
        self._handlers.clear()

    def fire(
        self,
        *args: tuple[Any],
        **kwargs: dict[str, Any],
    ) -> None:
        """Fires an event, calling all handlers with the passed arguments."""
        for eventhandler in self._handlers:
            eventhandler(*args, **kwargs)
