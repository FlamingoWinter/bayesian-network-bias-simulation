# Setup

Development on macOS is preferred. If developing on another platform, consult
`docs/setup_linux.md` or `docs/setup_windows.md`.

## Prerequisites

Install Miniconda (backend package manager):
```bash
brew install --cask miniconda
conda init zsh
```

Install Taskfile (task runner):
```bash
brew install go-task
```

Install Node and npm (frontend package manager):
```bash
brew install node
```

## Install dependencies

```bash
task install
```

This creates the conda environment from `environment.yml` and installs frontend npm packages.

## Run

```bash
task backend   # Django dev server
task frontend  # Vite dev server
```

> The frontend requires the backend server to be running.

## Adding or changing dependencies

Edit `environment.yml`, then:

```bash
task install-backend
```
