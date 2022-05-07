from dataclasses import dataclass

# from Settings import NB_RESOURCES, INVENTORY_CAPACITY

from Settings import INVENTORY_CAPACITY
from Resources import RESOURCES


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

    def GetCapacity(self) -> int:
        return self.Capacity

    def GetStock(self) -> int:
        return self.Stock

    def GetFreeSpace(self) -> int:
        return self.Capacity - self.Stock


class Inventory(object):
    def __init__(self):
        self.mSlots = [
            InventorySlot(0, INVENTORY_CAPACITY) for _ in range(len(RESOURCES))
        ]

    def __str__(self) -> str:
        output = "<Inventory -"
        for elem in self.mSlots:
            output += " "
            output += str(elem.Stock)
        return output + ">"

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key: int) -> InventorySlot:
        print(key)
        return self.mSlots[key]

    def GetStock(self, key: int) -> int:
        return self.mSlots[key].Stock

    def GetCapacity(self, key: int) -> int:
        return self.mSlots[key].Capacity

    def GetFillRate(self, key: int) -> float:
        return self.mSlots[key].FillRate

    def GetFreeSpace(self, key: int) -> int:
        return self.mSlots[key].GetFreeSpace()
