#!/usr/bin/env python3
"""Seed a ruthless 30-day crunch path from one_month_plan.md.

P3 areas (deep K8s/IaC/CI/CD/ethics/LLMOps) are omitted on purpose — add later
if time allows. All topics start as not-started.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from core.repo import Repo
from core.validate import validate

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "raw" / "research"

# (skill_id, name, description, topics)
# topic: (title, topic_id, min_required, enough)
SKILLS: list[tuple[str, str, str, list[tuple[str, str, bool, list[str]]]]] = [
    (
        "llm-fundamentals",
        "LLM Fundamentals",
        "Week 1 days 1–4 (P0). Models, tokens, decoding, prompting, API integration.",
        [
            (
                "Transformer architecture",
                "transformer-architecture",
                True,
                [
                    "Explain self-attention (QKV), multi-head attention, positional encoding",
                    "Describe FFN, layer norm, residuals, encoder-decoder vs decoder-only",
                    "Name MQA/GQA/Flash Attention and when they matter",
                ],
            ),
            (
                "Tokenization & context budgets",
                "tokenization",
                True,
                [
                    "Contrast BPE / WordPiece / SentencePiece / tiktoken",
                    "Count tokens, manage budgets, handle special tokens",
                ],
            ),
            (
                "Inference & decoding",
                "inference-decoding",
                True,
                [
                    "Explain temperature, top-k, top-p, greedy vs beam, stop sequences",
                    "Use structured generation (JSON mode / constrained decoding)",
                ],
            ),
            (
                "Model landscape & selection",
                "model-landscape",
                True,
                [
                    "Compare closed vs open-weight models and embedding options",
                    "Pick a model with explicit cost / latency / context / license / privacy trade-offs",
                ],
            ),
            (
                "Prompt engineering",
                "prompt-engineering",
                True,
                [
                    "Use roles, zero/few-shot, CoT, ReAct, structured-output prompting",
                    "Apply defensive prompting and prompt chaining",
                ],
            ),
            (
                "LLM API integration",
                "llm-api-integration",
                True,
                [
                    "Ship a script with tool calling, streaming, retries, and cost awareness",
                    "Use openai / anthropic / google-genai SDKs; handle rate limits and failover",
                ],
            ),
        ],
    ),
    (
        "rag",
        "RAG Systems",
        "Week 1 days 5–7 + Day 16 advanced patterns (P0). Build, evaluate, and extend RAG.",
        [
            (
                "Ingestion, chunking & embeddings",
                "rag-ingestion",
                True,
                [
                    "Parse docs, choose chunking, extract metadata",
                    "Explain dense vs sparse embeddings and pick a model",
                ],
            ),
            (
                "Vector indexes & hybrid search",
                "rag-search",
                True,
                [
                    "Explain HNSW/IVF/quantization and distance metrics",
                    "Implement semantic + BM25 + RRF hybrid search with metadata filters",
                ],
            ),
            (
                "Reranking, query transforms & generation",
                "rag-rerank-context",
                True,
                [
                    "Apply rerankers and query transforms (HyDE, multi-query, decomposition)",
                    "Mitigate lost-in-the-middle; RAG prompts with citations / I-don't-know; stream answers",
                ],
            ),
            (
                "RAG evaluation",
                "rag-evaluation",
                True,
                [
                    "Define faithfulness, relevance, context precision/recall, MRR/nDCG",
                    "Run RAGAS or DeepEval on a small golden set; use LLM-as-a-judge carefully",
                ],
            ),
            (
                "Advanced RAG patterns",
                "advanced-rag-patterns",
                True,
                [
                    "Explain CRAG / Self-RAG / Adaptive / RAPTOR / conversational / agentic / Graph RAG",
                    "Pick a pattern for a concrete retrieval failure mode",
                ],
            ),
        ],
    ),
    (
        "agentic-systems",
        "Agentic Systems & Frameworks",
        "Days 13, 15–16 (P0). Never cut. Agents, LangGraph/LangChain, MCP.",
        [
            (
                "Agent loop fundamentals",
                "agent-loop-fundamentals",
                True,
                [
                    "Implement ReAct, reflection, task decomposition, tool schemas + error handling",
                    "Manage short-term vs long-term memory and structured outputs",
                ],
            ),
            (
                "LangGraph state machines",
                "langgraph-state-machines",
                True,
                [
                    "Build StateGraph with schema, conditional edges, checkpointing, HITL, streaming",
                    "Rebuild a RAG chain as LangGraph with routing",
                ],
            ),
            (
                "LangChain fluency",
                "langchain-fluency",
                True,
                [
                    "Build a RAG chain with LCEL, retrievers, output parsers, callbacks",
                    "Know LlamaIndex at awareness level only",
                ],
            ),
            (
                "Multi-agent & MCP",
                "multi-agent-mcp",
                True,
                [
                    "Design supervisor/router teams; try one of CrewAI / AutoGen / OpenAI Agents SDK",
                    "Build a Python MCP server (tools/resources/prompts)",
                ],
            ),
            (
                "Agent evaluation & tracing",
                "agent-evaluation",
                True,
                [
                    "Trace trajectories (LangSmith or equiv), detect loops, track cost per step",
                ],
            ),
        ],
    ),
    (
        "python-mastery",
        "Python Mastery",
        "Week 2 days 8–10 & 14 (P1). Object model, concurrency, typing, testing.",
        [
            (
                "Object model, descriptors & dunders",
                "python-object-model",
                True,
                [
                    "Explain mutable vs immutable args; implement a descriptor and key dunders",
                    "Basic metaclasses / type awareness",
                ],
            ),
            (
                "Generators, imports & scoping",
                "python-generators-imports",
                True,
                [
                    "Use yield / yield from / send; resolve circular imports; closures + nonlocal",
                ],
            ),
            (
                "Concurrency & asyncio",
                "python-concurrency",
                True,
                [
                    "Choose threads vs processes vs asyncio; write producer-consumer both ways",
                    "Use TaskGroup/gather and bridge sync/async when needed",
                ],
            ),
            (
                "Typing & pytest quality",
                "python-typing-testing",
                True,
                [
                    "Annotate with generics/TypedDict/overload; validate with Pydantic + mypy/pyright",
                    "Write pytest fixtures, parametrize, asyncio tests, and mocks",
                ],
            ),
        ],
    ),
    (
        "python-production-stack",
        "Python Production Stack",
        "Week 2 days 11–12 (P1). FastAPI + Pydantic serving LLMs. Never cut.",
        [
            (
                "Pydantic v2",
                "pydantic-v2",
                True,
                [
                    "Use BaseModel, validators, discriminated unions, BaseSettings",
                    "Produce tool schemas via model_json_schema()",
                ],
            ),
            (
                "FastAPI core & DI",
                "fastapi-core",
                True,
                [
                    "Routes, validation, Depends (incl. yield), middleware/CORS",
                ],
            ),
            (
                "FastAPI streaming, auth & clients",
                "fastapi-streaming-auth",
                True,
                [
                    "Stream LLM tokens via SSE; JWT/API-key auth; lifespan; TestClient",
                    "Use httpx + tenacity for resilient async HTTP",
                ],
            ),
        ],
    ),
    (
        "dsa",
        "Data Structures & Algorithms",
        "Daily parallel track — 2 problems/day, ~60 over 30 days (P1). Patterns over quantity.",
        [
            (
                "Arrays, strings & hash tables",
                "arrays-hash-tables",
                True,
                [
                    "Solve two-pointer, sliding window, prefix sum, Kadane, frequency, N-Sum in ~20–25 min",
                ],
            ),
            (
                "Stacks, queues, heaps & linked lists",
                "stacks-queues-heaps-lists",
                True,
                [
                    "Monotonic stack, deque/heapq Top-K, linked-list fast/slow + LRU",
                ],
            ),
            (
                "Trees, tries & binary search",
                "trees-tries-binary-search",
                True,
                [
                    "BST traversals, Trie, LCA, binary search (classic + on-answer)",
                ],
            ),
            (
                "Graphs",
                "graphs",
                True,
                [
                    "BFS/DFS, topological sort, cycle detection, Dijkstra, Union-Find",
                ],
            ),
            (
                "Recursion, DP & greedy",
                "recursion-dp-greedy",
                True,
                [
                    "Backtracking, 1D/2D DP (coin change, LCS, knapsack), greedy intervals",
                ],
            ),
        ],
    ),
    (
        "architecture-system-design",
        "Architecture & System Design",
        "Week 3 days 17–18 & 21 (P2). Fluent talk for whiteboard rounds — not expert depth.",
        [
            (
                "Python design patterns",
                "design-patterns",
                True,
                [
                    "Implement strategy, decorator, DI, context manager, repository/service, retry, circuit breaker",
                ],
            ),
            (
                "Distributed system principles",
                "system-architecture",
                True,
                [
                    "Trade off monolith/microservices/events; CAP, scaling, caching, queues, consistency",
                ],
            ),
            (
                "API design for GenAI",
                "api-design",
                True,
                [
                    "REST + pagination/versioning/rate limits/auth; SSE/WebSockets for LLM streaming",
                ],
            ),
        ],
    ),
    (
        "databases",
        "Databases & Data Layer",
        "Week 3 days 19–20 (P2). SQL, Redis/Mongo basics, vector DBs hands-on.",
        [
            (
                "SQL engineering",
                "sql-engineering",
                True,
                [
                    "ACID/MVCC, indexes, isolation, EXPLAIN, CTEs/windows, N+1, SQLAlchemy/asyncpg safely",
                ],
            ),
            (
                "Redis & document/graph stores",
                "nosql-stores",
                True,
                [
                    "Redis cache/locks; Mongo schema/index basics; Neo4j/KG awareness for Graph RAG",
                ],
            ),
            (
                "Vector databases & pipelines",
                "vector-databases",
                True,
                [
                    "Hands-on with 2 of Qdrant/Chroma/pgvector; hybrid search + metadata schema",
                    "Batch embedding / incremental indexing awareness",
                ],
            ),
        ],
    ),
    (
        "production-engineering",
        "Production Engineering & Security",
        "Week 4 days 22–24 (P2). Observability, AppSec + LLM security, reliability. Cut after P0/P1 if time dies.",
        [
            (
                "Observability & LLM observability",
                "observability",
                True,
                [
                    "Logs/metrics/traces, RED/golden signals, OpenTelemetry basics",
                    "Track tokens, TTFT, cost, prompt logs, RAG provenance",
                ],
            ),
            (
                "App + LLM security",
                "security",
                True,
                [
                    "OWASP Top 10, OAuth2/JWT, secrets; OWASP LLM Top 10, prompt injection, PII redaction",
                ],
            ),
            (
                "Reliability & performance",
                "reliability-performance",
                True,
                [
                    "Circuit breaker, retry+jitter, timeouts, idempotency, rate limits, health checks",
                    "Profile hotspots; reason about P95/P99 and simple load tests",
                ],
            ),
        ],
    ),
]


def write_role(repo: Repo) -> None:
    (repo.root / "data" / "role.md").write_text(
        """\
---
role: Senior Python GenAI / RAG / Agentic Engineer
level: Senior
updated: 2026-08-09
skill_order: []
---

**30-day intensive path** (from `evidence/raw/research/one-month-plan.md`).

Strategy: nail specialization first (LLM / RAG / Agents), then Python + FastAPI,
then system design / DBs / production. Daily DSA in parallel.

Intentionally deferred for later (add if you get more time): deep K8s, IaC,
CI/CD specifics, cloud deep-dive, LLMOps/serving, ethics/regulatory, GenAI-specific
DSA, multimodal deep-dive. See `senior-genai-bare-minimum.md` as the backlog.
""",
        encoding="utf-8",
    )


def copy_evidence() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    src = Path.home() / "Downloads" / "one_month_plan.md"
    dest = EVIDENCE / "one-month-plan.md"
    body = src.read_text(encoding="utf-8").replace("- [x]", "- [ ]").replace("- [X]", "- [ ]")
    dest.write_text(
        "---\n"
        'source: "30-day intensive prep plan — Senior Python GenAI/RAG/Agentic"\n'
        "added: 2026-08-09\n"
        "---\n\n" + body,
        encoding="utf-8",
    )
    # Keep bare-minimum as backlog reference only (not wired into min_required).
    backlog = Path.home() / "Downloads" / "senior_genai_engineer_bare_minimum.md"
    if backlog.is_file():
        text = backlog.read_text(encoding="utf-8").replace("- [x]", "- [ ]").replace("- [X]", "- [ ]")
        (EVIDENCE / "senior-genai-bare-minimum.md").write_text(
            "---\n"
            'source: "Bare-minimum backlog — add after the 30-day path"\n'
            "added: 2026-08-09\n"
            "---\n\n" + text,
            encoding="utf-8",
        )


def main() -> None:
    skills_dir = ROOT / "data" / "skills"
    if skills_dir.exists():
        shutil.rmtree(skills_dir)
    skills_dir.mkdir(parents=True)

    copy_evidence()
    repo = Repo(ROOT)
    write_role(repo)

    evidence_refs = ["raw/research/one-month-plan.md"]

    for index, (skill_id, name, description, topics) in enumerate(SKILLS, start=1):
        repo.add_skill(skill_id, name, priority=index, description=description)
        for t_index, (title, topic_id, min_required, enough) in enumerate(topics, start=1):
            repo.add_topic(
                skill_id,
                title,
                topic_id=topic_id,
                status="not-started",
                priority=t_index,
                min_required=min_required,
                evidence=evidence_refs,
                enough=enough,
                notes="30-day crunch path; status not-started until demonstrated",
            )

    repo.set_focus(
        [
            ("llm-fundamentals", "transformer-architecture"),
            ("llm-fundamentals", "tokenization"),
            ("llm-fundamentals", "inference-decoding"),
        ]
    )

    conclusions = """\
## Skill priority ranking (with reasoning)

This tracker is the **30-day intensive plan only**. P3 depth is deferred.

1. **LLM Fundamentals** — Week 1 days 1–4. Job-title P0. Never cut.
2. **RAG Systems** — Week 1 days 5–7 (+ Day 16 advanced patterns). Job-title P0. Never cut.
3. **Agentic Systems & Frameworks** — Days 13, 15–16. Job-title P0. Never cut.
4. **Python Mastery** — Week 2 days 8–10 & 14. P1 coding deep-dives.
5. **Python Production Stack** — Week 2 days 11–12. P1. Never cut (FastAPI + streaming).
6. **Data Structures & Algorithms** — Daily 2 problems. P1 parallel track.
7. **Architecture & System Design** — Week 3 days 17–18 & 21. P2 fluency, not mastery.
8. **Databases & Data Layer** — Week 3 days 19–20. P2.
9. **Production Engineering & Security** — Week 4 days 22–24. P2; cut here before touching P0/P1 if time collapses.

**Deferred (add later):** K8s details, IaC, CI/CD deep-dive, cloud, LLMOps/serving,
ethics/regulatory, multimodal deep-dive, GenAI-specific DSA. Backlog lives in
`raw/research/senior-genai-bare-minimum.md`.

## Minimum bar for Senior Python GenAI / RAG / Agentic Engineer

For this crunch, the minimum bar is every `min_required: true` topic in the nine
skills above (the 30-day plan's non-negotiables compressed into interview-sized units).

Gut-check milestones from the plan:
- **End Week 1:** Whiteboard full RAG; call APIs with tools + streaming from memory.
- **End Week 2:** Production Python + FastAPI SSE/JWT + LangGraph RAG with routing.
- **End Week 3:** Whiteboard distributed GenAI (agents, DBs, caches, queues) + patterns.
- **End Week 4:** Talk observability/security/reliability; medium LC in ~20 min.

## Per-skill topic requirements

**LLM / RAG / Agents** — Depth and code. Explain-it test + tiny builds every day.

**Python / FastAPI** — Hands-on: descriptor/closure builds, async producer-consumer,
FastAPI app that streams LLM output with auth.

**DSA** — Patterns from the plan's 60-problem tracker; mornings only.

**Architecture / DBs / Production** — Fluent trade-offs for a 10K-user RAG+agents
design; one SQL + two vector stores hands-on; security must include prompt injection.

## Open contradictions / questions for the human

- **Scope deliberately reduced.** Full bare-minimum checklist is backlog, not the
  active path. Say when you want pieces promoted back in.
- **If only 4 hrs/day:** plan says cut Week 4 infra first (already deferred), then
  ethics (deferred), then design-patterns skim, then DSA to 1/day — never cut Weeks 1–2
  core or Days 15–16 agents.
- **Completion still blank.** All topics `not-started` until you report what's done.
"""

    repo.write_conclusions(conclusions)

    state = repo.load()
    print(f"skills={len(state.skills)} topics={len(state.all_topics)}")
    print(f"min_required={sum(1 for t in state.all_topics if t.min_required)}")
    print("order=", [s.id for s in state.skills])
    print("focus=", [f"{t.skill_id}/{t.id}" for t in state.all_topics if t.focus])
    print("validate=", validate(state)["counts"])


if __name__ == "__main__":
    main()
