import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found in .env")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=15000)
)

print("\n===== AVAILABLE GEMINI MODELS =====\n")

for model in client.models.list():
    if model.supported_actions and "generateContent" in model.supported_actions:
        print(model.name)

print("\n===== MODEL DISCOVERY COMPLETE =====")