<!-- Topics for Python Production Stack. See MASTER.md for the format. -->

## Pydantic v2
- id: pydantic-v2
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r5-obs-security-2026-08-10.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Model request/tool schemas with Field, validators, discriminated unions, BaseSettings
- Produce JSON Schema for tools via model_json_schema and bind structured outputs safely
- Choose validation failure handling (reject vs model-repair loop) for LLM-produced data

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Model with BaseModel, Field, field_validator, model_validator
- [ ] Serialize with model_dump / model_dump_json; use discriminated unions
- [ ] Load config via BaseSettings; define a custom type if needed
- [ ] Emit tool JSON Schema via model_json_schema and bind structured outputs
- [ ] Choose validation failure handling for LLM data: reject vs model-repair loop

## FastAPI core & DI
- id: fastapi-core
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r5-obs-security-2026-08-10.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Build typed routes with Pydantic validation, Depends (incl. yield), middleware/CORS
- Explain DI lifetime pitfalls (yield deps + streaming) and how you avoid leaked resources
- Structure routers/services so LLM orchestration stays testable behind Depends overrides

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Build typed routes: path/query/body + response models
- [ ] Wire Depends including yield dependencies; add CORS/custom middleware
- [ ] Explain DI lifetime pitfalls with yield deps + streaming; avoid leaked resources
- [ ] Structure routers/services so LLM orchestration is testable behind Depends overrides
- [ ] Override deps in TestClient for unit tests

## FastAPI streaming, auth & clients
- id: fastapi-streaming-auth
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/rubric-r5-obs-security-2026-08-10.md, raw/research/rubric-r1-llm-fundamentals-2026-08-10.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Stream tokens with SSE (WebSocket only if bidirectional); typed events (token/error/usage/done)
- On client disconnect: stop upstream LLM + release DB — check is_disconnected; don't hold idle txns
- Auth streams with short-lived tokens; plan for mid-stream expiry (renew vs reconnect)
- Retry only idempotent/transient failures; never naively retry a half-consumed stream (double bill)
- Use httpx + tenacity with jitter/budgets; alert on retry exhaustion

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Stream LLM tokens with StreamingResponse SSE; typed events (token/error/usage/done)
- [ ] On client disconnect: stop upstream LLM + release resources (is_disconnected)
- [ ] Auth streams with short-lived JWT/API key; plan mid-stream expiry (renew vs reconnect)
- [ ] Use httpx async client + tenacity with jitter/budgets; alert on retry exhaustion
- [ ] Never naively retry a half-consumed stream (double-bill risk)
- [ ] Build: FastAPI SSE stream + JWT auth end-to-end
- [ ] Know Uvicorn/Gunicorn deployment shape behind a reverse proxy
