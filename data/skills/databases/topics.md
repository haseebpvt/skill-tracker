<!-- Topics for Databases & Data Layer. Format reference: MASTER.md → "File formats". -->

## SQL and query planning
- id: sql-query-planning
- status: strong
- priority: 1
- min_required: true
- focus: false
- updated: 2026-05-30

### What "enough" looks like
- Comfortable with joins, window functions and CTEs without reaching for docs
- Can read an EXPLAIN plan and act on it
- Knows when an index will and will not be used

### Notes / log
- 2026-05-30: years of production experience here; treat as solid

## Schema design and normalisation
- id: schema-design
- status: strong
- priority: 2
- min_required: true
- focus: false
- updated: 2026-05-30

### What "enough" looks like
- Can design a schema for a described domain and defend the normalisation choices
- Knows when to denormalise and what it costs

### Notes / log
- 2026-05-30: solid

## Transactions and isolation levels
- id: transactions-isolation
- status: comfortable
- priority: 3
- min_required: true
- focus: false
- updated: 2026-06-10

### What "enough" looks like
- Can name the isolation levels and the anomaly each one permits
- Can reason about a concrete race and pick the right level or lock

### Notes / log
- 2026-06-10: refreshed; can talk through the anomalies

## Vector databases
- id: vector-databases
- status: learning
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-03
- evidence: [raw/jd/northwind-ai-platform-2026-08.md, raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can choose between pgvector and a dedicated store and justify it on operational grounds
- Understands index build/query trade-offs and recall tuning
- Can design metadata filtering that does not destroy recall

### Notes / log
- 2026-08-03: used pgvector on a side project; have not tuned an index in anger

## Agent state and memory persistence
- id: agent-state-persistence
- status: not-started
- priority: 5
- min_required: true
- focus: false
- evidence: [raw/jd/acme-agentic-2026-07.md]

### What "enough" looks like
- Can design the persistence layer for a resumable long-running agent
- Knows how checkpointing interacts with retries and idempotency
- Can separate short-term working state from long-term memory and justify the split

### Notes / log
- Not started. Directly named in one JD.

## Caching strategies
- id: caching-strategies
- status: not-started
- priority: 6
- min_required: false
- focus: false

### What "enough" looks like
- Can pick a cache layer and an invalidation strategy for a concrete workload
- Understands the interaction between application cache and LLM prompt caching

### Notes / log
- Not started.
