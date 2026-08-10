---
source: "Bare-minimum backlog — add after the 30-day path"
added: 2026-08-09
---

# Bare Minimum for a Senior Python GenAI/Agentic/RAG Engineer

> If you don't know these, it's a **no-go**. This is the non-negotiable baseline — not aspirational, not nice-to-have. Miss any of these and you are not ready for a senior role.

---

## 1. Advanced Python Proficiency

### Memory Management
- [ ] Reference Counting & Generational Garbage Collection
- [ ] `__slots__` vs `__dict__` (memory footprint implications)
- [ ] Weak References (`weakref` module)

### The GIL
- [ ] What the GIL is and how it affects CPU-bound vs I/O-bound tasks
- [ ] When and why to use threads vs processes vs asyncio

### Python Object Model
- [ ] Everything is an object — mutable vs immutable implications on function arguments
- [ ] `__new__` vs `__init__`
- [ ] Descriptor Protocol (`__get__`, `__set__`, `__delete__`)
- [ ] Method Resolution Order (MRO) & C3 Linearization
- [ ] Metaclasses (basic understanding of `type`)
- [ ] Magic/Dunder Methods (the Data Model)

### Execution Model & Bytecode
- [ ] Source to bytecode compilation (`.pyc` files, `__pycache__`)
- [ ] Basic awareness of the `dis` module and bytecode inspection

### Scoping & Namespaces
- [ ] LEGB Rule
- [ ] Closures & Free Variables
- [ ] `global` vs `nonlocal`

### The Import System
- [ ] `sys.path` and import search path
- [ ] Absolute vs Relative Imports
- [ ] Circular Imports — detection and resolution

### Iteration & Generators
- [ ] Iterator Protocol (`__iter__`, `__next__`)
- [ ] Generator Functions & Expressions
- [ ] `yield` vs `yield from`
- [ ] `send`, `throw`, `close` on generators

### Concurrency & Parallelism
- [ ] Concurrency vs Parallelism — when to use which
- [ ] `threading` — Thread lifecycle, `ThreadPoolExecutor`, Lock, Race Conditions, Producer-Consumer
- [ ] `multiprocessing` — `ProcessPoolExecutor`, Queue vs Pipe, Fork vs Spawn
- [ ] `asyncio` — `async def`, `await`, Event Loop, `create_task`, `gather`, `TaskGroup`
- [ ] Bridging sync & async — `run_in_executor()`, `to_thread()`
- [ ] Async Context Managers & Async Iterators
- [ ] Choosing threading vs multiprocessing vs asyncio for a given problem

### Advanced Typing
- [ ] Core hints: `Union`/`|`, `Optional`, `Literal`, `Final`, `Callable`
- [ ] `TypeVar`, `Generic`, Bounded TypeVars
- [ ] `Protocol` (structural subtyping)
- [ ] `TypedDict`
- [ ] `@overload`, `cast`, `TypeGuard`
- [ ] Pydantic for runtime validation

### Testing & Quality
- [ ] `pytest` — fixtures (scopes), `conftest.py`, parametrize, markers, plugins (`pytest-asyncio`)
- [ ] Mocking — `unittest.mock` (Mock, MagicMock, patch), dependency injection for testing
- [ ] Unit, Integration, and E2E testing understanding
- [ ] Type checking with `mypy` or `pyright`
- [ ] Linting with `ruff` or `flake8`
- [ ] Code coverage (branch vs line)

### AI-Specific Quality
- [ ] LLM Evaluation Frameworks — RAGAS, DeepEval (at least one)
- [ ] Deterministic vs Non-Deterministic Testing strategies
- [ ] Prompt Regression Testing

---

## 2. Software Architecture & Design Patterns

### Design Patterns (must-know subset)
- [ ] Singleton (module-level singletons in Python)
- [ ] Factory Method
- [ ] Strategy Pattern (replacing with first-class functions)
- [ ] Observer Pattern
- [ ] Decorator Pattern (function & class decorators)
- [ ] Iterator Pattern (generators)
- [ ] Dependency Injection (constructor injection)
- [ ] Context Manager Pattern (`with`, `__enter__`, `__exit__`)

### Concurrency Patterns
- [ ] Producer-Consumer
- [ ] Retry Pattern with exponential backoff
- [ ] Circuit Breaker Pattern

### Architectural Patterns (Code-Level)
- [ ] Repository Pattern
- [ ] Service Layer Pattern

### Architectural Patterns (System-Level)
- [ ] Monolithic vs Microservices — trade-offs
- [ ] Event-Driven Architecture (Pub/Sub)
- [ ] Hexagonal Architecture / Clean Architecture (conceptual)
- [ ] CQRS (conceptual)
- [ ] API Gateway Pattern

### API Design
- [ ] REST — resource naming, HTTP methods, status codes, idempotency
- [ ] Request/Response validation with Pydantic
- [ ] Pagination (offset vs cursor-based)
- [ ] Versioning strategies
- [ ] Rate Limiting
- [ ] Authentication — OAuth2, JWT, API Keys
- [ ] CORS
- [ ] OpenAPI / Swagger specification
- [ ] gRPC basics (Protocol Buffers, when to choose over REST)
- [ ] WebSockets & SSE (critical for streaming LLM output)

### System Design Principles
- [ ] CAP Theorem
- [ ] ACID vs BASE
- [ ] Horizontal vs Vertical Scaling
- [ ] Load Balancing (L4 vs L7)
- [ ] Consistent Hashing
- [ ] Caching Strategies (Cache-Aside, Write-Through)
- [ ] Eviction Policies (LRU, LFU)
- [ ] Message Queues (Pub/Sub, Point-to-Point)
- [ ] Batch vs Stream Processing
- [ ] Eventual vs Strong Consistency

---

## 3. Database Engineering

### Relational Databases (SQL)
- [ ] ACID properties
- [ ] MVCC basics
- [ ] Indexing — B-Tree, Composite Indexes, Covering Indexes, Partial Indexes
- [ ] Transaction Isolation Levels (Read Committed, Repeatable Read, Serializable)
- [ ] Optimistic vs Pessimistic Locking
- [ ] `EXPLAIN` / `EXPLAIN ANALYZE` interpretation
- [ ] Join algorithms awareness (Nested Loop, Hash, Merge)
- [ ] CTEs, Window Functions
- [ ] Normalization (1NF–3NF) & when to denormalize
- [ ] Connection Pooling (PgBouncer)
- [ ] Python drivers — `psycopg` (sync), `asyncpg` (async)
- [ ] ORM — SQLAlchemy or Django ORM
- [ ] N+1 Query Problem — detection and prevention (ORM `joinedload`/`select_related`)
- [ ] Preventing SQL Injection (parameterized queries)

### NoSQL
- [ ] Redis — data types, persistence (RDB/AOF), eviction policies, caching patterns, distributed locking, Pub/Sub
- [ ] MongoDB — schema design (embedding vs referencing), indexing, aggregation framework, replica sets
- [ ] Graph Databases (Neo4j) — Property Graph Model, Cypher basics, Knowledge Graph construction

### Vector Databases
- [ ] Dense vs Sparse embeddings
- [ ] Distance metrics — Cosine Similarity, Euclidean, Dot Product
- [ ] Indexing — HNSW, IVF, Product Quantization
- [ ] Hybrid Search (BM25 + semantic vector + Reciprocal Rank Fusion)
- [ ] Metadata filtering (pre-filtering vs post-filtering)
- [ ] Recall vs Latency trade-offs
- [ ] Tools — at least 2 of: Pinecone, Qdrant, Weaviate, Milvus, Chroma, pgvector

### Data Modeling
- [ ] OLTP vs OLAP
- [ ] Vector metadata schema design for hybrid search
- [ ] Schema evolution & migration strategies (Alembic)

---

## 4. Infrastructure, DevOps & Cloud

### Containerization (Docker)
- [ ] Dockerfile — multi-stage builds, layer caching, `.dockerignore`
- [ ] Base image selection (Alpine vs Debian vs Distroless)
- [ ] Python-specific — handling `requirements.txt`/Poetry, `PYTHONUNBUFFERED`
- [ ] PID 1 & signal handling, graceful shutdown
- [ ] Health checks
- [ ] Networking — bridge, host, port mapping
- [ ] Volumes — bind mounts vs named volumes
- [ ] Docker Compose
- [ ] Security — non-root user, image scanning, secrets management

### Orchestration (Kubernetes)
- [ ] Architecture — Control Plane vs Worker Nodes, API Server, etcd, Kubelet
- [ ] Pods, ReplicaSets, Deployments (rolling update)
- [ ] Services — ClusterIP, NodePort, LoadBalancer
- [ ] Ingress & Ingress Controllers
- [ ] ConfigMaps & Secrets
- [ ] Persistent Volumes & PVCs
- [ ] Liveness, Readiness, Startup Probes
- [ ] Resource Requests & Limits
- [ ] HPA (Horizontal Pod Autoscaler)
- [ ] RBAC basics
- [ ] Helm Charts basics
- [ ] `kubectl` — imperative vs declarative

### CI/CD
- [ ] CI vs CD vs Continuous Deployment
- [ ] Pipeline architecture (stages, jobs, triggers)
- [ ] Python CI — dependency caching, matrix testing, linting/type-checking gates
- [ ] Automated testing in pipelines
- [ ] Deployment strategies — Rolling, Blue-Green, Canary
- [ ] Secrets management in CI
- [ ] GitHub Actions or GitLab CI (at least one deeply)

### Cloud Fundamentals
- [ ] Compute — VMs, Serverless (Lambda), Container Services (ECS/EKS/GKE/Fargate)
- [ ] Networking — VPC, Subnets, Security Groups, Load Balancers, DNS
- [ ] Storage — S3/GCS (lifecycle policies, presigned URLs), EBS
- [ ] IAM — Users, Roles, Policies, Principle of Least Privilege
- [ ] Managed Databases — RDS/Cloud SQL
- [ ] Observability — CloudWatch/Cloud Logging, Metrics, Alarms
- [ ] Managed LLM Services — AWS Bedrock / Azure OpenAI / Vertex AI
- [ ] GPU instance types awareness (A100, H100)

### Infrastructure as Code
- [ ] Declarative vs Imperative
- [ ] Terraform basics — state, resources, variables, modules
- [ ] Secrets management — Vault / Cloud Secret Managers
- [ ] GitOps workflow concept

---

## 5. Production Engineering & Security

### Observability
- [ ] Three Pillars — Logs, Metrics, Traces
- [ ] Structured Logging (JSON) with contextual fields (request ID, user ID)
- [ ] Metric types — Counters, Gauges, Histograms
- [ ] RED Method (Rate, Errors, Duration) & Four Golden Signals
- [ ] Distributed Tracing — Spans, Traces, Context Propagation
- [ ] OpenTelemetry (auto-instrumentation & manual)
- [ ] SLIs, SLOs, SLAs
- [ ] Dashboards & Alerting (Grafana/Prometheus basics)

### LLM Observability
- [ ] Token usage tracking (prompt vs completion)
- [ ] Latency breakdown (TTFT, total latency)
- [ ] Cost monitoring per request/user
- [ ] Prompt & response logging
- [ ] RAG retrieval traceability (chunk relevance, source citation)

### Security
- [ ] OWASP Top 10
- [ ] SQL Injection prevention
- [ ] XSS, CSRF, SSRF (especially SSRF for agentic AI)
- [ ] CORS configuration
- [ ] Input validation & sanitization (Pydantic)
- [ ] OAuth 2.0 (Authorization Code + PKCE, Client Credentials)
- [ ] JWT — structure, signing algorithms, revocation
- [ ] Session management
- [ ] RBAC & ABAC
- [ ] API Key management (hashing, rotation)
- [ ] Secrets management — environment variables, cloud secret managers, secret rotation
- [ ] TLS/SSL basics, mTLS
- [ ] Python-specific — insecure deserialization (`pickle`), dependency supply chain attacks, Bandit

### LLM & GenAI Security
- [ ] OWASP Top 10 for LLMs
- [ ] Prompt Injection (direct & indirect via RAG data)
- [ ] Data Leakage prevention
- [ ] PII/PHI Redaction (Microsoft Presidio)
- [ ] DoS via token exhaustion / cost wallet attacks
- [ ] Output handling (XSS via LLM output)

### Reliability
- [ ] SLIs / SLOs / Error Budgets
- [ ] Circuit Breaker Pattern (Open, Closed, Half-Open)
- [ ] Retry with exponential backoff + jitter
- [ ] Timeouts (connection, read, inter-service)
- [ ] Idempotency (idempotency keys in APIs)
- [ ] Rate Limiting algorithms (Token Bucket, Sliding Window)
- [ ] Health Checks (Liveness, Readiness)
- [ ] Backpressure & Load Shedding
- [ ] Redundancy — Active-Active, Active-Passive
- [ ] MTTR, MTBF, RPO, RTO
- [ ] Blameless Post-Mortems

### Performance Engineering
- [ ] Profiling — `cProfile`, `py-spy`, `memray`/`tracemalloc`
- [ ] Flame Graphs
- [ ] GIL impact on performance
- [ ] Event loop latency — detecting blocking calls
- [ ] Connection Pooling (DB, HTTP)
- [ ] Serialization — `orjson` vs `json`
- [ ] Caching — `lru_cache`, Redis
- [ ] Latency percentiles — P50, P95, P99
- [ ] Load Testing — Locust or k6

---

## 6. AI & LLM Engineering (Specialization)

### RAG Architecture
- [ ] Document Parsing — PDF/OCR (Unstructured, LlamaParse), table extraction
- [ ] Chunking Strategies — fixed-size, recursive character, semantic chunking
- [ ] Metadata Extraction — auto-tagging, entity extraction for filtering
- [ ] Embedding Models — dense vs sparse, fine-tuning awareness, Sentence Transformers
- [ ] Vector DB internals — HNSW, IVF, quantization
- [ ] Query Transformation — query decomposition, HyDE, multi-query expansion
- [ ] Search — semantic (cosine), keyword (BM25), hybrid (RRF)
- [ ] Pre-filtering vs Post-filtering
- [ ] Reranking — cross-encoders (Cohere Rerank, BGE-Rerank)
- [ ] Context window management, lost-in-the-middle mitigation
- [ ] Parent Document Retriever, Auto-merging Retriever
- [ ] GraphRAG (Knowledge Graph + Vector Search)
- [ ] Prompt Engineering for RAG — CoT over context, source citation, "I don't know" handling
- [ ] Response Synthesis — Refine, Map-Reduce strategies
- [ ] Streaming in RAG pipelines
- [ ] RAG Evaluation — Faithfulness, Answer Relevance, Context Precision, Context Recall
- [ ] Evaluation frameworks — RAGAS, DeepEval/TruLens

### Agentic Frameworks
- [ ] ReAct (Reason + Act)
- [ ] Chain of Thought & Reflection / Self-Correction
- [ ] Task Decomposition
- [ ] State Management — FSM, cyclic graphs (LangGraph), checkpointing
- [ ] Human-in-the-Loop (breakpoints, approval flows)
- [ ] Tool Use — schema definition (JSON Schema / Pydantic), dynamic selection, error handling
- [ ] Structured Output Parsing
- [ ] Memory — short-term vs long-term, context window management (summarization)
- [ ] Multi-Agent — Supervisor/Router, hierarchical teams, message passing
- [ ] Agent Evaluation (trajectory analysis)
- [ ] Tracing & Observability (LangSmith or equivalent)
- [ ] Loop Detection & Prevention
- [ ] Cost Tracking per agent step

### LLM Evaluation
- [ ] Retrieval Metrics — Context Precision, Context Recall, MRR, nDCG
- [ ] Generation Metrics — Faithfulness, Answer Relevance, Hallucination Detection
- [ ] LLM-as-a-Judge — single-point grading, pairwise comparison
- [ ] Human evaluation workflows
- [ ] Golden Dataset creation & synthetic data generation
- [ ] Online metrics — user feedback signals, drift detection
- [ ] Performance benchmarking — TTFT, TPS, cost per query

### LLM Ops
- [ ] Model Serving — vLLM or TGI (at least awareness)
- [ ] Quantization awareness — AWQ, GPTQ, GGUF
- [ ] KV Cache, PagedAttention, Continuous Batching (conceptual)
- [ ] Semantic Caching (GPTCache / Redis)
- [ ] Guardrail frameworks — NeMo Guardrails / Guardrails AI
- [ ] Fine-tuning concepts — LoRA, QLoRA, PEFT
- [ ] RLHF & DPO (conceptual understanding)
- [ ] Model Registries (MLflow, Hugging Face Hub)

---

## 7. Data Structures, Algorithms & Problem Solving

### Complexity Analysis
- [ ] Big-O (O, Ω, Θ) — time & space
- [ ] Amortized analysis (conceptual)
- [ ] Common complexity classes

### Core Data Structures
- [ ] Arrays — two-pointer, sliding window, prefix sums, Kadane's algorithm
- [ ] Hash Tables — Python `dict` internals, frequency counting, N-Sum patterns
- [ ] Linked Lists — fast/slow pointer, reversal, LRU Cache implementation
- [ ] Stacks — monotonic stack, valid parentheses
- [ ] Queues — `deque`, priority queue (`heapq`)
- [ ] Trees — BST operations, traversals, Trie (autocomplete), LCA
- [ ] Heaps — Top-K, Merge K Sorted, Median of Stream
- [ ] Graphs — BFS, DFS, Topological Sort, Dijkstra's, Union-Find, Cycle Detection

### Core Algorithms
- [ ] Sorting — Merge Sort, Quick Sort, Python's Timsort awareness
- [ ] Binary Search — classic, lower/upper bound, search on answer
- [ ] Recursion & Backtracking — permutations, combinations, subsets
- [ ] Dynamic Programming — 1D (coin change, climbing stairs), 2D (LCS, edit distance), knapsack
- [ ] Greedy — interval scheduling, activity selection
- [ ] Bit Manipulation — XOR trick, power-of-two check, bitmask subsets

### GenAI-Relevant DSA
- [ ] Inverted Index (how BM25/keyword search works)
- [ ] Graph Algorithms for Knowledge Graphs (traversal, shortest path, community detection)
- [ ] Tree Structures for Retrieval (B-Trees, Tries, RAPTOR-style summarization trees)
- [ ] Hashing for Deduplication (MinHash, SimHash)
- [ ] Approximate Nearest Neighbor (LSH)
- [ ] Streaming Algorithms (Count-Min Sketch, HyperLogLog — for token/usage analytics)
- [ ] DAG Scheduling (topological sort for agent task decomposition)

---

## 8. LLM Fundamentals & Core Skills

### Transformer Architecture
- [ ] Self-Attention (Query, Key, Value)
- [ ] Multi-Head Attention
- [ ] Positional Encoding (RoPE, ALiBi awareness)
- [ ] Feed-Forward Networks, Layer Normalization, Residual Connections
- [ ] Encoder-Decoder vs Decoder-Only
- [ ] Attention variants — MQA, GQA, Flash Attention (awareness)

### Tokenization
- [ ] BPE, WordPiece, SentencePiece
- [ ] Token counting & budget management
- [ ] Special tokens (BOS, EOS, role tokens)
- [ ] Tokenization edge cases (multilingual, code, numbers)

### Inference & Decoding
- [ ] Autoregressive generation
- [ ] Temperature, Top-k, Top-p sampling
- [ ] Greedy vs Beam Search
- [ ] Stop sequences & max tokens
- [ ] Structured generation (JSON mode, constrained decoding)
- [ ] Speculative decoding (awareness)

### Model Landscape & Selection
- [ ] Closed-source: GPT-4o/o1/o3, Claude 3.5/4, Gemini 2.x
- [ ] Open-weight: Llama 3/4, Mistral/Mixtral, Qwen, DeepSeek
- [ ] Small Language Models: Phi, Gemma
- [ ] Selection criteria: cost, latency, context window, license, data privacy
- [ ] Embedding models: OpenAI, Cohere, BGE, E5, Jina
- [ ] Model benchmarks awareness (MMLU, HumanEval, Chatbot Arena)

### Multimodal AI
- [ ] Vision-Language Models awareness (GPT-4o, Claude, Gemini)
- [ ] Document Understanding (OCR + LLM, layout-aware models)
- [ ] Image Embeddings (CLIP, SigLIP)
- [ ] Audio/Speech awareness (Whisper)
- [ ] Multimodal RAG concepts (indexing images, tables, charts alongside text)

### Prompt Engineering
- [ ] System/User/Assistant message roles
- [ ] Zero-shot & Few-shot prompting
- [ ] Chain-of-Thought (CoT)
- [ ] ReAct prompting
- [ ] Structured Output prompting (JSON, function calling)
- [ ] Prompt templates & versioning
- [ ] Defensive prompting (injection resistance, delimiters)
- [ ] Prompt chaining (multi-step workflows)

### LLM API Integration
- [ ] Chat Completions API (OpenAI, Anthropic, Google)
- [ ] Streaming responses (SSE, token-by-token)
- [ ] Function / Tool Calling (JSON Schema, parallel calls)
- [ ] Structured Outputs (Pydantic model binding)
- [ ] Retry & fallback patterns (multi-provider failover)
- [ ] Rate limit handling (exponential backoff, request queuing)
- [ ] Cost management (input vs output pricing, caching)
- [ ] SDK usage — `openai`, `anthropic`, `google-genai`

---

## 9. GenAI Framework Ecosystem & Advanced Patterns

### Orchestration Frameworks (at least one deeply, awareness of others)
- [ ] **LangChain** — LCEL, Chains, Retrievers, Output Parsers, Callbacks
- [ ] **LlamaIndex** — Index Types, Query Engines, Response Synthesizers, Ingestion Pipeline
- [ ] **LangGraph** — StateGraph, State Schema, Checkpointing, Human-in-the-Loop, Subgraphs, Streaming

### Multi-Agent Frameworks (awareness)
- [ ] CrewAI or AutoGen or OpenAI Agents SDK (at least one)

### Advanced RAG Patterns
- [ ] Corrective RAG (CRAG)
- [ ] Self-RAG
- [ ] Adaptive RAG
- [ ] RAPTOR (recursive summarization trees)
- [ ] Conversational RAG (chat history contextualization, query rewriting)
- [ ] Multi-modal RAG (images, tables, charts)
- [ ] Contextual Retrieval (prepending document context to chunks)
- [ ] Agentic RAG (agent-driven iterative retrieval)
- [ ] Graph RAG (entity extraction → knowledge graph → community summarization)

### Model Context Protocol (MCP)
- [ ] MCP Architecture — Hosts, Clients, Servers
- [ ] MCP Primitives — Tools, Resources, Prompts
- [ ] Building MCP Servers (Python SDK)
- [ ] Tool Schema Standardization (JSON Schema, Pydantic-to-schema)

### Data Pipelines for GenAI
- [ ] Document Loaders (Unstructured.io, LlamaParse)
- [ ] Web Scraping (Scrapy, Playwright, Crawl4AI)
- [ ] Batch Embedding Pipelines (parallelization, batched API calls)
- [ ] Incremental Indexing (change detection, upsert, deduplication)
- [ ] Metadata Enrichment (entity extraction, auto-tagging)
- [ ] Pipeline Orchestration (Airflow/Prefect/Dagster awareness)

---

## 10. Python Production Stack

### FastAPI
- [ ] Route definitions, path/query params, request body
- [ ] Pydantic integration (request validation, response models)
- [ ] Dependency Injection (`Depends()`, yield dependencies)
- [ ] Middleware (CORS, custom)
- [ ] `StreamingResponse` (SSE for LLM token streaming)
- [ ] WebSocket support (real-time chat)
- [ ] Lifespan events (startup/shutdown hooks)
- [ ] Security — OAuth2 with JWT, API key dependencies
- [ ] Testing — `TestClient`, dependency overrides
- [ ] Deployment — Uvicorn, Gunicorn + Uvicorn, behind Nginx

### Pydantic v2
- [ ] `BaseModel`, `Field`, `field_validator`, `model_validator`
- [ ] Serialization — `model_dump()`, `model_dump_json()`
- [ ] Discriminated Unions
- [ ] `BaseSettings` (env var parsing, `.env` files)
- [ ] Custom types (`Annotated`, validators)
- [ ] `model_json_schema()` — used everywhere in LLM tool definitions

### Async HTTP Clients
- [ ] `httpx` — async client, connection pooling, timeouts, retries
- [ ] Resilience — `tenacity` for retries

### Task Queues
- [ ] Celery — tasks, workers, brokers (Redis/RabbitMQ), result backends
- [ ] Patterns — fan-out for parallel LLM calls, dead letter handling

### Project & Packaging
- [ ] `pyproject.toml`
- [ ] `uv` or `poetry` for dependency management
- [ ] Virtual environments
- [ ] Pre-commit hooks (ruff, mypy)

---

## 11. AI Ethics & Responsible AI

### Bias & Fairness
- [ ] Types of bias in training data and outputs
- [ ] Mitigation strategies (prompt debiasing, data augmentation)

### Explainability
- [ ] Source Attribution in RAG (citation generation, provenance tracking)
- [ ] Model Cards (knowing what they are and why they matter)
- [ ] Chain-of-Thought as explanation

### Content Safety
- [ ] Toxicity detection / content classification
- [ ] Output Guardrails (NeMo Guardrails / Guardrails AI)
- [ ] Red Teaming (adversarial testing)

### Privacy & Data Governance
- [ ] PII Detection & Redaction (Presidio, spaCy NER)
- [ ] Data Minimization
- [ ] Data Retention Policies for LLM interactions
- [ ] Right to Erasure from vector stores

### Regulatory Awareness
- [ ] EU AI Act (risk categories — awareness)
- [ ] GDPR implications for AI systems
- [ ] NIST AI Risk Management Framework (awareness)

---

## Quick Stats

| Section | Bare Minimum Items |
|---|---|
| 1. Advanced Python | ~47 |
| 2. Architecture & Design | ~40 |
| 3. Database Engineering | ~36 |
| 4. Infrastructure & Cloud | ~50 |
| 5. Production Engineering | ~50 |
| 6. AI & LLM Engineering | ~55 |
| 7. DSA & Problem Solving | ~35 |
| 8. LLM Fundamentals | ~50 |
| 9. GenAI Ecosystem | ~30 |
| 10. Python Production Stack | ~25 |
| 11. Ethics & Responsible AI | ~15 |
| **Total** | **~433 items** |

> These ~425 items are the **floor**, not the ceiling. A strong senior engineer will know many more topics from the full `learn.md`, but missing any of the above is a red flag.
