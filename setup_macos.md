# macOS Setup

## Prerequisites

Install Miniconda (backend package manager):
```bash
brew install --cask miniconda
conda init zsh
```

Install Node and npm (frontend package manager):
```bash
brew install node
```
## Backend

Create the conda environment:
```bash
conda env create -n bayesian-network-bias-simulation --file environment_macos.yml
```

Activate the environment:
```bash
conda activate bayesian-network-bias-simulation
```

Run the development server:
```bash
python api/manage.py runserver
```

## Frontend

Install dependencies:
```bash
cd frontend/bias-sim
npm install
```

Start the development server:
```bash
npm run dev
```

> The frontend requires the backend server to be running.

## Environment Management

Export current environment:
```bash
conda env export > environment_linux.yml
```

Update local environment from file:
```bash
conda env update --file environment_linux.yml --prune
```