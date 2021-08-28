
from Order import Order


class OrderFactory(object):
    mCurrentID: int = 0
    
    @classmethod
    def CreateNew(cls, idCreator: int, side: bool, quantity: int, price: int) -> Order:
        order = Order(ID=cls.mCurrentID, CreatorID=idCreator, Side=side, Price=price, Quantity=quantity)
        cls.mCurrentID += 1
        return order
