from typing import Dict

from backend.bias.recruiter_bias_analysis import RecruiterBiasAnalysis
from backend.recruiters.recruiter import Recruiter


def print_bias_summary(bias_by_recruiter: Dict[Recruiter, RecruiterBiasAnalysis]) -> None:
    print("-----------------------")
    print("Bias Summary")
    print("-----------------------")

    for recruiter, recruiter_bias_measurement in bias_by_recruiter.items():
        print(f"{recruiter.name}:")
        recruiter_bias_measurement.print_summary()
        print("--------------------------------------------------------------------------------------------------")
    pass

    print("")
