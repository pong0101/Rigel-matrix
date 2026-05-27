import json
import os
from datetime import datetime, timezone

MEMORY_PATH = os.path.join('memory', 'state.json')


def _ensure_memory_file():
    os.makedirs('memory', exist_ok=True)
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, 'w', encoding='utf-8') as f:
            json.dump({'history': []}, f, ensure_ascii=False, indent=2)


def load_memory():
    _ensure_memory_file()
    try:
        with open(MEMORY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'history' not in data or not isinstance(data['history'], list):
            data['history'] = []
        return data
    except Exception:
        return {'history': []}


def save_event(task, result):
    data = load_memory()
    data['history'].append({
        'time': datetime.now(timezone.utc).isoformat(),
        'task': task,
        'result': result,
    })
    data['history'] = data['history'][-50:]
    with open(MEMORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def recent_history(limit=10):
    data = load_memory()
    return data.get('history', [])[-limit:]
