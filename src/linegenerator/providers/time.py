from datetime import datetime, timedelta
from functools import partial
from typing import Callable

from linegenerator.core.provider import BaseProvider


class TimeProvider(BaseProvider):
    def __init__(self, start: datetime | None = None, interval: timedelta | None = None) -> None:
        # Type checks for start and interval
        if start and not isinstance(start, datetime):
            raise TypeError(f"start should be an instance of datetime, but got {type(start)}")
        if interval and not isinstance(interval, timedelta):
            raise TypeError(f"interval should be an instance of timedelta, but got {type(interval)}")

        self._initial_start = start or datetime.now()
        self._interval = interval or timedelta(seconds=1)
        self.reset()  # Initializes _current

    def reset(self) -> None:
        """Reset the current timestamp to the initial value."""
        self._current = self._initial_start

    def _next_timestamp(self, fmt: str) -> str:
        """Generate the next timestamp with the given format and increment the current time by the interval."""
        result = self._current.strftime(fmt)
        self._current += self._interval
        return result

    def get_generators(self) -> dict[str, Callable[[], str]]:
        """
        Returns a dictionary of timestamp generators with different formats.
        Uses functools.partial to pre-set the format.
        """
        return {
            "nginx_timestamp": partial(self._next_timestamp, "%d/%b/%Y:%H:%M:%S %z"),
            "pgsql_timestamp": partial(self._next_timestamp, "%Y-%m-%d %H:%M:%S.%f UTC"),
            "iso_timestamp": partial(self._next_timestamp, "%Y-%m-%dT%H:%M:%SZ"),
        }
