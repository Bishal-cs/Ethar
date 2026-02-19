from dotenv import dotenv_values

env = dotenv_values(".env")

GROQ_API_KEY = env.get("GroqAPIKey")
AI_NAME = env.get("Assistantname")
MODEL_NAME = "llama-3.3-70b-versatile"
USER_NAME = env.get("USERNAME")
