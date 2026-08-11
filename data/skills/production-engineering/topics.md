<!-- Topics for Production Engineering & Security. See MASTER.md for the format. -->

## Observability & LLM observability
- id: observability
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r5-obs-security-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Map logs/metrics/traces to incidents; use RED / golden signals for services
- Emit LLM metrics: TTFT, time-per-output-token, tokens, $ cost; keep spans open across streams
- Trace a RAG/agent request end-to-end with provenance (which chunk/doc IDs grounded the answer)
- Know OTel GenAI conventions exist and are still evolving — don't invent a private schema as 'the standard'
- Catch compound agent failures that request-level success metrics miss

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Map logs/metrics/traces to an incident; use RED / golden signals
- [ ] Emit LLM metrics: TTFT, time-per-output-token, tokens, $ cost; keep spans open across streams
- [ ] Trace a RAG/agent request end-to-end with provenance (chunk/doc IDs)
- [ ] Know OTel GenAI conventions exist and are evolving — don't invent a private 'standard'
- [ ] Catch compound agent failures that request-level success metrics miss
- [ ] Dashboards + alerting for SLIs/SLOs on an LLM gateway

## App + LLM security
- id: security
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r5-obs-security-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Apply OWASP web Top 10 table stakes: authn/z (OAuth2/JWT aud/iss/exp), secrets, SQLi, classic SSRF
- Map OWASP LLM Top 10 (esp. injection, sensitive disclosure, excessive agency, unbounded consumption)
- Defend indirect prompt injection via retrieved/tool content; treat model output as untrusted (LLM05)
- Place PII redaction (Presidio/NER+regex) before logs and egress; know mask vs tokenize trade-off
- Separate general AppSec from agentic guardrails (tool permissioning lives with agentic-guardrails)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Apply OWASP web table stakes: OAuth2/JWT (aud/iss/exp), secrets, SQLi, classic SSRF
- [ ] Map OWASP LLM Top 10 focus: injection, sensitive disclosure, excessive agency, unbounded consumption
- [ ] Defend indirect prompt injection via retrieved/tool content; treat model output as untrusted
- [ ] Place PII redaction (Presidio/NER+regex) before logs and egress; mask vs tokenize trade-off
- [ ] Python-specific: pickle risks, supply-chain, Bandit awareness
- [ ] Keep tool permissioning depth in agentic-guardrails — don't double-count

## Reliability & performance
- id: reliability-performance
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r5-obs-security-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Apply circuit breaker, retry+jitter, timeouts, idempotency keys, health checks, load shedding
- Profile Python hotspots; reason about P95/P99 and simple load tests for LLM gateways

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Apply circuit breaker, retry+jitter, timeouts, idempotency keys
- [ ] Add health checks, backpressure, and load shedding for an LLM gateway
- [ ] Profile a Python hotspot (cProfile/py-spy); reason about GIL/event-loop latency
- [ ] Reason about P50/P95/P99; sketch a Locust/k6 load test for streaming endpoints
- [ ] Cache wisely (lru_cache/Redis) without serving stale embeddings/answers blindly
- [ ] Know MTTR/MTBF/RPO/RTO and when a post-mortem is required
