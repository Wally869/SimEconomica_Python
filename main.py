from typing import List


## Systems
from Actor import Actor
from Market import Market



## Factories
from JobPicker import RandomJobPicker
from Factories import ActorFactory
from OrderFactory import OrderFactory
from MarketFactory import MarketFactory

## Data
from Resources import RESOURCES

## Utils  
from random import random, randrange, choice
from tqdm import tqdm



SIZE_ACTOR_POOL = 100

NB_ROUNDS = 10

# def Main():
# Create markets
MarketFactory.Reset()

markets = [MarketFactory.CreateNew() for i in range(len(RESOURCES))]
# Create ActorFactory and Actors
actorFactory = ActorFactory(rangeCapital = range(100, 1000, 10))
actors = [actorFactory.CreateNew() for i in range(SIZE_ACTOR_POOL)]


#print(actors)

# memalloc
qtt = 0
for idRound in tqdm(range(10)): # NB_ROUNDS):
    for act in actors:
        qtt = act.GetProductionCapacity()
        act.Produce(qtt)
    for act in actors:
        for elem in act.mCurrentRecipe.Inputs:
            qtt = act.mInventory.GetFreeSpace(elem.ResourceID)
            price = randrange(9, 12)
            qtt = min(qtt, max(int(act.mCapital / price), 0))
            #print(qtt * price > act.mCapital)
            #print(qtt)
            #print()
            if qtt > 0:
                act.PostOrder_SingleMarket(act.CreateOrder(False, qtt, price), markets[elem.ResourceID])
        for elem in act.mCurrentRecipe.Outputs:
            qtt = act.mInventory.GetStock(elem.ResourceID)
            if qtt > 0:
                act.PostOrder_SingleMarket(act.CreateOrder(True, qtt, randrange(8, 11)), markets[elem.ResourceID])
    for idMarket in range(len(markets)):
        markets[idMarket].MatchOrders()
        clearingPrice = markets[idMarket].ComputeClearingPrice()
        print(clearingPrice)
        markets[idMarket].ProcessResults(clearingPrice, actors)
    for idActor in range(len(actors)):
        actors[idActor].ProcessOrderResults()
        actors[idActor].ClearTempData()
    for idMarket in range(len(markets)):
        markets[idMarket].ClearTempData()

    print()

print(actors)


'''
class Simulation(object):
    def __init__(self):
        self.mActors: List[Actor]
        self.mActorFactory: ActorFactory = ActorFactory(rangeCapital = range(100, 1000, 10))
        self.mMarkets: List[Market] = []
        self.mPriceHistory: List[List[int]] = []
        
    def Initialize(self):
        self.mActors = [self.mActorFactory.CreateNew() for i in range(SIZE_ACTOR_POOL)]
        self.mMarkets = [MarketFactory.CreateNew() for i in range(len(RESOURCES))]

    def PrepMarkets(self):
        """
            Function executed at each step to clear intermediary data from markets.
        """
        for currMarket in self.mMarkets:
            currMarket.ClearTempData()

    def PrepActors(self):
        """
            Clear intermediary data for actors
        """
        for currActor in self.mActors:
            currActor.ClearTempData()
    
    def Run(self, nbRounds: int):
        for idRound in tqdm(range(nbRounds)):
            # define production capacity of actors
            # then create orders
            # process on markets
            # update state of actors
            # check for bankruptcies
            # go next round
            pass
'''


"""
actorFactory = ActorFactory(rangeCapital = range(100, 1000, 10))

actors = [actorFactory.CreateNew() for i in range(10)]


market = MarketFactory.CreateNew()


for act in actors:
    act.GetProductionCapacity()

for act in actors:
    act.Produce(act.GetProductionCapacity())


for act in actors:
    act.GetProductionCapacity()
"""
