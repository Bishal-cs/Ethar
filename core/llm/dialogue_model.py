from core.llm.client import LLMClient
from config.settings import AI_NAME
from memory.database import MemoryDB


class DialogueModel:
    def __init__(self):
        self.llm = LLMClient()
        self.memory = MemoryDB()

        self.system_prompt = f"""
You are {AI_NAME}, an intelligent home assistant.

You remember previous conversations.
Speak naturally and professionally.
Keep responses concise.
Do not mention being an AI model.
"""

    def process(self, text: str) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        # Load memory from SQLite
        history = self.memory.load_recent(limit=20)
        messages += history

        messages.append({"role": "user", "content": text})

        try:
            response = self.llm.generate(messages, temperature=0.6, max_tokens=300)

            # Save to SQLite
            self.memory.save_message("user", text)
            self.memory.save_message("assistant", response)

            return response

        except Exception:
            return "Something went wrong."
