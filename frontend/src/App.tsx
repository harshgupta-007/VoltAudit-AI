import React from "react";

export const App: React.FC = () => {
  return (
    <div className="app-container">
      <header>
        <div className="logo-container">
          <div className="logo-icon">⚡</div>
          <div className="logo-text">VoltAudit AI</div>
          <div className="logo-badge">Console</div>
        </div>
        <nav className="nav-links">
          <a href="/docs/onboarding.md" className="nav-link">Onboarding</a>
          <a href="/specs/specifications.md" className="nav-link">Specifications</a>
          <a href="/docs/engineering_standards.md" className="nav-link">Standards</a>
        </nav>
      </header>

      <main>
        <section className="hero-section">
          <h1 className="hero-title">
            Enterprise AI Workforce for <span>Invoice Auditing</span>
          </h1>
          <p className="hero-subtitle">
            Secure, spec-driven, and highly-explainable cognitive agents auditing corporate billing transactions in real-time.
          </p>
        </section>

        <section className="grid-container">
          <div className="glass-card">
            <div className="card-icon">📂</div>
            <h3 className="card-title">Ingestion API</h3>
            <p className="card-text">
              Accepts multipart PDF, PNG, and JPEG uploads. Automatically triggers OCR extraction and document classification pipelines.
            </p>
          </div>

          <div className="glass-card accent">
            <div className="card-icon">🤖</div>
            <h3 className="card-title">Cognitive Auditor</h3>
            <p className="card-text">
              Agentic reasoning loop powered by Gemini models. Compares line items against contractual terms and lists audit discrepancies.
            </p>
          </div>

          <div className="glass-card">
            <div className="card-icon">🔌</div>
            <h3 className="card-title">MCP Services</h3>
            <p className="card-text">
              Model Context Protocol (MCP) server providing secure database endpoints and contract validation tools to active AI agents.
            </p>
          </div>

          <div className="glass-card accent">
            <div className="card-icon">🛡️</div>
            <h3 className="card-title">Quality Gates</h3>
            <p className="card-text">
              Strict linting, static type checking, pre-commit scanners, and Semgrep security pipelines protecting code integrity.
            </p>
          </div>
        </section>
      </main>

      <footer>
        <div>© 2026 VoltAudit AI. All rights reserved.</div>
        <div>Status: Foundations Initialized</div>
      </footer>
    </div>
  );
};

export default App;
