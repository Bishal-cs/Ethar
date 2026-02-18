from .base import Device

class Fan(Device):
    def set_speed(self, speed):
        print(f"{self.name} speed set to {speed}")
