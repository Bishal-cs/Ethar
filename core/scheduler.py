import threading
import time
from datetime import datetime
from memory.database import MemoryDB
from router import route_command


class TaskExecutor:

    def __init__(self, interval=2):
        self.memory = MemoryDB()
        self.interval = interval
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while self.running:
            now = datetime.now().isoformat()

            tasks = self.memory.get_due_tasks()

            for device, action, execute_at in tasks:
                if execute_at <= now:
                    command = {
                        "device": device,
                        "intent": action
                    }

                    route_command(command)
                    self.memory.complete_task(device, action)

            time.sleep(self.interval)