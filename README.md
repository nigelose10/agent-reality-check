# Agent Reality Check: Deterministic Evaluation for AI Support Workflows

A reproducible Python evaluation benchmark for testing whether an AI support agent resolves subscription-billing cases accurately, preserves exact account state, cites required policy/ledger evidence, and escalates safely when requests fall outside policy or verification boundaries.

Built by **Nigel-Efeose Akhuetie** (Economics, York University). Read the full write-up in [`CASE_STUDY.md`](CASE_STUDY.md).

## Why This Exists

- **Anthropic** ([*Demystifying Evals for AI Agents*](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)) highlights that evaluating agents requires verifying both the trajectory and the final environment state—and notes that product, operations, and economics-minded contributors play a central role in defining what "done correctly" means.
- **Stripe** ([*Can AI Agents Build Real Stripe Integrations?*](https://stripe.com/blog/can-ai-agents-build-real-stripe-integrations)) demonstrates the gap between generating plausible text/code and reliably completing end-to-end operational tasks under strict constraints.

In customer operations, errors have **asymmetric economic cost**: a routine answer saves a few dollars of support time, while an unauthorized refund, unverified account cancellation, or hallucinated settlement status after a 503 timeout causes direct financial and compliance loss. This harness measures those failure modes explicitly.

## Repository Contents

| File | Description |
|---|---|
| `cases.jsonl` | 20 synthetic subscription-support scenarios spanning routine inquiries, prorated upgrades, duplicate charges, 30-day refund boundaries, prompt-injection overrides, failed identity checks, 503 tool timeouts, and compliance holds. |
| `grade.py` | Zero-dependency Python 3.10+ deterministic grader reporting Action Accuracy, Final-State Integrity, Evidence Grounding, Safe Escalation Rate, and specific unauthorized state mutations. |
| `sample_outputs.jsonl` | Policy-grounded oracle outputs (20/20 across all dimensions) demonstrating expected schema and boundary adherence. |
| `naive_agent_outputs.jsonl` | Synthetic failure baseline (8/20 full pass, 0/10 safe escalation) illustrating how an "over-helpful" agent fails via unauthorized state mutations. |
| `test_grade.py` | Unit test suite (`unittest`) verifying dataset integrity, oracle grading, and boundary-violation detection. |
| `CASE_STUDY.md` | Research & engineering memo detailing the evaluation taxonomy, diagnostic table, and asymmetric-loss economic framework. |

## Scope & Integrity Note

All 20 cases are synthetic; no real customer data or payment provider is used. Both `sample_outputs.jsonl` and `naive_agent_outputs.jsonl` are deterministic reference artifacts designed to test and demonstrate the grading harness—not claims about commercial LLM benchmark scores.

## Quickstart

Requires Python 3.10+ (standard library only):

```bash
# 1. Run unit tests
python3 test_grade.py

# 2. Grade the policy-grounded reference oracle (100% pass)
python3 grade.py cases.jsonl sample_outputs.jsonl

# 3. Grade the over-helpful naive baseline (exposes 10 unauthorized mutations)
python3 grade.py cases.jsonl naive_agent_outputs.jsonl
```

## Output Schema

To evaluate an agent run, output one JSON object per line in `your_outputs.jsonl`:

```json
{"case_id":"case-001","action":"answer|cancel|refund|pause|escalate","resolution":"...","evidence":["account.renewal_date"],"final_state":"open"}
```

Then run:

```bash
python3 grade.py cases.jsonl your_outputs.jsonl
```
