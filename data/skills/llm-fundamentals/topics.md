<!-- Topics for LLM Fundamentals. See MASTER.md for the format. -->

## Transformer architecture
- id: transformer-architecture
- status: not-started
- priority: 1
- min_required: true
- focus: true
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Explain encoder-decoder vs decoder-only and why decode is memory-bandwidth bound vs compute-heavy prefill
- Define GQA vs MHA/MQA and how shared KV heads shrink KV-cache footprint
- Explain RoPE at interview level and what breaks if you exceed pretrained context without extension (e.g. YaRN)
- Debug an OOM: distinguish massive-context prefill failure vs concurrent batch decode saturation
- Strong: relate PagedAttention to virtual memory / fragmentation, or FlashAttention's HBM↔SRAM goal (not just 'faster')

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [x] Sketch encoder-decoder vs decoder-only data flow and name when each is used
- [x] Write Q/K/V attention math for one head; extend to multi-head
- [x] Explain residual + LayerNorm placement and why FFN sits after attention
- [ ] Contrast MHA vs MQA vs GQA and how GQA shrinks KV-cache
- [ ] Explain RoPE at interview level and what breaks past pretrained context without extension
- [ ] Debug a mock OOM: distinguish giant-context prefill vs concurrent decode saturation
- [ ] One-liner each: FlashAttention goal (HBM↔SRAM) and PagedAttention as VM for KV cache

## Tokenization & context budgets
- id: tokenization
- status: not-started
- priority: 2
- min_required: true
- focus: true
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Contrast BPE / WordPiece / SentencePiece and when each shows up in practice
- Build deterministic token-counting middleware (tiktoken or HF) that rejects/truncates before API dispatch
- Use special tokens correctly for agent turns / structured outputs / FIM boundaries
- Explain asymmetric multilingual/code fragmentation and its cost + effective-context impact
- Debug prompt fragmentation from whitespace/YAML/casing changing the token sequence
- Strong: migrate between tokenizer families (e.g. cl100k→o200k) and adjust chunking for denser tokens

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Contrast BPE / WordPiece / SentencePiece with one real model each
- [ ] Count tokens with tiktoken (or HF) on the same prompt; note whitespace/casing diffs
- [ ] Build a small middleware that rejects or truncates by token budget before API call
- [ ] List special-token roles for chat turns, tools, and structured/FIM boundaries
- [ ] Show how multilingual or code text fragments denser/sparser than English prose
- [ ] Explain one-byte prompt-cache invalidation risk when prefixes are unstable

## Inference & decoding
- id: inference-decoding
- status: not-started
- priority: 3
- min_required: true
- focus: true
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Explain temperature/top-k/top-p, greedy vs beam, stop sequences, max tokens
- Use structured/constrained decoding for reliable JSON; know speculative decoding exists
- Relate sampling choices to agent reliability (too-hot tool JSON vs too-cold stuck plans)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Explain temperature, top-k, top-p, and when greedy beats sampling
- [ ] Contrast beam search vs sampling; name stop sequences and max-tokens traps
- [ ] Force valid JSON via structured/constrained decoding (schema or tool mode)
- [ ] Tune sampling for tool JSON reliability (too-hot vs too-cold failure modes)
- [ ] Know speculative decoding exists and what problem it targets

## Model landscape & selection
- id: model-landscape
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Compare closed vs open-weight families and embedding options with cost/latency/context/license/privacy
- Route cheap vs reasoning models with an explicit decision rule (ties to test-time-compute)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Compare one closed and one open-weight chat family on cost, latency, context, license, privacy
- [ ] Pick embedding models for RAG: when OpenAI/Cohere vs local BGE/E5/Jina
- [ ] Write a routing rule: cheap/fast model vs reasoning model by query type
- [ ] State when self-host open-weight beats API (data residency, cost at volume, customization)

## Prompt engineering
- id: prompt-engineering
- status: not-started
- priority: 5
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Build role boundaries (system/user/tool) that isolate instructions from untrusted input (defensive prompting)
- Implement ReAct and CoT so the model emits rationale before tool calls
- Enforce structured outputs via constrained decoding / JSON Schema / Pydantic (not fragile regex)
- Use few-shot without overfitting/repetition; chain discrete LLM calls with typed handoffs
- Strong: structure prompts for provider prompt-caching (stable prefix first; know one-byte invalidation)
- Strong: compact long sessions (summarize/scratchpad) instead of naive truncation alone

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Write system/user/tool role boundaries that isolate untrusted user content
- [ ] Implement a ReAct-style prompt that emits rationale before a tool call
- [ ] Enforce structured output via JSON Schema / Pydantic — not regex scraping
- [ ] Add few-shot examples without overfitting; note repetition failure mode
- [ ] Structure a stable prompt prefix for provider prompt-caching
- [ ] Compact a long session (summarize/scratchpad) instead of naive truncation alone

## LLM API integration
- id: llm-api-integration
- status: not-started
- priority: 6
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Stream via SSE with usable TTFT; separate reasoning vs tool-argument streams when both appear
- Normalize tool/function schemas across providers (e.g. OpenAI tools ↔ Anthropic tool_use)
- Handle 429/529 with exponential backoff + jitter + circuit breaker; failover without dropping schemas
- Parse partial JSON mid-stream safely; recover if the connection dies mid tool-call without double side-effects
- Cap recursion / tool-call depth / cost so autonomous loops cannot bankrupt the system
- Strong: multi-provider failover while preserving tool schemas and isolating provider usage metadata

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Call chat completions with tool/function schemas on one provider SDK
- [ ] Stream via SSE and measure usable TTFT; handle partial tokens cleanly
- [ ] Normalize a tool schema across two providers (e.g. OpenAI tools ↔ Anthropic tool_use)
- [ ] Implement 429/529 backoff with jitter + circuit breaker; no silent schema drop on failover
- [ ] Parse partial JSON mid-stream; recover mid tool-call without double side-effects
- [ ] Cap tool-call depth / recursion / cost so agent loops cannot runaway
- [ ] Build: script that streams + tool-calls + retries end-to-end
