---
updated: 2026-08-10
evidence_files_considered:
- path: raw/research/agentic-ai-engineer-study-plan.md
  hash: a56babee17c739e01e904bf8a061c37f81a7cccc37d7085235bc455a0a1cea06
- path: raw/research/one-month-plan.md
  hash: 8d81b4626214c651b141647851295c40797dea1fcebb6b8b838409765532f076
- path: raw/research/rubric-r1-llm-fundamentals-2026-08-10.md
  hash: 570babf02d809fe26b5f09f7c3017f38988812bc4e06aa414bce668f8543358c
- path: raw/research/rubric-r2-rag-2026-08-10.md
  hash: dd697780d14c62634f3ad4e7421b464f475d65d792567276559e2f2571157b71
- path: raw/research/rubric-r3-agentic-2026-08-10.md
  hash: 2ec2dce0c169493bb9fc7be576361cd1b764caa653335f3a4ee0addabe71ad3f
- path: raw/research/rubric-r4-vector-sql-2026-08-10.md
  hash: 6ed3e268e93d15d9a5edddd844315c2dc009e5a5d421dff80125c29acd39cfb2
- path: raw/research/rubric-r5-obs-security-2026-08-10.md
  hash: 67ad4399b71a82af33ad06bde1a22b2e93b50c3d615fa3267085c3bab777ce9e
- path: raw/research/senior-genai-bare-minimum.md
  hash: b60c95bfc2ad119c5e053da021909ff322302ab5b82f7634a7271116785ce63b
---

## Skill priority ranking (with reasoning)

Spine remains the **30-day intensive plan**. Skill order unchanged.

1. **LLM Fundamentals** — P0. Rubrics upgraded from R1 deep research (transformers/GQA/RoPE, tokenization budgets, context engineering + prompt caching, resilient multi-provider APIs).
2. **RAG Systems** — P0. Rubrics from R2 (ingestion/contextual retrieval, hybrid+filterable ANN, eval bias control, symptom→pattern advanced RAG).
3. **Agentic Systems & Frameworks** — P0. Rubrics from R3 (+ prior agentic study plan): LangGraph durability/HITL, LCEL limits, multi-agent orchestration, tracing, benchmarks/CI, test-time compute, agentic guardrails.
4. **Python Mastery** — P1. Rubrics tightened from senior engineering bar (no external research).
5. **Python Production Stack** — P1. Streaming/auth failure modes from R5; Pydantic/FastAPI core tightened.
6. **DSA (NeetCode)** — P1 parallel track at **1 problem/day** in NeetCode roadmap order. UI topics are pattern sections; per-problem checklist lives in `data/skills/dsa/_neetcode-progress.md` (#1–#75 now, Graphs+DP next). Slower than the old 2/day plan — acceptable if blind-attempt quality holds.
7. **Architecture & System Design** — P2 fluency rubrics tightened.
8. **Databases & Data Layer** — P2. Vector+SQL rubrics from R4 (Qdrant/Weaviate + Postgres AI-backend bar).
9. **Production Engineering & Security** — P2. Observability + AppSec/LLM security from R5; clear split vs agentic guardrails.

**Still deferred:** deep K8s/IaC/CI/CD/cloud, ethics, multimodal deep-dive, GenAI-specific DSA extras. Agent PEFT remains optional.

## Minimum bar for Senior Python GenAI / RAG / Agentic Engineer

Every `min_required: true` topic. Pass/fail for `comfortable` is the topic's **What "enough" looks like** block.

For DSA pattern topics: section checklist complete + timed re-solves (not merely "watched NeetCode video").

## Per-skill topic requirements

**LLM / RAG / Agents** — Probe with rubric questions before upgrading status. Prefer "has built/debugged" over "has read".

**DSA (NeetCode)** — 1/day in listed order. Tell the agent each finished problem to check `_neetcode-progress.md`. After a full pattern section, probe + status upgrade. Continue into Graphs then DP after #75 — stopping at backtracking is not interview-complete.

**Python / FastAPI / Architecture** — Standard senior software bar; judge with code + trade-off probes.

**Databases / Production** — GenAI-shaped: hybrid vector ops, Postgres for AI services, OTel/LLM metrics, OWASP LLM + AppSec split from agentic guardrails.

## Open contradictions / questions for the human

- **Skill order still LLM→RAG→Agents.** Agentic guide is agentic-first; say yes if you want Agentic promoted to #1.
- **multi-agent-mcp vs mcp-architecture.** Rubrics now split orchestration vs protocol; titles still overlap — rename topic later if you want cleaner UI.
- **Rubric docs may overfit 2026 vendor details** (FlashAttention-3, specific OTel attribute names). Reward concepts + correct trade-offs; don't require memorizing every attribute string.
- **DSA pace vs old plan.** Old plan wanted 2/day; you do 1/day. We adopted 1/day as the official track. If a coding round is <6 weeks away, consider 2/day on weak patterns only.
- **GenAI topics still mostly not-started.** DSA `nc-arrays-hashing` is `learning` under the NeetCode track.
