# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS frontend-build
WORKDIR /build/frontend/bias-sim

RUN corepack enable && corepack prepare pnpm@10.33.2 --activate

COPY frontend/bias-sim/package.json frontend/bias-sim/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/bias-sim/ ./

ARG VITE_API_URL=https://api.modelling-bias.com/
ARG VITE_WS_URL=wss://api.modelling-bias.com/ws
ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_WS_URL=${VITE_WS_URL}

RUN pnpm run build

FROM mambaorg/micromamba:1.5.10 AS backend

USER root
WORKDIR /app

COPY environment.yml /tmp/environment.yml
RUN micromamba create -y -n bayesian-network-bias-simulation -f /tmp/environment.yml \
    && micromamba clean --all --yes

COPY backend/ /app/backend/

ENV MAMBA_DOCKER_ACTIVATE=1
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=server.settings

FROM nginx:1.27-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/*

COPY --from=backend /opt/conda /opt/conda
COPY --from=backend /app /app
COPY --from=frontend-build /build/frontend/bias-sim/build /var/www/frontend

COPY deploy/nginx.conf /etc/nginx/nginx.conf
COPY deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PATH="/opt/conda/envs/bayesian-network-bias-simulation/bin:${PATH}"
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=server.settings
ENV MAMBA_ROOT_PREFIX=/opt/conda

EXPOSE 8080

ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]
