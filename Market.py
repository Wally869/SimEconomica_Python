from typing import List

from dataclasses import dataclass

@dataclass
class Order(object):
    ID: int
    CreatorID: int
    Side: bool
    Price: int
    Quantity: int


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
    Bids: List[Order]
    Offers: List[Order]
    Matches: List[Match]

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

    def ComputeClearingPrice(self) -> int:
        clearingPrice = 0
        for match in self.Matches:
            clearingPrice += (match.Bid.Price + match.Ask.Price) / 2
        return int(clearingPrice)


