from typing import List
from dataclasses import dataclass

# Systems
from Inventory import Inventory
from Order import Order, OrderResult
from OrderFactory import OrderFactory

# Data
from Resources import Recipe, Resource
from Resources import RESOURCES, RECIPES
from Job import JOBS

# Interfaces 
from Interfaces import IClearable


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
        self._mOrderResults: List[OrderResult] = list()

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
                if temp < capacity:
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

    def CreateOrder(self, side: bool, quantity: int, price: int) -> Order:
        return OrderFactory.CreateNew(self.kID, side, quantity, price)
        #return Order(OrderFactory.ID, self.kID, side, price, quantity)

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

    def ClearTempData(self):
        """
            Clear _mOrderResults
        """
        self._mOrderResults = []

