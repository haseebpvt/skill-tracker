<!-- Topics for Python Mastery. See MASTER.md for the format. -->

## Object model, descriptors & dunders
- id: python-object-model
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Predict mutable-default / aliasing bugs; implement a useful descriptor and key dunders (__eq__/__hash__/__repr__)
- Explain MRO/C3 enough to debug diamond inheritance; know when metaclasses are NOT the answer
- Use __slots__ with a measured memory reason, not cargo-cult

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Predict a mutable-default / aliasing bug; fix it without surprises
- [ ] Implement a useful descriptor (__get__/__set__) for a real validation case
- [ ] Implement __eq__/__hash__/__repr__ correctly for a value type
- [ ] Explain MRO/C3 on a diamond hierarchy; know when metaclasses are NOT the answer
- [ ] Use __slots__ with a measured memory reason (not cargo-cult)
- [ ] Build: custom descriptor + slots class with the dunders above

## Generators, imports & scoping
- id: python-generators-imports
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Write generators with yield/yield from; know send/throw/close exist and when not to use them
- Resolve circular imports with structure (interfaces, lazy import) — not random hacks
- Use closures/nonlocal correctly; explain LEGB when shadowing bites

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Write generator functions/expressions with yield and yield from
- [ ] Know send/throw/close exist; state when NOT to use them in app code
- [ ] Resolve a circular import via structure (interfaces / lazy import)
- [ ] Use closures + nonlocal correctly; explain LEGB when shadowing bites
- [ ] Contrast absolute vs relative imports; fix a broken package layout

## Concurrency & asyncio
- id: python-concurrency
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Choose threads vs processes vs asyncio with GIL/I/O reasoning for agent tool fan-out
- Use TaskGroup/gather safely; cancel and bound concurrency under provider rate limits
- Bridge sync SDKs with to_thread/run_in_executor without blocking the event loop

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Choose threads vs processes vs asyncio with GIL/I/O reasoning for tool fan-out
- [ ] Write producer-consumer with threading; rewrite with asyncio
- [ ] Use gather/TaskGroup safely; cancel and bound concurrency under rate limits
- [ ] Bridge a sync SDK with to_thread/run_in_executor without blocking the loop
- [ ] Name Lock/race pitfalls and fork vs spawn process start methods

## Typing & pytest quality
- id: python-typing-testing
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Annotate generics/TypedDict/Protocol/overload so mypy/pyright catches real bugs
- Write pytest fixtures, parametrize, asyncio tests; mock at boundaries (not the unit under test's guts)
- Choose unit vs integration vs e2e for an LLM-calling service without over-mocking the model

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Annotate a module with Generic/TypeVar, TypedDict, Protocol, overload; pass mypy/pyright
- [ ] Write pytest fixtures (scopes), parametrize, markers, pytest-asyncio tests
- [ ] Mock at boundaries (HTTP/LLM client) — not the guts of the unit under test
- [ ] Choose unit vs integration vs e2e for an LLM-calling service without over-mocking the model
- [ ] Lint with ruff; know branch vs line coverage; package via pyproject.toml + uv/poetry
