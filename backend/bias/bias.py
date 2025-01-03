from typing import List, Dict

from backend.candidates.candidate import Candidate
from backend.recruiters.recruiter import Recruiter


def calculate_bias(scored_applications: List[float], candidates: List[Candidate]) -> float:
    # TODO - and this will have to be for different types
    pass

def print_bias_summary(bias_by_recruiter: Dict[Recruiter, float]) -> None:
    # TODO
    pass