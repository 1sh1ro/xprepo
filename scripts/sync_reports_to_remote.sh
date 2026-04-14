#!/usr/bin/env bash
set -euo pipefail

# Sync local reports to a remote Linux server.
#
# Recommended:
#   1) Configure SSH key auth first.
#   2) Run this script on a schedule (cron/systemd timer).
#
# Example:
#   ./scripts/sync_reports_to_remote.sh \
#     --host 39.97.36.47 \
#     --user ubuntu \
#     --remote-dir /data/xp-reports \
#     --source /Users/my/xp/reports

HOST=""
USER_NAME=""
REMOTE_DIR=""
SOURCE_DIR="/Users/my/xp/reports"
SSH_KEY="${HOME}/.ssh/id_ed25519_xp_persist"
SSH_PORT="22"
DRY_RUN="0"

usage() {
  cat <<'EOF'
Usage:
  sync_reports_to_remote.sh --host <host> --user <user> --remote-dir <dir> [options]

Required:
  --host <host>            Remote host (e.g. 39.97.36.47)
  --user <user>            Remote SSH user
  --remote-dir <dir>       Remote target directory

Optional:
  --source <dir>           Local reports directory (default: /Users/my/xp/reports)
  --ssh-key <file>         SSH private key path (default: ~/.ssh/id_ed25519_xp_persist)
  --port <port>            SSH port (default: 22)
  --dry-run                Show what would change without writing
  -h, --help               Show help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST="${2:-}"; shift 2 ;;
    --user)
      USER_NAME="${2:-}"; shift 2 ;;
    --remote-dir)
      REMOTE_DIR="${2:-}"; shift 2 ;;
    --source)
      SOURCE_DIR="${2:-}"; shift 2 ;;
    --ssh-key)
      SSH_KEY="${2:-}"; shift 2 ;;
    --port)
      SSH_PORT="${2:-}"; shift 2 ;;
    --dry-run)
      DRY_RUN="1"; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "[error] Unknown arg: $1" >&2
      usage
      exit 1 ;;
  esac
done

if [[ -z "${HOST}" || -z "${USER_NAME}" || -z "${REMOTE_DIR}" ]]; then
  echo "[error] Missing required args." >&2
  usage
  exit 1
fi

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "[error] Source dir not found: ${SOURCE_DIR}" >&2
  exit 1
fi

if [[ ! -f "${SSH_KEY}" ]]; then
  echo "[error] SSH key not found: ${SSH_KEY}" >&2
  echo "[hint] Create one: ssh-keygen -t ed25519 -f ${SSH_KEY} -N ''" >&2
  echo "[hint] Install on server: ssh-copy-id -i ${SSH_KEY}.pub -p ${SSH_PORT} ${USER_NAME}@${HOST}" >&2
  exit 1
fi

SSH_OPTS=(
  -i "${SSH_KEY}"
  -p "${SSH_PORT}"
  -o BatchMode=yes
  -o ConnectTimeout=10
  -o StrictHostKeyChecking=accept-new
)

echo "[info] Checking remote access..."
ssh "${SSH_OPTS[@]}" "${USER_NAME}@${HOST}" "mkdir -p '${REMOTE_DIR}'" >/dev/null

echo "[info] Syncing ${SOURCE_DIR} -> ${USER_NAME}@${HOST}:${REMOTE_DIR}"
RSYNC_ARGS=(
  -az
  --delete
  --human-readable
  --itemize-changes
  -e "ssh ${SSH_OPTS[*]}"
)
if [[ "${DRY_RUN}" == "1" ]]; then
  RSYNC_ARGS+=(--dry-run)
fi

rsync "${RSYNC_ARGS[@]}" "${SOURCE_DIR}/" "${USER_NAME}@${HOST}:${REMOTE_DIR}/"
echo "[ok] Sync completed."

