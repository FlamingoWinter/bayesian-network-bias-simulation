# Generate Simulation
from typing import List

from backend.bias.bias import calculate_bias, print_bias_summary
from backend.candidates.candidate_generation import generate_candidates
from backend.candidates.candidate import Candidate
from backend.recruiters.recruiter import Recruiter
from backend.network.network_generation import generate_network
from backend.network.bayesian_network import BayesianNetwork

def simulate(network, candidates, recruiters):
    applications = [candidate.get_application() for candidate in candidates]
    scored_applications_by_recruiter = {recruiter: recruiter.score_applications(applications) for recruiter in recruiters}
    bias_by_recruiter = {recruiter: calculate_bias(scored_applications_by_recruiter[recruiter], candidates) for recruiter in recruiters}
    print_bias_summary(bias_by_recruiter)

if __name__ == "__main__":
    network: BayesianNetwork = generate_network()
    candidates: List[Candidate] = generate_candidates(network)
    recruiters: List[Recruiter] = [] #TODO

    simulate(network, candidates, recruiters)