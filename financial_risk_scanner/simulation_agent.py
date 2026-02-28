from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

def simulate_scenario(context, user_question):

    prompt = f"""
You are a Financial Scenario Simulation Agent.

Use ONLY the provided context.

CONTEXT:
{context}

USER QUESTION:
{user_question}

Explain possible consequences clearly.
Do NOT give legal advice.
Keep explanation structured.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content