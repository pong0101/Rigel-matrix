#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${RIGEL_APP_DIR:-/home/pi/Rigel-matrix}"
SERVICE_NAME="${RIGEL_SERVICE_NAME:-rigel-matrix}"
PORT="${RIGEL_PORT:-8000}"

warn(){ printf '[rigel-validate:warn] %s\n' "$*" >&2; }
fail(){ printf '[rigel-validate:error] %s\n' "$*" >&2; exit 1; }
need_cmd(){ command -v "$1" >/dev/null 2>&1 || { warn "missing command: $1"; return 1; }; }

echo "[rigel-validate] app dir: ${APP_DIR}"
test -d "$APP_DIR" || fail "missing app dir"
cd "$APP_DIR"

test -f requirements.txt || fail "missing requirements.txt"
test -x venv/bin/python || fail "missing venv/bin/python"

. venv/bin/activate
python -m compileall core agents hardware . >/dev/null || warn "python compile warning"

need_cmd git || true
need_cmd curl || true

test -d "$HOME/.rigel" || warn "~/.rigel missing; settings/chat memory will be created on first run"

if command -v systemctl >/dev/null 2>&1; then
  systemctl is-active "$SERVICE_NAME" >/dev/null 2>&1 || warn "$SERVICE_NAME is not active"
fi

if command -v curl >/dev/null 2>&1; then
  if ! curl -fsS "http://127.0.0.1:${PORT}/health" >/dev/null 2>&1; then
    warn "health check failed on port ${PORT}"
  fi
fi

echo "[rigel-validate] done"
