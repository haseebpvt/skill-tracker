<!-- Topics for RAG Systems. See MASTER.md for the format. -->

## Ingestion, chunking & embeddings
- id: rag-ingestion
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r2-rag-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Prefer semantic/overlap-aware chunking over naive fixed splits; tag metadata for hybrid filters
- Distinguish dense vs sparse embeddings and when keyword/SKU/code lookup needs sparse/hybrid
- Handle PDF tables without flattening into nonsense (VLM/Markdown/structured extract path)
- Explain coreference/context loss from naive chunking and a mitigation (e.g. contextual retrieval)
- Strong: cost-control for contextual enrichment (prompt caching) and incremental re-embed on updates
- Pitfall: never mix embedding model spaces in one collection; overlap ≠ free context

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Parse a PDF with tables via Unstructured/LlamaParse (or VLM path) — not flatten-to-garbage
- [ ] Chunk with overlap-aware / recursive strategy; tag source + section metadata
- [ ] Explain coreference loss from naive splits; name contextual-retrieval (or similar) mitigation
- [ ] Embed dense vectors; state when sparse/hybrid is required (SKU, code, exact terms)
- [ ] Never mix embedding model spaces in one collection — write a migration note
- [ ] Sketch incremental re-embed on doc update (what invalidates, what stays)

## Vector indexes & hybrid search
- id: rag-search
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r2-rag-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Contrast Flat vs IVF vs HNSW and the recall/latency tradeoff of ANN
- Implement hybrid dense+BM25 fused with RRF (or equivalent) plus metadata filters
- Explain why naive post-filtering destroys recall under selective filters; name pre-filter / filterable-HNSW remedies
- Tune at least one HNSW knob set (M / efConstruction / efSearch) with efSearch ≥ k reasoning
- Strong: use quantization + second-stage rerank to reclaim recall; know when pgvector/local beats a distributed DB

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Contrast Flat vs IVF vs HNSW recall/latency for ANN
- [ ] Pick distance metric (cosine / dot / L2) and justify for your embeddings
- [ ] Implement hybrid dense + BM25 fused with RRF (or equivalent)
- [ ] Add metadata pre-filter; explain why naive post-filter kills recall
- [ ] Tune HNSW (M / efConstruction / efSearch) with efSearch ≥ k reasoning
- [ ] State when pgvector/local beats a distributed vector DB

## Reranking, query transforms & generation
- id: rag-rerank-context
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r2-rag-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Place high-relevance chunks in high-attention positions after rerank; cite sources / allow I-don't-know
- Apply HyDE / multi-query / decomposition when recall is the bottleneck
- Mitigate lost-in-the-middle; know parent-document / auto-merging when chunks are too small
- Stream generation without losing attribution metadata

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Implement one query transform: HyDE or multi-query or decomposition
- [ ] Use parent-document or auto-merging when chunks are too small
- [ ] Add cross-encoder rerank on a bounded top-K; place best chunks in high-attention positions
- [ ] Mitigate lost-in-the-middle (ordering / windowing strategy)
- [ ] Prompt for citations + explicit I-don't-know when context is insufficient
- [ ] Stream generation without dropping attribution metadata

## RAG evaluation
- id: rag-evaluation
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r2-rag-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Separate retrieval metrics (context precision/recall, MRR, nDCG) from generation (faithfulness, answer relevancy)
- Run an automated eval (RAGAS / DeepEval / TruLens) — reject vibes-only gating
- Explain why faithfulness alone is insufficient (faithful-but-irrelevant answers)
- Mitigate LLM-as-judge positional and verbosity bias (swaps / dimensional rubrics)
- Maintain a stratified golden set (incl. multi-hop + answer-not-in-corpus); know a minimal size recipe (~200+)
- Strong: measure precision gap (retriever top-K vs true top-K) and context-rot / mid-context failures

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Separate retrieval metrics (precision/recall, MRR, nDCG) from generation (faithfulness, relevancy)
- [ ] Build a small stratified golden set incl. multi-hop + answer-not-in-corpus
- [ ] Know a minimal golden-set size recipe (~200+) for regression gating
- [ ] Run one automated eval stack (RAGAS or DeepEval/TruLens) — no vibes-only gating
- [ ] Explain faithful-but-irrelevant failure; why faithfulness alone fails
- [ ] Mitigate LLM-as-judge bias (position swap / dimensional rubric)

## Advanced RAG patterns
- id: advanced-rag-patterns
- status: not-started
- priority: 5
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r2-rag-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Use cross-encoder rerank on a bounded top-K to close the precision gap from bi-encoders
- Map symptoms→patterns: CRAG/Self-RAG for bad/irrelevant context; GraphRAG/RAPTOR for global themes
- Apply query rewrite for conversational ambiguity before retrieve
- Avoid agentic multi-hop for simple factual lookups (cost/latency/failure overhead)
- Strong: Adaptive routing by query complexity; ColBERT/late-interaction when cross-encoder latency blows up

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Map symptom→pattern: CRAG/Self-RAG for bad context; GraphRAG/RAPTOR for global themes
- [ ] Apply conversational query rewrite before retrieve
- [ ] State when NOT to use agentic multi-hop (simple factual lookup cost/latency)
- [ ] Sketch Adaptive RAG routing by query complexity
- [ ] Know ColBERT/late-interaction as alternative when cross-encoder latency blows up
