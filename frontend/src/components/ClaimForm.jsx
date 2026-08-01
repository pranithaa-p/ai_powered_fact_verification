import { Search, SendHorizontal, Sparkles } from "lucide-react";
import { useState } from "react";

function ClaimForm({ onVerify, loading }) {
  const [claim, setClaim] = useState("");

  const examples = [
    "The Eiffel Tower is located in Paris.",
    "Water boils at 100°C at sea level.",
    "The Great Wall of China is visible from space.",
  ];

  function handleSubmit(e) {
    e.preventDefault();

    if (!claim.trim()) return;

    onVerify(claim);
  }

  return (
    <form className="claim-form" onSubmit={handleSubmit}>
      <div className="section-heading compact claim-form-intro">
        <span className="eyebrow">
          <Sparkles size={14} />
          Start a verification
        </span>
        <h2>Enter a claim</h2>
      </div>

      <div className="input-card glass-card">
        <div className="input-header">
          <Search size={18} />
          <span>Claim text</span>
        </div>

        <div className="textarea-field">
          <label className="textarea-label" htmlFor="claim-input">
            Enter one or more factual claims
          </label>

          <textarea
            id="claim-input"
            rows="8"
            placeholder="Example: India is the most populated country and New Delhi is its capital."
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
          />
        </div>

        <div className="form-meta">
          <small>{claim.length} characters</small>
          <small>Paste one or multiple factual claims.</small>
        </div>

        <div className="example-row" aria-label="Example claims">
          {examples.map((example) => (
            <button
              key={example}
              type="button"
              className="example-chip"
              onClick={() => setClaim(example)}
            >
              {example}
            </button>
          ))}

          <button
            type="button"
            className="example-chip example-chip-more"
            onClick={() => setClaim("Singapore has four official languages.")}
          >
            + More examples
          </button>
        </div>

        <div className="input-footer">
          <span className="input-hint">Results return in a summary + claim-by-claim review.</span>
          <button type="submit" disabled={loading || !claim.trim()}>
            {loading ? "Verifying..." : "Verify Claim"}
            <SendHorizontal size={18} />
          </button>
        </div>
      </div>
    </form>
  );
}

export default ClaimForm;