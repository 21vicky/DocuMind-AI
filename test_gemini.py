from src.gemini_client import generate_answer


context = """
Machine Learning is a branch of Artificial Intelligence.
It allows computers to learn patterns from data
and improve their performance without being explicitly programmed.
"""

question = "What is Machine Learning?"


answer = generate_answer(context, question)

print("\n===== DOCUMIND AI ANSWER =====")
print(answer)

print("\n===== TEST SUCCESSFUL =====")