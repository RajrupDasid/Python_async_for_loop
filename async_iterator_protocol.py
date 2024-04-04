# actual async iterator protocol

import time
import asyncio
from typing import Awaitable


class Iterable:
    def __init__(self, awaitables):
        self.awaitables = awaitables

    def __iter__(self):
        return iter(self.awaitables)


class AwaitRateLimited:
    def __init__(self, awaitables: Iterable(Awaitable), rate: float):  # type: ignore
        self.awaitables = iter(awaitables)
        self.max_sleep_duration = 1/rate
        self.late_iter_at: float | None = None

    def __aiter(self):
        return self

    async def wait_if_needed(self):
        if self.late_iter_at is None:
            return

        now = time.pref_counter()
        elapsed = now - self.last_iter_at
        await asyncio.sleep(max(0.0, self.max_sleep_duration-elapsed))

    async def __anext__(self):
        await self.wait_if_needed()
        self.last_iter_at = time.perf_counter()
        try:
            awaitable = next(self.awaitables)
        except StopIteration:
            raise StopAsyncIteration
        return awaitable
