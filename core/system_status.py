import os
import shutil
import socket
import subprocess
import time

_BOOT_TIME = time.time()


def _read_first(path, default=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return default


def _read_cpu_temp_c():
    raw = _read_first('/sys/class/thermal/thermal_zone0/temp')
    try:
        return round(int(raw) / 1000, 1)
    except Exception:
        return None


def _read_meminfo():
    info = {}
    try:
        with open('/proc/meminfo', 'r', encoding='utf-8') as f:
            for line in f:
                key, value = line.split(':', 1)
                info[key] = int(value.strip().split()[0])
    except Exception:
        return None
    total = info.get('MemTotal', 0)
    available = info.get('MemAvailable', 0)
    used = max(total - available, 0)
    percent = round((used / total) * 100, 1) if total else None
    return {
        'total_mb': round(total / 1024, 1),
        'used_mb': round(used / 1024, 1),
        'available_mb': round(available / 1024, 1),
        'percent': percent,
    }


def _read_uptime_seconds():
    try:
        with open('/proc/uptime', 'r', encoding='utf-8') as f:
            return int(float(f.read().split()[0]))
    except Exception:
        return int(time.time() - _BOOT_TIME)


def _hostname():
    try:
        return subprocess.check_output(['hostname'], text=True).strip()
    except Exception:
        return socket.gethostname() or 'unknown'


def _ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return 'unknown'


def _cpu_load():
    try:
        one, five, fifteen = os.getloadavg()
        cores = os.cpu_count() or 1
        return {
            'load_1m': round(one, 2),
            'load_5m': round(five, 2),
            'load_15m': round(fifteen, 2),
            'cores': cores,
            'percent_estimate': round(min((one / cores) * 100, 100), 1),
        }
    except Exception:
        return None


def _board_model():
    model = _read_first('/proc/device-tree/model') or _read_first('/sys/firmware/devicetree/base/model')
    if model:
        return model.replace('\x00', '').strip()
    return 'unknown'


def _throttled():
    try:
        out = subprocess.check_output(['vcgencmd', 'get_throttled'], text=True, timeout=2).strip()
        return out
    except Exception:
        return 'unavailable'


def _service_state():
    try:
        out = subprocess.check_output(['systemctl', 'is-active', 'rigel-matrix'], text=True, timeout=2).strip()
        return out
    except Exception:
        return 'unknown'


def get_system_status():
    disk = shutil.disk_usage('/')
    disk_used = disk.total - disk.free
    return {
        'name': 'Rigel Matrix',
        'board': {
            'model': _board_model(),
            'hostname': _hostname(),
            'ip': _ip_address(),
            'cpu_temp_c': _read_cpu_temp_c(),
            'throttled': _throttled(),
        },
        'service': {
            'name': 'rigel-matrix',
            'state': _service_state(),
            'pid': os.getpid(),
        },
        'cpu': _cpu_load(),
        'memory': _read_meminfo(),
        'disk': {
            'total_gb': round(disk.total / (1024 ** 3), 2),
            'used_gb': round(disk_used / (1024 ** 3), 2),
            'free_gb': round(disk.free / (1024 ** 3), 2),
            'percent': round((disk_used / disk.total) * 100, 1) if disk.total else None,
        },
        'uptime_seconds': _read_uptime_seconds(),
        'timestamp': int(time.time()),
    }
