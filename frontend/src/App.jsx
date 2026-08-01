import { useEffect, useState } from "react";
import Header from "./components/Header";
import ClaimForm from "./components/ClaimForm";
import Loader from "./components/Loader";
import OverallVerdict from "./components/OverallVerdict";
import ClaimCard from "./components/ClaimCard";
import { verifyClaim } from "./services/api";
import { AlertCircle, CheckCircle2, ShieldCheck, XCircle } from "lucide-react";

function getClaimKey(claim) {
  if (typeof claim === "string") return claim;

  if (claim && typeof claim === "object") {
    return claim.text || claim.claim || claim.fact || claim.evidence || JSON.stringify(claim);
  }

  return String(claim || "claim");
}

function App() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    if (!notification) return undefined;

    const timer = window.setTimeout(() => {
      setNotification(null);
    }, 4200);

    return () => window.clearTimeout(timer);
  }, [notification]);

  async function handleVerify(claim) {
    setLoading(true);
    setReport(null);
    setNotification(null);

    try {
      const data = await verifyClaim(claim);
      setReport(data);
      setNotification({
        type: "success",
        title: "Verification complete",
        message: "Evidence review and AI summary are ready.",
      });
    } catch (error) {
      setNotification({
        type: "error",
        title: "Verification failed",
        message: error.message || "Unable to verify the claim right now.",
      });
    } finally {
      setLoading(false);
    }
  }

  const verdict = report?.overall_verdict ?? "No verdict yet";
  const confidence = Number(report?.overall_confidence ?? 0);
  const claimsVerified = Array.isArray(report?.results) ? report.results.length : 0;
  const verificationTime =
    report?.verification_time ??
    report?.verification_time_ms ??
    report?.execution_time ??
    report?.time_taken ??
    null;

  return (
    <div className="app-shell">
      <div className="background-pattern" aria-hidden="true" />

      <Header />

      {notification && (
        <div className={`notification notification-${notification.type}`} role="status" aria-live="polite">
          <div className="notification-icon">
            {notification.type === "success" ? <CheckCircle2 size={18} /> : <XCircle size={18} />}
          </div>
          <div>
            <strong>{notification.title}</strong>
            <p>{notification.message}</p>
          </div>
        </div>
      )}

      <main className="app">
        <div className="workspace-heading">
          <div className="section-heading">
            <span className="eyebrow">Workflow</span>
            <h2>Input and review</h2>
          </div>
        </div>

        <section className="dashboard-grid" aria-label="Verification workspace">
          <div className="panel panel-input">
            <div className="panel-label">
              <span className="panel-number">01</span>
              <span>Input</span>
            </div>
            <ClaimForm onVerify={handleVerify} loading={loading} />
          </div>

          <div className="panel panel-results">
            <div className="results-header">
              <div className="panel-label">
                <span className="panel-number">02</span>
                <span>Verification Results</span>
              </div>

              <span className="results-status">
                <CheckCircle2 size={14} />
                Verified just now
              </span>
            </div>

            <div className="results-scroll">
              {loading ? (
                <Loader />
              ) : report ? (
                <>
                  <div className="section-heading results-heading">
                    <span className="eyebrow">Verification Summary</span>
                    <h2>Outcome at a glance</h2>
                  </div>

                  <OverallVerdict
                    verdict={verdict}
                    confidence={confidence}
                    summary={report.summary}
                    claimsVerified={claimsVerified}
                    verificationTime={verificationTime}
                  />

                  <div className="claims-list">
                    <div className="section-heading compact results-heading">
                      <span className="eyebrow">Claims</span>
                      <h3>Individual verdicts</h3>
                    </div>

                    {report.results?.map((item, index) => (
                      <ClaimCard
                        key={`${getClaimKey(item.claim)}-${index}`}
                        claimResult={item}
                        index={index}
                        animationDelay={index * 90}
                      />
                    ))}
                  </div>

                  <section className="about-card glass-card result-reveal">
                    <div className="about-card-icon">
                      <AlertCircle size={18} />
                    </div>

                    <div className="about-card-copy">
                      <div className="summary-label">
                        <span>About verification</span>
                      </div>
                      <p>
                        Decipher compares claims against trusted web evidence and summarizes the
                        result with source-backed reasoning. Always review the cited references.
                      </p>
                    </div>
                  </section>
                </>
              ) : (
                <div className="empty-state">
                  <div className="empty-state-icon">
                    <AlertCircle size={22} />
                  </div>
                  <h2>No verification results yet</h2>
                  <p>
                    Submit a claim to see the overall verdict, confidence, extracted claims,
                    and source references in a clean executive summary.
                  </p>
                </div>
              )}
            </div>
          </div>
        </section>

        <footer className="app-footer" aria-label="Application footer">
          <ShieldCheck size={14} />
          <span>2025 Decipher</span>
          <span>AI-Powered Fact Verification Platform</span>
        </footer>
      </main>
    </div>
  );
}

export default App;