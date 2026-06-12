#!/usr/bin/env bash
# Build image, push to GHCR, SSH to droplet, replace running container.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${DEPLOY_ENV:-${SCRIPT_DIR}/deploy.env}"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}. Copy deploy/deploy.env.example to deploy/deploy.env and edit it." >&2
  exit 1
fi

# Docker Desktop (macOS) installs the CLI here; add it if the app is installed but shell PATH is stale.
if ! command -v docker >/dev/null 2>&1; then
  for docker_bin in \
    /usr/local/bin/docker \
    /Applications/Docker.app/Contents/Resources/bin/docker; do
    if [[ -x "${docker_bin}" ]]; then
      export PATH="$(dirname "${docker_bin}"):${PATH}"
      break
    fi
  done
fi
if ! command -v docker >/dev/null 2>&1; then
  echo "docker: command not found. Install Docker Desktop (https://www.docker.com/products/docker-desktop/), start it, then retry." >&2
  echo "On the droplet you also need Docker: https://docs.docker.com/engine/install/ubuntu/" >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo "Docker is installed but the daemon is not running. Open Docker Desktop and wait until it is ready, then retry." >&2
  exit 1
fi

# shellcheck disable=SC1090
source "${ENV_FILE}"

required_vars=(
  GITHUB_USER
  GITHUB_TOKEN
  IMAGE_NAME
  DROPLET_HOST
  DROPLET_USER
  CONTAINER_NAME
)
for var in "${required_vars[@]}"; do
  if [[ -z "${!var:-}" ]]; then
    echo "Set ${var} in ${ENV_FILE}" >&2
    exit 1
  fi
done

IMAGE_TAG="${IMAGE_TAG:-latest}"
GITHUB_USER_LC="$(echo "${GITHUB_USER}" | tr '[:upper:]' '[:lower:]')"
REGISTRY_IMAGE="ghcr.io/${GITHUB_USER_LC}/${IMAGE_NAME}:${IMAGE_TAG}"
PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"

build_args=()
if [[ -n "${VITE_API_URL:-}" ]]; then
  build_args+=(--build-arg "VITE_API_URL=${VITE_API_URL}")
fi
if [[ -n "${VITE_WS_URL:-}" ]]; then
  build_args+=(--build-arg "VITE_WS_URL=${VITE_WS_URL}")
fi

echo "==> Building ${REGISTRY_IMAGE} (${PLATFORM})"
docker build \
  --platform "${PLATFORM}" \
  "${build_args[@]}" \
  -t "${REGISTRY_IMAGE}" \
  "${ROOT_DIR}"

echo "==> Logging in to ghcr.io"
echo "${GITHUB_TOKEN}" | docker login ghcr.io -u "${GITHUB_USER_LC}" --password-stdin

echo "==> Pushing ${REGISTRY_IMAGE}"
docker push "${REGISTRY_IMAGE}"

SSH_TARGET="${DROPLET_USER}@${DROPLET_HOST}"
REMOTE_PORT="${CONTAINER_PORT:-8080}"

echo "==> Deploying on ${SSH_TARGET}"
ssh "${SSH_TARGET}" bash -s <<EOF
set -euo pipefail
if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed on this host. On Ubuntu, run once as root:" >&2
  echo "  curl -fsSL https://get.docker.com | sh" >&2
  echo "  systemctl enable --now docker" >&2
  exit 127
fi
echo "${GITHUB_TOKEN}" | docker login ghcr.io -u "${GITHUB_USER_LC}" --password-stdin

docker pull "${REGISTRY_IMAGE}"

if docker ps -a --format '{{.Names}}' | grep -qx '${CONTAINER_NAME}'; then
  docker rm -f '${CONTAINER_NAME}'
fi

# Remove other stopped containers from previous deploys of this image (optional cleanup).
docker image prune -f >/dev/null 2>&1 || true

docker run -d \\
  --name '${CONTAINER_NAME}' \\
  --restart unless-stopped \\
  -p 127.0.0.1:${REMOTE_PORT}:8080 \\
  -e DJANGO_SECRET_KEY='${DJANGO_SECRET_KEY}' \\
  -e DJANGO_DEBUG='${DJANGO_DEBUG:-false}' \\
  -e DJANGO_ALLOWED_HOSTS='${DJANGO_ALLOWED_HOSTS:-api.modelling-bias.com,localhost}' \\
  -e DJANGO_DB_PATH=/data/db.sqlite3 \\
  -v bias-sim-data:/data \\
  '${REGISTRY_IMAGE}'

docker ps --filter name='^${CONTAINER_NAME}\$'
EOF

echo "==> Done. App listening on ${DROPLET_HOST}:${REMOTE_PORT} (map 80/443 with Caddy or nginx + Let's Encrypt on the host)."
