import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env file.")


# Initialize Gemini client
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=180000
    )
)


def generate_answer(context: str, question: str) -> str:

    prompt = f"""
You are DocuMind AI, an intelligent PDF assistant.

Answer the user's question using ONLY the provided context.

If the answer is unavailable in the context,
say that the document does not contain enough information.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    print("Connecting to Gemini 3.5 Flash-Lite...")

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=256
        )
    )

    return response.text or "No answer was generated."