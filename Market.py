from typing import List
from dataclasses import field, dataclass

from Actor import Actor
from Order import Order, Match, OrderResult




@dataclass
class Market(object):
    ID: int
    Bids: List[Order] = field(default_factory=list)
    Offers: List[Order] = field(default_factory=list)
    Matches: List[Match] = field(default_factory=list)

    def AddOrder(self, order: Order):
        """
            Add order to registered orders depending on Order.Side (bid or offer): is a buy if false, sell if true
        """
        if order.Side:
            self.Offers.append(order)
        else:
            self.Bids.append(order)
    
    def MatchOrders(self):
        """
            Compute matches from buy and sell orders, to be used to compute clearing price. 
        """
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
        """
            Compute auction clearing price from matching orders
        """
        clearingPrice = 0
        for match in self.Matches:
            clearingPrice += (match.Bid.Price + match.Ask.Price) / 2
        clearingPrice /= len(self.Matches)
        return int(clearingPrice)

    def ProcessResults(self, clearingPrice: int, actorsPool: List[Actor]):
        """
            Process Results from auction: notify participants of results
        """
        # process matches  
        for match in self.Matches:
            actorsPool[match.Bid.CreatorID].NotifyOrderResult(OrderResult.FromMatchedOrder(self.ID, clearingPrice, match.Bid))
            actorsPool[match.Bid.CreatorID].NotifyOrderResult(OrderResult.FromMatchedOrder(self.ID, clearingPrice, match.Bid))
        for segment in [self.Bids, self.Offers]:
            for order in segment:
                actorsPool[order.CreatorID].NotifyOrderResult(OrderResult.FromRejectedOrder(self.ID, clearingPrice, order))

