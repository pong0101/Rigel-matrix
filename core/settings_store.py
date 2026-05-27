import json
import os

SETTINGS_PATH = os.path.join('config', 'settings.json')
DEFAULT_SETTINGS = {
    'provider': 'deepseek',
    'base_url': 'https://api.deepseek.com',
    'api_key': '',
    'model': 'deepseek-chat',
    'temperature': 0.7,
    'max_tokens': 1024,
    'timeout_seconds': 60,
    'system_language': 'th',
    'agent_mode': 'sequential',
    'save_history': True,
}


def ensure_settings_file():
    os.makedirs('config', exist_ok=True)
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)


def load_settings():
    ensure_settings_file()
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
    merged = DEFAULT_SETTINGS.copy()
    merged.update(data)
    return merged


def save_settings(settings):
    os.makedirs('config', exist_ok=True)
    merged = DEFAULT_SETTINGS.copy()
    merged.update(settings)
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    return merged


def public_settings():
    data = load_settings()
    data['api_key_set'] = bool(data.get('api_key'))
    data['api_key'] = ''
    return data
