import { ExternalLink, Link2 } from "lucide-react";

function getReferenceLabel(reference) {
	const rawTitle = String(reference?.title || "").trim();
	const rawUrl = String(reference?.url || "").trim();

	if (rawTitle && !rawTitle.startsWith("http")) {
		return rawTitle.replace(/^https?:\/\//i, "");
	}

	try {
		const hostname = new URL(rawUrl || rawTitle).hostname.replace(/^www\./i, "").toLowerCase();

		if (hostname.includes("wikipedia")) return "Wikipedia";
		if (hostname.includes("britannica")) return "Britannica";
		if (hostname.includes("nasa")) return "NASA";
		if (hostname.includes("reuters")) return "Reuters";
		if (hostname.includes("bbc")) return "BBC";

		return hostname.split(".")[0] || rawTitle || "Source";
	} catch {
		return rawTitle || "Source";
	}
}

function ReferenceList({ references = [] }) {
	return (
		<div className="reference-list">
			<div className="summary-label">
				<Link2 size={15} />
				Verified Sources
			</div>

			{references.length > 0 ? (
				<div className="reference-grid">
					{references.map((reference, index) => (
						<a
							key={`${reference.url}-${index}`}
							className="reference-chip"
							href={reference.url}
							target="_blank"
							rel="noreferrer"
						>
							<span>{getReferenceLabel(reference)}</span>
							<ExternalLink size={14} />
						</a>
					))}
				</div>
			) : (
				<p className="empty-copy">No references were returned for this claim.</p>
			)}
		</div>
	);
}

export default ReferenceList;
