import re


def split_claims(text: str):
    """
    Split multiple factual statements into individual claims.
    """

    claims = re.split(r"[.\n;]+", text)

    claims = [c.strip() for c in claims if c.strip()]

    return claims