import json
from groq import Groq
from app.config.settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def extract_claims(text: str):

    prompt = f"""
You are an expert NLP system.

Your task is to extract all independent factual claims from the text.

Rules:
- Split compound statements into separate factual claims.
- Preserve wording as much as possible.
- Ignore opinions or questions.
- Return ONLY valid JSON.

Example:

Input:
Earth is flat. There are 8 days in a week. Sun rises in east.

Output:
{{
    "claims":[
        "Earth is flat",
        "There are 8 days in a week",
        "Sun rises in east"
    ]
}}

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

    content = response.choices[0].message.content

    print(content)

    return json.loads(content)["claims"]