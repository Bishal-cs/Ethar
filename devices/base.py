class Device:
    def __init__(self, name):
        self.name = name
        self.state = "OFF"

    def turn_on(self):
        if self.state == "ON":
            return f"{self.name} is already ON."

        self.state = "ON"
        print(f"⚡ {self.name} is ON")
        return f"{self.name} turned ON."

    def turn_off(self):
        if self.state == "OFF":
            return f"{self.name} is already OFF."

        self.state = "OFF"
        print(f"⚡ {self.name} is OFF")
        return f"{self.name} turned OFF."

    def status(self):
        return f"{self.name} is {self.state}"
