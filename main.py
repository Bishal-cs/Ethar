from interpreter import interpret
from router import route

print("Ethar is running... Type 'exit' to stop.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Shutting down Ethar...")
        break

    parsed = interpret(user_input)
    response = route(parsed)
    print("Ethar:", response)
