import json
import os
from datetime import datetime, timezone

CHAT_PATH = os.path.expanduser('~/.rigel/chat_memory.json')
MAX_MESSAGES = 300


def _ensure():
    os.makedirs(os.path.dirname(CHAT_PATH), exist_ok=True)
    if not os.path.exists(CHAT_PATH):
        _write({'messages': []})


def _read():
    _ensure()
    try:
        with open(CHAT_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {'messages': []}
    if not isinstance(data, dict):
        data = {'messages': []}
    if 'messages' not in data or not isinstance(data['messages'], list):
        data['messages'] = []
    return data


def _write(data):
    os.makedirs(os.path.dirname(CHAT_PATH), exist_ok=True)
    with open(CHAT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_chat():
    return _read()


def recent_messages(limit=80):
    data = _read()
    return data['messages'][-limit:]


def append_chat(role, content, agent=None, kind='message'):
    data = _read()
    item = {
        'ts': datetime.now(timezone.utc).isoformat(),
        'role': role,
        'content': str(content),
        'kind': kind,
    }
    if agent:
        item['agent'] = agent
    data['messages'].append(item)
    data['messages'] = data['messages'][-MAX_MESSAGES:]
    _write(data)
    return data['messages']


def clear_chat():
    _write({'messages': []})
    return []
