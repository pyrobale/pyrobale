import asyncio
import aiohttp


def build_api_url(base: str, endpoint: str) -> str:
    return f"{base}/{endpoint}"


async def make_post(url: str, data: dict = None, headers: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()


async def make_get(url: str, headers: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


def pythonize(dictionary: dict) -> dict:
    """Converts a dictionary with keys in snake_case to camelCase."""
    result = {}
    for key, value in dictionary.items():
        if key == "from":
            key = "from_user"
        result[key] = value
    return result
