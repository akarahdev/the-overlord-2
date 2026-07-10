from openai import OpenAI
import os

ai_client = OpenAI(
    api_key="sk-dummy",
    base_url="https://api.openai.com/v1"
)

api_key = os.getenv("OPEN_AI_TOKEN")
if api_key is None:
    print("API key does not exist?")
    exit(1)

ai_client.api_key = api_key

model = "ggml-org/gemma-4-E4B-it-GGUF:Q4_K_M"
model = "gpt-5.4-nano"
system_prompt = """
You are The Overlord, ruler of the DiamondFire mini game called "The Overlord 2".
Don't use emojis. Keep your responses short and concise, to fit in Minecraft's tiny chat window.

For the chat log history, note that you cans only see the past 20 messages in the game.
"""