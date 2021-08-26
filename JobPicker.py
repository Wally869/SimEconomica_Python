

from Job import JOBS
from Resources import RECIPES
import Settings as SETTINGS

from random import randrange


class BaseJobPicker(object):
    def PickJob(self, **kwargs) -> int:
        pass


class RandomJobPicker(BaseJobPicker):
    def __init__(self):
        self.mJobsRange = range(len(JOBS))
    
    def PickJob(self, **kwargs) -> int:
        return randrange(self.mJobsRange.start, self.mJobsRange.stop)

