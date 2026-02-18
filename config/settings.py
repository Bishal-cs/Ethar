from dotenv import dotenv_values

env_vars = dotenv_values(".env")

GROQ_API_KEY = env_vars.get("GroqAPIKey")
AI_NAME = env_vars.get("Assistantname", "Ethar")
MODEL_NAME = "llama-3.3-70b-versatile"
