# the function is use to interpret the text and return the meaning of the text
def interpret(text: str):
    # convert the text to lower case
    text = text.lower()

    # check if the the text contains the word...
    if "turn on the light" in text:
        return {"intent": "LIGHT_ON"}
    
    if "turn off the light" in text:
        return {"intent": "LIGHT_OFF"}
    
    return {"intent": "UNKNOWN"}
    

