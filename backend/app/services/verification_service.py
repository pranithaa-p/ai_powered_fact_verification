from app.services.claim_extractor import extract_claims
from app.services.tavily_service import search_claim
from app.services.groq_service import verify_with_llm
from app.services.summary_service import generate_summary
from app.services.query_rewriter import rewrite_query


def verify_claim(claim: str):

    claims = extract_claims(claim)

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

        references = []

        for result in search_results["results"][:3]:
            references.append({
                "title": result["title"],
                "url": result["url"]
            })

        all_results.append({
            "claim": single_claim,
            "verdict": llm_response["verdict"],
            "confidence": llm_response["confidence"],
            "explanation": llm_response["explanation"],
            "references": references
        })

    overall = generate_summary(all_results)

    return {
        "overall_verdict": overall["overall_verdict"],
        "overall_confidence": overall["overall_confidence"],
        "summary": overall["summary"],
        "results": all_results
    }