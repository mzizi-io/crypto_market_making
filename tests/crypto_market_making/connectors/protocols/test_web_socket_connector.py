import aiohttp, asyncio
from crypto_market_making.connectors.data_types.web_socket_data_types.ws_request import WSJSONRequest
from crypto_market_making.connectors.protocols.web_socket_connector import WSConnector

async def test_web_socket():
    async with aiohttp.ClientSession("wss://ws-api.coincheck.com") as session:
        ws_connector = WSConnector(session)
        await ws_connector.connect("/")

        requestor = WSJSONRequest(payload={"type": "subscribe", 'channel': "btc_jpy-orderbook"})
        await ws_connector.send(requestor)
        while True:
            result = await ws_connector.receive()
            print(result)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_web_socket())