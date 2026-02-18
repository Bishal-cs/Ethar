from devices.registry import devices


def route_command(command: dict) -> str:
    intent = command.get("intent")
    device_name = command.get("device")

    if intent == "NONE":
        return "Unhandled command."

    if device_name not in devices:
        return "Device not found."

    device = devices[device_name]

    if intent == "TURN_ON":
        return device.turn_on()

    elif intent == "TURN_OFF":
        return device.turn_off()

    elif intent == "STATUS":
        return device.status()

    return "Unhandled command."
