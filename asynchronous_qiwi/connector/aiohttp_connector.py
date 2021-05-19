import aiohttp
import asyncio
from typing import Union
from loguru import logger
from socket import gaierror
from ..data_types.connector.request_type import GET, POST, PUT, DELETE, PATCH
from ..data_types.error_codes.http_errors import http_request_errors


class Connector:

    @classmethod
    async def request(cls, url: str, headers: dict, request_type: Union[GET, POST, PUT, DELETE, PATCH],
                      timeout: float = 5.0, is_file: bool = False, is_email: bool = False, is_webhook: bool = False,
                      **kwargs) -> Union[aiohttp.ClientResponse, bytes]:
        get_response: bool = False
        timeout = aiohttp.ClientTimeout(total=timeout)
        while not get_response:
            try:
                async with aiohttp.ClientSession(headers=headers) as session:
                    response: aiohttp.ClientResponse = await session.request(method=request_type, url=url,
                                                                             timeout=timeout, **kwargs)
                    response_status: int = response.status
                    if response_status == 500:
                        if not is_webhook:
                            logger.warning("Internal Server Error (We are sleep and try again).")
                            await asyncio.sleep(5)
                            continue
                    if is_file:
                        response: bytes = await response.read()
            except BaseException as e:
                if isinstance(e, gaierror):
                    logger.warning("socket.gaierror (We are sleep and try again): " + str(e))
                    await asyncio.sleep(5)
                    continue
                if isinstance(e, aiohttp.ClientTimeout):
                    logger.warning("ClientTimeout (We are sleep and try again): " + str(e))
                    await asyncio.sleep(5)
                    continue
                if isinstance(e, aiohttp.ClientConnectorError):
                    logger.warning("ClientConnectorError (We are sleep and try again): " + str(e))
                    await asyncio.sleep(5)
                    continue
                if isinstance(e, aiohttp.ServerTimeoutError):
                    logger.warning("ServerTimeoutError (We are sleep and try again): " + str(e))
                    await asyncio.sleep(5)
                    continue
                if isinstance(e, asyncio.exceptions.TimeoutError):
                    logger.warning("TimeoutError (We are sleep and try again): " + str(e))
                    await asyncio.sleep(5)
                    continue
                if isinstance(e, BaseException):
                    logger.error("BaseException (Need handle this exception): " + str(e))
                    get_response = True
            else:
                if response_status in [200, 201, 202, 204]:
                    return response
                else:
                    get_response = True
                    if not is_email:
                        if not is_file:
                            try:
                                logger.warning("[WARNING IN CONNECTOR]: " + http_request_errors.get(response_status))
                            except TypeError:
                                logger.error("UNKNOWN ERROR IN CONNECTOR")
            finally:
                await session.close()
        raise aiohttp.ClientError
