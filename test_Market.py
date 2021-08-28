
from Market import *  


def test_ComputeClearingPrice():
    market = Market(0)



market = Market(0)
market.AddOrder(Order(0, 0, False, 10, 1))
market.AddOrder(Order(1, 1, False, 11, 1))
market.AddOrder(Order(2, 2, True, 9, 1))
market.AddOrder(Order(3, 8, True, 10, 1))

market.MatchOrders()
market.ComputeClearingPrice()
