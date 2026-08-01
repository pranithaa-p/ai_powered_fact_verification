import json
from groq import Groq
from app.config.settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def rewrite_query(claim: str):

    prompt = f"""
You are a search query optimizer.

Your job is NOT to verify the claim.

Your job is ONLY to rewrite the user's claim into the best possible search query.

Rules:

- Preserve the meaning.
- Preserve tense (past, present, future).
- Preserve entities.
- Remove unnecessary words.
- Make it suitable for a search engine.

Examples:

Claim:
There are 8 days in a week.

Search Query:
current number of days in a standard week

------------

Claim:
There were 8 days in a week.

Search Query:
historical eight-day week calendar

------------

Claim:
New Delhi is the capital of India.

Search Query:
capital of India

------------

Return ONLY JSON.

{{
    "query":"..."
}}

Claim:
{claim}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)["query"]