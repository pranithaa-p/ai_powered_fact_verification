import json
import re
from groq import Groq
from app.config.settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def extract_claims(text: str):

    prompt = f"""
You are an expert NLP system.

Extract all independent factual claims.

Rules:
- Split compound factual statements.
- Ignore opinions.
- Ignore personal preferences.
- Ignore greetings.
- Ignore questions.
- If no factual claims exist, return:
{{"claims":[]}}

Return ONLY valid JSON.

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    print("LLM Output:")
    print(content)

    # Remove markdown if present
    content = content.replace("```json", "").replace("```", "").strip()

    # Extract JSON object if extra text exists
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        return []

    try:
        data = json.loads(match.group())
        return data.get("claims", [])
    except Exception:
        return []