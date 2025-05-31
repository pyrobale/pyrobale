from ..exceptions import *
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


def pythonize(dictionary: dict) -> dict:
    """Converts a dictionary with keys in snake_case to camelCase."""
    result = {}
    for key, value in dictionary.items():
        if key == "from":
            key = "from_user"
        result[key] = value
    return result
