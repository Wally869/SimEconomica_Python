


from JobPicker import RandomJobPicker
from Factories import ActorFactory
from OrderFactory import OrderFactory
from MarketFactory import MarketFactory


from Settings import NB_JOBS

actorFactory = ActorFactory(rangeCapital = range(100, 1000, 10))

actors = [actorFactory.CreateNew() for i in range(10)]


market = MarketFactory.CreateNew()


for act in actors:
    act.GetProductionCapacity()

for act in actors:
    act.Produce(act.GetProductionCapacity())


for act in actors:
    act.GetProductionCapacity()

