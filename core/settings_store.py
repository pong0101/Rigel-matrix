import json
import os

# Store user secrets outside the git repository so API keys survive git pull/re-clone.
SETTINGS_DIR = os.path.expanduser('~/.rigel')
SETTINGS_PATH = os.path.join(SETTINGS_DIR, 'settings.json')
LEGACY_SETTINGS_PATH = os.path.join('config', 'settings.json')
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


def _read_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass


def ensure_settings_file():
    os.makedirs(SETTINGS_DIR, exist_ok=True)
    if not os.path.exists(SETTINGS_PATH):
        legacy = _read_json(LEGACY_SETTINGS_PATH)
        if legacy:
            _write_json(SETTINGS_PATH, _migrate_old_settings(legacy))
        else:
            _write_json(SETTINGS_PATH, DEFAULT_SETTINGS)


def _migrate_old_settings(data):
    if not isinstance(data, dict):
        return DEFAULT_SETTINGS.copy()
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
    data = _read_json(SETTINGS_PATH) or {}
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
                cfg = cfg.copy()
                # Empty API key means keep the old saved key.
                if cfg.get('api_key', '') == '':
                    cfg['api_key'] = current['agents'][name].get('api_key', '')
                current['agents'][name].update(cfg)
    for key in ['system_language', 'agent_mode', 'save_history']:
        if key in settings:
            current[key] = settings[key]
    _write_json(SETTINGS_PATH, current)
    return public_settings()


def public_settings():
    data = load_settings()
    public = data.copy()
    public['settings_path'] = SETTINGS_PATH
    public['agents'] = {}
    for name, cfg in data['agents'].items():
        safe = cfg.copy()
        safe['api_key_set'] = bool(safe.get('api_key'))
        safe['api_key'] = ''
        public['agents'][name] = safe
    return public
