from groq import Groq
from config.settings import GROQ_API_KEY, MODEL_NAME


class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = MODEL_NAME

    def chat(self, messages, temperature=0, max_tokens=150):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return completion.choices[0].message.content.strip()
