#!/usr/bin/env bash
# Install Caddy on the droplet and install deploy/Caddyfile (reads deploy/deploy.env).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${DEPLOY_ENV:-${SCRIPT_DIR}/deploy.env}"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "${ENV_FILE}"

: "${DROPLET_HOST:?Set DROPLET_HOST in ${ENV_FILE}}"
: "${DROPLET_USER:?Set DROPLET_USER in ${ENV_FILE}}"

SSH_TARGET="${DROPLET_USER}@${DROPLET_HOST}"

scp "${SCRIPT_DIR}/Caddyfile" "${SSH_TARGET}:/tmp/Caddyfile.bias-sim"

ssh "${SSH_TARGET}" bash -s <<'REMOTE'
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

if ! command -v docker >/dev/null 2>&1; then
  echo "Install Docker first (curl -fsSL https://get.docker.com | sh)" >&2
  exit 1
fi

apt-get update
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl

if [[ ! -f /usr/share/keyrings/caddy-stable-archive-keyring.gpg ]]; then
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' \
    | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
    | tee /etc/apt/sources.list.d/caddy-stable.list
  apt-get update
fi

apt-get install -y caddy

install -m 644 /tmp/Caddyfile.bias-sim /etc/caddy/Caddyfile
rm -f /tmp/Caddyfile.bias-sim

systemctl enable caddy
systemctl reload caddy || systemctl restart caddy

echo "Caddy status:"
systemctl --no-pager status caddy | head -5
echo ""
echo "Ensure DigitalOcean DNS A record for @ points to this server's public IP."
echo "Test locally: curl -s -o /dev/null -w '%{http_code}\n' -H 'Host: api.modelling-bias.com' http://127.0.0.1:8080/csrf/"
REMOTE

echo "==> Caddy installed on ${SSH_TARGET}. After DNS A → droplet IP, try https://modelling-bias.com"
