import json
from pathlib import Path
from datetime import datetime
import threading

LOG_PATH = Path("memory/device_logs.json")

class DeviceLogger:
    _lock = threading.Lock()

    def __init__(self):
        LOG_PATH.parent.mkdir(exist_ok=True)
        if not LOG_PATH.exists():
            with open(LOG_PATH, "w") as f:
                json.dump([], f)

    def log(self, device_name, action, result):
        with self._lock:
            try:
                if LOG_PATH.exists():
                    with open(LOG_PATH, "r") as f:
                        content = f.read().strip()
                        logs = json.loads(content) if content else []
                else:
                    logs = []
            except Exception:
                logs = []

            logs.append({
                "timestamp": datetime.now().isoformat(),
                "device": device_name,
                "action": action,
                "result": result
            })

            with open(LOG_PATH, "w") as f:
                json.dump(logs, f, indent=4)
