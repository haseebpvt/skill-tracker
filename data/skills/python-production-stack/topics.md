<!-- Topics for Python Production Stack. See MASTER.md for the format. -->

## Pydantic v2
- id: pydantic-v2
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Use BaseModel, validators, discriminated unions, BaseSettings
- Produce tool schemas via model_json_schema()

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## FastAPI core & DI
- id: fastapi-core
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Routes, validation, Depends (incl. yield), middleware/CORS

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## FastAPI streaming, auth & clients
- id: fastapi-streaming-auth
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-09
- evidence: [raw/research/one-month-plan.md]

### What "enough" looks like
- Stream LLM tokens via SSE; JWT/API-key auth; lifespan; TestClient
- Use httpx + tenacity for resilient async HTTP

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
