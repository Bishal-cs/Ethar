import json
import re
from devices.registry import devices
from core.llm.client import GroqClient


class LLMInterpreter:
    def __init__(self):
        self.llm = GroqClient()

    def interpret(self, text: str) -> dict:
        device_list = ", ".join(devices.keys())

        system_prompt = f"""
You are a command interpreter for a smart home assistant.

Available devices: {device_list}

Return ONLY valid JSON.

Format:
{{
  "intent": "TURN_ON" | "TURN_OFF" | "STATUS" | "UNKNOWN",
  "device": "<device_name_or_null>"
}}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        try:
            response = self.llm.chat(messages)

            print("RAW:", response)

            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group())

            return {"intent": "UNKNOWN", "device": None}

        except Exception as e:
            print("INTERPRETER ERROR:", e)
            return {"intent": "UNKNOWN", "device": None}
