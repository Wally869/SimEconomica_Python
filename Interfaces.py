
from Order import Order

class IClearable(object):
    """
        Interface related to clearing data in between rounds, and resetting elements
    """
    def ClearStateData(self, **kwargs):
        pass

    def ClearTempData(self):
        pass


class IMarket(object):
    """
        Interface for basic market functions: add order, clearing c
    """
    def AddOrder(self, order: Order):
        pass
