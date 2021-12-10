from typing import List
from dataclasses import dataclass

# Systems
from Inventory import Inventory
from Order import Order, OrderResult, ActorOrderRecord, WaitingOrder
from OrderFactory import OrderFactory

# Data
from Resources import Recipe, Resource
from Resources import RESOURCES, RECIPES
from Job import JOBS

# Interfaces 
from Interfaces import IClearable, IMarket


class BaseActor(object):
    pass


class Actor(BaseActor, IClearable):
    def __init__(self, id: int, job: int, capital: int, recipe: Recipe):
        self.kID: int = id
        self.mJob: int = job
        self.mCapital: int = capital
        self.mAvailableCapital: int = capital
        self.mInventory: Inventory = Inventory()
        self.mCurrentRecipe: Recipe = recipe
        self.mWaitingOrders: List[WaitingOrder] = list()
        self._mOrderResults: List[OrderResult] = list()
        self.mOrderRecords: List[ActorOrderRecord] = list()

    def __str__(self):
        return JOBS[self.mJob].Name + " - " + self.mCurrentRecipe.Name + " - Capital: " + str(self.mCapital)

    def __repr__(self):
        return str(self)

    def GetProductionCapacity(self) -> int:
        """
            Check current recipe and current state of inventory to compute max number of units that can be produced.
        """
        capacity = 0
        if len(self.mCurrentRecipe.Inputs) > 0:
            for ingredient in self.mCurrentRecipe.Inputs:
                temp = self.mInventory[ingredient.ResourceID].Stock / ingredient.Quantity
                if temp < capacity or capacity == 0:
                    capacity = temp
        else:
            resourceID = self.mCurrentRecipe.Outputs[0].ResourceID
            capacity = int((self.mInventory[resourceID].GetCapacity() - self.mInventory[resourceID].GetStock()) / self.mCurrentRecipe.Outputs[0].Quantity)
        return int(capacity)

    def Produce(self, quantityToProduce: int):
        """
            Adjust state according to what resources are needed for current recipe, its outputs and a given quantity to produce.  
            This function is unsafe, and GetProductionCapacity must be called to ensure quantityToProduce is valid, and inventory quantities does not go negative
        """
        for ingredient in self.mCurrentRecipe.Inputs:
            self.mInventory[ingredient.ResourceID].Sub(ingredient.Quantity * quantityToProduce)
        for ingredient in self.mCurrentRecipe.Outputs:
            self.mInventory[ingredient.ResourceID].Add(ingredient.Quantity * quantityToProduce)

    def DeterminePurchaseQuantity(self, idProduct: int, market: IMarket):
        """
            Determine how much to bid for for current recipe
        """
        pass

    def CreateOrder(self, side: bool, quantity: int, price: int) -> Order:
        return OrderFactory.CreateNew(self.kID, side, quantity, price)
        #return Order(OrderFactory.ID, self.kID, side, price, quantity)

    def PrepareOrders(self):
        """
            Prepare bids and offers according to current state of inventory and capital available
        """
        tempOrder = OrderFactory.CreateNew(self.kID, True, 4, 11)
        self.mWaitingOrders.append(WaitingOrder(self.mCurrentRecipe.Outputs[0].ResourceID, tempOrder))

    def PostOrder(self, order: Order, marketID: int, markets: List[IMarket]):
        self.PostOrder_SingleMarket(order, markets[marketID])

    def PostOrder_SingleMarket(self, order: Order, market: IMarket):
        self.mAvailableCapital -= order.Quantity * order.Price
        market.AddOrder(order)
        self.mOrderRecords.append(ActorOrderRecord(order.Side, order.Price, order.Quantity))

    def NotifyOrderResult(self, orderResult: OrderResult): 
        """
            Called by a market to notify the actor of the result of one of its orders. 
            Takes an OrderResult instance as argument and appends it to _mOrderResults
        """
        self._mOrderResults.append(orderResult)

    def ProcessOrderResults(self):
        """
            Adjust inventory according to matched bids and offers on markets, and set data to compute adjustments to price belief.
        """
        # only process successful orders for now
        for order in self._mOrderResults:
            if (order.IsMatched):
                if (not order.Side):
                    self.mInventory[order.MarketID].Add(order.Quantity)
                    self.mCapital -= order.Quantity * order.ClearingPrice
                else:
                    self.mInventory[order.MarketID].Sub(order.Quantity)
                    self.mCapital += order.Quantity * order.ClearingPrice

    def AdjustPriceBeliefs(self):
        """
            Adjust price beliefs according to quantity matched and price given
        """
        # need to recompose stuff
        marketIDs = set()
        for order in self._mOrderResults:
            marketIDs.add(order.MarketID)
        marketIDs = list(marketIDs)

    def ClearTempData(self):
        """
            Clear order results, order records and set available capital back to capital
        """
        self._mOrderResults = []
        self.mOrderRecords = []
        self.mAvailableCapital = self.mCapital
