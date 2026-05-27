#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${RIGEL_APP_DIR:-/home/pi/Rigel-matrix}"
SERVICE_USER="${RIGEL_SERVICE_USER:-pi}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
REPO_URL="${REPO_URL:-https://github.com/pong0101/Rigel-matrix.git}"
BRANCH="${BRANCH:-main}"
INSTALL_SYSTEM_PACKAGES="${INSTALL_SYSTEM_PACKAGES:-true}"

echo "[rigel-bootstrap] app dir: ${APP_DIR}"

if [ "$INSTALL_SYSTEM_PACKAGES" = "true" ]; then
  sudo apt update
  sudo apt install -y git python3 python3-venv python3-pip curl
fi

if [ ! -d "${APP_DIR}" ]; then
  echo "[rigel-bootstrap] cloning ${REPO_URL} (${BRANCH})"
  mkdir -p "$(dirname "${APP_DIR}")"
  git clone --branch "${BRANCH}" "${REPO_URL}" "${APP_DIR}"
fi

cd "${APP_DIR}"
if [ ! -f requirements.txt ]; then
  echo "[rigel-bootstrap:error] requirements.txt not found in ${APP_DIR}" >&2
  exit 1
fi

mkdir -p scripts ~/.rigel
chmod +x scripts/*.sh || true

if [ ! -d "venv" ]; then
  "${PYTHON_BIN}" -m venv venv
fi

. venv/bin/activate
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt

sudo chown -R "${SERVICE_USER}:${SERVICE_USER}" "${APP_DIR}"

python -m compileall core agents hardware . >/dev/null || true

if [ -f rigel-matrix.service ]; then
  sudo cp rigel-matrix.service /etc/systemd/system/rigel-matrix.service
  sudo systemctl daemon-reload
  sudo systemctl enable rigel-matrix
fi

if [ -x scripts/validate_runtime.sh ]; then
  RIGEL_APP_DIR="${APP_DIR}" scripts/validate_runtime.sh || true
fi

echo "[rigel-bootstrap] done"
