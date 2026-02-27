# AI-Assisted Architecture Review

This project provides an **AI-assisted architecture review** for infrastructure changes defined in Terraform.  
It integrates a Large Language Model (LLM) into the pull request workflow to **surface architectural, security, compliance, reliability, and FinOps considerations** at design time — without automating decisions or blocking deployments.

The goal is **to support human reviewers**, not replace them.

---

## ✨ Key Goals

- Improve the quality and consistency of infrastructure reviews
- Surface risks and trade-offs early, during pull request review
- Increase cost awareness (FinOps) without introducing false precision
- Demonstrate responsible and explainable use of Generative AI
- Provide a reusable, provider-agnostic foundation for platform teams

---

## 🧠 What This Is (and What It Is Not)

### ✅ This project does
- Analyze Terraform plans using a real LLM
- Highlight risks as **hypotheses**, not facts
- Explicitly acknowledge uncertainty and missing context
- Surface **FinOps considerations** without estimating costs
- Post structured feedback directly on pull requests
- Keep humans as the final decision-makers

### ❌ This project does not
- Approve or reject changes
- Block CI/CD pipelines
- Enforce policies automatically
- Estimate cloud costs numerically
- Assume runtime behavior or usage patterns

---

## 🏗️ High-Level Architecture

```
Pull Request
   ↓
GitHub Actions
   ↓
Terraform plan + versioned prompt
   ↓
LLM (pluggable provider)
   ↓
Structured architecture review
   ↓
Comment posted on PR
```

The solution is intentionally designed to be **advisory, not authoritative**.

---

## 📁 Repository Structure

```
.
├── infra/
│   └── s3.tf
├── examples/
│   └── terraform-plan.txt
├── prompts/
│   └── architecture-review.txt
├── scripts/
│   ├── ai_review.py
│   └── llm/
│       ├── base.py
│       └── gemini.py
├── .github/workflows/
│   └── ai-architecture-review.yml
└── README.md
```

---

## 🔌 LLM Design (Provider-Agnostic)

The solution treats the LLM as a **pluggable dependency**.

- The core review logic is provider-agnostic
- Providers implement a shared interface (`LLMClient`)
- Models can be swapped via environment variables or CLI flags
- No vendor-specific logic leaks into the main workflow

Currently supported:
- **Google Gemini** (via `google-genai`)

---

## 💰 FinOps by Design (No False Precision)

Terraform plans do not contain usage or cost context.  
For this reason, the AI **never returns numeric cost estimates**.

Instead, the review:
- Surfaces **cost drivers**
- Distinguishes new resources vs. modifications
- Explicitly states uncertainty
- Frames FinOps as questions, not conclusions

---

## 🔐 Responsible AI Guardrails

- Risks are framed as **hypotheses**
- Uncertainty is explicit
- No automated enforcement
- No approvals or rejections
- Humans remain accountable

---

## 🚀 How It Works

1. A pull request modifies `.tf` files
2. GitHub Actions runs the review
3. Terraform plan + prompt are sent to the LLM
4. A structured review is generated
5. The review is posted as a PR comment

---

## 🧪 Local Usage

```bash
export GOOGLE_API_KEY="your_api_key"
export LLM_MODEL="gemini-2.5-flash"

python scripts/ai_review.py examples/terraform-plan.txt
```

---

## ⚙️ CI / GitHub Actions

The workflow installs dependencies, runs the AI review, and posts the result as a pull request comment.

Required secret:
- `GOOGLE_API_KEY`

---

## 📌 Design Limitations (By Intent)

- No cost calculation
- No policy enforcement
- No PR gating
- No runtime assumptions

---

## 🎯 Intended Audience

- Platform Engineering teams
- DevOps / SREs
- Infrastructure reviewers
- FinOps-aware teams
