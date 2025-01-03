from abc import ABC, abstractmethod
from typing import List

from backend.candidates.candidate import Application


class Recruiter(ABC):
    def __init__(self):
        # TODO
        pass

    @abstractmethod
    def score_applications(self, applications: List[Application]) -> float:
        # TODO
        pass
