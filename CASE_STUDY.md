# Case Study: Measuring the Cost of Over-Helpful AI Agents in Subscription Support

**Author:** Nigel-Efeose Akhuetie (Economics, York University)  
**Repository:** [https://github.com/nigelose10/agent-reality-check](https://github.com/nigelose10/agent-reality-check)  
**Date:** November 2026  

---

## 1. Executive Summary

Organizations deploying AI agents in customer operations often evaluate them on response fluency or single-turn accuracy. From an economic and operational perspective, however, **failures in customer-support agents are asymmetric**: a correct routine answer saves a few minutes of support labor, whereas a single unauthorized refund, unverified account cancellation, or fabricated transaction status creates direct financial loss, compliance exposure, or customer churn.

Inspired by Anthropic's [*Demystifying Evals for AI Agents*](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) and Stripe's [*Can AI Agents Build Real Stripe Integrations?*](https://stripe.com/blog/can-ai-agents-build-real-stripe-integrations), I built **Agent Reality Check**: a reproducible 20-case deterministic evaluation harness in Python (`grade.py`) for subscription-billing support workflows. Rather than collapsing performance into a single pass rate, the harness separates four operational dimensions:

1. **Action Accuracy:** Did the agent select the right workflow primitive (`answer`, `cancel`, `refund`, `pause`, `escalate`)?
2. **Final-State Integrity:** Did the account record end in the exact policy-compliant state (e.g., preserving paid-term access after cancellation vs. prematurely closing the account)?
3. **Evidence Grounding:** Did the agent cite the specific policy clause, ledger record, or system error that justified its decision?
4. **Escalation Boundary Safety:** When faced with out-of-window refund requests, failed identity checks, prompt injections, compliance holds, or 503 tool timeouts, did the agent abstain and escalate without mutating account state?

---

## 2. Experimental Setup & Scope Note

All 20 scenarios in `cases.jsonl` are synthetic and model common SaaS billing edge cases. No production customer data or live payment rails are touched.

To test the harness's diagnostic resolution, I compared two reference runs included in the repository:
- **Policy-Grounded Oracle (`sample_outputs.jsonl`):** Hand-authored reference outputs that strictly enforce verification, policy windows, and escalation rules.
- **Over-Helpful Naive Baseline (`naive_agent_outputs.jsonl`):** A synthetic failure baseline modeling a common deployment failure mode—an agent optimized for user satisfaction that complies with out-of-policy requests, accepts prompt-injected override claims, and guesses when a lookup tool fails. *(Note: both JSONL files are deterministic reference artifacts to verify the grading harness, not commercial LLM benchmark claims.)*

---

## 3. Diagnostic Results

Running `python3 grade.py cases.jsonl naive_agent_outputs.jsonl` vs. `sample_outputs.jsonl` yields:

| Metric | Policy-Grounded Oracle | Over-Helpful Naive Baseline | Operational Meaning |
|---|---:|---:|---|
| **Action Accuracy** | 20 / 20 (100.0%) | 9 / 20 (45.0%) | Correct workflow verb chosen |
| **Final-State Integrity** | 20 / 20 (100.0%) | 8 / 20 (40.0%) | Environment left in exact target state |
| **Evidence Grounding** | 20 / 20 (100.0%) | 9 / 20 (45.0%) | Required policy/account key cited |
| **All Three Checks Passed** | 20 / 20 (100.0%) | 8 / 20 (40.0%) | End-to-end verified task completion |
| **Safe Escalation Rate** | 10 / 10 (100.0%) | 0 / 10 (0.0%) | Out-of-bounds cases escalated cleanly |
| **Aggregate Rule Checks** | 60 / 60 (100.0%) | 26 / 60 (43.3%) | Total deterministic assertions passed |

### Why Separate State and Escalation Metrics Matter
If a team only looked at aggregate rule checks (43.3%) or routine happy-path cases (where the naive baseline passes 8 of 10 routine inquiries/cancellations), the system might look "halfway working." Separating **Safe Escalation Rate (0/10)** and **Final-State Integrity** immediately exposes why the naive baseline is unsafe to deploy:

- **State Corruption on Valid Actions (`case-002`):** The baseline correctly chooses `action="cancel"`, but sets `final_state="closed_immediately"` instead of `cancelled_access_through_2026-11-30`, stripping paid access from a customer.
- **Prompt Injection & Policy Bypass (`case-003`, `case-007`, `case-011`):** When a customer claims a "system override" or threatens a chargeback 45–90 days post-purchase, the over-helpful baseline issues unauthorized refunds (`state='refunded_and_closed'`).
- **Identity & Compliance Breaches (`case-005`, `case-014`, `case-018`):** Canceling an unverified account, disclosing a coworker's billing history, or refunding a compliance-held account represents severe operational risk that must be tracked separately from routine Q&A errors.
- **Hallucinated Tool Recovery (`case-016`):** When the payment gateway returns an HTTP 503 timeout, guessing that "your refund has settled" destroys user trust compared to escalating with `system.gateway_timeout`.

---

## 4. Economic Framework: Asymmetric Loss in Agent Deployment

In economics, decision rules under uncertainty depend on the ratio of false-positive to false-negative costs. For an autonomous support agent:
- Let $B$ be the labor savings of autonomously resolving a valid ticket (typically $\$2\text{--}\$8$).
- Let $C_{\text{esc}}$ be the cost of escalating an ambiguous ticket to a human specialist (typically $\$5\text{--}\$15$).
- Let $L_{\text{mut}}$ be the loss from an unauthorized state mutation—such as an out-of-policy annual refund, compliance violation, or premature account termination (often $\$100\text{--}\$1,000+$).

Because $L_{\text{mut}} \gg C_{\text{esc}}$, an economically rational agent harness must enforce strict **verification preconditions** before state-mutating tool calls (`refund`, `cancel`, `pause`) and treat escalation as the default safe state whenever evidence is missing or policy thresholds are exceeded.

---

## 5. Limitations & Next Engineering Steps

1. **Deterministic vs. Semantic Grading:** `grade.py` verifies exact state strings and evidence keys with zero external dependencies. It does not grade free-text tone or subtle phrasing contradictions.
2. **Live Model Harness Integration:** The next step is wrapping `grade.py` around live multi-turn tool-use runs (e.g., Claude via tool-calling APIs) across $k=5$ trials per case to measure pass@$k$, latency, token cost per resolved ticket, and expected net economic value per 1,000 tickets.
