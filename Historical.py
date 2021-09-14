


from dataclasses import dataclass

@dataclass
class Historical(object):
    BidQuantity: int
    OfferQuantity: int
    ClearingPrice: int
    ClearingQuantity: int 


