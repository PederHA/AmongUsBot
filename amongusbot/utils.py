import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator


async def _progress(char: str=".", interval: float=0.5) -> None:
    while True:
        await asyncio.sleep(interval)
        print(char, end="")


@asynccontextmanager
async def progress(loop, char: str=".", interval: float=0.5) -> AsyncGenerator:
    t = loop.create_task(_progress(char, interval))
    try:
        yield
    finally:
        t.cancel()
        print("✔")
