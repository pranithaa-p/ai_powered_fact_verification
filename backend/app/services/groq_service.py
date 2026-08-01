import json
from groq import Groq
from app.config.settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def verify_with_llm(claim: str, evidence: str):

    prompt = f"""
You are Decipher, an AI Fact Verification Engine.

Your task is to verify EXACTLY ONE factual claim using ONLY the supplied evidence.

========================
CLAIM
========================
{claim}

========================
EVIDENCE
========================
{evidence}

========================
REASONING RULES
========================

1. First determine the intended context of the claim.

Possible contexts:
- Present-day fact
- Historical fact
- Future prediction
- Fictional universe
- Hypothetical statement

Use the wording of the claim to determine the context.
Do NOT change the user's intended meaning.

Examples:
"There ARE 8 days in a week."
→ Present-day claim

"There WERE 8 days in a week."
→ Historical claim

"Superman was born on Krypton."
→ Fictional claim

"Humans will live on Mars."
→ Future claim

"If gravity disappeared..."
→ Hypothetical claim

--------------------------------------------------

2. Interpret the claim literally.

Do NOT rewrite it.

Do NOT weaken it.

Do NOT strengthen it.

--------------------------------------------------

3. Evaluate ONLY within the detected context.

Example:

Claim:
"There were 8 days in a week."

Historical evidence about the Roman 8-day calendar IS relevant.

Claim:
"There are 8 days in a week."

Historical evidence is NOT sufficient because the claim is about the present.

--------------------------------------------------

4. Ignore evidence that is unrelated even if it contains similar words.

Examples of unrelated evidence:
- Movies
- TV series
- Songs
- Books
- Product names
- Celebrity names
- Fictional pages
- Discussion forums

--------------------------------------------------

5. Prefer evidence in this order:

1. Government websites
2. Scientific organizations
3. Universities
4. Britannica
5. WHO
6. NASA
7. Peer-reviewed sources
8. Wikipedia

Treat Quora, Reddit, blogs and social media as weak evidence.

--------------------------------------------------

6. If authoritative sources disagree, explain why.

--------------------------------------------------

7. Never use your own knowledge unless it is directly supported by the supplied evidence.

--------------------------------------------------

8. Confidence Guidelines

95–100
Multiple authoritative sources clearly support the verdict.

80–94
Strong evidence with minor ambiguity.

60–79
Evidence is limited or partially conflicting.

Below 60
Weak evidence.

--------------------------------------------------

9. Explanation

Maximum 60 words.

Explain WHY the verdict was chosen.

Mention if evidence was ignored because it was irrelevant.

--------------------------------------------------

10. Verdict Rules

TRUE
Every important part of the claim is supported.

FALSE
The evidence clearly contradicts the claim.

PARTIALLY TRUE
Some parts are correct while others are incorrect.

NOT ENOUGH INFORMATION
The supplied evidence is insufficient.

--------------------------------------------------

Return ONLY valid JSON.

{{
    "verdict": "TRUE | FALSE | PARTIALLY TRUE | NOT ENOUGH INFORMATION",
    "confidence": 95,
    "explanation": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )
    except Exception:
        return {
            "verdict": "ERROR",
            "confidence": 0,
            "explanation": "Unable to contact the AI service."
        }

    answer = response.choices[0].message.content

    try:
        return json.loads(answer)
    except json.JSONDecodeError:
        return {
            "verdict": "ERROR",
            "confidence": 0,
            "explanation": "The AI returned an invalid response."
        }