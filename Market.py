from typing import List
from dataclasses import field, dataclass

from Actor import Actor
from Order import Order, OrderResult


@dataclass
class Match(object):
    Bid: Order
    Ask: Order


@dataclass
class AuctionResult(object):
    Bids: List[Order]
    Asks: List[Order]
    Matches: List[Match]
    ClearingPrice: int




@dataclass
class Market(object):
    ID: int
    Bids: List[Order] = field(default_factory=list)
    Offers: List[Order] = field(default_factory=list)
    Matches: List[Match] = field(default_factory=list)

    def AddOrder(self, order: Order):
        if order.Side:
            self.Offers.append(order)
        else:
            self.Bids.append(order)
    
    def MatchOrders(self):
        orderedBids = sorted(self.Bids, key=lambda x: x.Price)[::-1]
        orderedOffers = sorted(self.Offers, key=lambda x: x.Price)
        while (True):
            if len(orderedBids) == 0 or len(orderedOffers) == 0:
                break
            if orderedBids[0].Price > orderedOffers[0].Price:
                # we got a match
                self.Matches.append(Match(orderedBids.pop(), orderedOffers.pop()))
            else:
                break
        self.Bids = orderedBids
        self.Offers = orderedOffers

    def ComputeClearingPrice(self) -> int:
        clearingPrice = 0
        for match in self.Matches:
            clearingPrice += (match.Bid.Price + match.Ask.Price) / 2
        clearingPrice /= len(self.Matches)
        return int(clearingPrice)

    def ProcessResults(self, actorsPool: List[Actor]):
        """
            Process Results from auction: notify participants of results
        """
        pass