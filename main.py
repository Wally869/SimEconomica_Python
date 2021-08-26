


from JobPicker import RandomJobPicker
from Factories import ActorFactory

from Settings import NB_JOBS

actorFactory = ActorFactory(rangeCapital = range(100, 1000, 10))

actors = [actorFactory.CreateNew() for i in range(10)]

