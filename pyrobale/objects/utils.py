from ..exceptions import *

import asyncio
import inspect
from functools import wraps
import functools
from typing import Any, Callable, Union
import aiohttp


def build_api_url(base: str, endpoint: str) -> str:
    return f"{base}/{endpoint}"


async def make_post(url: str, data: dict = None, headers: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            json = await response.json()
            if json['ok']:
                if 'result' in json.keys():
                    return json
                else:
                    if json['error_code'] == 404:
                        raise NotFoundException(f"Error not found 404 : {json['description'] if json['description'] else 'No description returned in error'}")
                    elif json['error_code'] == 403:
                        raise ForbiddenException(f"Error Forbidden 403 : {json['description'] if json['description'] else 'No description returned in error'}")
                    else:
                        raise PyroBaleException(f"unknown error : {json['description'] if json['description'] else 'No description!'}")


async def make_get(url: str, headers: dict = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            json = await response.json()
            if json['ok']:
                if 'result' in json.keys():
                    return json
                else:
                    if json['error_code'] == 404:
                        raise NotFoundException(f"Error not found 404 : {json['description'] if json['description'] else 'No description returned in error'}")
                    elif json['error_code'] == 403:
                        raise ForbiddenException(f"Error Forbidden 403 : {json['description'] if json['description'] else 'No description returned in error'}")
                    else:
                        raise PyroBaleException(f"unknown error : {json['description'] if json['description'] else 'No description'}")

async def make_via_multipart(url: str, data: aiohttp.FormData) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            json_response = await resp.json()
            if json_response.get('ok'):
                return json_response
            else:
                error_code = json_response.get('error_code', 0)
                description = json_response.get('description', 'No description')

                if error_code == 404:
                    raise NotFoundException(f"Error not found 404 : {description}")
                elif error_code == 403:
                    raise ForbiddenException(f"Error Forbidden 403 : {description}")
                else:
                    raise PyroBaleException(f"Unknown error {error_code}: {description}")

def pythonize(dictionary: dict) -> dict:
    """Converts a dictionary with keys in snake_case to camelCase."""
    result = {}
    for key, value in dictionary.items():
        replacements = {
            "from": "from_user",
            "type": "chat_type"
        }
        if key in replacements.keys():
            key = replacements.get(key)

        result[key] = value
    return result


def sync_to_async(func: Callable) -> Callable:
    if inspect.iscoroutinefunction(func):
        return func

    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, functools.partial(func, *args, **kwargs)
        )

    return wrapper


def async_to_sync(func: Callable) -> Callable:
    if not inspect.iscoroutinefunction(func):
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise RuntimeError(
                    "Cannot call async function from running event loop. "
                    "Use await directly."
                )
        except RuntimeError:
            pass

        return asyncio.run(func(*args, **kwargs))

    return wrapper


def smart_method(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    return func(self, *args, **kwargs)
                else:
                    result = async_to_sync(func)(self, *args, **kwargs)
                    return result
            except RuntimeError:
                result = async_to_sync(func)(self, *args, **kwargs)
                return result
        else:
            return func(self, *args, **kwargs)

    return wrapper