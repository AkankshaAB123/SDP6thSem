import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Get API key safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Please check your .env file.")

# Initialize Groq model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2
)


def analyze_risk(context: str) -> str:
    """
    Takes retrieved RAG context and returns structured JSON risk analysis.
    """

    prompt = ChatPromptTemplate.from_template("""
You are an advanced Financial Risk Analysis Agent.

STRICT RULES:
- Use ONLY the provided CONTEXT.
- Do NOT hallucinate.
- Do NOT give legal advice.
- If information is missing, say "Insufficient evidence".
- Return VALID JSON only.
- Risk scores must be between 0 and 100.

CONTEXT:
{context}

Return JSON in this exact structure:

{{
  "document_type": "",
  "overall_risk_score": 0,
  "risk_breakdown": {{
      "financial_risk": 0,
      "legal_risk": 0,
      "long_term_liability": 0,
      "hidden_clause_risk": 0
  }},
  "risk_level": "LOW | MEDIUM | HIGH",
  "flagged_clauses": [
    {{
      "clause_text": "",
      "risk_type": "",
      "explanation": "",
      "impact": "",
      "recommendation": "",
      "confidence": 0
    }}
  ]
}}
""")

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"context": context})

    # Clean markdown if model adds ```
    response = response.strip()
    if response.startswith("```"):
        response = response.replace("```json", "").replace("```", "").strip()

    return response