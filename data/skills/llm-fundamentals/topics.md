<!-- Topics for LLM Fundamentals. See MASTER.md for the format. -->

## Transformer architecture
- id: transformer-architecture
- status: not-started
- priority: 1
- min_required: true
- focus: true
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Explain self-attention (QKV), multi-head attention, positional encoding
- Describe FFN, layer norm, residuals, encoder-decoder vs decoder-only
- Name MQA/GQA/Flash Attention and when they matter

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Tokenization & context budgets
- id: tokenization
- status: not-started
- priority: 2
- min_required: true
- focus: true
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Contrast BPE / WordPiece / SentencePiece / tiktoken
- Count tokens, manage budgets, handle special tokens

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Inference & decoding
- id: inference-decoding
- status: not-started
- priority: 3
- min_required: true
- focus: true
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Explain temperature, top-k, top-p, greedy vs beam, stop sequences
- Use structured generation (JSON mode / constrained decoding)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Model landscape & selection
- id: model-landscape
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Compare closed vs open-weight models and embedding options
- Pick a model with explicit cost / latency / context / license / privacy trade-offs

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Prompt engineering
- id: prompt-engineering
- status: not-started
- priority: 5
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Use roles, zero/few-shot, CoT, ReAct, structured-output prompting
- Apply defensive prompting and prompt chaining

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## LLM API integration
- id: llm-api-integration
- status: not-started
- priority: 6
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Ship a script with tool calling, streaming, retries, and cost awareness
- Use openai / anthropic / google-genai SDKs; handle rate limits and failover

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
