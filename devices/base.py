from memory.database import MemoryDB
from core.device_logger import DeviceLogger

memory = MemoryDB()

class Device:
    def __init__(self, name):
        self.name = name
        self.state = memory.load_device_state(name) or "OFF"
        self.logger = DeviceLogger()

    def turn_on(self):
        if self.state == "ON":
            return f"{self.name} is already ON."
        self.state = "ON"
        memory.save_device_state(self.name, self.state)
        result = f"{self.name} turned ON."
        print(f"⚡ {self.name} is ON")
        self.logger.log(self.name, "TURN_ON", result)
        return result

    def turn_off(self):
        if self.state == "OFF":
            return f"{self.name} is already OFF."
        self.state = "OFF"
        memory.save_device_state(self.name, self.state)
        result = f"{self.name} turned OFF."
        print(f"⚡ {self.name} is OFF")
        self.logger.log(self.name, "TURN_OFF", result)
        return result
