# simulation

`simulate.py` does the following:
1. `build_network/` — constructs a Bayesian network for how an applicant's characteristics may be distributed.
2. `sample_applicants.py` — represent and split a population sampled from that network.
3. `train_recruiters/` — train ML hiring models and apply bias mitigations
4. `measure_bias/` — compute fairness and prediction quality metrics
