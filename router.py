from devices.registry import devices

def route_command(command):
    device_name = command.get("device")
    intent = command.get("intent")

    if device_name not in devices:
        return "Device not found."

    device = devices[device_name]

    if intent == "TURN_ON":
        return device.turn_on()
    elif intent == "TURN_OFF":
        return device.turn_off()
    else:
        return "Unhandled command."
