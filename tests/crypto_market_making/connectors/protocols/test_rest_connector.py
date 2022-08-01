import aiohttp, asyncio
from crypto_market_making.connectors.data_types.rest_data_types.rest_request import RESTRequest
from crypto_market_making.connectors.data_types.rest_data_types.rest_method import RESTMethod
from crypto_market_making.connectors.protocols.rest_connector import RESTConnector

async def test_dydx_public_exchange():
    async with aiohttp.ClientSession(base_url="https://api.stage.dydx.exchange") as session:
        rest_connector = RESTConnector(session)

        # Build request
        request = RESTRequest(method=RESTMethod.GET, url="/v3/orderbook/BTC-USD")

        # Get all markets
        response = await rest_connector.call(request)
        print(f"DYDX Order Book Response: {response}")

        # Test contents of response
        assert response["url"] == 'https://api.stage.dydx.exchange/v3/orderbook/BTC-USD'
        assert response["method"] == 'GET'
        assert response["status"] == 200

async def test_coincheck_public_exchange():
    async with aiohttp.ClientSession(base_url="https://coincheck.com") as session:
        rest_connector = RESTConnector(session)

        # Build request
        request = RESTRequest(method=RESTMethod.GET,
                              url="/api/order_books",
                              params = {'pair': 'btc_jpy'})

        # Get all markets
        response = await rest_connector.call(request)
        print(f"COINCHECK Order Book: {response}")

        rest_connector = RESTConnector(session)

        # Build request
        request = RESTRequest(method=RESTMethod.GET,
                              url="/api/trades",
                              params = {'pair': 'btc_jpy'})

        # Get all markets
        response = await rest_connector.call(request)
        print(f"COINCHECK Trades: {response}")

        # Test contents of response
        assert response["url"] == 'https://coincheck.com/api/trades?pair=btc_jpy'
        assert response["method"] == 'GET'
        assert response["status"] == 200

async def test_rest_connector_public_api():
    result = await asyncio.gather(test_coincheck_public_exchange(), test_dydx_public_exchange(), )
    return result


async def test_rest_connector_private_api():
    async with aiohttp.ClientSession(base_url="https://api.stage.dydx.exchange") as session:
        rest_connector = RESTConnector(session)

        # Build request
        request = RESTRequest(method = RESTMethod.GET, url = "/v3/markets")

        # Get all markets
        response = await rest_connector.call(request)

        # Test contents of response
        assert response["url"] == 'https://api.stage.dydx.exchange/v3/markets'
        assert response["method"] == RESTMethod.GET
        assert response["status"] == 200

async def test_rest_connector():
    result = await asyncio.gather(test_rest_connector_public_api(), test_rest_connector_private_api())
    return result

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_rest_connector_public_api())