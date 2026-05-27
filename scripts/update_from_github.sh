#!/usr/bin/env bash
set -Eeuo pipefail

export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"

PROJECT_DIR="${PROJECT_DIR:-/home/pi/Rigel-matrix}"
BACKUP_DIR="${HOME:-/home/pi}/.rigel/backups"
mkdir -p "$BACKUP_DIR"
cd "$PROJECT_DIR"

STAMP="$(date +%Y%m%d-%H%M%S)"
if [ -d "${HOME:-/home/pi}/.rigel" ]; then
  tar -czf "$BACKUP_DIR/rigel-$STAMP.tgz" "${HOME:-/home/pi}/.rigel" >/dev/null 2>&1 || true
fi

git fetch --all --prune
git pull --ff-only
. venv/bin/activate
python -m pip install -r requirements.txt
./scripts/validate_runtime.sh
curl -fsS http://127.0.0.1:8000/health >/dev/null && echo '[rigel-update] success; restart service if needed'
