#!/usr/bin/env bash
# Exits non-zero (and says why) if the live frontend or backend is down.
# Run daily by .github/workflows/healthcheck.yml; also runnable locally.
set -uo pipefail

FRONTEND_URL="${FRONTEND_URL:-https://modelling-bias.com/}"
BACKEND_URL="${BACKEND_URL:-https://api.modelling-bias.com/csrf/}"

failed=0

# check <name> <url> <text the body must contain>
# Checks the body, not just the status: the frontend returns 200 for every path.
check() {
  local name="$1" url="$2" expected_text="$3"
  local body_file code
  body_file="$(mktemp)"
  code="$(curl -s -o "${body_file}" -w '%{http_code}' --max-time 20 \
    --retry 3 --retry-delay 5 --retry-all-errors "${url}")" || code="000"

  if [[ "${code}" == "200" ]] && grep -q "${expected_text}" "${body_file}"; then
    echo "OK    ${name} (${url})"
  else
    echo "FAIL  ${name} (${url}) -> HTTP ${code}, expected body containing '${expected_text}'"
    failed=1
  fi
  rm -f "${body_file}"
}

check "frontend" "${FRONTEND_URL}" "<html"
check "backend"  "${BACKEND_URL}"  '"token"'

exit "${failed}"
