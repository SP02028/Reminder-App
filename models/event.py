from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Event:
    title: str
    date: date
    start_time: str = ''
    end_time: str = ''
    location: str = ''
    ensembles: List[str] = None

    def __post_init__(self):
        if self.ensembles is None:
            self.ensembles = []
