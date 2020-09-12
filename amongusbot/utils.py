import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator


@asynccontextmanager
async def progress(loop, char: str=".", interval: float=0.5) -> AsyncGenerator:
    async def _progress():
        while True:
            await asyncio.sleep(interval)
            print(char, end="")    
    t = loop.create_task(_progress())
    try:
        yield
    finally:
        t.cancel()
        print("✔")
