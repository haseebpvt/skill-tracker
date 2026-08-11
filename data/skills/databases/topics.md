<!-- Topics for Databases & Data Layer. See MASTER.md for the format. -->

## SQL engineering
- id: sql-engineering
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r4-vector-sql-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Choose indexes (B-tree/GIN/partial/covering) with EXPLAIN ANALYZE evidence; avoid blind over-indexing
- Explain Read Committed vs stronger isolation under MVCC; know serialization-failure retry
- Detect and eliminate N+1 (joins / joinedload / IN-batch) in an AI backend data path
- Size connection pooling (PgBouncer transaction vs session) against max_connections
- Ship safe Alembic/DDL migrations (CONCURRENTLY indexes, expand/contract, lock awareness)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Choose indexes (B-tree/GIN/partial/covering) with EXPLAIN ANALYZE evidence
- [ ] Explain Read Committed vs stronger isolation under MVCC; serialization-failure retry
- [ ] Detect and eliminate N+1 (joins / joinedload / IN-batch) in an AI backend path
- [ ] Size connection pooling (PgBouncer txn vs session) against max_connections
- [ ] Ship safe Alembic/DDL migrations (CONCURRENTLY indexes, expand/contract)
- [ ] Write a CTE + window function query; prevent SQL injection via parameters

## Redis & document/graph stores
- id: nosql-stores
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r4-vector-sql-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Use Redis for cache, locks, and rate/limit patterns with eviction/persistence awareness
- Design Mongo embed-vs-reference schemas and indexes for an agent/session store
- Explain when a graph store helps GraphRAG vs when vectors+SQL suffice

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Use Redis for cache, distributed lock, and rate-limit patterns; know eviction/persistence
- [ ] Design Mongo embed-vs-reference schema + indexes for an agent/session store
- [ ] Explain when Neo4j/graph helps GraphRAG vs when vectors+SQL suffice
- [ ] Sketch Cypher or property-graph basics for a knowledge-graph RAG case

## Vector databases & pipelines
- id: vector-databases
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r4-vector-sql-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Hands-on with ≥2 stores (prefer Qdrant/Weaviate/pgvector/Chroma): hybrid search + metadata filters + upsert-by-id
- Explain filterable/pre-filter search vs post-filter recall collapse with a concrete example
- Design a chunk metadata schema (doc_id, chunk_index, source, tenant, timestamp, text-for-BM25) with indexes
- Tune recall vs latency (efSearch/M/alpha/quantization) for a stated workload
- Discuss incremental indexing / dedup via stable IDs on volatile corpora

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Hands-on with ≥2 stores (Qdrant/Chroma/pgvector): hybrid search + metadata filters + upsert-by-id
- [ ] Explain pre-filter vs post-filter recall collapse with a concrete example
- [ ] Design chunk metadata schema (doc_id, chunk_index, source, tenant, timestamp, BM25 text) with indexes
- [ ] Tune recall vs latency (efSearch/M/quantization) for a stated workload
- [ ] Discuss incremental indexing / dedup via stable IDs on volatile corpora
- [ ] Sketch batch embedding + pipeline orchestration awareness (loaders → embed → index)
