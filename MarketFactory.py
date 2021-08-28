

from Market import Market


class MarketFactory(object):
    mCurrentID: int = 0
    
    @classmethod
    def CreateNew(cls) -> Market:
        newMarket = Market(cls.mCurrentID)
        cls.mCurrentID += 1
        return newMarket

