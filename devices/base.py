from memory.database import save_device_state, load_device_state


class Device:
    def __init__(self, name):
        self.name = name

        # Load saved state from DB
        saved_state = load_device_state(self.name)
        self.state = saved_state if saved_state else "OFF"

    def turn_on(self):
        if self.state == "ON":
            return f"{self.name} is already ON."

        self.state = "ON"
        save_device_state(self.name, self.state)

        print(f"⚡ {self.name} is ON")
        return f"{self.name} turned ON."

    def turn_off(self):
        if self.state == "OFF":
            return f"{self.name} is already OFF."

        self.state = "OFF"
        save_device_state(self.name, self.state)

        print(f"⚡ {self.name} is OFF")
        return f"{self.name} turned OFF."

    def status(self):
        return f"{self.name} is {self.state}"
