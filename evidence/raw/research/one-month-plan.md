---
source: "30-day intensive prep plan — Senior Python GenAI/RAG/Agentic"
added: 2026-08-09
---

# 30-Day Intensive Prep Plan — Senior Python GenAI/RAG/Agentic Engineer

> **Status:** 15/376 items checked. **361 items remaining in 30 days.**
>
> This plan is ruthlessly prioritized. In a 1-month crunch, you cannot go deep on everything equally. The strategy: **nail your specialization first, then broaden.**

---

## Ground Rules

1. **Daily DSA** — Every single day, do 2 LeetCode/NeetCode problems in the morning before anything else. Non-negotiable. This runs parallel to everything below.
2. **Time budget** — Assume 6–8 focused hours/day. If you have less, cut from Week 4 first.
3. **Learn by doing** — For every topic, write code. Don't just read. Build tiny scripts, debug in a REPL, write a mini-project.
4. **Anki cards** — After each study block, create 3–5 flashcards for the hardest concepts. Review daily.
5. **"Explain it" test** — If you can't explain a topic to a junior dev in 2 minutes, you don't know it yet.

---

## Priority Tiers

| Tier | What | Why |
|------|------|-----|
| **P0 — CRITICAL** | LLM Fundamentals, RAG, Agents, Prompt Engineering, LLM APIs | This is your **job title**. If you can't ace these, nothing else matters. |
| **P1 — HIGH** | Python internals, FastAPI/Pydantic, Frameworks (LangChain/LangGraph), DSA patterns | Tested in every coding round & technical deep-dive. |
| **P2 — MEDIUM** | System Design, Architecture, Databases, Security | System design round. You need to talk fluently, not be an expert. |
| **P3 — LOWER** | K8s details, IaC deep-dive, CI/CD specifics, Ethics | Important for the job, but rarely the reason you fail an interview. Skim, don't master. |

---

## Week 1: Your Differentiator (Days 1–7)

> **Goal:** After this week, you should be able to whiteboard a production RAG system end-to-end, explain every component, and discuss trade-offs fluently.

### Day 1 — LLM Fundamentals: How Models Work
- [ ] Transformer Architecture: Self-Attention (QKV), Multi-Head Attention, Positional Encoding
- [ ] Feed-Forward Networks, Layer Norm, Residual Connections
- [ ] Encoder-Decoder vs Decoder-Only
- [ ] Attention variants awareness (MQA, GQA, Flash Attention)
- **DSA (morning):** 2 problems — Arrays (two-pointer, sliding window)

### Day 2 — Tokenization & Inference
- [ ] Tokenization: BPE, WordPiece, SentencePiece, tiktoken
- [ ] Token counting & budget management, special tokens
- [ ] Autoregressive generation, Temperature, Top-k, Top-p
- [ ] Greedy vs Beam Search, stop sequences, max tokens
- [ ] Structured generation (JSON mode, constrained decoding)
- **DSA (morning):** 2 problems — Arrays (prefix sums, Kadane's)

### Day 3 — Model Landscape & Prompt Engineering
- [ ] Closed-source models: GPT-4o/o1/o3, Claude 3.5/4, Gemini 2.x
- [ ] Open-weight: Llama 3/4, Mistral/Mixtral, Qwen, DeepSeek
- [ ] Selection criteria: cost, latency, context window, license, privacy
- [ ] Embedding models: OpenAI, Cohere, BGE, E5, Jina
- [ ] System/User/Assistant roles, Zero-shot & Few-shot prompting
- [ ] Chain-of-Thought, ReAct prompting
- [ ] Structured Output prompting (JSON, function calling)
- [ ] Defensive prompting, prompt chaining
- **DSA (morning):** 2 problems — Hash Tables (frequency counting, two-sum)

### Day 4 — LLM API Integration (Hands-on)
- [ ] Chat Completions API (OpenAI, Anthropic, Google)
- [ ] Streaming responses (SSE, token-by-token handling)
- [ ] Function / Tool Calling (JSON Schema, parallel calls)
- [ ] Structured Outputs (Pydantic model binding)
- [ ] Retry & fallback patterns, rate limit handling
- [ ] Cost management (input vs output pricing)
- [ ] SDK usage — `openai`, `anthropic`, `google-genai`
- **Build:** Write a script that calls OpenAI with tool calling, streams the response, handles errors with retries
- **DSA (morning):** 2 problems — Hash Tables (N-Sum, grouping)

### Day 5 — RAG Core: Ingestion & Retrieval
- [ ] Document Parsing — PDF/OCR (Unstructured, LlamaParse)
- [ ] Chunking Strategies — fixed-size, recursive character, semantic
- [ ] Metadata Extraction — auto-tagging, entity extraction
- [ ] Embedding Models — dense vs sparse, Sentence Transformers
- [ ] Vector DB internals — HNSW, IVF, quantization
- [ ] Distance metrics — Cosine Similarity, Euclidean, Dot Product
- [ ] Dense vs Sparse embeddings
- **DSA (morning):** 2 problems — Stacks (valid parentheses, monotonic stack)

### Day 6 — RAG Core: Search, Reranking & Generation
- [ ] Semantic search, Keyword search (BM25), Hybrid search (RRF)
- [ ] Pre-filtering vs Post-filtering, metadata filtering
- [ ] Reranking — cross-encoders (Cohere Rerank, BGE-Rerank)
- [ ] Query Transformation — decomposition, HyDE, multi-query expansion
- [ ] Context window management, lost-in-the-middle mitigation
- [ ] Parent Document Retriever, Auto-merging Retriever
- [ ] Prompt Engineering for RAG — CoT over context, source citation, "I don't know"
- [ ] Response Synthesis — Refine, Map-Reduce strategies
- [ ] Streaming in RAG pipelines
- **DSA (morning):** 2 problems — Queues/Deque, Priority Queue (heapq)

### Day 7 — RAG Evaluation & Multimodal AI + Week 1 Review
- [ ] RAG Evaluation — Faithfulness, Answer Relevance, Context Precision, Context Recall
- [ ] Evaluation frameworks — RAGAS, DeepEval/TruLens
- [ ] Retrieval Metrics — MRR, nDCG, Hit Rate
- [ ] LLM-as-a-Judge — single-point grading, pairwise comparison
- [ ] Multimodal AI awareness — Vision-Language Models, Document Understanding, CLIP, Whisper
- [ ] Multimodal RAG concepts
- **Evening:** Review all Week 1 material. Do a mock "explain RAG end-to-end" to yourself. Time: 10 minutes.
- **DSA (morning):** 2 problems — Binary Search (classic, search on answer)

---

## Week 2: Python Mastery & Production Stack (Days 8–14)

> **Goal:** After this week, you can write production-quality Python, build a FastAPI app serving an LLM, and use LangChain/LangGraph fluently.

### Day 8 — Python Object Model & Scoping
- [ ] Mutable vs immutable — implications on function arguments
- [ ] Descriptor Protocol (`__get__`, `__set__`, `__delete__`)
- [ ] Metaclasses — basic understanding of `type`
- [ ] Magic/Dunder Methods (the Data Model) — `__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, `__getitem__`, `__call__`
- [ ] Closures & Free Variables
- [ ] `global` vs `nonlocal`
- **Build:** Create a custom descriptor, a class with `__slots__` + dunder methods, a closure that captures state
- **DSA (morning):** 2 problems — Linked Lists (fast/slow pointer, reversal)

### Day 9 — Generators, Import System & Concurrency
- [ ] Generator Functions & Expressions
- [ ] `yield` vs `yield from`
- [ ] `send`, `throw`, `close` on generators
- [ ] `sys.path`, absolute vs relative imports, circular imports
- [ ] Concurrency vs Parallelism — when to use which
- [ ] `threading` — ThreadPoolExecutor, Lock, Race Conditions, Producer-Consumer
- [ ] `multiprocessing` — ProcessPoolExecutor, Queue vs Pipe, Fork vs Spawn
- **Build:** Write a producer-consumer with threading, then rewrite with asyncio
- **DSA (morning):** 2 problems — Linked Lists (merge sorted, LRU cache)

### Day 10 — Asyncio Deep Dive & Advanced Typing
- [ ] `asyncio` — `async def`, `await`, Event Loop, `create_task`, `gather`, `TaskGroup`
- [ ] Core type hints: `Union`/`|`, `Optional`, `Literal`, `Final`, `Callable`
- [ ] `TypeVar`, `Generic`, Bounded TypeVars
- [ ] `TypedDict`
- [ ] `@overload`, `cast`, `TypeGuard`
- [ ] Pydantic for runtime validation
- **Build:** Type-annotate a small module with generics + TypedDict, validate with mypy
- **DSA (morning):** 2 problems — Trees (BST traversals, validate BST)

### Day 11 — Pydantic v2 & FastAPI Core
- [ ] Pydantic: `BaseModel`, `Field`, `field_validator`, `model_validator`
- [ ] Serialization: `model_dump()`, `model_dump_json()`
- [ ] Discriminated Unions, `BaseSettings`, Custom types
- [ ] `model_json_schema()` — critical for LLM tool definitions
- [ ] FastAPI: Route definitions, path/query params, request body
- [ ] Pydantic integration in FastAPI (request validation, response models)
- [ ] Dependency Injection (`Depends()`, yield dependencies)
- [ ] Middleware (CORS, custom)
- **DSA (morning):** 2 problems — Trees (Trie, LCA)

### Day 12 — FastAPI Advanced & Async HTTP Clients
- [ ] `StreamingResponse` (SSE for LLM token streaming)
- [ ] WebSocket support (real-time chat)
- [ ] Lifespan events (startup/shutdown hooks)
- [ ] Security — OAuth2 with JWT, API key dependencies
- [ ] Testing — `TestClient`, dependency overrides
- [ ] Deployment — Uvicorn, Gunicorn + Uvicorn, behind Nginx
- [ ] `httpx` — async client, connection pooling, timeouts, retries
- [ ] `tenacity` for retries
- **Build:** Build a FastAPI app that streams LLM output via SSE, with JWT auth
- **DSA (morning):** 2 problems — Heaps (Top-K, Merge K Sorted)

### Day 13 — LangChain + LangGraph (Hands-on)
- [ ] LangChain — LCEL, Chains, Retrievers, Output Parsers, Callbacks
- [ ] LlamaIndex — Index Types, Query Engines, Response Synthesizers (awareness)
- [ ] LangGraph — StateGraph, State Schema, Checkpointing, Human-in-the-Loop, Subgraphs, Streaming
- **Build:** Build a simple RAG chain in LangChain, then rebuild as a LangGraph with conditional routing + checkpointing
- **DSA (morning):** 2 problems — Graphs (BFS, DFS)

### Day 14 — Testing, Quality & Week 2 Review
- [ ] pytest — fixtures (scopes), conftest.py, parametrize, markers, `pytest-asyncio`
- [ ] Mocking — `unittest.mock` (Mock, MagicMock, patch), dependency injection for testing
- [ ] Unit, Integration, E2E testing understanding
- [ ] Type checking with mypy or pyright
- [ ] Linting with ruff, code coverage (branch vs line)
- [ ] Project & Packaging — `pyproject.toml`, `uv`/`poetry`, pre-commit hooks
- **Evening:** Review Week 2. Mock exercise: "Design and code a FastAPI endpoint that runs a RAG query." Whiteboard it, then code it.
- **DSA (morning):** 2 problems — Graphs (Topological Sort, Cycle Detection)

---

## Week 3: System Design, Architecture & Agents (Days 15–21)

> **Goal:** After this week, you can design a distributed GenAI system on a whiteboard and discuss agents, databases, and architecture confidently.

### Day 15 — Agentic Frameworks Core
- [ ] ReAct (Reason + Act), Chain of Thought & Reflection
- [ ] Task Decomposition
- [ ] State Management — FSM, cyclic graphs (LangGraph), checkpointing
- [ ] Human-in-the-Loop (breakpoints, approval flows)
- [ ] Tool Use — schema definition, dynamic selection, error handling
- [ ] Structured Output Parsing
- [ ] Memory — short-term vs long-term, context window management (summarization)
- **DSA (morning):** 2 problems — Graphs (Dijkstra's, Union-Find)

### Day 16 — Multi-Agent, Advanced RAG Patterns & MCP
- [ ] Multi-Agent — Supervisor/Router, hierarchical teams, message passing
- [ ] Agent Evaluation, Tracing (LangSmith), Loop Detection, Cost Tracking
- [ ] CrewAI or AutoGen or OpenAI Agents SDK (pick one, hands-on)
- [ ] Advanced RAG: Corrective RAG, Self-RAG, Adaptive RAG
- [ ] RAPTOR, Conversational RAG, Agentic RAG, Graph RAG, Contextual Retrieval
- [ ] MCP — Architecture, Primitives, Building MCP Servers
- **DSA (morning):** 2 problems — Recursion/Backtracking (permutations, subsets)

### Day 17 — Design Patterns (Python-Focused)
- [ ] Singleton (module-level), Factory Method
- [ ] Strategy Pattern (first-class functions), Observer Pattern
- [ ] Decorator Pattern (function & class decorators)
- [ ] Iterator Pattern (generators)
- [ ] Dependency Injection (constructor injection)
- [ ] Context Manager Pattern (`with`, `__enter__`, `__exit__`)
- [ ] Producer-Consumer, Retry with exponential backoff, Circuit Breaker
- [ ] Repository Pattern, Service Layer Pattern
- **Build:** Implement each pattern as a small Python snippet in a single file
- **DSA (morning):** 2 problems — Recursion/Backtracking (N-Queens, combinations)

### Day 18 — Architecture & System Design Principles
- [ ] Monolithic vs Microservices, Event-Driven Architecture (Pub/Sub)
- [ ] Hexagonal/Clean Architecture (conceptual), CQRS, API Gateway
- [ ] CAP Theorem, ACID vs BASE
- [ ] Horizontal vs Vertical Scaling, Load Balancing (L4 vs L7)
- [ ] Consistent Hashing
- [ ] Caching Strategies (Cache-Aside, Write-Through), Eviction (LRU, LFU)
- [ ] Message Queues, Batch vs Stream Processing
- [ ] Eventual vs Strong Consistency
- **DSA (morning):** 2 problems — Dynamic Programming 1D (coin change, climbing stairs)

### Day 19 — Database Engineering: SQL & NoSQL
- [ ] ACID, MVCC basics
- [ ] Indexing — B-Tree, Composite, Covering, Partial
- [ ] Transaction Isolation Levels, Optimistic vs Pessimistic Locking
- [ ] EXPLAIN / EXPLAIN ANALYZE, Join algorithms
- [ ] CTEs, Window Functions, Normalization, N+1 Problem
- [ ] Connection Pooling, `psycopg`/`asyncpg`, SQLAlchemy, SQL Injection prevention
- [ ] Redis — data types, persistence, eviction, caching patterns, distributed locking
- [ ] MongoDB — schema design, indexing, aggregation, replica sets
- [ ] Neo4j — Property Graph Model, Cypher basics, Knowledge Graph construction
- **DSA (morning):** 2 problems — Dynamic Programming 2D (LCS, edit distance)

### Day 20 — Vector Databases & Data Pipelines
- [ ] Hybrid Search (BM25 + vector + RRF) — deeper dive
- [ ] Metadata filtering, recall vs latency trade-offs
- [ ] Tools hands-on — pick 2 of: Qdrant, Chroma, pgvector
- [ ] OLTP vs OLAP, vector metadata schema design, schema migration (Alembic)
- [ ] Data Pipelines: Document Loaders, Web Scraping, Batch Embedding
- [ ] Incremental Indexing, Metadata Enrichment, Pipeline Orchestration awareness
- **DSA (morning):** 2 problems — Dynamic Programming (knapsack, house robber)

### Day 21 — API Design & Week 3 Review
- [ ] REST — resource naming, HTTP methods, status codes, idempotency
- [ ] Request/Response validation with Pydantic
- [ ] Pagination (offset vs cursor-based), versioning strategies
- [ ] Rate Limiting, Authentication (OAuth2, JWT, API Keys), CORS
- [ ] OpenAPI/Swagger, gRPC basics
- [ ] WebSockets & SSE (for streaming LLM output)
- **Evening:** Mock system design: "Design a production RAG system with agents that serves 10K users." Draw the architecture, name every component, discuss trade-offs. 20 minutes.
- **DSA (morning):** 2 problems — Greedy (interval scheduling, jump game)

---

## Week 4: Production, Security, Infra & Final Review (Days 22–30)

> **Goal:** Round out the remaining areas. Fill gaps. Do mock interviews. Polish.

### Day 22 — Observability & LLM Observability
- [ ] Three Pillars — Logs, Metrics, Traces
- [ ] Structured Logging (JSON), contextual fields
- [ ] Metric types, RED Method, Four Golden Signals
- [ ] Distributed Tracing, OpenTelemetry
- [ ] SLIs, SLOs, SLAs, Dashboards & Alerting
- [ ] LLM Observability: Token tracking, TTFT, cost monitoring, prompt logging, RAG traceability
- **DSA (morning):** 2 problems — Bit manipulation (XOR trick, power of two)

### Day 23 — Security (AppSec + LLM Security)
- [ ] OWASP Top 10, SQL Injection, XSS, CSRF, SSRF
- [ ] CORS, Input validation (Pydantic)
- [ ] OAuth 2.0 (Auth Code + PKCE, Client Credentials), JWT (structure, signing, revocation)
- [ ] Session management, RBAC & ABAC, API Key management
- [ ] Secrets management, TLS/SSL, mTLS
- [ ] Python-specific: `pickle` risks, supply chain attacks, Bandit
- [ ] OWASP Top 10 for LLMs, Prompt Injection (direct & indirect)
- [ ] Data Leakage, PII Redaction (Presidio), DoS via token exhaustion
- **DSA (morning):** 2 problems — Sliding Window (variable size, minimum window substring)

### Day 24 — Reliability & Performance Engineering
- [ ] SLIs/SLOs/Error Budgets
- [ ] Circuit Breaker, Retry + jitter, Timeouts, Idempotency
- [ ] Rate Limiting algorithms, Health Checks, Backpressure, Load Shedding
- [ ] Redundancy, MTTR/MTBF/RPO/RTO, Post-Mortems
- [ ] Profiling — cProfile, py-spy, memray/tracemalloc, Flame Graphs
- [ ] GIL impact, event loop latency, Connection Pooling
- [ ] Serialization (orjson), Caching (lru_cache, Redis)
- [ ] Latency percentiles (P50/P95/P99), Load Testing (Locust/k6)
- **DSA (morning):** 2 problems — Interval problems (merge intervals, insert interval)

### Day 25 — Docker & Kubernetes
- [ ] Dockerfile — multi-stage builds, layer caching, .dockerignore
- [ ] Base image selection, Python-specific patterns, PID 1, Health checks
- [ ] Networking, Volumes, Docker Compose, Security (non-root)
- [ ] K8s: Control Plane vs Workers, Pods, Deployments (rolling update)
- [ ] Services, Ingress, ConfigMaps/Secrets, PV/PVCs
- [ ] Probes (Liveness, Readiness, Startup), Resource Requests/Limits
- [ ] HPA, RBAC basics, Helm, kubectl
- **DSA (morning):** 2 problems — Graph (BFS on grid / Island problems)

### Day 26 — CI/CD, Cloud & IaC
- [ ] CI vs CD vs Continuous Deployment, Pipeline architecture
- [ ] Python CI — caching, matrix testing, linting gates
- [ ] Deployment strategies — Rolling, Blue-Green, Canary
- [ ] Secrets in CI, GitHub Actions (deeply)
- [ ] Cloud: Compute, Networking, Storage, IAM, Managed DBs, Observability
- [ ] Managed LLM Services (Bedrock/Azure OpenAI/Vertex AI), GPU instances
- [ ] Terraform basics, Secrets management, GitOps
- **DSA (morning):** 2 problems — Trie (word search, autocomplete)

### Day 27 — LLM Ops, Task Queues & Ethics
- [ ] Model Serving (vLLM/TGI), Quantization (AWQ, GPTQ, GGUF)
- [ ] KV Cache, PagedAttention, Continuous Batching
- [ ] Semantic Caching, Guardrails (NeMo/Guardrails AI)
- [ ] Fine-tuning (LoRA, QLoRA, PEFT), RLHF & DPO concepts
- [ ] Model Registries (MLflow, HF Hub)
- [ ] Celery — tasks, workers, brokers, fan-out patterns
- [ ] Ethics: Bias, Explainability, Content Safety, PII, Regulations
- **DSA (morning):** 2 problems — DP on Trees / State Machine DP

### Day 28 — AI-Specific Testing & Evaluation Deep Dive
- [ ] LLM Evaluation Frameworks — RAGAS, DeepEval
- [ ] Deterministic vs Non-Deterministic Testing
- [ ] Prompt Regression Testing
- [ ] Golden Dataset creation & synthetic data generation
- [ ] Human evaluation workflows
- [ ] Online metrics — user feedback signals, drift detection
- [ ] Performance benchmarking — TTFT, TPS, cost per query
- **DSA (morning):** 2 problems — Hard problems from weak areas

### Day 29 — GenAI-Relevant DSA & Weak Area Review
- [ ] Inverted Index (BM25 internals)
- [ ] Graph Algorithms for Knowledge Graphs
- [ ] Tree Structures for Retrieval (B-Trees, Tries, RAPTOR trees)
- [ ] Hashing for Deduplication (MinHash, SimHash)
- [ ] LSH (Approximate Nearest Neighbor)
- [ ] Streaming Algorithms (Count-Min Sketch, HyperLogLog)
- [ ] DAG Scheduling (topological sort for agents)
- **Afternoon:** Go back to your weakest 2 sections and re-study them
- **DSA (morning):** 2 problems — Mixed/Hard from weak patterns

### Day 30 — Full Review & Mock Interview Day
- [ ] **Morning:** 3 DSA problems (medium-hard, timed 25 min each)
- [ ] **Late morning:** Mock system design — "Design a multi-tenant RAG platform with agentic capabilities" (45 min)
- [ ] **Afternoon:** Rapid-fire concept review — flip through all Anki cards
- [ ] **Late afternoon:** Mock behavioral — prepare 3 stories: (1) a hard technical problem you solved, (2) a time you disagreed with a design decision, (3) a production incident you handled
- [ ] **Evening:** Rest. You've done the work.

---

## DSA Problem Tracker (60 problems over 30 days)

> 2 problems/day. Use NeetCode 150 or Blind 75 as your source. Prioritize patterns over quantity.

| Pattern | Target # | Days |
|---------|----------|------|
| Arrays & Strings (two-pointer, sliding window, prefix sum) | 8 | Days 1–4 |
| Hash Tables (frequency, N-Sum, grouping) | 4 | Days 3–4 |
| Stacks & Queues (monotonic stack, heapq) | 4 | Days 5–6 |
| Binary Search (classic, on answer) | 2 | Day 7 |
| Linked Lists (fast/slow, reversal, LRU) | 4 | Days 8–9 |
| Trees (BST, Trie, LCA) | 4 | Days 10–11 |
| Heaps (Top-K, Merge K) | 2 | Day 12 |
| Graphs (BFS, DFS, Topological, Dijkstra, Union-Find) | 6 | Days 13, 15, 25 |
| Recursion & Backtracking | 4 | Days 16–17 |
| Dynamic Programming (1D, 2D, knapsack) | 6 | Days 18–20 |
| Greedy | 2 | Day 21 |
| Bit Manipulation | 2 | Day 22 |
| Intervals, Sliding Window, Trie, Mixed | 6 | Days 23–26 |
| Hard/Weak areas | 6 | Days 27–30 |
| **Total** | **60** | |

---

## Weekly Milestones (Gut Check)

| End of | You should be able to... |
|--------|--------------------------|
| **Week 1** | Whiteboard a full RAG pipeline. Explain every component (chunking → embedding → indexing → retrieval → reranking → generation → evaluation). Discuss trade-offs fluently. Call LLM APIs with tool calling and streaming from memory. |
| **Week 2** | Write production-quality Python with proper types, async, generators, decorators. Build a FastAPI app with SSE streaming and JWT auth. Use LangChain/LangGraph to build a RAG chain with conditional routing. Write pytest tests. |
| **Week 3** | Design a distributed GenAI system architecture on a whiteboard (load balancing, caching, queues, databases, vector stores, agents). Discuss SQL vs NoSQL trade-offs, design schemas, explain agent architectures. Implement 8+ design patterns in Python from memory. |
| **Week 4** | Talk confidently about Docker, K8s, CI/CD, cloud, security, observability, LLMOps at a senior level. Handle curveball questions on prompt injection, PII redaction, circuit breakers, cost optimization. Solve medium LeetCode problems in 20 minutes. |

---

## Time Allocation per Day

```
┌──────────────────────────────────────────────┐
│         6–8 hrs/day breakdown                │
├──────────────────────────────────────────────┤
│  ■ DSA Practice          1.0 hr  (morning)   │
│  ■ Core Study Topic      3.5 hr  (main)      │
│  ■ Hands-on Building     1.5 hr  (coding)    │
│  ■ Anki Review + Cards   0.5 hr  (evening)   │
│  ■ Review / Mock         0.5 hr  (evening)   │
└──────────────────────────────────────────────┘
```

---

## If You Only Have 4 Hours/Day

Cut in this order (least painful first):

1. **Days 25–26** (Docker/K8s/CI/CD/Cloud) — Skim in 1 day instead of 2. You can explain these at a high level from general experience.
2. **Day 27 afternoon** (Ethics) — Read a summary article instead of deep study. Rarely tested in interviews.
3. **Day 17** (Design Patterns) — If you already use decorators, context managers, DI naturally, just skim the list.
4. **Reduce DSA to 1 problem/day** — Only if desperate. This is the last thing to cut.

**Never cut:** Week 1 (LLM/RAG), Days 8–12 (Python + FastAPI), Day 15–16 (Agents).
