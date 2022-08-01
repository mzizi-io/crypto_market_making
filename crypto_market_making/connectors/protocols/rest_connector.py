import aiohttp
from typing import Dict
from crypto_market_making.connectors.data_types.rest_data_types.rest_request import RESTRequest
from crypto_market_making.connectors.data_types.rest_data_types.rest_response import RESTResponse


class RESTConnector:
    '''
    This class contains all REST-related logic
    '''

    def __init__(self, aiohttp_client_session: aiohttp.ClientSession):
        self._client_session = aiohttp_client_session

    async def call(self, request: RESTRequest) -> Dict:
        '''
        Perform asynchronous API call using aiohttp
        :param request: request namedtuple object containing request parameters
        :return: response: response namedtuple containing http response
        '''
        aiohttp_response = await self._client_session.request(method=request.method.value,
                                                 url=request.url,
                                                 params=request.params,
                                                 data=request.data,
                                                 headers=request.headers)

        # Return JSON from values
        response_json: Dict = await aiohttp_response.json()

        # Add properties of response to final json value
        response_json['url']: str = aiohttp_response.url.__str__()
        response_json['headers']: Dict = dict(aiohttp_response.headers)
        response_json['status']: str = aiohttp_response.status
        response_json['method']: str = aiohttp_response.method

        return response_json

    async def _build_response(self, aiohttp_response: aiohttp.ClientResponse) -> RESTResponse:
        response = RESTResponse(aiohttp_response)
        return response
