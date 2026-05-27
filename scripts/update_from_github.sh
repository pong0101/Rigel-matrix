#!/usr/bin/env bash
set -Eeuo pipefail
PROJECT_DIR="${PROJECT_DIR:-/home/pi/Rigel-matrix}"
SERVICE_NAME="${SERVICE_NAME:-rigel-matrix}"
BACKUP_DIR="$HOME/.rigel/backups"
mkdir -p "$BACKUP_DIR"
cd "$PROJECT_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
[ -d ~/.rigel ] && tar -czf "$BACKUP_DIR/rigel-$STAMP.tgz" ~/.rigel >/dev/null 2>&1 || true
git fetch --all --prune
git pull --ff-only
. venv/bin/activate
pip install -r requirements.txt
./scripts/validate_runtime.sh
sudo systemctl restart "$SERVICE_NAME"
curl -fsS http://127.0.0.1:8000/status >/dev/null && echo '[rigel-update] success'
