from typing import List
from dataclasses import field, dataclass

from Actor import Actor
from Order import Order, Match, OrderResult
from Historical import Historical

from Interfaces import IClearable, IMarket


@dataclass
class Market(IMarket, IClearable):
    ID: int
    Bids: List[Order] = field(default_factory=list)
    Offers: List[Order] = field(default_factory=list)
    Matches: List[Match] = field(default_factory=list)
    Historicals: List[Historical] = field(default_factory=list)

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
        if (len(self.Matches) == 0):
            return 0
        
        else:
            clearingPrice = 0
            for match in self.Matches:
                clearingPrice += (match.Bid.Price + match.Ask.Price) / 2
            clearingPrice /= len(self.Matches)
            return int(clearingPrice)

    def RecordHistorical(self, clearingPrice: int):
        """
            Record historical data on quantity bid and offer as well as matches and clearing price for a given round.  
        """
        summedBidQuantity = 0
        for i in range(len(self.Bids)):
            summedBidQuantity += self.Bids[i].Quantity

        summedOfferQuantity = 0
        for i in range(len(self.Offers)):
            summedOfferQuantity += self.Offers[i].Quantity

        summedMatchedQuantity = 0
        for i in range(len(self.Matches)):
            summedMatchedQuantity += self.Matches[i].Quantity

        summedBidQuantity += summedMatchedQuantity
        summedOfferQuantity += summedMatchedQuantity

        self.Historicals.append(Historical(summedBidQuantity, summedOfferQuantity, clearingPrice, summedMatchedQuantity))

    def ComputeHistoricalPrice(self, sizeWindow: int) -> int:
        """
            From historicals, compute a mean price for a given window. 
        """
        temp = []
        for historical in self.Historicals[-sizeWindow:]:
            if historical.ClearingPrice != -1:
                temp.append(historical.ClearingPrice)
        if len(temp) != 0:
            return int(sum(temp) / len(temp))
        else:
            return 0

    def ProcessResults(self, clearingPrice: int, actorsPool: List[Actor]):
        """
            Process Results from auction: notify participants of results
        """
        self.RecordHistorical(clearingPrice)
        # process matches  
        for match in self.Matches:
            actorsPool[match.Bid.CreatorID].NotifyOrderResult(OrderResult.FromMatchedOrder(self.ID, clearingPrice, match.Bid))
            actorsPool[match.Ask.CreatorID].NotifyOrderResult(OrderResult.FromMatchedOrder(self.ID, clearingPrice, match.Ask))
        for segment in [self.Bids, self.Offers]:
            for order in segment:
                actorsPool[order.CreatorID].NotifyOrderResult(OrderResult.FromRejectedOrder(self.ID, clearingPrice, order))

    def ClearTempData(self):
        self.Bids = []
        self.Offers = []
        self.Matches = []
