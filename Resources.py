from typing import List, Tuple

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from Data import RESOURCES_RAW, RECIPES_RAW

class BaseResource(object):
    pass


@dataclass_json
@dataclass
class Resource(BaseResource):
    Name: str


@dataclass_json
@dataclass
class Ingredient(object):
    ResourceID: int
    Quantity: int


@dataclass_json
@dataclass
class Recipe(object):
    Name: str
    JobsRequired: List[int]
    Inputs: List[Ingredient]
    Outputs: List[Ingredient]



RESOURCES = [Resource.from_dict(RESOURCES_RAW[idElement]) for idElement in range(len(RESOURCES_RAW))]
RECIPES = [
    Recipe(
        Name=RECIPES_RAW[idElement]["Name"],
        JobsRequired=RECIPES_RAW[idElement]["JobsRequired"],
        Inputs=[
            Ingredient(
                ResourceID=data[0],
                Quantity=data[1]
            ) for data in RECIPES_RAW[idElement]["Inputs"]
        ],
        Outputs=[
            Ingredient(
                ResourceID=data[0],
                Quantity=data[1]
            ) for data in RECIPES_RAW[idElement]["Outputs"]
        ]
    ) for idElement in range(len(RECIPES_RAW))
]

