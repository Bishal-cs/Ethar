from .base import Device

class Light(Device):
    def set_brightness(self, level):
        print(f"{self.name} brightness set to {level}")
