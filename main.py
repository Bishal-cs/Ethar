from core.llm.llm_interpreter import LLMInterpreter
from router import route_command
from config.settings import AI_NAME


def main():
    interpreter = LLMInterpreter()

    print(f"{AI_NAME} is running...")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        command = interpreter.interpret(user_input)
        print("DEBUG:", command)

        response = route_command(command)
        print(f"{AI_NAME}: {response}")


if __name__ == "__main__":
    main()
