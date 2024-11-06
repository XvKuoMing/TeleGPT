import asyncio
import aiohttp
from typing import List, Tuple


async def fetch_url(session: aiohttp.ClientSession, url: str) -> Tuple[str, str]:
    """fetches single url text"""
    async with session.get(url) as response:
        page = await response.text()
        return url, page

async def fetch_all(urls: List[str]) -> List[Tuple[str, str]]:
    """fetches all given url"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                asyncio.ensure_future(
                    fetch_url(session, url)
                )
            )
        return await asyncio.gather(*tasks)

