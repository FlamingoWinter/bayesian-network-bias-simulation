# Backend

Python/Django backend serving the simulation engine over a REST and WebSocket API.

## Structure

### `network/`
The core abstraction. A `BayesianNetwork` defines a set of characteristics (nodes) with probability distributions and the dependencies between them. `PgmPyNetwork` is the sole implementation, wrapping [pgmpy](https://pgmpy.org/) for discrete networks.

`network/generation/` handles procedural network construction — generating a random DAG structure, assigning characteristics to nodes, and fitting conditional probability distributions. `network/predefined/` contains hand-authored networks (sprinkler, shark sightings, random seeded) used as defaults on startup. `network/naming_characteristics/` uses an LLM to generate human-readable names for generated network nodes.

### `applicants/`
Samples synthetic candidates from a Bayesian network. Produces an `Applicants` object holding characteristic values and scores for each candidate, which can be split into train/holdout/test sets for simulation.

### `recruiters/`
ML models that take applicant characteristics as input and produce a hiring decision. The abstract `Recruiter` base class defines the `train` / `predict_scores` interface. Concrete implementations in `categorical_output/` include logistic regression, random forest, SVM, shallow MLP, deep MLP, encoder-only transformer, and a Bayesian recruiter. A continuous output linear model lives in `continuous_output/`.

Each recruiter is paired with a list of `Mitigation` strategies (see below) that post-process its scores into final decisions.

### `recruiters/categorical_bias_mitigation/`
Post-training bias mitigations applied to a recruiter's score outputs. Each mitigation implements a different fairness criterion:

- **No mitigation** — raw scores thresholded uniformly
- **Demographic parity** — equalises hire rates across groups
- **Proportional parity** — hires proportionally to group representation
- **Equalised odds** — optimises for equal FPR and/or FNR across groups
- **Predictive parity** — optimises for equal FDR and/or FOR across groups

### `bias/`
Measures fairness outcomes after a simulation run. `RecruiterBiasAnalysis` collects predictions vs. actuals across test candidates and computes metrics for each mitigation. `MitigationBiasAnalysis` breaks those down by protected group. Results are serialised into response types for the API.

### `entropy/`
Computes entropy-based measures over the network and applicant distributions, used as part of the bias analysis.

### `experiments/`
Batch experiment runner used for offline research (not exposed via the API). `setup_experiment.py` orchestrates running many recruiter/mitigation/network combinations and saving results to the database.

### `api/`
Django application exposing the simulation over HTTP and WebSockets.

- **REST endpoints** (`api/views.py`) — fetch the current network, fetch bias results, apply conditioning on a node, and manage session keys.
- **WebSocket consumers** (`api/consumers/`) — long-running operations (running a full simulation, generating a random network, naming characteristics) stream progress back to the client via Django Channels.
- **Cache** (`api/cache.py`) — networks and results are stored in Django's cache layer using `dill` serialisation, keyed by session ID. Several predefined networks are pre-loaded on startup via `AppConfig.ready()`.

### `simulate.py`
The top-level simulation entry point. Takes an `Applicants` pool and a list of `Recruiter` instances, splits candidates into train/holdout/test, trains each recruiter, initialises mitigations, and returns a `RecruiterBiasAnalysis` per recruiter.
