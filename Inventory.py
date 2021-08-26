

from dataclasses import dataclass 

from Settings import NB_RESOURCES, INVENTORY_CAPACITY


@dataclass
class InventorySlot(object):
    Stock: int
    Capacity: int 
    def GetFillRate(self) -> float:
        return self.Stock / self.Capacity
    @property
    def FillRate(self) -> float:
        return self.GetFillRate()
    def __sub__(self, value: int) -> int:
        return self.Stock - value
    def __add__(self, value: int) -> int:
        return self.Stock + value
    def Add(self, value: int):
        self.Stock = self + value
    def Sub(self, value: int):
        self.Stock = self - value
    


class Inventory(object):
    def __init__(self):
        self.mSlots = [InventorySlot(0, INVENTORY_CAPACITY) for _ in range(NB_RESOURCES)]
    def __getitem__(self, key: int) -> InventorySlot:
        return self.mSlots[key]
    def GetStock(self, key: int) -> int:
        return self.mSlots[key].Stock
    def GetCapacity(self, key: int) -> int:
        return self.mSlots[key].Capacity
    def GetFillRate(self, key: int) -> int:
        return self.mSlots[key].FillRate


