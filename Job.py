
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from Data import JOBS_RAW


@dataclass_json
@dataclass
class Job(object):
    Name: str


JOBS = [Job.from_dict(JOBS_RAW[idElement]) for idElement in range(len(JOBS_RAW))]
