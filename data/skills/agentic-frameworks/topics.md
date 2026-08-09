<!-- Topics for Agentic Frameworks. Format reference: MASTER.md → "File formats". -->

## Agent loop fundamentals
- id: agent-loop-fundamentals
- status: strong
- priority: 1
- min_required: true
- focus: false
- updated: 2026-07-28
- evidence: [raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can write a bare ReAct-style loop from scratch, no framework, in ~100 lines
- Can explain when the loop should stop, and how to bound it (step cap, budget, no-progress detection)
- Knows why tool results go back in as messages rather than as prompt text

### Notes / log
- 2026-07-28: wrote a from-scratch loop with tool dispatch; comfortable explaining it end to end

## LangGraph state machines
- id: langgraph-state-machines
- status: learning
- priority: 2
- min_required: true
- focus: true
- updated: 2026-08-07
- evidence: [raw/jd/acme-agentic-2026-07.md, raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can build a multi-node graph with conditional edges and a typed state object
- Understands checkpointing, persistence, and resuming an interrupted run
- Can add a human-in-the-loop interrupt and resume from it
- Has built at least one real project on it, not just the tutorial

### Notes / log
- 2026-08-05: finished the official tutorial
- 2026-08-07: built a two-node graph with a conditional edge; checkpointing still fuzzy

## Tool / function calling design
- id: tool-calling-design
- status: comfortable
- priority: 3
- min_required: true
- focus: false
- updated: 2026-08-02
- evidence: [raw/jd/acme-agentic-2026-07.md]

### What "enough" looks like
- Can design a tool schema that the model actually calls correctly first time
- Handles parallel tool calls and partial failures
- Knows how to keep tool descriptions cheap in tokens without losing precision

### Notes / log
- 2026-08-02: shipped a 6-tool agent; learned the hard way that vague descriptions cause wrong-tool calls

## Model Context Protocol (MCP)
- id: mcp-servers
- status: learning
- priority: 4
- min_required: true
- focus: true
- updated: 2026-08-09
- evidence: [raw/jd/northwind-ai-platform-2026-08.md, raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can write an MCP server with tools, resources and prompts over stdio
- Understands the transport options and when each is appropriate
- Can register a server with a client and debug the handshake when it fails

### Notes / log
- 2026-08-09: building this repo's MCP server as the first real one

## Multi-agent orchestration
- id: multi-agent-orchestration
- status: not-started
- priority: 5
- min_required: false
- focus: false
- evidence: [raw/research/agentic-stack-2026.md]

### What "enough" looks like
- Can articulate when multi-agent genuinely beats one well-prompted agent (and when it does not)
- Knows the common topologies: supervisor/worker, hand-off, blackboard
- Can reason about context isolation and the cost of passing state between agents

### Notes / log
- Not started.

## Agent evaluation and tracing
- id: agent-evaluation
- status: not-started
- priority: 6
- min_required: true
- focus: false
- evidence: [raw/jd/northwind-ai-platform-2026-08.md, raw/jd/acme-agentic-2026-07.md]

### What "enough" looks like
- Can build a regression suite of task traces and score runs against it
- Knows the difference between step-level and outcome-level evaluation
- Has used a tracing tool to debug a real multi-step failure

### Notes / log
- Not started. Flagged in two JDs as a hard requirement — this is the biggest single gap.

## Guardrails and failure handling
- id: guardrails-failure-handling
- status: not-started
- priority: 7
- min_required: false
- focus: false

### What "enough" looks like
- Can bound cost and latency per run, and degrade gracefully at the limit
- Handles malformed tool arguments, tool timeouts and infinite loops
- Knows where to put validation so a bad model output cannot cause a side effect

### Notes / log
- Not started.
