# this is a simple router that takes a command and routes it to the appropriate handler based on the intent
def route(command: dict):
    intent = command["intent"]

    # based on the intent, we can route to the appropriate handler
    if intent == "LIGHT_ON":
        print("💡 Light is ON")
        return "Light turned on."

    if intent == "LIGHT_OFF":
        print("💡 Light is OFF")
        return "Light turned off."

    return "I don't understand."
