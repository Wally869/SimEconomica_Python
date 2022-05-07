
from Market import *  


def test_ComputeClearingPrice():
    market = Market(0)



market = Market(0)
market.AddOrder(Order(0, 0, False, 1000, 1))
market.AddOrder(Order(1, 1, False, 1100, 1))
market.AddOrder(Order(2, 2, True, 900, 2))
market.AddOrder(Order(3, 8, True, 950, 1))

market.MatchOrders()
market.ComputeClearingPrice()
