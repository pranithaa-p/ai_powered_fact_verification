import { BadgeCheck, CircleAlert, CircleSlash, HelpCircle, Info, Quote, Sparkles } from "lucide-react";
import ReferenceList from "./ReferenceList";

function formatClaimText(claim) {
	if (typeof claim === "string") return claim;

	if (claim && typeof claim === "object") {
		return claim.text || claim.claim || claim.fact || claim.evidence || JSON.stringify(claim);
	}

	return String(claim || "");
}

function getVerdictTone(verdict) {
	const normalized = String(verdict || "").trim().toUpperCase();

	if (normalized === "TRUE" || normalized.includes("TRUE") || normalized === "SUPPORTED") {
		return "success";
	}

	if (normalized === "FALSE" || normalized.includes("FALSE") || normalized === "INCORRECT" || normalized.includes("DISPUTED")) {
		return "danger";
	}

	if (normalized === "PARTIALLY TRUE" || normalized.includes("PARTIALLY TRUE") || normalized.includes("PARTIAL")) {
		return "warning";
	}

	if (normalized === "NOT ENOUGH INFORMATION" || normalized.includes("NOT ENOUGH INFORMATION") || normalized.includes("UNKNOWN")) {
		return "neutral";
	}

	return "neutral";
}

function getVerdictIcon(tone) {
	if (tone === "success") return <BadgeCheck size={16} />;
	if (tone === "danger") return <CircleSlash size={16} />;
	if (tone === "warning") return <CircleAlert size={16} />;
	return <HelpCircle size={16} />;
}

function formatVerdictLabel(verdict) {
	const normalized = String(verdict || "").trim().toUpperCase();

	if (normalized.includes("PARTIAL")) return "PARTIALLY TRUE";
	if (normalized.includes("TRUE") && !normalized.includes("NOT ENOUGH")) return "TRUE";
	if (normalized.includes("FALSE")) return "FALSE";
	if (normalized.includes("NOT ENOUGH")) return "NOT ENOUGH INFORMATION";

	return normalized || "UNKNOWN";
}

function ClaimCard({ claimResult, index, animationDelay = 0 }) {
	const tone = getVerdictTone(claimResult.verdict);
	const confidence = Math.max(0, Math.min(100, Number(claimResult.confidence) || 0));
	const barTone = confidence > 90 ? "success" : confidence >= 60 ? "warning" : "danger";
	const displayVerdict = formatVerdictLabel(claimResult.verdict);
	const displayClaim = formatClaimText(claimResult.claim);

	return (
		<article className={`claim-card glass-card result-reveal claim-card-${tone}`} style={{ animationDelay: `${animationDelay}ms` }}>
			<div className="claim-card-top">
				<div className="claim-card-index">
					<span>Claim {index + 1}</span>
					<Sparkles size={14} />
				</div>

				<span className={`verdict-badge verdict-${tone}`}>
					{getVerdictIcon(tone)}
					{displayVerdict}
				</span>
			</div>

			<p className="claim-text">
				<Quote size={16} />
				{displayClaim}
			</p>

			<div className="claim-body-grid">
				<div className="claim-metrics">
					<div className="claim-metric-card">
						<div className="claim-metric-label">
							<BadgeCheck size={14} />
							Verdict
						</div>
						<span className={`verdict-badge verdict-${tone}`}>
							{getVerdictIcon(tone)}
							{displayVerdict}
						</span>
					</div>

					<div className="claim-metric-card">
						<div className="claim-metric-label">
							<BadgeCheck size={14} />
							Confidence
						</div>
						<strong>{confidence}%</strong>
						<div className="confidence-track" aria-hidden="true">
							<span className={`progress-fill progress-${barTone}`} style={{ width: `${confidence}%` }} />
						</div>
					</div>
				</div>

				<div className="claim-explanation">
					<div className="summary-label">
						<Info size={15} />
						Explanation
					</div>
					<p>{claimResult.explanation}</p>
				</div>
			</div>

			<ReferenceList references={claimResult.references || []} />
		</article>
	);
}

export default ClaimCard;
