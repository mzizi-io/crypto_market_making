import pyximport

pyximport.install()
from crypto_market_making.core.data_types.order_book_entry import OrderBookEntry

# Test functioning of limit order
def test_order_book_entry():
    entry_1 = OrderBookEntry(price = 100.0,
                                      amount = 10.0,
                                      update_id = "0000001")

    entry_2 = OrderBookEntry(price = 120.0,
                                      amount = 10.0,
                                      update_id = "0000001")

    # Compare order entries
    assert entry_1 < entry_2
    assert entry_2 > entry_1

if __name__ == '__main__':
    test_order_book_entry()