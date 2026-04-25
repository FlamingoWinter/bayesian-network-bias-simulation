# Frontend

SvelteKit application providing two modes: an interactive network visualisation, and a guided walkthrough.

## Structure

### `src/routes/`
SvelteKit file-based routing. Three top-level sections:

- **`/visualisation`** — the main interactive tool. Renders the Bayesian network as a force-directed graph, lets users condition on node values, trigger simulations, and view bias results.
- **`/walkthrough`** — a step-by-step guided tour through a single simulation run, explaining each stage as it happens.

### `src/components/`

**`characteristic/`** — the main building block of the visualisation. Each node in the network expands into a `CharacteristicConfig` panel showing its probability distribution and allowing the user to condition on it. Distributions are rendered as SVG charts: `CategoricalDistribution`, `ContinuousDistribution`, and `DiscreteDistribution`, each with custom axes.

**`modals/`** — overlay panels for key interactions:
- `NewNetworkModal` — configure and generate a new random Bayesian network
- `NameNetworkModal` — trigger LLM-based naming of network characteristics
- `SimulateModal` — configure and run a simulation
- `ShowBiasModal` — display bias results broken down by recruiter and mitigation, including summaries for demographic parity, equalised odds, and predictive parity

**`animations/`** — `RecruiterAnimation` and `DecisionTree` provide visual explanations of how recruiters process applicants, used in the walkthrough.

**`menu/`** — side drawer navigation and utility buttons. Separate drawer layouts for the visualisation, walkthrough, and guide modes.

**`loading/`** — loading states for long-running WebSocket operations.

**`popups/`** — `InfoHover` tooltips and floating info panels used throughout.

### `src/stores/`
Global Svelte state in `store.ts`: the active network, D3 force simulation instance, session key, conditioning state, posterior distributions, and bias analysis results. `functions.ts` contains store-level logic for interacting with the API.

### `src/utilities/`
- `api.ts` — HTTP calls to the Django REST endpoints
- `socket.ts` — WebSocket helpers (`awaitSocketOpen`, `awaitSocketClose`) used for streaming simulation progress
- `toTitleCase.ts` — formatting utility

### `src/types/`
TypeScript type definitions for the network structure (`network.ts`), bias analysis results (`Bias.ts`), and probability types (`ProbabilityType.ts`).

### `src/animation/`
D3-based animation primitives: force simulation layout (`forceSimulation.ts`), zoom behaviour (`zoom.ts`), transitions (`transition.ts`), and the top-level `animate.ts` that coordinates the graph rendering.
