from devices.registry import devices

def interpret(text: str):
    text = text.lower()

    for device_name in devices.keys():
        if device_name in text:
            if "on" in text:
                return {"intent": "TURN_ON", "device": device_name}
            if "off" in text:
                return {"intent": "TURN_OFF", "device": device_name}

    return {"intent": "UNKNOWN"}
