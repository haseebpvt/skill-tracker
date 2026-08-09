---
source: "SEED EXAMPLE (fictional) — JD, Northwind, AI Platform Engineer"
url:
added: 2026-08-04
seed_example: true
---

> **This is placeholder seed data, not a real job posting.** Northwind is
> fictional. Replace with real postings before trusting the conclusions.

## AI Platform Engineer — Northwind

**The team**

We build the retrieval and agent platform the rest of the company builds on.

**Responsibilities**

- Own the retrieval stack: ingestion, chunking, embedding, reranking, evaluation
- Run and tune the vector store; own recall and latency SLOs
- Expose internal capabilities to agents through the Model Context Protocol
- Build observability into agent runs — tracing, step-level metrics, failure taxonomy

**Requirements**

- Deep understanding of embeddings and vector search internals (index types, recall/latency trade-offs)
- Production RAG experience, including honest measurement of retrieval quality separate from generation quality
- Familiarity with MCP or a comparable tool-exposure protocol
- Strong SQL and data modelling; we run pgvector alongside a dedicated store
- Experience instrumenting and debugging non-deterministic systems

**Notes from the recruiter call**

- They care much more about evaluation rigour than about framework familiarity
- Expect a system design round centred on a retrieval pipeline
