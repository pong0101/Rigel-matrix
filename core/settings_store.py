import json
import os

SETTINGS_PATH = os.path.join('config', 'settings.json')
AGENTS = ['RM-CEO', 'RM-SYS', 'RM-ANL', 'RM-DEV', 'RM-MEM']
BASE_AGENT = {
    'provider': 'deepseek',
    'base_url': 'https://api.deepseek.com',
    'api_key': '',
    'model': 'deepseek-chat',
    'temperature': 0.7,
    'max_tokens': 1024,
    'timeout_seconds': 60,
}
DEFAULT_SETTINGS = {
    'system_language': 'th',
    'agent_mode': 'sequential',
    'save_history': True,
    'agents': {name: BASE_AGENT.copy() for name in AGENTS},
}


def ensure_settings_file():
    os.makedirs('config', exist_ok=True)
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)


def _migrate_old_settings(data):
    if 'agents' in data:
        return data
    old = BASE_AGENT.copy()
    for key in old:
        if key in data:
            old[key] = data[key]
    return {
        'system_language': data.get('system_language', 'th'),
        'agent_mode': data.get('agent_mode', 'sequential'),
        'save_history': data.get('save_history', True),
        'agents': {name: old.copy() for name in AGENTS},
    }


def load_settings():
    ensure_settings_file()
    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}
    data = _migrate_old_settings(data)
    merged = DEFAULT_SETTINGS.copy()
    merged.update({k: v for k, v in data.items() if k != 'agents'})
    merged['agents'] = {name: BASE_AGENT.copy() for name in AGENTS}
    for name, cfg in data.get('agents', {}).items():
        if name in merged['agents'] and isinstance(cfg, dict):
            merged['agents'][name].update(cfg)
    return merged


def save_settings(settings):
    current = load_settings()
    if 'agents' in settings:
        for name, cfg in settings['agents'].items():
            if name in current['agents'] and isinstance(cfg, dict):
                if cfg.get('api_key', '') == '':
                    cfg = cfg.copy()
                    cfg['api_key'] = current['agents'][name].get('api_key', '')
                current['agents'][name].update(cfg)
    for key in ['system_language', 'agent_mode', 'save_history']:
        if key in settings:
            current[key] = settings[key]
    os.makedirs('config', exist_ok=True)
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    return current


def public_settings():
    data = load_settings()
    public = data.copy()
    public['agents'] = {}
    for name, cfg in data['agents'].items():
        safe = cfg.copy()
        safe['api_key_set'] = bool(safe.get('api_key'))
        safe['api_key'] = ''
        public['agents'][name] = safe
    return public
