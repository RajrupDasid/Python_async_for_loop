import asyncio
import time


async def use_api(x: int):
    await asyncio.sleep(0.1)
    return 2*x


async def await_rate_limited(awaitables, rate: float):
    max_sleep_duration = 1/rate
    for aw in awaitables:
        start = time.perf_counter()
        yield await aw
        elapsed = time.perf_counter() - start
        await asyncio.sleep(max(0.0, max_sleep_duration-elapsed))


async def main():
    awaitables = (use_api(x)for x in range(1000))
    start = time.perf_counter()
    """assigning rate limit to the api"""
    async for result in await_rate_limited(awaitables, rate=5.0):
        elapsed = time.perf_counter() - start
        print(f"[{elapsed:.2f}s] Got result: {result}")

    # for awaitable in awaitables:
    #     result = await awaitable
    #     elapsed = time.perf_counter() - start
    #     print(f"[{elapsed:.2f}s] Got result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
