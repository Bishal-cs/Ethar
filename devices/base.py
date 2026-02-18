from memory.database import MemoryDB


class Device:
    def __init__(self, name):
        self.name = name
        self.memory = MemoryDB()

        stored_state = self.memory.load_device_state(self.name)
        self.state = stored_state if stored_state else "OFF"

    def turn_on(self):
        if self.state == "ON":
            return f"{self.name} is already ON."

        self.state = "ON"
        self.memory.save_device_state(self.name, self.state)
        print(f"⚡ {self.name} is ON")
        return f"{self.name} turned ON."

    def turn_off(self):
        if self.state == "OFF":
            return f"{self.name} is already OFF."

        self.state = "OFF"
        self.memory.save_device_state(self.name, self.state)
        print(f"⚡ {self.name} is OFF")
        return f"{self.name} turned OFF."

    def status(self):
        return f"{self.name} is {self.state}."
