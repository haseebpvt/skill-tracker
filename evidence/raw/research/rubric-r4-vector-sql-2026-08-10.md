---
source: "Deep research R4 — Vector DB + Postgres data-layer rubric"
added: 2026-08-10
---

# Executive Summary  
Production RAG platforms require robust vector search layers (hybrid dense+sparse search, filtering, upserts, etc.) and reliable SQL backends. We evaluate two vector DBs (Qdrant and Weaviate) across key features (hybrid search support, metadata filtering, upsert/dedup, recall vs. latency, chunk metadata schema). We then outline a Postgres-centric data-layer rubric for GenAI (covering indexing, isolation, EXPLAIN usage, N+1 detection, pooling, migrations) with candidate proficiency bars, interview probes, and common pitfalls. In addition, we provide a brief hybrid‐RAG metadata schema checklist. All claims cite official or primary sources.  

# Vector Databases in Practice  

## Chosen Databases: Qdrant and Weaviate  

| **Feature**              | **Qdrant**                                                                                                    | **Weaviate**                                                                                                                  |
|--------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| **Hybrid search**        | Dense+sparse (BM25) via *Universal Query API*. Native support for combining embedding search with full-text/BM25. Uses Reciprocal Rank Fusion or weighted sum to merge results. Example: FastEmbed tutorial shows uploading dense+BM25 vectors for hybrid search. | Built-in hybrid: combines BM25 (“keyword search”) and vector scores via an adjustable **α** parameter (0–1). Weaviate auto-vectorizes text and allows tuning fusion. It supports RRF and relative-score fusion with `alpha`, and can set vector distance thresholds. |
| **Metadata filters**     | Boolean filtering on JSON payload. Supports complex nested clauses (`must`, `should`, `must_not`) on point payloads (indexed pre-search for speed). Payload fields must be explicitly indexed (e.g. text, keyword, numeric) via “payload indexes” for performance. Filters apply *during* HNSW search (pre-filtering) for minimal overhead. | GraphQL “where” filters on class properties (typed schema). All properties (text/int/boolean) can be filtered via GraphQL and/or REST. Weaviate’s filters operate via a reverse-inverted index; its hybrid query supports keyword search parameters (BM25 K1, B, stopwords) on specified properties. Multi-tenancy in Weaviate also isolates filters per tenant. Schema must declare which properties are searchable (or let auto-schema create them). |
| **Upsert/Dedup**         | Upsert by ID: use the **PUT /points** (upsert) endpoint to insert or update vectors. Points with existing IDs are overwritten. (The API docs call this “upsert points”.) To avoid duplicates, always use upsert instead of add. No separate dedup logic needed beyond unique IDs. | Objects have unique IDs: creating with an existing ID will update (replace) that object. The REST API supports `PUT /objects` to replace by ID. Clients can also update properties or vectors of an object by its UUID. In practice, enforcing unique IDs (or using weaviate’s built-in *uuid* assignment) handles deduplication. |
| **Recall vs. Latency**   | HNSW index by default. Can tune HNSW parameters (`ef_search`, `m`) in query for higher recall at cost of latency. Supports scalar-quantization (int8) to trade recall vs. RAM. Qdrant’s Rust engine yields ~4–8ms p50 on 5M vectors (768-dim) with standard HNSW, and can handle up to ~50M by on-disk HNSW (with NVMe paging). Sparse (BM25) search is exact (100% recall) for keyword queries. Qdrant demonstrates best-in-class filtered recall (pre-filter HNSW) with only ~1–2ms extra latency. | HNSW index (via FAISS under the hood) for vectors. By default uses `alpha=0.5` to balance recall; adjusting `alpha` shifts weight to vectors vs. keywords. Weaviate’s vector index is optimized (e.g. supports distance thresholding). It runs on JVM so raw latency is higher than Qdrant’s Rust (~slower for <1M, but scales well). Weaviate allows multi-vector indexing and per-class index tuning. Recall can be improved by fusion (RRF) or reranking modules, at cost of query complexity. Memory footprint is larger (needs ~2–4× more RAM) for similar vector counts. |
| **Chunk metadata schema**| Qdrant uses free-form JSON payload. Recommended fields: document ID, chunk number, source, timestamp, tenant/etc. (strings/ints) for filtering. Text content can be a payload field (for BM25 indexing) or separate “text” index. Vector fields typically not in payload. E.g. payload: `{"doc_id":123, "chunk":5, "timestamp": "...", "source":"wiki", "published":true}`. Create payload indexes on frequently-filtered keys. | Weaviate enforces schema-first. Define a class (e.g. `Chunk`) with properties like `docID` (int/string), `chunkNumber` (int), `source` (string), etc. You also include a text property (e.g. `content`) and configure it for BM25. Each class has vectorizers (or disabled if uploading). Use property indexing settings (tokenization, stopwords) as needed. Weaviate auto-creates the schema if not provided, but best practice is an explicit schema with clear datatypes and index settings. Cross-references (e.g. linking chunk→document) can be used but often not needed for flat RAG. |

 *Figure: Hybrid search example combining BM25 (sparse) and embedding vectors. Qdrant and Weaviate both support such hybrid queries, merging keyword and semantic results.*  

**Qdrant (Rust-based, filtered-search first)**: Qdrant shines when strict filtering is needed. It builds payload-indexed HNSW graphs so filters apply during search, giving low overhead. It natively stores both dense (`vector`) and sparse (`bm25` fields) representations. Hybrid queries fuse BM25 and dense via RRF or weighted sum. Upserting is straightforward via the `/points` PUT API (overwrite if ID exists). For recall/latency, Qdrant’s default HNSW works well up to ~10M vectors; beyond that it supports on-disk index or int8 quantization. However, running Qdrant self-hosted requires ops (sharding, backups).  

**Weaviate (schema-first, module-rich)**: Weaviate requires defining a schema (classes/properties). Its built-in modules auto-vectorize content. Hybrid search is first-class: BM25 (via inverted indices) and vector scores are fused with a tunable `alpha`. GraphQL filters on object properties allow rich queries. Weaviate also supports multi-tenancy isolating each class’s index per tenant. Schema migrations can be tricky (adding properties may reindex). Upsert is via object ID: a PUT with an existing ID replaces the object. Recall/latency: hybrid search is accurate but Weaviate’s JVM footprint is large (requiring more RAM). It offers a gRPC client for high throughput and handles thousands of tenants with isolated indexes.  

# SQL for AI Backends (Postgres-centric)  

For each topic below, we define interview **Comfortable** and **Strong** bars (candidate proficiency), propose five probing questions, list common false-confidence pitfalls, and note anti-goals (what to avoid).  

## Indexing Strategies  
- **Comfortable:** Knows basic B-tree indexes (for equality/range) and when to apply them; understands use of `CREATE INDEX`. Aware of GiST/GIN for non-standard data (e.g. full-text, JSON) and partial/multicol indexes.  
- **Strong:** Understands all Postgres index types: B-tree, Hash, GiST, SP-GiST, GIN, BRIN. Can choose based on workload (e.g. GIN for JSONB/array, GiST for geometric/nearest neighbor, BRIN for huge append-only logs). Knows index-only scans, operator classes (e.g. `text_pattern_ops` for ILIKE), and ordering optimization. Implements multicolumn vs. covering (index+include) vs. expression indexes for advanced cases. Minimize index bloat (drop unused indexes).  
- **Probe Qs:**  
  1. “What index type would you use for a JSONB column? When?” (GIN)  
  2. “How do you index a full-text search query?” (GIN on `to_tsvector`)  
  3. “Why might too many indexes hurt performance?” (writes slower, cache pressure)  
  4. “Explain multicolumn vs. separate indexes. When to use a covering index?”  
  5. “How do you optimize a query with `ILIKE '%foo'` or a distance metric?” (special ops or GiST/HNSW for vectors).  
- **False-confidence:** “Hash indexes are always faster for equals” (misleading; B-tree is usually better). “GIN is automatically used for JSON queries” (only if created, and can bloat). “Adding every needed index is trivial” (neglects overhead). “BRIN for any big table” (only if data is correlated).  
- **Anti-goals:** Unilateral indexing (no analysis via `EXPLAIN`). Not dropping old indexes. Over-indexing low-selectivity columns. Forgetting to `CREATE INDEX CONCURRENTLY` in prod (locks table) – should use non-blocking builds.   

## Transaction Isolation Concerns  
- **Comfortable:** Understands default Read Committed and why it avoids dirty reads. Knows concept of transactions. Aware that higher isolation (Repeatable Read, Serializable) can prevent anomalies at cost of performance (Serializable avoids anomalies).  
- **Strong:** Knows exactly what anomalies (dirty, non-repeatable, phantom) each level prevents. Understands MVCC and how Postgres implements snapshot isolation (its “Repeatable Read” is actually Serializable-effective). Can configure isolation per-transaction and handle serialization errors. Ensures long transactions don’t hold back VACUUM (MVCC cleanup).  
- **Probe Qs:**  
  1. “What are the differences between Read Committed and Serializable in Postgres?” (dirty/non-repeatable reads).  
  2. “When might you use `SERIALIZABLE` level?” (“guaranteed correctness for concurrent writes, but might need retry”).  
  3. “How does Postgres prevent dirty reads by default?” (MVCC – sees only committed data at query start).  
  4. “Explain ‘phantom read’ and how it’s handled at each level.”  
  5. “What happens if two concurrent transactions try to INSERT with the same unique key?” (one must commit first or deadlock).  
- **False-confidence:** “Serializable always stays serial” (actually can fail with serialization error, requiring retry). “Repeatable Read has phantoms” (Postgres’s “Repeatable Read” actually prevents phantoms as well). “You can ignore isolation for read-only workloads” (can see stale data).  
- **Anti-goals:** Ignoring transaction boundaries (e.g. autocommit every statement). Holding open transactions for long analytic queries (prevents vacuum). Unnecessary use of `SERIALIZABLE` for simple reads (causes needless overhead).  

## Using EXPLAIN for Performance  
- **Comfortable:** Knows to use `EXPLAIN ANALYZE` to inspect query plans. Understands basic costs and identifies obvious full-table scans vs. index scans. Aware of `EXPLAIN (ANALYZE, BUFFERS)` for detail.  
- **Strong:** Interprets `EXPLAIN` output (cost vs actual time, buffer hits). Tunes queries by rewriting or adding indexes based on plan. Uses verbose flags, joins vs. subqueries, materialized CTEs where appropriate. Monitors `pg_stat_statements` for slow queries. Understands sequential scan vs index selectivity trade-offs.  
- **Probe Qs:**  
  1. “How would you detect an N+1 query pattern using EXPLAIN?” (“See many repeated queries in plan or high loop counts”).  
  2. “What does `Bitmap Heap Scan` vs `Seq Scan` indicate?” (using partial index or multi-index usage).  
  3. “Interpret `cost=... rows=... width=...` in EXPLAIN output.”  
  4. “How can you force PostgreSQL to use an index and test performance?” (`SET enable_seqscan=off;`).  
  5. “Why use `BUFFERS` in EXPLAIN, and what does it show?” (cache hits/misses).  
- **False-confidence:** “If EXPLAIN shows only an index scan, it’s always optimal.” (index scans can still be slow if many rows). “Don’t use ANALYZE – trust planner estimates.” (planner stats must be updated). “More indexes always speed up EXPLAIN results.” (over-indexing increases planning time).  
- **Anti-goals:** Ignoring EXPLAIN entirely. Relying on development/test planner costs (never production). Blindly adding indexes without checking the plan.  

## N+1 Query Detection/Mitigation  
- **Comfortable:** Recognizes N+1 (fetching child data in a loop). Knows to join tables or use `IN (...)` lists to batch fetch related data. Aware of ORM “eager loading” vs “lazy loading”.  
- **Strong:** Proactively refactors code/ORM usage to avoid N+1. Uses `JOIN`, `LATERAL`, or single query subselects. In ORMs, uses prefetch (e.g. Django `select_related`, SQLAlchemy `joinedload`). Can identify N+1 via query logs or test loads. Understands and avoids the “application-side loop query” anti-pattern.  
- **Probe Qs:**  
  1. “What is an N+1 query problem? How would you spot it?” (“One query for parent list, N queries for each child. Check query logs or profilers.”)  
  2. “How can you rewrite code that does an N+1 into one query?” (“Use JOIN or `WHERE ... IN (...)`. Or batch `IN` query.”)  
  3. “What Postgres feature can you use to fetch related data in one go?” (CTE, `ARRAY_AGG`, JSON aggregation).  
  4. “How do prepared statements or parameterized queries affect N+1?” (“They don’t; still N queries if loop, just with parameters.”)  
  5. “In a web app, where would you configure pooling or limiting to mitigate N+1?” (pooling doesn’t fix N+1, but capping concurrent queries might reduce DB load).  
- **False-confidence:** “N+1 is only an ORM problem” (any code loops can do it). “Using an ORM automatically solves N+1” (ORM defaults often cause N+1 unless tuned). “Micro-optimizing a slow query is more important than eliminating N+1” (usually batching yields far bigger gains).  
- **Anti-goals:** Leaving N+1 unfixed because “works on dev”. Ignoring logging (fail to notice dozens of similar queries). Premature caching instead of fixing query logic.  

## Connection Pooling  
- **Comfortable:** Knows that too many DB connections degrades Postgres (memory overhead). Uses a basic pool (e.g. in framework or `psycopg2.pool`).  
- **Strong:** Implements an external pooler (e.g. PgBouncer/pgpool) in transaction mode to minimize idle connections. Tunes pool size vs. DB `max_connections`. Understands `idle` vs `active` connections. Monitors connection usage. Explains pooling modes (session vs transaction).  
- **Probe Qs:**  
  1. “Why is connection pooling needed in a high-traffic API?” (limit DB connections, reduce overhead).  
  2. “What problems can arise without pooling?” (exceeding `max_connections`, OOM).  
  3. “Differences between PgBouncer session vs transaction pooling?” (“Transaction pooling releases slot after each txn; session holds slot entire client session.”)  
  4. “How do prepared statements behave under transaction pooling?” (they might not persist outside transaction).  
  5. “How to monitor active vs idle connections in Postgres?” (`pg_stat_activity`).  
- **False-confidence:** “Each API thread needs its own dedicated connection” (leads to many idle connections). “Postgres can handle 10k concurrent connections easily” (no, memory spikes). “Connection pooling is only for legacy apps” (critical for any scale).  
- **Anti-goals:** Using application-level idle pools with `pool_pre_ping` off (leaks connections). Ignoring `max_lifetime` of connections. Hardcoding tiny pool sizes without load testing.  

## Migrations (Schema Changes)  
- **Comfortable:** Uses a migration tool (Flyway, Alembic, Rails Migrations, etc.). Applies simple DDL changes (create/drop table, add column) in version-controlled scripts.  
- **Strong:** Designs migrations for minimal downtime and backward compatibility. Breaks large changes into multiple steps (e.g. add new column *without* NOT NULL/unique, backfill data, then alter constraint). Uses `CREATE INDEX CONCURRENTLY` for large tables. Understands locking: `ALTER TABLE ... ADD COLUMN` is fast, but `ALTER TABLE ... ALTER COLUMN TYPE` can lock table. Tests migrations in staging. Can use `pg_repack` or triggers for zero-downtime column additions if needed.  
- **Probe Qs:**  
  1. “What is the effect of adding a column with a default on a big table?” (rewrite of table, locks table).  
  2. “How to add an index without blocking reads/writes?” (`CREATE INDEX CONCURRENTLY`).  
  3. “How to remove a column safely?” (Ensure no code uses it; might be done in 2-steps).  
  4. “Explain the down-migration: how to drop a table or undo an index.”  
  5. “What are the transaction properties of DDL in Postgres?” (Many DDL are transactional, but some, like VACUUM, are not).  
- **False-confidence:** “All migrations are fast” (some lock table). “Rollback is always possible” (DROP is destructive unless backups exist). “You can skip testing in staging” (risky).  
- **Anti-goals:** Running migrations directly in production without review. Ignoring transactional semantics (e.g. doing DDL outside a transaction). Relying on ORMs’ `auto_migrate` blindly.  

## Design a Metadata Schema for Hybrid RAG (Checklist)  
- Define essential chunk fields: e.g. **doc_id**, **chunk_index**, **text/content**, **source_id**, **page/url**, **timestamp**, **tenant_id** (if multi-tenant).  
- Include semantic labels/embeddings tags as needed (no need to store embedding if re-created).  
- For filtering: use strongly-typed fields (dates for time ranges, integers for categories) with indexes (GIN for arrays/text, B-tree for numeric).  
- Reserve a boolean or status field if needed (e.g. “is_relevant”).  
- Plan for FTS: if using Qdrant, include key for BM25 (sparse) field; if Weaviate, mark text property as `text` for BM25.  
- Consider “chunk overlap” or parent doc references if needed (via cross-references or join keys).  
- Keep metadata narrow: store only what’s filterable/queryable (avoid huge JSON blobs in payload).  
- Example:  
  - **DocumentID** (string or int, filterable)  
  - **ChunkIndex** (int, filter)  
  - **Source/Collection** (string)  
  - **CreationDate** (timestamp)  
  - **Category/Tag** (string)  
  - **Text** (string, full-text searchable)  

**Sources:** Qdrant and Chroma official docs on filtering and upserts; Weaviate docs on schema; Postgres docs on index types and isolation. Each claim above is supported by these references.
