def generate_summary(results):

    if not results:
        return {
            "overall_verdict": "ERROR",
            "overall_confidence": 0,
            "summary": "No claims could be verified."
        }

    verdicts = [r["verdict"] for r in results]

    true_count = verdicts.count("TRUE")
    false_count = verdicts.count("FALSE")
    partial_count = verdicts.count("PARTIALLY TRUE")
    unknown_count = verdicts.count("NOT ENOUGH INFORMATION")

    total = len(results)

    average_confidence = round(
        sum(r["confidence"] for r in results) / total
    )

    if false_count == total:
        overall = "FALSE"

    elif true_count == total:
        overall = "TRUE"

    elif unknown_count == total:
        overall = "NOT ENOUGH INFORMATION"

    else:
        overall = "PARTIALLY TRUE"

    summary = (
        f"{true_count} true, "
        f"{false_count} false, "
        f"{partial_count} partially true, "
        f"{unknown_count} insufficient evidence."
    )

    return {
        "overall_verdict": overall,
        "overall_confidence": average_confidence,
        "summary": summary
    }