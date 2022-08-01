from libccp.set cimport set
from libccp.vector cimport vector
from libcpp.stdint cimport int64_t
from libccp.algorithm cimport sort as stdsort

import pyximport
pyximport.install()
from crypto_market_making.core.data_types.order_book_entry import OrderBookEntry

cdef class OrderBook:
    cdef vector[OrderBookEntry] _bid_book
    cdef vector[OrderBookEntry] _ask_book
    cdef int64_t _snapshot_uid
    cdef int64_t _last_diff_uid
    cdef double _best_bid
    cdef double _best_ask
    cdef double _last_trade_price
    cdef double _last_applied_trade
    cdef double _last_trade_price_rest_updated

    def __init__(self)
        self._snapshot_uid = 0
        self._last_diff_uid = 0
        self._best_bid = self._best_ask = float("NaN")
        self._last_trade_price = float("NaN")
        self._last_applied_trade = -1000.0
        self._last_trade_price_rest_updated = -1000

    cdef fill_order_book_from_vector_entries(self, vector[OrderBookEntry] bids, vector[OrderBookEntry] asks, int64_t update_id):
        '''
            Fill the order book from a vector of bids and asks. Entries are sorted by their price.

            The comparison function is defined in OrderBookEntry

            :param bids: vector containing most recent bids
            :param asks: vector containing most recent asks
            :param update_id: identifier for each update
        '''
        self._bid_book = stdsort(bids.begin(), bids.end())
        self._ask_book = stdsort(asks.begin(), asks.end())

        # Get best bid and ask prices
        self._best_bid = self._bid_book.end()
        self._best_ask = self._ask_book.end()

    cdef fill_order_book_from_list_entries(self, List[OrderBookEntry] bids, List[OrderBookEntry] asks, int64_t update_id):
        '''
            Fill the order book from a vector of bids and asks. Entries are sorted by their price.

            The comparison function is defined in OrderBookEntry

            :param bids: vector containing most recent bids
            :param asks: vector containing most recent asks
            :param update_id: identifier for each update
        '''
        cdef:
            vector[OrderBookEntry] ccp_bids
            vector[OrderBookEntry] ccp_asks

        for entry in bids:
            ccp_bids.push_back(entry)

        for entry in asks:
            ccp_asks.push_back(entry)

        self._bid_book = stdsort(ccp_bids.begin(), bids.end())
        self._ask_book = stdsort(ccp_asks.begin(), asks.end())

    def __repr__(self):

