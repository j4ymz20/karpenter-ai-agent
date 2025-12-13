# Karpenter AI Agent – Roadmap (Open Source)

> This roadmap outlines planned improvements for the **open-source Karpenter AI Agent**.  
> All items below focus on deterministic analysis, explainability, and safe automation.  
> There are **no SaaS, billing, or premium features** planned as part of this project.

---

## Roadmap Phases

### Step 1 — Full EC2NodeClass rule coverage

- Detect missing AMI selectors
- Detect incomplete subnet selector configuration
- Detect incomplete security group selector configuration
- Validate `instanceProfile` presence and basic correctness
- Cross-validate NodePool ↔ EC2NodeClass references
- Generate patch suggestions for all EC2NodeClass findings
- Surface EC2NodeClass details in the UI and link them to related NodePools

---

### Step 2 — Deterministic scoring system (0–100)

- Derive a single **Karpenter Health Score** from rule results
- Weight high-severity issues more heavily than medium/low
- Show:
  - Per-NodePool score
  - Overall cluster score
- Color-coded severity badges (red / yellow / green)
- Short human-readable risk labels (e.g., *High cost risk*, *Low efficiency risk*)

---

### Step 3 — Provisioner / NodePool comparison dashboard

- Table view comparing NodePools on:
  - Spot usage
  - Graviton usage
  - Consolidation status
  - TTL configuration
  - Instance family diversity
- Sorting and filtering by:
  - Severity
  - Name
  - Score
- Direct links to suggested YAML patches per NodePool

---

### Step 4 — Exportable analysis reports

- Export analysis as:
  - Standalone HTML report
  - Printable PDF report
- Reports include:
  - Summary metrics
  - Detailed rule findings
  - AI-generated explanations
  - (Optional) truncated YAML patch examples
- Reports are static and safe to share with teams

---

### Step 5 — Safe auto-fix patch bundling

- Generate a combined patch bundle grouped by NodePool
- Allow users to include/exclude:
  - Spot recommendations
  - Consolidation changes
  - TTL changes
  - Graviton recommendations
- Output a single `karpenter-fixes.yaml`
- Include clear safety notes and manual review guidance

---

## Planned Enhancements (OSS)

### Cost-focused analysis improvements

- Instance family diversity checks
- Estimated relative cost impact per recommendation
- Improved scoring weights based on AWS pricing characteristics
- Detection of Spot-only configurations without on-demand fallback
- ARM64 compatibility hints for Graviton adoption

---

### Reliability & operational best-practice checks

- Detect Karpenter controller placement risks
- Warn if controller pods run on Karpenter-managed nodes
- AMI hygiene checks (e.g., overly broad selectors)
- NodePool capacity narrowness detection
- Spot-only reliability warnings
- Taints and toleration mismatch detection
- NodePool ↔ EC2NodeClass consistency validation

---

### UI / UX improvements

- Mode selector: **Cost-Focused** vs **Full Advisor**
- Category-level scores (Cost, Efficiency, Reliability)
- Side-by-side comparison of two configurations
- “Before vs After” analysis when applying suggested fixes
- Clear visual explanation of why each rule fired

---

### Tooling & integrations

- GitHub Actions integration for validating Karpenter YAML in PRs
- CLI interface for local and CI usage
- Structured JSON output for automation and integrations
- Plugin-style rule registration for easier extensibility
- Version-aware validation for multiple Karpenter releases

---

### Architecture & maintainability

- Rule engine modularization
- Improved test coverage for edge-case configurations
- Caching of AI explanations (optional, local only)
- Clear separation between:
  - Deterministic rules
  - AI explanation layer
- Future support for additional platforms (long-term, experimental)

---

## Milestones & Versioning

| Version | Scope |
|------|------|
| v0.4 | NodePool rules, basic UI, AI explanations, patch suggestions |
| v0.5 | EC2NodeClass validation and UI surface |
| v0.6 | Scoring system and comparison dashboard |
| v0.7 | Report export and bundled patch generation |
| v0.8 | Reliability and operational best-practice rules |
| v1.0 | Stable OSS release with documented extension points |

---

## Non-Goals

To keep the project focused and maintainable, the following are explicitly **out of scope**:

- Cluster mutation or automatic writes
- Continuous background monitoring
- Billing, user accounts, or SaaS infrastructure
- Vendor lock-in or managed services
- Replacing human review in production environments
