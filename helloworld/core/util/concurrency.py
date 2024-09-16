from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor

async def run_sync_in_executor(func, *args):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        await loop.run_in_executor(executor, func, *args)