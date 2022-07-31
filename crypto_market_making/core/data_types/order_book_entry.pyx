# distutils: language=c++

cdef class OrderBookEntry:
    '''
    This class is a generic entry in the order book. The only pertinent variables are the price, amount and update_id
    '''
    cdef double price
    cdef double amount
    cdef str update_id

    def __init__(self, price:double, amount:double, update_id:str):
        self.price = price
        self.amount = amount
        self.update_id = update_id

    @property
    def price(self) -> double:
        return self.price

    @property
    def amount(self) -> double:
        return self.amount

    @property
    def update_id(self) -> str:
        return self.update_id

    # Compare the prices of order book entries
    def __gt__(self, OrderBookEntry other):
        '''
        Compare the prices of order book entries using their prices.
        '''
        cdef bint result
        result = False
        if self.price > other.price:
            result = True

        return result

    # Compare the prices of order book entries
    def __lt__(self, OrderBookEntry other):
        '''
        Compare the prices of order book entries using their prices.
        '''
        cdef bint result
        result = False
        if self.price < other.price:
            result = True

        return result

    def __repr__(self):
        return (f"OrderBookEntry(price={self.price}, amount={self.amount}, update_id='{self.update_id}'))")