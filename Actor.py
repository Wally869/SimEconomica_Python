from typing import List
from dataclasses import dataclass

# Systems
from Inventory import Inventory
from Order import Order, OrderResult

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
        capacity = 0
        for ingredient in self.mCurrentRecipe.Inputs:
            temp = self.mInventory[ingredient.ResourceID] / ingredient.Quantity
            if temp < capacity:
                capacity = temp
        return int(capacity)

    def Produce(self, quantityToProduce: int):
        for ingredient in self.mCurrentRecipe.Inputs:
            self.mInventory[ingredient.ResourceID].Sub(ingredient.Quantity * quantityToProduce)
        for ingredient in self.mCurrentRecipe.Outputs:
            self.mInventory[ingredient.ResourceID].Add(ingredient.Quantity * quantityToProduce)

    def CreateOrder(self, side: bool, quantity: int, price: int) -> Order:
        return Order(0, self.kID, side, price, quantity)

    def NotifyOrderResult(self, orderResult: OrderResult): 
        self._mOrderResults.append(orderResult)

    def ProcessOrderResults(self):
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
        self._mOrderResults = []

