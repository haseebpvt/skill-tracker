---
updated: 2026-08-10
evidence_files_considered:
- path: raw/research/agentic-ai-engineer-study-plan.md
  hash: a56babee17c739e01e904bf8a061c37f81a7cccc37d7085235bc455a0a1cea06
- path: raw/research/one-month-plan.md
  hash: 8d81b4626214c651b141647851295c40797dea1fcebb6b8b838409765532f076
- path: raw/research/senior-genai-bare-minimum.md
  hash: b60c95bfc2ad119c5e053da021909ff322302ab5b82f7634a7271116785ce63b
---

## Skill priority ranking (with reasoning)

This tracker remains the **30-day intensive plan** as the spine. New evidence
(`raw/research/agentic-ai-engineer-study-plan.md`) deepens **Agentic Systems**
rather than reshuffling skill order.

1. **LLM Fundamentals** — Week 1 days 1–4. Job-title P0. Never cut.
2. **RAG Systems** — Week 1 days 5–7 (+ Day 16 advanced patterns). Job-title P0. Never cut.
3. **Agentic Systems & Frameworks** — Days 13, 15–16 (P0) **plus** the 2026 Senior
   Agentic AI Engineer curriculum: workflows vs agents, MCP depth, framework
   selection, failure modes, test-time compute, memory, guardrails, eval/benchmarks.
   Never cut.
4. **Python Mastery** — Week 2 days 8–10 & 14. P1 coding deep-dives.
5. **Python Production Stack** — Week 2 days 11–12. P1. Never cut (FastAPI + streaming).
6. **Data Structures & Algorithms** — Daily 2 problems. P1 parallel track.
7. **Architecture & System Design** — Week 3 days 17–18 & 21. P2 fluency, not mastery.
8. **Databases & Data Layer** — Week 3 days 19–20. P2.
9. **Production Engineering & Security** — Week 4 days 22–24. P2; cut here before
   touching P0/P1 if time collapses. Overlaps agentic guardrails — treat agentic
   guardrails as the GenAI-specific layer; keep AppSec here.

**Deferred (add later):** K8s details, IaC, CI/CD deep-dive, cloud, general LLMOps
serving, ethics/regulatory, multimodal deep-dive, GenAI-specific DSA. Backlog in
`raw/research/senior-genai-bare-minimum.md`. Agent PEFT / trajectory SFT is in the
tracker as optional (`min_required: false`).

## Minimum bar for Senior Python GenAI / RAG / Agentic Engineer

Minimum bar = every `min_required: true` topic across the nine skills.

**Delta from the Agentic study plan (now in-bar under Agentic Systems):**
- Choose workflow vs agent with failure-cost reasoning; know the six design patterns.
- MCP architecture (JSON-RPC, transports, tools/resources/prompts) + poka-yoke tools.
- Framework selection: LangGraph vs OpenAI Agents SDK vs PydanticAI vs CrewAI.
- Agentic failure modes and concrete mitigations.
- Test-time compute / reasoning-model routing and async delivery (queues + SSE).
- Episodic vs semantic agent memory.
- Layered agentic guardrails (edge / NeMo / Guardrails AI).
- Agent benchmarks awareness (SWE-bench, GAIA, Tau-bench) + LLM-as-judge CI gates.

Gut-check milestones (unchanged from 30-day plan):
- **End Week 1:** Whiteboard full RAG; call APIs with tools + streaming from memory.
- **End Week 2:** Production Python + FastAPI SSE/JWT + LangGraph RAG with routing.
- **End Week 3:** Whiteboard distributed GenAI (agents, DBs, caches, queues) + patterns.
- **End Week 4:** Talk observability/security/reliability; medium LC in ~20 min.

## Per-skill topic requirements

**LLM / RAG** — Unchanged: depth + tiny builds. Advanced RAG still covers Self-RAG /
CRAG / GraphRAG named in the agentic guide.

**Agentic Systems** — Expanded. Interview bar is no longer "build a ReAct loop" alone.
Must argue when *not* to use agents, pick frameworks by durable-state needs, design
MCP tools, handle silent agent failures, and plan for long-thinking models.

**Python / FastAPI** — Unchanged. Async + structured outputs remain load-bearing for agents.

**DSA** — Unchanged. Mornings only.

**Architecture / DBs / Production** — Unchanged spine; agentic security depth lives
primarily under Agentic → guardrails, with OWASP AppSec still under Production.

## Open contradictions / questions for the human

- **Skill order unchanged.** The new guide is agentic-first; our order still puts
  LLM → RAG → Agents (30-day Week 1 logic). Propose promoting Agentic Systems to #1
  if you want the tracker to match that guide — needs your yes before `update_role_order`.
- **Overlap kept on purpose.** Multi-agent & MCP still exists alongside the deeper
  MCP Architecture topic; evaluation sits beside new benchmarks/CI topic. Tell me if
  you want these merged to reduce count.
- **Agent PEFT left optional.** Guide treats trajectory SFT / MoR as staple; 30-day
  crunch still defers deep fine-tuning. Promote to min-required if your target JDs demand it.
- **Completion still blank.** All topics `not-started` until you report what's done.
