import pyximport

pyximport.install()
from crypto_market_making.core.data_types.order_book_entry import OrderBookEntry
from crypto_market_making.core.data_types.order_book import OrderBook

# Test functioning of limit order
def test_order_book():
    entry_1 = OrderBookEntry(price = 100.0,
                                      amount = 10.0,
                                      update_id = "0000001")

    entry_2 = OrderBookEntry(price = 120.0,
                                      amount = 10.0,
                                      update_id = "0000001")

    entry_3 = OrderBookEntry(price = 100.0,
                                      amount = 10.0,
                                      update_id = "0000001")

    entry_4 = OrderBookEntry(price = 100.0,
                                      amount = 10.0,
                                      update_id = "0000001")

    bids = [entry_1, entry_2]
    asks = [entry_2, entry_3, entry_4]
    update_id = 1

    order_book = OrderBook()
    order_book.fill_order_book_from_list_entries(bids, asks, update_id)


if __name__ == '__main__':
    test_order_book()
