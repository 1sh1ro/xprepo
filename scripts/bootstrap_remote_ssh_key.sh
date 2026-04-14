#!/usr/bin/env bash
set -euo pipefail

# Bootstrap SSH key auth for remote report persistence.
#
# This script is intentionally interactive (password prompt via ssh-copy-id).
#
# Example:
#   ./scripts/bootstrap_remote_ssh_key.sh \
#     --host 39.97.36.47 \
#     --user ubuntu

HOST=""
USER_NAME=""
SSH_KEY="${HOME}/.ssh/id_ed25519_xp_persist"
SSH_PORT="22"

usage() {
  cat <<'EOF'
Usage:
  bootstrap_remote_ssh_key.sh --host <host> --user <user> [options]

Required:
  --host <host>          Remote host
  --user <user>          Remote SSH user

Optional:
  --ssh-key <file>       Key path (default: ~/.ssh/id_ed25519_xp_persist)
  --port <port>          SSH port (default: 22)
  -h, --help             Show help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST="${2:-}"; shift 2 ;;
    --user)
      USER_NAME="${2:-}"; shift 2 ;;
    --ssh-key)
      SSH_KEY="${2:-}"; shift 2 ;;
    --port)
      SSH_PORT="${2:-}"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "[error] Unknown arg: $1" >&2
      usage
      exit 1 ;;
  esac
done

if [[ -z "${HOST}" || -z "${USER_NAME}" ]]; then
  echo "[error] Missing required args." >&2
  usage
  exit 1
fi

if [[ ! -f "${SSH_KEY}" ]]; then
  echo "[info] Creating SSH key: ${SSH_KEY}"
  mkdir -p "$(dirname "${SSH_KEY}")"
  ssh-keygen -t ed25519 -f "${SSH_KEY}" -N ""
fi

echo "[info] Installing public key with ssh-copy-id..."
ssh-copy-id -i "${SSH_KEY}.pub" -p "${SSH_PORT}" "${USER_NAME}@${HOST}"

echo "[info] Verifying key login..."
ssh -i "${SSH_KEY}" -p "${SSH_PORT}" -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "${USER_NAME}@${HOST}" "echo ok"
echo "[ok] SSH key auth is ready."

