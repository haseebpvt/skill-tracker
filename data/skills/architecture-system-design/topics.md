<!-- Topics for Architecture & System Design. See MASTER.md for the format. -->

## Python design patterns
- id: design-patterns
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Implement strategy, decorator, DI, context manager, repository/service, retry, circuit breaker in Python
- Pick patterns for LLM clients (retry/breaker) and tool registries (strategy/factory) with trade-offs

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Implement Strategy (first-class funcs) and Factory for a tool registry
- [ ] Implement Decorator (function/class) and Context Manager patterns
- [ ] Implement DI (constructor injection) + Repository/Service layer split
- [ ] Implement Retry with exponential backoff + Circuit Breaker for an LLM client
- [ ] Know Singleton-as-module and Observer when they actually earn their keep
- [ ] Build: one file with each pattern as a tiny Python snippet

## Distributed system principles
- id: system-architecture
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Trade off monolith vs services vs events for a GenAI app; apply CAP/consistency where state matters
- Design caching, queues, and scaling for LLM latency/cost asymmetry (not CRUD-only thinking)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Trade off monolith vs services vs event-driven for a GenAI app
- [ ] Apply CAP/consistency where agent/session state matters
- [ ] Design caching (cache-aside/write-through) and eviction (LRU/LFU) for LLM asymmetry
- [ ] Place queues + batch vs stream processing for embedding/index work
- [ ] Explain L4 vs L7 load balancing and horizontal vs vertical scaling for LLM gateways
- [ ] Whiteboard: production RAG+agents for 10K users — name every component

## API design for GenAI
- id: api-design
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Design REST with pagination/versioning/idempotency/rate limits/auth suitable for agent backends
- Choose SSE vs WebSocket for LLM streaming with failure-mode awareness

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Design REST resources with idempotency, status codes, and clear naming
- [ ] Choose offset vs cursor pagination and a versioning strategy
- [ ] Add rate limiting + auth (OAuth2/JWT/API keys) suitable for agent backends
- [ ] Choose SSE vs WebSocket for LLM streaming with failure-mode awareness
- [ ] Ship OpenAPI; know when gRPC earns its keep
