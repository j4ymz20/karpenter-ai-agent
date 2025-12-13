# Karpenter AI Agent

**Karpenter AI Agent** is an open-source analysis and optimization tool for Kubernetes clusters using **Karpenter**. It evaluates Provisioners, NodePools, and EC2NodeClasses to detect misconfigurations, cost inefficiencies, and operational risks using deterministic rules, then optionally generates an AI-assisted natural-language summary.

The core analysis is fully deterministic and does **not** require an LLM. AI summaries are an optional enhancement.

---

## Key Capabilities

### Configuration Analysis
- Parses Karpenter **Provisioner**, **NodePool**, and **EC2NodeClass** resources
- Safe YAML parsing with edge-case handling
- Cross-resource validation (NodePool ↔ EC2NodeClass)

### Rule-Based Detection
- Spot capacity usage
- Consolidation enablement
- Graviton (ARM64) adoption
- `ttlSecondsAfterEmpty` configuration
- EC2NodeClass IAM, subnet, and security group checks

### AI-Assisted Summary (Optional)
- Natural-language explanation of findings
- Ordered by severity and impact
- Designed to complement—not replace—deterministic rules

### Remediation Guidance
- Suggested YAML patch snippets per issue
- Copy-to-clipboard support
- Designed for **manual review before applying**

### Web Interface
- FastAPI backend
- Dark-mode UI
- Health score visualization
- Structured issue cards with recommendations

### Testing
- Pytest-based test suite
- Edge-case Karpenter YAML fixtures

---

## Installation

Clone the repository:

```bash
git clone https://github.com/matt-e-builds/karpenter-ai-agent.git
cd karpenter-ai-agent
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

(Optional) Enable AI summaries:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

> The application works fully without an API key; AI summaries will simply be disabled.

---

## Running the Application

```bash
python main.py
```

Then open:

```
http://127.0.0.1:5000
```

---

## Project Structure

```text
karpenter-ai-agent/
├── main.py
├── parser.py
├── rules.py
├── models.py
├── llm_client.py
├── templates/
├── tests/
│   ├── fixtures/
│   └── test_rules.py
├── README.md
└── ROADMAP.md
```

---

## License

MIT License

---

## Roadmap

See [ROADMAP.md](./ROADMAP.md) for planned open-source enhancements, including expanded rule coverage, scoring improvements, reporting, and UX refinements.

---

## Maintainer

Maintained by **Matt E**  
GitHub: https://github.com/matt-e-builds
