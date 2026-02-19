from core.llm.client import LLMClient
from config.settings import AI_NAME
from memory.database import MemoryDB


class DialogueModel:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = MemoryDB()

    def build_system_prompt(self):
        name = self.memory.get_profile("name")

        profile_info = ""
        if name:
            profile_info = f"The user's name is {name}. Address them naturally when appropriate."

        return f"""
You are {AI_NAME}, an intelligent home assistant.

{profile_info}

Speak naturally and professionally.
Keep responses concise.
Do not mention being an AI model.
"""

    def process(self, text: str) -> str:
        system_prompt = self.build_system_prompt()

        messages = [{"role": "system", "content": system_prompt}]

        history = self.memory.load_recent(limit=20)
        messages += history

        messages.append({"role": "user", "content": text})

        try:
            response = self.llm.generate(messages, temperature=0.6, max_tokens=300)

            self.memory.save_message("user", text)
            self.memory.save_message("assistant", response)

            return response

        except Exception:
            return "Something went wrong."
