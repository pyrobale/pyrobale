from ..exceptions import *

import asyncio
import inspect
from functools import wraps
import functools
from typing import Any, Callable, Union, TypeVar, Awaitable, overload
import aiohttp


def pythonize(dictionary: dict) -> dict:
    """Converts a dictionary with keys in snake_case to camelCase."""
    result = {}
    for key, value in dictionary.items():
        replacements = {
            "from": "from_user"
        }
        if key in replacements.keys():
            key = replacements.get(key)

        result[key] = value
    return result

# F = TypeVar('F', bound=Callable[..., Any])

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


def async_to_sync(func: Callable[..., Awaitable[Any]]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise RuntimeError("Cannot call async function from running event loop.")
        except RuntimeError:
            pass
        return asyncio.run(func(*args, **kwargs))
    return wrapper

@overload
def smart_method(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]: ...
@overload
def smart_method(func: Callable[..., Any]) -> Callable[..., Any]: ...

def smart_method(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if inspect.iscoroutinefunction(func):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    return func(*args, **kwargs)
                else:
                    return async_to_sync(func)(*args, **kwargs)
            except RuntimeError:
                return async_to_sync(func)(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return wrapper