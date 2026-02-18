from core.llm.command_parser import CommandParser
from core.llm.dialogue_model import DialogueModel
from router import route_command
from config.settings import AI_NAME


def main():
    parser = CommandParser()
    dialogue = DialogueModel()

    print(f"{AI_NAME} is running...")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        command = parser.process(user_input)

        if command["intent"] != "NONE":
            device_result = route_command(command)

            final_response = dialogue.process(
                f"The system executed this action: {device_result}. "
                f"Respond naturally."
            )
        else:
            final_response = dialogue.process(user_input)

        print(f"{AI_NAME}: {final_response}")


if __name__ == "__main__":
    main()
