import re
from datetime import datetime, timedelta
from core.llm.command_parser import CommandParser
from core.llm.dialogue_model import DialogueModel
from router import route_command
from config.settings import AI_NAME
from memory.database import MemoryDB
from core.scheduler import Scheduler

def main():
    parser = CommandParser()
    dialogue = DialogueModel()
    memory = MemoryDB()
    scheduler = Scheduler()

    print(f"{AI_NAME} is running...")

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
            print(f"{AI_NAME}: Your name is {name}." if name else f"{AI_NAME}: I don't know your name yet.")
            continue

        # ----------------------------
        # Delayed commands
        # ----------------------------
        delay_match = re.search(r"after (\d+) (minute|minutes|min)", user_input.lower())
        if delay_match:
            minutes = int(delay_match.group(1))
            delay_seconds = minutes * 60

            command = parser.process(user_input)
            if command["intent"] != "NONE":
                device_name = command["device"]
                action = command["intent"]
                execute_time = datetime.now() + timedelta(seconds=delay_seconds)
                memory.add_scheduled_task(device_name, action, execute_time.isoformat())

                def delayed_action():
                    route_command(command)
                    memory.complete_task(device_name, action)

                scheduler.schedule(delay_seconds, delayed_action)
                print(f"{AI_NAME}: Timer set for {minutes} minutes.")
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
