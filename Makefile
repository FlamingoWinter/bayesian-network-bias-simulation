CONDA_ENV = bayesian-network-bias-simulation
CONDA_RUN = conda run -n $(CONDA_ENV) --no-capture-output

.DEFAULT_GOAL := help

# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  Dev servers"
	@echo "    backend          Run the Django dev server"
	@echo "    frontend         Run the Vite dev server"
	@echo ""
	@echo "  Setup"
	@echo "    install          Install both backend and frontend dependencies"
	@echo "    install-backend  Create/update the conda environment"
	@echo "    install-frontend Install npm dependencies"
	@echo ""
	@echo "  Code quality"
	@echo "    lint             Check frontend formatting"
	@echo "    format           Auto-format frontend code"
	@echo "    check            Run svelte-check (type checking)"
	@echo ""
	@echo "  Environment"
	@echo "    env-export       Export conda env to environment_macos.yml"
	@echo "    env-update       Update conda env from environment_macos.yml"
	@echo ""

# ── Dev servers ───────────────────────────────────────────────────────────────

.PHONY: backend
backend:
	$(CONDA_RUN) env PYTHONPATH=$(CURDIR) python backend/api/manage.py runserver

.PHONY: frontend
frontend:
	cd frontend/bias-sim && npm run dev

# ── Setup ─────────────────────────────────────────────────────────────────────

.PHONY: install
install: install-backend install-frontend

.PHONY: install-backend
install-backend:
	conda env create -n $(CONDA_ENV) --file environment_macos.yml 2>/dev/null || \
	conda env update -n $(CONDA_ENV) --file environment_macos.yml --prune

.PHONY: install-frontend
install-frontend:
	cd frontend/bias-sim && npm install

# ── Code quality ──────────────────────────────────────────────────────────────

.PHONY: lint
lint:
	cd frontend/bias-sim && npm run lint

.PHONY: format
format:
	cd frontend/bias-sim && npm run format

.PHONY: check
check:
	cd frontend/bias-sim && npm run check

# ── Environment management ────────────────────────────────────────────────────

.PHONY: env-export
env-export:
	conda env export -n $(CONDA_ENV) > environment_macos.yml

.PHONY: env-update
env-update:
	conda env update -n $(CONDA_ENV) --file environment_macos.yml --prune
