from typing import List
from dataclasses import dataclass

# Systems
from Market import Order
from Inventory import Inventory


# Data
from Resources import Recipe, Resource
from Resources import RESOURCES, RECIPES
from Job import JOBS



class Actor(object):
    def __init__(self, id: int, job: int, capital: int, recipe: Recipe):
        self.kID: int = id
        self.mJob: int = job
        self.mCapital: int = capital
        self.mAvailableCapital: int = capital
        self.mInventory: Inventory = Inventory()
        self.mCurrentRecipe: Recipe = recipe

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

    def CreateOrder(self) -> Order:
        pass


