# Rigel Matrix

**Rigel Matrix** is a lightweight multi-agent AI company starter project designed for Raspberry Pi Zero 2 W first, while keeping the hardware layer portable for future Raspberry Pi / mini PC upgrades.

## What it does in v1

- Runs a small multi-agent workflow in the terminal
- Uses cloud AI API instead of heavy local models
- Stores simple project memory in JSON
- Detects hardware profile through a configurable adapter layer
- Includes a tiny dashboard placeholder that can run later with FastAPI

## Agents

- **RM-CEO**: breaks down tasks and summarizes decisions
- **RM-ENG**: helps with code, ESP32, Raspberry Pi, and engineering tasks
- **RM-ANL**: analyzes logs and errors
- **RM-DSN**: suggests simple UI / dashboard improvements
- **RM-MEM**: keeps lightweight memory notes

## Target hardware

Recommended first device:

- Raspberry Pi Zero 2 W
- Raspberry Pi OS Lite
- Python 3.11+

Future upgrade targets:

- Raspberry Pi 4
- Raspberry Pi 5
- Mini PC / Linux server

## Install on Raspberry Pi

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip

git clone https://github.com/pong0101/Rigel-matrix.git
cd Rigel-matrix

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
nano .env
```

Put your API key in `.env`.

## Run

```bash
python main.py
```

Type a task, for example:

```text
วิเคราะห์ error ESP32 compile failed
```

Exit with:

```text
exit
```

## Design rule

Keep it light for Pi Zero 2 W:

- No local LLM in v1
- No heavy frontend framework
- No vector database yet
- One agent call at a time by default

## Project structure

```text
Rigel-matrix/
├── agents/
├── config/
├── core/
├── dashboard/
├── hardware/
├── memory/
├── main.py
├── requirements.txt
└── README.md
```
