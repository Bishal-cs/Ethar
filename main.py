import re
from datetime import datetime, timedelta
from core.llm.command_parser import CommandParser
from core.llm.dialogue_model import DialogueModel
from router import route_command
from config.settings import AI_NAME
from memory.database import MemoryDB
from core.scheduler import TaskExecutor
from datetime import datetime

def main():
    parser = CommandParser()
    dialogue = DialogueModel()
    memory = MemoryDB()
    scheduler = TaskExecutor()

    print(dialogue.process("You are starting up. Say hi to the user."))

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # ----------------------------
        # Name detection
        # ----------------------------
        name_match = re.search(r"my name is (.+)", user_input.lower())
        if name_match:
            name = name_match.group(1).strip().title()
            memory.set_profile("name", name)

        # ----------------------------
        # Profile query
        # ----------------------------
        if "who am i" in user_input.lower():
            name = memory.get_profile("name")
            print(dialogue.process(f"{AI_NAME}: Your name is {name}." if name else f"{AI_NAME}: I don't know your name yet."))
            continue

        if "date" in user_input.lower():
            today = datetime.now().strftime("%d %B %Y")
            print(dialogue.process(f"Today's date is {today}."))

        # ----------------------------
        # Delayed commands
        # ----------------------------
        delay_match = re.search(r"after (\d+) (minute|minutes|min)", user_input.lower())

        if delay_match:
            minutes = int(delay_match.group(1))
            execute_time = datetime.now() + timedelta(minutes=minutes)

            command = parser.process(user_input)

            if command["intent"] != "NONE":
                memory.add_scheduled_task(
                    command["device"],
                    command["intent"],
                    execute_time.isoformat()
                )

                print(dialogue.process(f"{AI_NAME}: Timer set for {minutes} minutes."))
                continue
        # ----------------------------
        # Normal command
        # ----------------------------
        command = parser.process(user_input)
        device_result = None
        if command["intent"] != "NONE":
            device_result = route_command(command)

        # ----------------------------
        # Hybrid response
        # ----------------------------
        if device_result:
            final_prompt = f"""
User said: {user_input}

System executed this device action:
{device_result}

Respond naturally answering everything the user asked.
"""
            final_response = dialogue.process(final_prompt)
        else:
            final_response = dialogue.process(user_input)

        print(f"{AI_NAME}: {final_response}")

if __name__ == "__main__":
    main()
