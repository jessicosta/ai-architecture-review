import os
import sys
import argparse
from llm.gemini import GeminiClient


# ============================================================
# Argument parsing (reusability starts here)
# ============================================================

parser = argparse.ArgumentParser(
    description="AI-assisted Architecture Review for Infrastructure Changes"
)

parser.add_argument("plan_file", help="Terraform plan file")
parser.add_argument(
    "--model",
    default=os.getenv("LLM_MODEL", "gemini-2.5-flash"),
    help="LLM model to use (default: gemini-2.5-flash)",
)
parser.add_argument(
    "--temperature",
    type=float,
    default=0.2,
    help="LLM temperature (default: 0.2)",
)
parser.add_argument(
    "--max-tokens",
    type=int,
    default=2048,
    help="Maximum output tokens (default: 2048)",
)

args = parser.parse_args()


# ============================================================
# File validation
# ============================================================

PROMPT_FILE = "prompts/architecture-review.txt"

if not os.path.exists(args.plan_file):
    print(f"Terraform plan file not found: {args.plan_file}")
    sys.exit(1)

if not os.path.exists(PROMPT_FILE):
    print(f"Prompt file not found: {PROMPT_FILE}")
    sys.exit(1)


# ============================================================
# Read inputs
# ============================================================

with open(args.plan_file, "r") as f:
    terraform_plan = f.read()

with open(PROMPT_FILE, "r") as f:
    system_prompt = f.read()


# ============================================================
# Build final prompt (provider-agnostic)
# ============================================================

full_prompt = f"""
{system_prompt}

---
Terraform plan:
{terraform_plan}

Formatting requirements:
- Respond in plain Markdown
- Produce a single, continuous response
- Include the following sections:
  - Summary
  - Risks (clearly marked as hypotheses)
  - Questions for Human Review
- Do not approve or reject the change
- Do not recommend automated actions
"""


# ============================================================
# Initialize LLM client (pluggable)
# ============================================================

llm = GeminiClient(
    model=args.model,
    temperature=args.temperature,
    max_output_tokens=args.max_tokens,
)


# ============================================================
# Generate review
# ============================================================

print("### 🤖 AI-assisted Architecture Review\n")

output = []

for chunk in llm.generate(full_prompt):
    output.append(chunk)
    print(chunk, end="", flush=True)

print("\n\n---\nEnd of AI review\n")


# ============================================================
# Persist output
# ============================================================

with open("ai_review_output.md", "w") as f:
    f.write("# AI-assisted Architecture Review\n\n")
    f.write("".join(output))

print("📄 Review saved to ai_review_output.md")