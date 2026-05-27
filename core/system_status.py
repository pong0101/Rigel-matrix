import os
import shutil
import subprocess
import time

_BOOT_TIME = time.time()


def _read_cpu_temp_c():
    path = '/sys/class/thermal/thermal_zone0/temp'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return round(int(f.read().strip()) / 1000, 1)
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
        return 'unknown'


def get_system_status():
    disk = shutil.disk_usage('/')
    disk_used = disk.total - disk.free
    return {
        'name': 'Rigel Matrix',
        'hostname': _hostname(),
        'cpu_temp_c': _read_cpu_temp_c(),
        'memory': _read_meminfo(),
        'disk': {
            'total_gb': round(disk.total / (1024 ** 3), 2),
            'used_gb': round(disk_used / (1024 ** 3), 2),
            'free_gb': round(disk.free / (1024 ** 3), 2),
            'percent': round((disk_used / disk.total) * 100, 1) if disk.total else None,
        },
        'uptime_seconds': _read_uptime_seconds(),
        'pid': os.getpid(),
    }
