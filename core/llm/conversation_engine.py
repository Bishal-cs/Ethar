from core.llm.client import GroqClient
from config.settings import AI_NAME


class ConversationEngine:
    def __init__(self):
        self.llm = GroqClient()

    def process(self, text: str) -> str:
        system_prompt = f"""
You are {AI_NAME}.

You speak naturally, calmly, and intelligently.
Keep responses concise.
Do not mention being an AI.
No emojis.
No stage directions.
Sound present and real.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        try:
            return self.llm.chat(messages, temperature=0.6, max_tokens=300)
        except Exception:
            return "Something went wrong."
