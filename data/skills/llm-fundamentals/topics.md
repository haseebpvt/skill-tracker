<!-- Topics for LLM Fundamentals. Format reference: MASTER.md → "File formats". -->

## Tokenisation and context windows
- id: tokenisation-context
- status: comfortable
- priority: 1
- min_required: true
- focus: false
- updated: 2026-07-20

### What "enough" looks like
- Can estimate token counts and cost for a given workload without guessing
- Understands what actually degrades as context grows, and where in the window
- Can explain prompt caching: what is cacheable, what invalidates a cache prefix

### Notes / log
- 2026-07-20: costed out a real workload end to end; comfortable with the arithmetic

## Sampling parameters
- id: sampling-parameters
- status: comfortable
- priority: 2
- min_required: false
- focus: false
- updated: 2026-07-20

### What "enough" looks like
- Can explain temperature, top-p and their interaction without hand-waving
- Knows which knobs matter for structured output vs. creative generation

### Notes / log
- 2026-07-20: reviewed; solid enough for interview questions

## Prompting technique
- id: prompting-technique
- status: comfortable
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-01
- evidence: [raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can diagnose a failing prompt systematically rather than by trial and error
- Knows when few-shot examples help and when they lock the model into a bad pattern
- Can write a system prompt that survives adversarial user input

### Notes / log
- 2026-08-01: rewrote a flaky classifier prompt; failure rate dropped noticeably

## Structured output and schema enforcement
- id: structured-output
- status: learning
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-04
- evidence: [raw/jd/acme-agentic-2026-07.md]

### What "enough" looks like
- Can force valid JSON reliably and knows what to do when it still comes back malformed
- Understands the trade-off between tool-call-based and grammar-based enforcement
- Can design a schema the model finds easy to satisfy

### Notes / log
- 2026-08-04: hit repeated schema violations on nested objects; flattened the schema and it stabilised

## Embeddings and vector search
- id: embeddings-vector-search
- status: learning
- priority: 5
- min_required: true
- focus: false
- updated: 2026-07-30
- evidence: [raw/jd/northwind-ai-platform-2026-08.md]

### What "enough" looks like
- Can explain cosine similarity, dimensionality and what an embedding actually encodes
- Knows the index types (HNSW, IVF) well enough to pick one and defend the choice
- Understands chunking strategy and why it dominates retrieval quality

### Notes / log
- 2026-07-30: built a small semantic search over personal notes

## RAG architecture
- id: rag-architecture
- status: learning
- priority: 6
- min_required: true
- focus: false
- updated: 2026-08-06
- evidence: [raw/jd/northwind-ai-platform-2026-08.md, raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can design a retrieval pipeline end to end: ingest, chunk, embed, retrieve, rerank, generate
- Knows the standard failure modes and how to measure retrieval quality separately from generation quality
- Can explain when agentic retrieval beats a fixed single-shot retrieve step

### Notes / log
- 2026-08-06: read up on reranking; have not built a full pipeline yet

## Fine-tuning vs. prompting vs. RAG
- id: finetuning-tradeoffs
- status: not-started
- priority: 7
- min_required: false
- focus: false

### What "enough" looks like
- Can make the build/buy/tune call for a concrete problem and justify it on cost and latency
- Knows roughly what LoRA does and what data volume a fine-tune actually needs

### Notes / log
- Not started.
