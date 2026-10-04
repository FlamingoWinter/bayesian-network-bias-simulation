#!/usr/bin/env bash
# SSH to the droplet and report exactly why TLS is unhealthy.
# Reads deploy/deploy.env for DROPLET_HOST / DROPLET_USER.
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

ssh "${SSH_TARGET}" bash -s <<'REMOTE'
set -uo pipefail

hr() { printf '\n=== %s ===\n' "$*"; }

hr "Caddy service status"
systemctl --no-pager status caddy | head -20 || true

hr "Caddy version + validate"
caddy version || true
caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile || true

hr "Active Caddyfile on droplet"
cat /etc/caddy/Caddyfile

hr "Listening sockets on :80, :443, :8080 (no filter regex)"
ss -ltnp 2>/dev/null | grep -E '(:80|:443|:8080)( |\b)' || echo "(nothing listening on those ports)"

hr "ufw / firewall"
ufw status 2>/dev/null || echo "ufw not installed"
iptables -S INPUT 2>/dev/null | head -20 || true

hr "Public IPv4 + IPv6 of this droplet"
echo "v4: $(curl -s -4 -m 5 https://api.ipify.org || echo '(none)')"
echo "v6: $(curl -s -6 -m 5 https://api64.ipify.org || echo '(none)')"

hr "Docker / app backend (Caddy proxies to 127.0.0.1:8080)"
docker ps --filter "name=bias-sim" --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || echo "(docker not installed?)"
echo "--- last 30 lines of bias-sim container logs ---"
docker logs --tail=30 bias-sim 2>&1 | sed 's/^/  /' || echo "(no such container)"

PUBLIC_V4="$(curl -s -4 -m 5 https://api.ipify.org)"
PUBLIC_V6="$(curl -s -6 -m 5 https://api64.ipify.org)"

for host in modelling-bias.com www.modelling-bias.com api.modelling-bias.com; do
  hr "DNS for ${host} (Cloudflare 1.1.1.1)"
  echo "A:    $(dig +short A    "${host}" @1.1.1.1 | tr '\n' ' ')"
  echo "AAAA: $(dig +short AAAA "${host}" @1.1.1.1 | tr '\n' ' ')"

  hr "Cert via 127.0.0.1 (loopback — what Caddy itself answers) for ${host}"
  echo | timeout 8 openssl s_client -servername "${host}" -connect 127.0.0.1:443 2>/dev/null \
    | openssl x509 -noout -issuer -subject -dates 2>/dev/null \
    || echo "(no TLS handshake on 127.0.0.1:443 for SNI ${host})"

  if [[ -n "${PUBLIC_V4}" ]]; then
    hr "Cert via public IPv4 ${PUBLIC_V4} for ${host} (what off-box IPv4 clients see)"
    echo | timeout 8 openssl s_client -4 -servername "${host}" -connect "${PUBLIC_V4}:443" 2>/dev/null \
      | openssl x509 -noout -issuer -subject -dates 2>/dev/null \
      || echo "(no TLS handshake on ${PUBLIC_V4}:443)"
  fi

  if [[ -n "${PUBLIC_V6}" ]]; then
    hr "Cert via public IPv6 [${PUBLIC_V6}] for ${host} (what off-box IPv6 clients see)"
    echo | timeout 8 openssl s_client -6 -servername "${host}" -connect "[${PUBLIC_V6}]:443" 2>/dev/null \
      | openssl x509 -noout -issuer -subject -dates 2>/dev/null \
      || echo "(no TLS handshake on [${PUBLIC_V6}]:443)"
  fi
done

hr "Recent Caddy errors / ACME activity (last 200 lines)"
journalctl -u caddy --no-pager -n 200 \
  | grep -E -i 'error|acme|challenge|certificate|obtain|renew|tls' \
  | tail -80 || true

hr "Files in Caddy's data dir (cert storage)"
find /var/lib/caddy/.local/share/caddy/certificates -maxdepth 4 -type f 2>/dev/null \
  | head -40 || echo "(no certs dir yet)"

hr "Done"
REMOTE
