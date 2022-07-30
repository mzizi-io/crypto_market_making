import pyximport
pyximport.install()
from crypto_market_making.core.events.events import LimitOrderStatus
from crypto_market_making.core.data_types.limit_order import LimitOrder

# Test functioning of limit order
def test_limit_order():
    limit_order = LimitOrder(client_order_id="100000",
                 trading_pair="USD/BTC",
                 is_buy=True,
                 base_currency="USD",
                 quote_currency="USD",
                 price=22000.0,
                 quantity=100.0,
                 filled_quantity=10.0,
                 creation_timestamp=1,
                 status=LimitOrderStatus.FAILED)

    print(limit_order)
    print(limit_order.order_age_from_creation())


if __name__ == '__main__':
    test_limit_order()