# distutils: language=c++
import time

import pyximport
pyximport.install()

from crypto_market_making.core.events.events import LimitOrderStatus

cdef class LimitOrder:
    '''
        This class contains information on limit orders and is used to feed strategies.

        This data is obtained from or sent to the connectors i.e. the collection of limit orders in the blotter can be obtained and can also be added on to.
    '''
    cdef str client_order_id
    cdef str trading_pair
    cdef bint is_buy
    cdef str base_currency
    cdef str quote_currency
    cdef double price
    cdef double quantity
    cdef double filled_quantity
    cdef int creation_timestamp
    cdef int status

    def __init__(self,
                 client_order_id: str,
                 trading_pair: str,
                 is_buy: bint,
                 base_currency: str,
                 quote_currency: str,
                 price: double,
                 quantity: double,
                 filled_quantity: double = 0.0,
                 creation_timestamp: int = 0,
                 status: LimitOrderStatus = LimitOrderStatus.UNKNOWN):
        self.client_order_id = client_order_id
        self.trading_pair = trading_pair
        self.is_buy = is_buy
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.price = self.price
        self.quantity = quantity
        self.filled_quantity = filled_quantity
        self.creation_timestamp = creation_timestamp
        self.status = status

    @property
    def client_order_id(self) -> str:
        return self.client_order_id

    @property
    def trading_pair(self) -> str:
        return self.trading_pair

    @property
    def is_buy(self) -> bint:
        return self.is_buy

    @property
    def base_currency(self) -> str:
        return self.base_currency

    @property
    def quote_currency(self) -> str:
        return self.quote_currency

    @property
    def price(self) -> double:
        return self.price

    @property
    def quantity(self) -> double:
        return self.quantity

    @property
    def filled_quantity(self) -> double:
        return self.filled_quantity

    @property
    def creation_timestamp(self) -> int:
        return self.creation_timestamp

    @property
    def status(self) -> LimitOrderStatus:
        return self.status

    cpdef long long order_age_till_end_timestamp(self, long long end_timestamp):
        """
        Calculates and returns age of the order since it was created til end_timestamp in seconds
        :param end_timestamp: The end timestamp
        :return: The age of the order in seconds
        """
        cdef long long start_timestamp = 0

        if start_timestamp < end_timestamp:
            start_timestamp = self.creation_timestamp
            return end_timestamp - start_timestamp
        else:
            return -1

    cpdef long long order_age_from_creation(self):
        """
        Calculates and returns age of the order since it was created till current moment
        """
        return self.order_age_till_end_timestamp(int(time.time()))

    def __repr__(self) -> str:
        return (f"LimitOrder(client_order_id='{self.client_order_id}', trading_pair='{self.trading_pair}', is_buy={self.is_buy},"
                f"base_currency='{self.base_currency}', quote_currency='{self.quote_currency}', "
                f"price={self.price}, quantity={self.quantity}, filled_quantity={self.filled_quantity}, "
                f"creation_timestamp={self.creation_timestamp})")