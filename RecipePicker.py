

from Resources import RECIPES, Recipe
from Job import JOBS
import Settings as SETTINGS

from random import randrange, choice


class BaseRecipePicker(object):
    def PickRecipe(self, **kwargs) -> Recipe:
        pass


class RandomRecipePicker(BaseRecipePicker):
    def __init__(self):
        pass

    def PickRecipe(self, jobID: int, **kwargs) -> Recipe:
        allowedRecipes = list(filter(lambda x: jobID in x.JobsRequired, RECIPES))
        return choice(allowedRecipes)


