import { Globe2, SearchCheck, Sparkles, ShieldCheck, WandSparkles } from "lucide-react";

function Header() {
  return (
    <header className="header-band">
      <div className="header-band-inner">
        <div className="header header-split">
          <div className="header-brand">
            <div className="logo" aria-hidden="true">
              <ShieldCheck size={32} strokeWidth={2.1} />
            </div>

            <div className="header-copy">
              <h1>Decipher</h1>

              <p>AI-Powered Fact Verification Platform</p>

              <span className="subtitle">
                Verify claims using trusted web evidence and AI-assisted reasoning.
              </span>
            </div>
          </div>

          <div className="feature-chips" aria-label="Platform highlights">
            <span className="feature-chip">
              <Sparkles size={14} />
              Multi-Claim Support
            </span>
            <span className="feature-chip">
              <WandSparkles size={14} />
              AI Reasoning
            </span>
            <span className="feature-chip">
              <SearchCheck size={14} />
              Trusted Web Sources
            </span>
            <span className="feature-chip">
              <Globe2 size={14} />
              Real-time Verification
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;