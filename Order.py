from dataclasses import field, dataclass

@dataclass
class Order(object):
    """
        Order object sent from actor to market. Side is false for buy, true for sell
    """
    ID: int
    CreatorID: int
    Side: bool
    Price: int
    Quantity: int


@dataclass
class Match(object):
    Bid: Order
    Ask: Order




class BaseOrderResult(object):
    pass


class OrderResult(BaseOrderResult):
    """
        Data sent from Market to Actor, since no records of trades in actor
    """
    MarketID: int
    IsMatched: bool
    Side: bool
    Quantity: int
    OrderPrice: int
    ClearingPrice: int

    @classmethod
    def FromMatchedOrder(cls, marketID: int, clearingPrice: int, order: Order) -> "OrderResult":
        return OrderResult(marketID, True, order.Side, order.Quantity, order.Price, clearingPrice)

    @classmethod
    def FromRejectedOrder(cls, marketID: int, clearingPrice: int, order: Order) -> "OrderResult":
        return OrderResult(marketID, False, order.Side, order.Quantity, order.Price, clearingPrice)
