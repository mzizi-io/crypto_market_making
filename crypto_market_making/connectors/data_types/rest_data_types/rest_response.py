import aiohttp
from dataclasses import dataclass
from typing import Mapping, Optional, Any

from crypto_market_making.connectors.data_types.rest_data_types.rest_method import RESTMethod

@dataclass(init=False)
class RESTResponse:
    '''
    Convert aiohttp.ClientResponse into a data class.

    Class contains the following fields.
        - url: url of the API Call
        - method: REST Method (GET, POST etc)
        - status: 200 for success
        - headers:
        - json: Return data from API call
        - text: Return text from API call
    '''
    url: str
    method: RESTMethod
    status: int
    headers: Optional[Mapping[str, str]]

    def __init__(self, aiohttp_response: aiohttp.ClientResponse):
        self._aiohttp_response = aiohttp_response

    @property
    def url(self) -> str:
        url_str = str(self._aiohttp_response.url)
        return url_str

    @property
    def method(self) -> RESTMethod:
        method_ = RESTMethod[self._aiohttp_response.method.upper()]
        return method_

    @property
    def status(self) -> int:
        status_ = int(self._aiohttp_response.status)
        return status_

    @property
    def headers(self) -> Optional[Mapping[str, str]]:
        headers_ = self._aiohttp_response.headers
        return headers_

    async def json(self) -> Any:
        json_ = await self._aiohttp_response.json()
        return json_

    async def text(self) -> str:
        text_ = await self._aiohttp_response.text()
        return text_

    async def read(self) -> Any:
        data_ = await self._aiohttp_response.read()
        return data_
