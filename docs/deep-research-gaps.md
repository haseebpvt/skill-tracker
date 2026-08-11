# Deep Research Brief — Skill Tracker Rubric Gaps

**Status: R1–R5 ingested (2026-08-10).** Topic `enough` criteria rewritten from the rubric reports. This file kept as the audit trail / prompt archive.

**Role:** Senior Python GenAI / RAG / Agentic Engineer  
**Purpose:** Fill gaps in *what “enough” looks like* so an agent can honestly grade you (and set UI status colors) when you explain what you know.  
**Credits:** Limited — run prompts in order. Stop after R1–R3 if budget is tight; R4–R5 are optional.

---

## How grading will work (confirmed)

When you come back and say what you learned / already know:

1. Read that topic’s **What “enough” looks like** criteria.
2. Ask 1–2 probing questions (trade-off / failure mode / “what happens if”).
3. Judge against the criteria — not vibes.
4. Update the markdown via skill-tracker MCP (`not-started` → `learning` → `comfortable` → `strong`).
5. UI box colors follow those statuses.

**Bar for `comfortable`+ is “has done”, not “has read”.**

---

## Audit summary (46 topics)

| Bucket | Count | Meaning |
|--------|------:|---------|
| Rubric OK enough to judge now | 11 | Concrete do + trade-off signals |
| Thin / weak rubrics | 35 | Need sharper criteria and/or fresher market evidence |

**Important distinction**

| Area | Research needed? | Why |
|------|------------------|-----|
| Python mastery, FastAPI/Pydantic, DSA, classic design patterns, basic REST/CAP | **No** | Strong prior knowledge; I’ll tighten “enough” bullets myself without burning credits |
| LLM fundamentals, RAG eval, Agentic 2026 stack, vector DBs, GenAI security/obs | **Yes (prioritized below)** | Fast-moving bar; current “enough” is too shallow to probe a senior candidate fairly |

Existing evidence (`one-month-plan`, `bare-minimum`, `agentic study plan`) is good for **topic lists**, weaker for **interview-grade pass/fail rubrics** (what separates `learning` vs `comfortable` vs `strong`).

---

## Highest-importance gaps (P0, unlearned, thin rubric)

These score highest: **skill priority × min_required × rubric weakness × not-started**.

### Tier A — research first (blocks honest grading of your differentiator)

| # | Skill | Topic id | Gap |
|---|-------|----------|-----|
| A1 | llm-fundamentals | `tokenization` | No “do” bar; no senior failure cases (fragmentation, multilingual/code cost) |
| A2 | llm-fundamentals | `prompt-engineering` | Checklist of techniques; no when-not-to / injection trade-offs |
| A3 | llm-fundamentals | `transformer-architecture` | Explain-only; missing complexity/cost implications seniors get asked |
| A4 | llm-fundamentals | `llm-api-integration` | Build script OK; missing production failure modes (partial streams, tool errors) |
| A5 | rag | `rag-ingestion` | Too short; no chunking failure modes / table/OCR trade-offs |
| A6 | rag | `rag-search` | Implements hybrid; missing recall/latency/filter-order interview probes |
| A7 | rag | `rag-evaluation` | Metric names only; weak on metric gaming / judge bias / golden-set design |
| A8 | rag | `advanced-rag-patterns` | Name-drop list; needs “symptom → pattern” decision table |
| A9 | agentic-systems | `langgraph-state-machines` | Build graph OK; missing durability/HITL/failure interview probes |
| A10 | agentic-systems | `langchain-fluency` | Tutorial-shaped; no when-not-LangChain / LCEL limits |
| A11 | agentic-systems | `multi-agent-mcp` | Overlaps deeper MCP topic; multi-agent bar unclear |
| A12 | agentic-systems | `agent-evaluation` | One bullet; not enough to judge tracing maturity |
| A13 | agentic-systems | `agent-benchmarks-eval-ci` | Awareness + vague CI; need concrete gate design |
| A14 | agentic-systems | `test-time-compute` | Design sketch OK; need 2026 interview-standard answers |
| A15 | agentic-systems | `agentic-guardrails` | Layer names OK; missing hands-on “enough” and failure cases |

### Tier B — research if credits remain (P1–P2, still min_required)

| # | Skill | Topic id | Gap |
|---|-------|----------|-----|
| B1 | databases | `vector-databases` | Hands-on named; weak ops trade-offs (filtering, upsert, hybrid) |
| B2 | databases | `sql-engineering` | Laundry list; need GenAI-service SQL interview bar |
| B3 | production-engineering | `observability` | Pillars listed; weak LLM-trace “enough” |
| B4 | production-engineering | `security` | Topic soup; need senior GenAI AppSec probe set |
| B5 | python-production-stack | `fastapi-streaming-auth` | Feature list; missing SSE/auth failure modes |

### Tier C — do **not** spend deep-research credits

I’ll rewrite rubrics from known senior bars (no research):

- All **DSA** topics  
- **python-object-model**, **python-generators-imports**, **python-typing-testing**, **python-concurrency**  
- **pydantic-v2**, **fastapi-core**  
- **design-patterns**, **system-architecture**, **api-design**  
- **nosql-stores** (Redis/Mongo basics)  
- Already-OK agentic topics: workflows-vs-agents, agent-loop, mcp-architecture, framework-selection, failure-modes, memory  

Optional / low ROI: `agent-peft-trajectories` (`min_required: false`) — skip unless a JD forces it.

---

## How to use these prompts

1. Run **one prompt per deep-research job**, in order R1 → R5.  
2. Ask the tool for **markdown output** with the exact section headings in the prompt.  
3. Drop the result into:

```text
evidence/raw/research/rubric-<rN-slug>-YYYY-MM-DD.md
```

with YAML frontmatter:

```yaml
---
source: "Deep research — <title>"
added: YYYY-MM-DD
---
```

4. Come back here and say: *“recompile from new rubric research”* — I’ll tighten topic `enough` bullets and keep skill order stable unless you approve a change.

---

## R1 — LLM Fundamentals senior interview rubric (2026)

**Covers:** `transformer-architecture`, `tokenization`, `prompt-engineering`, `llm-api-integration`  
**Priority:** Highest (skill #1, all min_required, currently focus area)

### Prompt (copy-paste)

```text
I am preparing for Senior Python GenAI / Agentic AI Engineer interviews (2026).
I need a GRADING RUBRIC, not a tutorial.

Target topics:
1) Transformer architecture (attention, positional encoding, encoder-decoder vs decoder-only, MQA/GQA/FlashAttention)
2) Tokenization & context budgets (BPE/WordPiece/SentencePiece/tiktoken, special tokens, fragmentation costs)
3) Prompt engineering (roles, few-shot, CoT, ReAct, structured outputs, defensive prompting, chaining)
4) LLM API integration (OpenAI/Anthropic/Google SDKs, streaming/SSE, tool calling, structured outputs, retries, rate limits, multi-provider failover, cost control)

For EACH topic, output:

## <Topic name>
### Comfortable bar (must demonstrate)
- 5–8 concrete, checkable bullets (prefer “can explain X and build/debug Y”)
### Strong bar (follow-up / edge)
- 3–5 bullets (failure modes, trade-offs, production scars)
### Probe questions
- 5 interview questions a senior interviewer would ask
### Common false confidence
- 3 things people claim after reading blogs that do not count as competence
### Anti-goals
- What is OUT of scope for this topic at senior level (defer elsewhere)

Constraints:
- Focus on what interviewers actually test in 2025–2026 for agentic/RAG roles.
- Prefer primary sources (lab blogs, API docs, well-known papers) and cite them.
- No generic motivational content. No long architecture essays.
- Keep total under ~1,500 words.
```

---

## R2 — Production RAG + evaluation rubric

**Covers:** `rag-ingestion`, `rag-search`, `rag-evaluation`, `advanced-rag-patterns`  
**Priority:** Highest (skill #2)

### Prompt (copy-paste)

```text
I need a senior-interview GRADING RUBRIC for production RAG systems (2026), not a survey paper.

Topics:
1) Ingestion / chunking / embeddings (PDF/OCR/tables, chunking strategies, dense vs sparse, metadata)
2) Vector indexes & hybrid search (HNSW/IVF/quantization, BM25+vector+RRF, metadata pre vs post filtering, recall vs latency)
3) RAG evaluation (faithfulness, answer relevance, context precision/recall, MRR/nDCG, RAGAS/DeepEval/TruLens, LLM-as-judge pitfalls, golden sets)
4) Advanced RAG pattern selection (CRAG, Self-RAG, Adaptive RAG, RAPTOR, conversational, agentic, GraphRAG, contextual retrieval)

For EACH topic:

## <Topic name>
### Comfortable bar
### Strong bar
### Symptom → technique decision table
(especially for advanced patterns and search failures)
### Probe questions (5)
### Metric / design pitfalls (what looks good on paper but fails in prod)
### Anti-goals

Also include one short section:
## Minimal golden-set recipe
- How many examples, what labels, how to avoid leakage, how often to refresh

Cite practical sources (framework docs, evaluation library docs, industry engineering posts).
Max ~1,800 words. Rubric bullets must be checkable in a conversation or short coding exercise.
```

---

## R3 — Agentic systems rubric gaps (2026)

**Covers:** `langgraph-state-machines`, `langchain-fluency`, `multi-agent-mcp`, `agent-evaluation`, `agent-benchmarks-eval-ci`, `test-time-compute`, `agentic-guardrails`  
**Priority:** Highest differentiator depth (skill #3). Skip topics already strong: workflows-vs-agents, agent-loop, mcp-architecture, framework-selection, failure-modes, memory.

### Prompt (copy-paste)

```text
I already have solid rubrics for: workflows vs agents, ReAct/agent loops, MCP architecture, framework selection (LangGraph vs Agents SDK vs PydanticAI vs CrewAI), agentic failure modes, and agent memory.

I need GRADING RUBRICS only for these remaining Senior Agentic AI Engineer topics (2026):

1) LangGraph in production (StateGraph, checkpointing, HITL, streaming, durable execution, resume after crash)
2) LangChain fluency & limits (LCEL/chains/retrievers/callbacks — when it helps vs when to avoid)
3) Multi-agent orchestration (supervisor/router/hierarchical teams) — separate from MCP protocol details
4) Agent evaluation & tracing (LangSmith/Langfuse/Phoenix/OpenTelemetry-style trajectory debugging, loop/cost tracking)
5) Agent benchmarks & eval CI (what SWE-bench, GAIA, Tau-bench actually measure; how to build LLM-as-judge + red-team gates in CI)
6) Test-time compute / reasoning models in agent pipelines (o-series / DeepSeek-R1 style; queues + SSE; routing cheap vs reasoning models; cost)
7) Agentic guardrails (Guardrails AI vs NeMo; layered defense; OWASP LLM risks: injection, data leak, hallucinated tools, excessive agency)

For EACH:

## <Topic name>
### Comfortable bar (checkable)
### Strong bar
### Probe questions (5)
### Production failure stories / anti-patterns interviewers expect
### Anti-goals

Add a final section:
## Overlap cleanup
- Which bullets belong in MCP-architecture vs multi-agent vs guardrails vs production-security so we do not double-count

Cite docs and reputable 2025–2026 engineering posts. Max ~2,000 words. No PEFT/fine-tuning chapter.
```

---

## R4 — Vector DB + data layer for GenAI services (optional)

**Covers:** `vector-databases`, `sql-engineering` (GenAI-shaped only)  
**Priority:** Medium — run only if R1–R3 are done and credits remain.

### Prompt (copy-paste)

```text
Create a senior-interview GRADING RUBRIC for the data layer of a production RAG/agent platform.

Topics:
1) Vector databases in practice (pick any 2 of Qdrant, Chroma, pgvector, Pinecone, Weaviate, Milvus)
   - hybrid search, metadata filters, upsert/dedup, recall vs latency, schema for chunk metadata
2) SQL for AI backends (Postgres-centric)
   - indexing, isolation, EXPLAIN, N+1, pooling, migrations — only what a GenAI backend engineer must defend in interview

For each: Comfortable bar, Strong bar, 5 probe questions, common false confidence, anti-goals.
Include a tiny “design a metadata schema for hybrid RAG” checklist.
Max ~1,200 words. Cite official docs where possible.
```

---

## R5 — GenAI observability & security interview bar (optional)

**Covers:** `observability`, `security`, and sharpen `fastapi-streaming-auth` failure modes  
**Priority:** Lower than P0; still min_required for Week 4.

### Prompt (copy-paste)

```text
Create a senior-interview GRADING RUBRIC for production GenAI services:

1) Observability & LLM observability (logs/metrics/traces, OpenTelemetry, RED/golden signals, token/TTFT/cost tracking, prompt logging, RAG provenance)
2) AppSec + LLM security (OWASP Top 10 + OWASP LLM Top 10; OAuth2/JWT/secrets; prompt injection direct/indirect; PII redaction; SSRF risk for tool-using agents)
3) Serving LLM streams securely (FastAPI SSE/WebSockets, auth on streams, retries with httpx/tenacity — failure modes only)

For each: Comfortable bar, Strong bar, 5 probes, false confidence, anti-goals.
Distinguish what belongs in “agentic guardrails” vs general AppSec to avoid duplication.
Max ~1,200 words. Cite OWASP GenAI and mainstream observability docs.
```

---

## Recommended spend

| Credits available | Run |
|-------------------|-----|
| Very low | **R1 only** |
| Low | **R1 + R2** |
| Medium | **R1 + R2 + R3** (best ROI) |
| Higher | Add **R4**, then **R5** |

Do **not** run separate researches per topic — these five batches already cover the high-importance gaps.

---

## After research lands

Tell me which `rubric-*.md` files you added. I will:

1. Diff evidence and recompile conclusions incrementally  
2. Rewrite weak `### What "enough" looks like` blocks into Comfortable/Strong-checkable bullets  
3. Keep skill order unless you explicitly approve a reorder (e.g. promote Agentic → #1)
