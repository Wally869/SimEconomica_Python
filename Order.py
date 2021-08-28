from dataclasses import field, dataclass

@dataclass
class Order(object):
    ID: int
    CreatorID: int
    Side: bool
    Price: int
    Quantity: int



class BaseOrderResult(object):
    pass


class OrderResult(BaseOrderResult):
    MarketID: int
    IsMatched: bool
    Side: bool
    Quantity: int
    ClearingPrice: int

