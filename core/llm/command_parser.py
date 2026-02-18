import json
import re
from devices.registry import devices
from core.llm.client import LLMClient


class CommandParser:
    def __init__(self):
        self.llm = LLMClient()

    def process(self, text: str) -> dict:
        device_list = ", ".join(devices.keys())

        system_prompt = f"""
You are a strict device command extractor.

If the user mentions any device control request,
extract it EVEN IF the sentence includes other conversation.

Available devices: {device_list}

Return ONLY JSON.

If device control exists:
{{
  "intent": "TURN_ON" | "TURN_OFF" | "STATUS",
  "device": "<device_name>"
}}

If no device control exists:
{{
  "intent": "NONE",
  "device": null
}}
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        try:
            response = self.llm.generate(messages, temperature=0)

            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                data = json.loads(match.group())

                # normalize
                intent = data.get("intent", "NONE").upper().strip()
                device = data.get("device")

                if device:
                    device = device.lower().strip()

                return {"intent": intent, "device": device}

            return {"intent": "NONE", "device": None}

        except Exception:
            return {"intent": "NONE", "device": None}
