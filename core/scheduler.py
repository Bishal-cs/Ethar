import threading
import time

class Scheduler:
    def schedule(self, delay_seconds, action, *args):
        def task():
            time.sleep(delay_seconds)
            action(*args)

        thread = threading.Thread(target=task)
        thread.daemon = True
        thread.start()
