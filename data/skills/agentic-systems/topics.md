<!-- Topics for Agentic Systems & Frameworks. See MASTER.md for the format. -->

## Workflows vs agents & design patterns
- id: workflows-vs-agents-patterns
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Choose workflow vs autonomous agent with explicit failure-cost / predictability / token-cost reasoning
- Sketch prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, autonomous loops
- State the triad for justified agents: environment, tools, system prompt/stop conditions
- Call out over-engineering: multi-agent for simple repeatable business processes

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Choose workflow vs autonomous agent with failure-cost / predictability / token-cost reasoning
- [ ] Sketch prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- [ ] State the triad for justified agents: environment, tools, stop conditions/system prompt
- [ ] Call out multi-agent over-engineering for simple repeatable processes

## Agent loop fundamentals
- id: agent-loop-fundamentals
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Implement ReAct/reflection/decomposition with tool schemas and error handling
- Manage short-term vs long-term memory and structured outputs inside the loop
- Bound steps/tokens and detect repeated tool calls (ties to failure-modes topic)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Implement ReAct with tool schemas and error handling on tool failure
- [ ] Add reflection or task decomposition inside the loop
- [ ] Manage short-term vs long-term memory handoff in the loop
- [ ] Enforce structured outputs for tool args / final answer
- [ ] Bound steps/tokens; detect repeated tool-call loops

## LangChain fluency
- id: langchain-fluency
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Build LCEL/chains with retrievers, output parsers, and callbacks/tracing
- Decide chain vs agent: use a chain when steps are known; don't pay agent-loop entropy for fixed pipelines
- Name LangChain limits (over-chaining, opaque agents, token blowups) and when to drop to direct SDK / LangGraph
- Use callbacks for streaming/monitoring rather than blind trust of chain output

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars
- 2026-08-11: priority 3 (before LangGraph) so LCEL/chains come first

### Checklist
- [ ] Build an LCEL/chain with retriever, output parser, and callbacks
- [ ] Decide chain vs agent: fixed steps → chain; don't pay agent-loop entropy
- [ ] Name LangChain limits (over-chaining, opaque agents, token blowups) and when to drop to SDK/LangGraph
- [ ] Use callbacks for streaming/monitoring rather than blind trust of chain output
- [ ] Awareness: LlamaIndex index/query engines as alternative retrieval stack

## LangGraph state machines
- id: langgraph-state-machines
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Build a StateGraph with typed state, conditional edges, streaming, and a real checkpointer
- Pause/resume with HITL interrupts (prefer dynamic interrupts over permanently blocking static ones)
- Recover after crash using durable checkpointing (e.g. PostgresSaver) — not memory-only in prod talk
- Separate short-term checkpoints from longer-term stores; control retention to avoid checkpoint bloat
- Anti-pattern: manual external state hacks that fight the graph runtime; or LangGraph for one-step tasks

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars
- 2026-08-11: priority 4 (after LangChain fluency)

### Checklist
- [ ] Build StateGraph with typed state, conditional edges, and streaming
- [ ] Add a durable checkpointer (not memory-only for prod talk)
- [ ] Pause/resume with HITL interrupt (prefer dynamic over permanently blocking)
- [ ] Separate short-term checkpoints from longer-term stores; control retention
- [ ] Anti-pattern check: no manual external state fighting the graph; no LangGraph for one-step tasks
- [ ] Build: RAG chain rebuilt as LangGraph with conditional routing + checkpointing

## MCP architecture & tool design
- id: mcp-architecture
- status: not-started
- priority: 5
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Explain host/client/server, JSON-RPC, stdio vs SSE, tools/resources/prompts
- Design poka-yoke tool schemas and least-privilege exposure
- Build a Python MCP server; discuss auditability of tool calls

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Explain host/client/server, JSON-RPC, stdio vs SSE transports
- [ ] Map primitives: tools, resources, prompts
- [ ] Design poka-yoke tool schemas with least-privilege exposure
- [ ] Build a minimal Python MCP server
- [ ] Discuss auditability of tool calls (who called what, with what args)

## Framework selection (LangGraph / Agents SDK / PydanticAI / CrewAI)
- id: agent-framework-selection
- status: not-started
- priority: 6
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Compare LangGraph, OpenAI Agents SDK, PydanticAI, CrewAI on orchestration + durable state
- Map failure-cost profile → framework (durable/HITL vs fast handoffs vs type-safe DI)
- Describe a prototype→production migration path when ephemeral state breaks down

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Compare LangGraph, OpenAI Agents SDK, PydanticAI, CrewAI on orchestration + durable state
- [ ] Map failure-cost profile → framework (durable/HITL vs fast handoffs vs type-safe DI)
- [ ] Describe prototype→production migration when ephemeral state breaks down
- [ ] Hands-on: pick one non-LangGraph framework and run a tiny agent

## Multi-agent & MCP
- id: multi-agent-mcp
- status: not-started
- priority: 7
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Design supervisor/router vs hierarchical teams with clear specialist roles and result synthesis
- Choose parallel router vs sequential handoff with latency/duplication trade-offs
- Handle multi-agent failures: loops, duplicated work, supervisor SPOF, missing context handoff
- Keep MCP protocol depth in mcp-architecture — this topic is orchestration/team design
- Anti-pattern: multi-agent theater when a single agent/workflow suffices

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Design supervisor/router vs hierarchical teams with clear specialist roles
- [ ] Choose parallel router vs sequential handoff with latency/duplication trade-offs
- [ ] Handle failures: loops, duplicated work, supervisor SPOF, missing context handoff
- [ ] Anti-pattern: multi-agent theater when a single agent/workflow suffices
- [ ] Keep MCP protocol depth in mcp-architecture — focus orchestration here

## Agentic failure modes
- id: agentic-failure-modes
- status: not-started
- priority: 8
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Mitigate infinite tool loops, paralysis, context poisoning/truncation, CFL, multi-agent error propagation
- Specify controls: step counters, similarity loop detection, hard token limits, scratchpad hygiene

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Mitigate infinite tool loops and agent paralysis
- [ ] Handle context poisoning / truncation and catastrophic forgetting of goals
- [ ] Contain multi-agent error propagation
- [ ] Specify controls: step counters, similarity loop detection, hard token limits, scratchpad hygiene

## Test-time compute & reasoning models
- id: test-time-compute
- status: not-started
- priority: 9
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Explain test-time compute / long-thinking models vs ordinary next-token chat models
- Design async delivery (queue + SSE/WebSocket progress) so long reasoning does not time out clients
- Route simple work to cheap/fast models and escalate only hard multi-step work to reasoning models
- Instrument cost/latency per query; add early-exit/caching so loops cannot explode spend
- Anti-pattern: forcing every query through slow-thinking pipelines

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Explain test-time compute / long-thinking vs ordinary next-token chat models
- [ ] Design async delivery (queue + SSE/WS progress) so long reasoning doesn't time out clients
- [ ] Route simple work to cheap/fast; escalate only hard multi-step work
- [ ] Instrument cost/latency per query; add early-exit/caching against spend explosions
- [ ] Anti-pattern: forcing every query through slow-thinking pipelines

## Agent memory systems
- id: agent-memory-systems
- status: not-started
- priority: 10
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Differentiate episodic vs semantic memory and place each in an architecture
- Describe production long-term memory approaches (Mem0/Zep-style) at design level with failure modes (poisoning)

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Differentiate episodic vs semantic memory; place each in an architecture sketch
- [ ] Describe production LTM approaches (Mem0/Zep-style) at design level
- [ ] Name memory poisoning failure modes and a mitigation
- [ ] Compact long sessions (summarize/scratchpad) vs dumping full history

## Agent evaluation & tracing
- id: agent-evaluation
- status: not-started
- priority: 11
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Capture full trajectories (LLM + tool + branch) in LangSmith/Langfuse/Phoenix or OTel gen_ai spans
- Track per-step tokens, latency, loop/tool counts, and cost — not only final-answer score
- Debug a 'all steps 200 OK but wrong answer' compound failure from the trace tree
- Combine offline eval on saved traces with online sampling on live traffic

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Capture full trajectories (LLM + tool + branch) in LangSmith/Langfuse/Phoenix or OTel
- [ ] Track per-step tokens, latency, loop/tool counts, and cost — not only final-answer score
- [ ] Debug an 'all steps 200 OK but wrong answer' failure from the trace tree
- [ ] Combine offline eval on saved traces with online sampling on live traffic

## Agentic guardrails
- id: agentic-guardrails
- status: not-started
- priority: 12
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Layer defenses: input/retrieval rails, schema validation on tool calls, output filters, tool-call gating
- Contrast Guardrails AI (structural validators) vs NeMo (dialogue/execution rails) with a fit reason
- Defend LLM01/LLM06-style risks: injection (esp. indirect via tools/RAG) and excessive agency
- Detect hallucinated / unauthorized tool calls at runtime; HITL for high-impact actions
- Keep classic AppSec (JWT/SQLi) in production-engineering/security — don't double-count here

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Layer defenses: input/retrieval rails, schema validation on tool calls, output filters, tool gating
- [ ] Contrast Guardrails AI vs NeMo with a fit reason for one use case
- [ ] Defend indirect injection via tools/RAG and excessive agency (LLM01/LLM06-style)
- [ ] Detect hallucinated/unauthorized tool calls; HITL for high-impact actions
- [ ] Keep classic AppSec (JWT/SQLi) in production-engineering/security

## Agent benchmarks & eval CI
- id: agent-benchmarks-eval-ci
- status: not-started
- priority: 13
- min_required: true
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Explain what SWE-bench, GAIA, and Tau-bench measure and when each is relevant
- Build a private golden/regression set for your real tasks (don't ship on public leaderboard alone)
- Gate PRs with LLM-as-judge + tool-path checks; include red-team cases (injection, malicious tool output)
- Know judge pitfalls (no gold / vague rubrics → false pass) and alert on eval regressions

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Explain what SWE-bench, GAIA, and Tau-bench measure and when each is relevant
- [ ] Build a private golden/regression set for your real tasks (not public leaderboard alone)
- [ ] Gate PRs with LLM-as-judge + tool-path checks; include injection/malicious-tool red-team cases
- [ ] Know judge pitfalls (no gold / vague rubrics → false pass); alert on eval regressions

## Agent PEFT & trajectory tuning
- id: agent-peft-trajectories
- status: not-started
- priority: 14
- min_required: false
- focus: false
- updated: 2026-08-11
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md, raw/research/rubric-r3-agentic-2026-08-10.md]

### What "enough" looks like
- Explain trajectory SFT (thought→tool→observation→answer) and resolution-based gating
- Describe LoRA/QLoRA and Mixture-of-Roles at conceptual level — optional depth for this crunch

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
- 2026-08-10: Rubric refreshed from deep-research comfortable/strong bars

### Checklist
- [ ] Explain trajectory SFT (thought→tool→observation→answer) and resolution-based gating
- [ ] Describe LoRA/QLoRA at conceptual level for agent fine-tunes
- [ ] Know Mixture-of-Roles exists as an optional depth idea — not required for crunch
