---
updated: 2026-08-09
evidence_files_considered:
- path: raw/jd/acme-agentic-2026-07.md
  hash: 4833ba002b1159211b0264fafe1aae64c3c8873d6c307259b7351ee1e15d21fe
- path: raw/jd/northwind-ai-platform-2026-08.md
  hash: 9577874013916bf67c8d8687f4c2516d9179233f281ec7a6dd1944324114cdb2
- path: raw/research/agentic-stack-2026.md
  hash: 718c66c3049a37392bba25b4394d1bcaf8da3289d58d4d1474790c73a3f4510b
---

> **Seed content.** These conclusions were compiled from the placeholder
> evidence files shipped with the repo, which are fictional. Replace the evidence
> with real job descriptions and research, then ask your agent to recompile.

## Skill priority ranking (with reasoning)

1. **Agentic Frameworks** — named explicitly in every scanned JD, usually in the
   first three bullets. Orchestration and tool design are the load-bearing skills;
   depth here returns more than breadth across frameworks.
2. **LLM Fundamentals** — the area interviewers use to separate people who wire
   APIs together from people who can debug bad output. Retrieval quality and
   structured-output reliability come up repeatedly.
3. **Data Structures & Algorithms** — absent from every JD, but it is the gate in
   the first technical round at most target companies. High cost of failure, so it
   cannot be deprioritised despite not being "the job".
4. **Databases & Data Layer** — the existing baseline is strongest here, so the
   marginal value of study time is lowest. Vector stores and agent state
   persistence are the exceptions and are marked min-required.

## Minimum bar for Senior Agentic AI Engineer

The 21 topics marked `min_required: true` constitute the bar. Grouped:

- **Can build an agent that works:** agent loop fundamentals, LangGraph state
  machines, tool/function calling design, MCP servers.
- **Can show it works:** agent evaluation and tracing. Both JDs name evaluation as
  a hard requirement, and the research notes flag it as the most commonly
  under-invested area. This is the single highest-leverage gap.
- **Can make retrieval good:** embeddings and vector search, RAG architecture,
  vector databases.
- **Can reason about the model:** tokenisation and context economics, prompting
  technique, structured output.
- **Can pass the coding round:** complexity analysis, arrays/two pointers, hash
  maps, binary search, trees and graphs, dynamic programming.
- **Can persist state:** SQL, schema design, transactions, agent state persistence.

## Per-skill topic requirements

**Agentic Frameworks** — Orchestration is expected to be state-machine-shaped
(explicit graph, conditional edges, checkpointing), not a linear chain. Tool design
is judged on reliability rather than demos: schema quality, error semantics,
partial-failure handling. Evaluation and tracing are required. Multi-agent is
nice-to-have only.

**LLM Fundamentals** — Retrieval work is judged on measurement: retrieval quality
must be assessable separately from generation quality. Chunking strategy comes up
more than embedding-model choice. Structured output is expected to be reliable
under adversarial input. Fine-tuning is framed as something to know when *not* to do.

**Data Structures & Algorithms** — Ordinary interview DSA, not AI-specific. Dynamic
programming is the standing weak spot and carries the most interview risk.

**Databases & Data Layer** — pgvector versus a dedicated store should be a
defensible operational choice. Agent state persistence and checkpointing are named
directly in one JD and are not currently covered at all.

## Open contradictions / questions for the human

- **Multi-agent weighting.** One JD lists multi-agent systems as nice-to-have; the
  research notes argue it is over-discussed relative to demand. Currently marked
  `min_required: false`. Confirm that is the call you want.
- **DSA weighting.** DSA appears in no job description but gates the first round.
  It is ranked 3rd as a compromise between "not the job" and "fails you fastest".
  If your target companies skip the algorithmic round, this should drop to 4th.
- **Evaluation has no owner topic yet.** `agent-evaluation` is `not-started` and
  min-required, and is the largest single gap against the compiled bar. Worth
  confirming before it is set as focus.
- **Evidence is synthetic.** Every conclusion above derives from placeholder files.
  Treat the ranking as a worked example, not advice.
