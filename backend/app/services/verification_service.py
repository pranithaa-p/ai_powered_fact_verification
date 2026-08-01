from app.services.claim_extractor import extract_claims
from app.services.tavily_service import search_claim
from app.services.groq_service import verify_with_llm
from app.services.summary_service import generate_summary
from app.services.query_rewriter import rewrite_query


def verify_claim(claim: str):

    claims = extract_claims(claim)

    # Handle cases where no factual claims are found
    if not claims:
        return {
            "overall_verdict": "NOT ENOUGH INFORMATION",
            "overall_confidence": 0,
            "summary": "No factual claims were found in the input.",
            "results": [
                {
                    "claim": claim,
                    "verdict": "NOT ENOUGH INFORMATION",
                    "confidence": 0,
                    "explanation": "The input does not contain a verifiable factual claim. It appears to be an opinion, preference, question, or conversational statement.",
                    "references": []
                }
            ]
        }

    all_results = []

    for single_claim in claims:

        search_query = rewrite_query(single_claim)
        search_results = search_claim(search_query)

        if not search_results.get("results"):
            all_results.append({
                "claim": single_claim,
                "verdict": "NOT ENOUGH INFORMATION",
                "confidence": 0,
                "explanation": "No relevant evidence was found.",
                "references": []
            })
            continue

        evidence = ""

        for result in search_results["results"]:
            evidence += (
                f"Title: {result['title']}\n"
                f"Content: {result['content']}\n"
                f"URL: {result['url']}\n\n"
            )

        llm_response = verify_with_llm(single_claim, evidence)

        # Handle malformed LLM response
        if not llm_response:
            llm_response = {
                "verdict": "NOT ENOUGH INFORMATION",
                "confidence": 0,
                "explanation": "Unable to verify the claim."
            }

        references = [
            {
                "title": result["title"],
                "url": result["url"]
            }
            for result in search_results["results"][:3]
        ]

        all_results.append({
            "claim": single_claim,
            "verdict": llm_response.get("verdict", "NOT ENOUGH INFORMATION"),
            "confidence": llm_response.get("confidence", 0),
            "explanation": llm_response.get(
                "explanation",
                "Unable to verify the claim."
            ),
            "references": references
        })

    overall = generate_summary(all_results)

    return {
        "overall_verdict": overall["overall_verdict"],
        "overall_confidence": overall["overall_confidence"],
        "summary": overall["summary"],
        "results": all_results
    }