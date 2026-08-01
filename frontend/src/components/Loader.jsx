function Loader() {
	const steps = [
		{ label: "Extracting Claims", state: "complete" },
		{ label: "Query Rewriting", state: "complete" },
		{ label: "Searching Evidence", state: "active" },
		{ label: "AI Verification", state: "pending" },
		{ label: "Generating Summary", state: "pending" },
	];

	return (
		<div className="loader-card result-reveal">
			<div className="section-heading compact">
				<span className="eyebrow">Processing pipeline</span>
				<h2>Working through the evidence</h2>
			</div>

			<div className="pipeline">
				{steps.map((step) => (
					<div key={step.label} className={`pipeline-step pipeline-${step.state}`}>
						<span className="pipeline-icon" aria-hidden="true">
							{step.state === "complete" ? "✓" : step.state === "active" ? "⏳" : "○"}
						</span>
						<span>{step.label}</span>
					</div>
				))}
			</div>
		</div>
	);
}

export default Loader;
