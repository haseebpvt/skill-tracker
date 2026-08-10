<!-- Topics for RAG Systems. See MASTER.md for the format. -->

## Ingestion, chunking & embeddings
- id: rag-ingestion
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Parse docs, choose chunking, extract metadata
- Explain dense vs sparse embeddings and pick a model

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Vector indexes & hybrid search
- id: rag-search
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Explain HNSW/IVF/quantization and distance metrics
- Implement semantic + BM25 + RRF hybrid search with metadata filters

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Reranking, query transforms & generation
- id: rag-rerank-context
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Apply rerankers and query transforms (HyDE, multi-query, decomposition)
- Mitigate lost-in-the-middle; RAG prompts with citations / I-don't-know; stream answers

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## RAG evaluation
- id: rag-evaluation
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Define faithfulness, relevance, context precision/recall, MRR/nDCG
- Run RAGAS or DeepEval on a small golden set; use LLM-as-a-judge carefully

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Advanced RAG patterns
- id: advanced-rag-patterns
- status: not-started
- priority: 5
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Explain CRAG / Self-RAG / Adaptive / RAPTOR / conversational / agentic / Graph RAG
- Pick a pattern for a concrete retrieval failure mode

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
