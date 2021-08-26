

from Actor import Actor
from JobPicker import BaseJobPicker, RandomJobPicker
from RecipePicker import BaseRecipePicker, RandomRecipePicker

import Settings as SETTINGS

from random import randrange

class BaseFactory(object):
    def __init__(self, prototypeConstructor: object, isCountable: bool = True):
        self.mPrototypeConstructor = prototypeConstructor
        self.bIsCountable = True
        self.mCurrentID = 0
    
    def CreateNew(self) -> object:
        newObject = self.mPrototypeConstructor()
        if (self.bIsCountable):
            newObject.ID = self.mCurrentID
        return newObject


class ActorFactory(object):
    def __init__(self, jobPicker: BaseJobPicker = RandomJobPicker(), recipePicker: BaseRecipePicker = RandomRecipePicker(), rangeCapital: range = range(100, 1000, 10)):
        self.kJobPicker = jobPicker
        self.kRecipePicker = recipePicker
        self.kRangeCapital = rangeCapital
        self.mCurrentID = 0
    
    def CreateNew(self) -> Actor:
        idJob = self.kJobPicker.PickJob()
        recipe = self.kRecipePicker.PickRecipe(jobID=idJob)
        newActor = Actor(self.mCurrentID, idJob, randrange(self.kRangeCapital.start, self.kRangeCapital.stop), recipe)
        self.mCurrentID += 1
        return newActor

    def Redraw(self, actor: Actor) -> Actor:
        idJob = self.kJobPicker.PickJob()
        recipe = self.kRecipePicker.PickRecipe(JobID=idJob)
        return Actor(actor.mCurrentID, idJob, randrange(self.kRangeCapital.start, self.kRangeCapital.stop), recipe)



