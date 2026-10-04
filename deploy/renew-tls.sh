#!/usr/bin/env bash
# Wipe Caddy's cert/account storage on the droplet and re-issue Let's Encrypt certs.
# Use after a DNS/firewall fix or after Caddy has been stuck serving its internal CA.
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

install -m 644 /tmp/Caddyfile.bias-sim /etc/caddy/Caddyfile
rm -f /tmp/Caddyfile.bias-sim

caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile

echo "==> Stopping caddy"
systemctl stop caddy

echo "==> Removing stale cert + ACME account storage so Caddy re-issues from Let's Encrypt"
rm -rf /var/lib/caddy/.local/share/caddy/certificates \
       /var/lib/caddy/.local/share/caddy/acme \
       /var/lib/caddy/.config/caddy

echo "==> Starting caddy (this triggers fresh ACME orders)"
systemctl start caddy
sleep 5

echo "==> Caddy status:"
systemctl --no-pager status caddy | head -10

echo "==> Last 60 log lines:"
journalctl -u caddy --no-pager -n 60
REMOTE

echo "==> Done. Re-run 'task diagnose-tls' in ~30s to confirm issuer = 'Let's Encrypt'."
