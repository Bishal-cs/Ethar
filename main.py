from interpreter import interpret
from router import route
from dotenv import dotenv_values

env_val = dotenv_values()
User = env_val.get("User_Name")

while True:
    user_input = input(f"\n{User}: ")
    parsed = interpret(user_input)
    response = route(parsed)
    print("Ethar:", response)