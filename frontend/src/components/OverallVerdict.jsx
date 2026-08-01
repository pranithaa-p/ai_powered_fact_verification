import { BadgeCheck, BarChart3, BrainCircuit, Clock3, ShieldAlert } from "lucide-react";

function getVerdictTone(verdict) {
	const normalized = String(verdict || "").trim().toUpperCase();

	if (normalized === "FALSE" || normalized.includes("FALSE") || normalized === "INCORRECT" || normalized.includes("DISPUTED")) {
		return "danger";
	}

	if (normalized === "PARTIALLY TRUE" || normalized.includes("PARTIALLY TRUE") || normalized.includes("PARTIAL")) {
		return "warning";
	}

	if (normalized === "NOT ENOUGH INFORMATION" || normalized.includes("NOT ENOUGH INFORMATION") || normalized.includes("UNKNOWN")) {
		return "neutral";
	}

	return "success";
}

function formatVerificationTime(verificationTime) {
	if (verificationTime === null || verificationTime === undefined || verificationTime === "") {
		return null;
	}

	if (typeof verificationTime === "number") {
		if (verificationTime >= 1000) {
			return `${(verificationTime / 1000).toFixed(1)}s`;
		}

		return `${verificationTime}ms`;
	}

	return String(verificationTime);
}

function OverallVerdict({ verdict, confidence, summary, claimsVerified, verificationTime }) {
	const tone = getVerdictTone(verdict);
	const safeConfidence = Math.max(0, Math.min(100, Number(confidence) || 0));
	const barTone = safeConfidence > 90 ? "success" : safeConfidence >= 60 ? "warning" : "danger";
	const displayTime = formatVerificationTime(verificationTime);
	const normalizedVerdict = String(verdict || "").trim().toUpperCase();
	const displayVerdict =
		normalizedVerdict === "TRUE" ||
		normalizedVerdict === "FALSE" ||
		normalizedVerdict === "PARTIALLY TRUE" ||
		normalizedVerdict === "NOT ENOUGH INFORMATION"
			? normalizedVerdict
			: verdict;

	return (
		<section className="summary-block glass-card result-reveal">
			<div className="summary-cards">
				<article className={`summary-card summary-${tone}`}>
					<div className="summary-label">
						<ShieldAlert size={16} />
						Overall Verdict
					</div>
					<strong>{displayVerdict}</strong>
				</article>

				<article className="summary-card">
					<div className="summary-label">
						<BadgeCheck size={16} />
						Confidence
					</div>
					<strong>{safeConfidence}%</strong>
					<div className="mini-progress" aria-hidden="true">
						<span className={`progress-fill progress-${barTone}`} style={{ width: `${safeConfidence}%` }} />
					</div>
				</article>

				<article className="summary-card">
					<div className="summary-label">
						<BarChart3 size={16} />
						Claims Verified
					</div>
					<strong>{claimsVerified}</strong>
					<span className="summary-subtext">claims reviewed from the request</span>
				</article>

				<article className="summary-card summary-time">
					<div className="summary-label">
						<Clock3 size={16} />
						Verification Time
					</div>
					<strong>{displayTime || "—"}</strong>
					<span className="summary-subtext">backend processing duration</span>
				</article>
			</div>

			<div className="summary-narrative">
				<div className="summary-label">
					<BrainCircuit size={16} />
					Executive Summary
				</div>
				<p>{summary || "No summary available yet."}</p>
			</div>
		</section>
	);
}

export default OverallVerdict;
