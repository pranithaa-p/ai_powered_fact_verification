
import logging

from app.services.claim_extractor import extract_claims
from app.services.tavily_service import search_claim
from app.services.groq_service import verify_with_llm
from app.services.summary_service import generate_summary
from app.services.query_rewriter import rewrite_query


logger = logging.getLogger(__name__)


def _not_enough_information(claim: str, explanation: str):
    """Return a consistent fallback result for a claim."""
    return {
        "claim": claim,
        "verdict": "NOT ENOUGH INFORMATION",
        "confidence": 0,
        "explanation": explanation,
        "references": [],
    }


def _safe_confidence(value):
    """Ensure confidence is a valid integer between 0 and 100."""
    try:
        confidence = int(float(value))
        return max(0, min(100, confidence))
    except (TypeError, ValueError):
        return 0


def verify_claim(claim: str):
    logger.info("Starting verification pipeline")

    # 1. Extract factual claims
    try:
        logger.info("Extracting claims")
        claims = extract_claims(claim)

        if not isinstance(claims, list):
            logger.warning("Claim extractor returned an unexpected value")
            claims = []

        logger.info("Extracted %d claims", len(claims))

    except Exception:
        logger.exception("Claim extraction failed")
        raise

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
                    "explanation": (
                        "The input does not contain a verifiable factual "
                        "claim. It appears to be an opinion, preference, "
                        "question, or conversational statement."
                    ),
                    "references": [],
                }
            ],
        }

    all_results = []

    # 2. Process each extracted claim
    for index, single_claim in enumerate(claims, start=1):
        logger.info("Processing claim %d/%d", index, len(claims))

        # Rewrite the claim into a search query
        try:
            logger.info("Rewriting search query")
            search_query = rewrite_query(single_claim)

            if not search_query or not isinstance(search_query, str):
                logger.warning("Query rewriting returned an invalid query")
                all_results.append(
                    _not_enough_information(
                        single_claim,
                        "Unable to create a search query for this claim.",
                    )
                )
                continue

        except Exception:
            logger.exception("Query rewriting failed")
            all_results.append(
                _not_enough_information(
                    single_claim,
                    "An error occurred while preparing the search query.",
                )
            )
            continue

        # 3. Search for evidence using Tavily
        try:
            logger.info("Searching Tavily for evidence")
            search_results = search_claim(search_query)

            if not isinstance(search_results, dict):
                logger.warning("Tavily returned an unexpected response")
                all_results.append(
                    _not_enough_information(
                        single_claim,
                        "The evidence search returned an invalid response.",
                    )
                )
                continue

            results = search_results.get("results", [])

            if not isinstance(results, list) or not results:
                logger.warning("No Tavily search results found")
                all_results.append(
                    _not_enough_information(
                        single_claim,
                        "No relevant evidence was found.",
                    )
                )
                continue

        except Exception:
            logger.exception("Tavily search failed")
            all_results.append(
                _not_enough_information(
                    single_claim,
                    "An error occurred while searching for evidence.",
                )
            )
            continue

        # 4. Prepare evidence and source references
        evidence_parts = []
        references = []

        for result in results:
            if not isinstance(result, dict):
                continue

            title = result.get("title", "Untitled source")
            content = result.get("content", "")
            url = result.get("url", "")

            evidence_parts.append(
                f"Title: {title}\n"
                f"Content: {content}\n"
                f"URL: {url}\n"
            )

            if url:
                references.append({
                    "title": title,
                    "url": url,
                })

        evidence = "\n".join(evidence_parts)

        if not evidence.strip():
            logger.warning("No usable evidence was returned")
            all_results.append(
                _not_enough_information(
                    single_claim,
                    "No usable evidence was found for this claim.",
                )
            )
            continue

        # 5. Verify the claim using Groq
        try:
            logger.info("Calling Groq for claim verification")
            llm_response = verify_with_llm(single_claim, evidence)

        except Exception:
            logger.exception("Groq verification failed")
            llm_response = None

        if not isinstance(llm_response, dict):
            logger.warning("Groq returned an invalid response")
            llm_response = {}

        verdict = llm_response.get(
            "verdict", "NOT ENOUGH INFORMATION"
        )

        # Treat AI service failures as insufficient information,
        # rather than incorrectly classifying them as a verdict.
        if verdict not in {
            "TRUE",
            "FALSE",
            "PARTIALLY TRUE",
            "NOT ENOUGH INFORMATION",
        }:
            logger.warning("Invalid or error verdict received from Groq")
            verdict = "NOT ENOUGH INFORMATION"

        confidence = _safe_confidence(
            llm_response.get("confidence", 0)
        )

        explanation = llm_response.get(
            "explanation",
            "Unable to verify the claim with the available evidence.",
        )

        if not isinstance(explanation, str):
            explanation = "Unable to verify the claim."

        all_results.append({
            "claim": single_claim,
            "verdict": verdict,
            "confidence": confidence,
            "explanation": explanation,
            "references": references[:3],
        })

    # 6. Generate the overall summary
    try:
        logger.info("Generating overall verification summary")
        overall = generate_summary(all_results)

        if not isinstance(overall, dict):
            raise ValueError("Summary service returned an invalid response")

    except Exception:
        logger.exception("Summary generation failed")
        raise

    logger.info("Verification pipeline completed successfully")

    return {
        "overall_verdict": overall.get(
            "overall_verdict", "NOT ENOUGH INFORMATION"
        ),
        "overall_confidence": _safe_confidence(
            overall.get("overall_confidence", 0)
        ),
        "summary": overall.get(
            "summary", "Verification completed."
        ),
        "results": all_results,
    }