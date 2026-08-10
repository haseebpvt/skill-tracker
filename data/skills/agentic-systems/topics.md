<!-- Topics for Agentic Systems & Frameworks. See MASTER.md for the format. -->

## Workflows vs agents & design patterns
- id: workflows-vs-agents-patterns
- status: not-started
- priority: 1
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Choose workflow vs autonomous agent with explicit failure-cost / predictability reasoning
- Explain and sketch prompt chaining, routing, parallelization (sectioning/voting), orchestrator-workers, evaluator-optimizer, and autonomous agent loops
- State the triad for justified agents: environment (state), tools (actions), system prompt (goals/stops)

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Agent loop fundamentals
- id: agent-loop-fundamentals
- status: not-started
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Implement ReAct, reflection, task decomposition, tool schemas + error handling
- Manage short-term vs long-term memory and structured outputs

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## LangGraph state machines
- id: langgraph-state-machines
- status: not-started
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Build StateGraph with schema, conditional edges, checkpointing, HITL, streaming
- Rebuild a RAG chain as LangGraph with routing

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## LangChain fluency
- id: langchain-fluency
- status: not-started
- priority: 4
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Build a RAG chain with LCEL, retrievers, output parsers, callbacks
- Know LlamaIndex at awareness level only

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## MCP architecture & tool design
- id: mcp-architecture
- status: not-started
- priority: 5
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Explain host/client/server, JSON-RPC, stdio vs SSE transports, and tools/resources/prompts
- Design mistake-proof tool schemas (names, constraints, descriptions) and least-privilege access
- Build a Python MCP server and describe auditability of tool calls

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Framework selection (LangGraph / Agents SDK / PydanticAI / CrewAI)
- id: agent-framework-selection
- status: not-started
- priority: 6
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Compare LangGraph, OpenAI Agents SDK, PydanticAI, and CrewAI on orchestration philosophy and durable state
- Map a failure-cost profile to a framework (e.g. LangGraph for durable/HITL; Agents SDK for fast handoffs)
- Describe a realistic migration path from prototype (CrewAI/SDK) to production LangGraph

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Multi-agent & MCP
- id: multi-agent-mcp
- status: not-started
- priority: 7
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Design supervisor/router teams; try one of CrewAI / AutoGen / OpenAI Agents SDK
- Build a Python MCP server (tools/resources/prompts)

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Agentic failure modes
- id: agentic-failure-modes
- status: not-started
- priority: 8
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Name and mitigate infinite tool loops, paralysis, context poisoning/truncation, cognitive framework lag, and multi-agent error propagation
- Specify concrete controls: step counters, similarity-based loop detection, hard token limits, scratchpad hygiene

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Test-time compute & reasoning models
- id: test-time-compute
- status: not-started
- priority: 9
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Explain test-time compute / long-thinking models (o-series, DeepSeek-R1) vs next-token chat models
- Design async pipelines (queues + SSE/WebSockets) so long reasoning does not time out clients
- Route simple tasks to cheap/fast models and reserve reasoning models for hard multi-step work with cost awareness

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Agent memory systems
- id: agent-memory-systems
- status: not-started
- priority: 10
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Differentiate episodic vs semantic memory and when each belongs in an agent architecture
- Describe production memory approaches (e.g. Mem0 / Zep-style long-term memory) at design level

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Agent evaluation & tracing
- id: agent-evaluation
- status: not-started
- priority: 11
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/one-month-plan.md, raw/research/agentic-ai-engineer-study-plan.md]

### What "enough" looks like
- Trace trajectories (LangSmith or equiv), detect loops, track cost per step

### Notes / log
- 2026-08-09: topic added
- 2026-08-09: 30-day crunch path; status not-started until demonstrated

## Agentic guardrails
- id: agentic-guardrails
- status: not-started
- priority: 12
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Layer defenses: edge classifiers, dialogue rails (NeMo/Colang), structural output validation (Guardrails AI / Pydantic)
- Tie guardrails to OWASP GenAI risks: prompt injection, sensitive disclosure, hallucinated tools, excessive agency

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Agent benchmarks & eval CI
- id: agent-benchmarks-eval-ci
- status: not-started
- priority: 13
- min_required: true
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Know SWE-bench, GAIA, and Tau-bench at the level of what they measure
- Design an LLM-as-judge / red-team regression gate in CI before shipping agent changes

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional

## Agent PEFT & trajectory tuning
- id: agent-peft-trajectories
- status: not-started
- priority: 14
- min_required: false
- focus: false
- updated: 2026-08-10
- evidence: [raw/research/agentic-ai-engineer-study-plan.md, raw/research/one-month-plan.md]

### What "enough" looks like
- Explain trajectory-based SFT (thought → tool → observation → answer) and resolution-based gating
- Describe LoRA/QLoRA for agents and Mixture-of-Roles (reasoner/executor/summarizer) at conceptual level

### Notes / log
- 2026-08-10: topic added
- 2026-08-10: Added from Agentic AI Engineer study plan (2026); overlap with 30-day path kept intentional
