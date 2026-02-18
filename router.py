from devices.registry import devices

def route_command(command: dict):
    intent = command["intent"]
    device_name = command.get("device")

    if intent == "UNKNOWN":
        return "I don't understand."

    if device_name not in devices:
        return "Device not found."

    device = devices[device_name]

    if intent == "TURN_ON":
        return device.turn_on()

    if intent == "TURN_OFF":
        return device.turn_off()

    return "Unhandled command."
