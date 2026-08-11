---
source: "Deep research R5 — GenAI observability, AppSec, streaming failure modes"
added: 2026-08-10
---

# Senior Engineering Interview Rubric: Production GenAI Services

**Scope note.** This rubric grades three competency areas for engineers building and operating production LLM/GenAI services. A cross-cutting section at the end draws the line between **agentic guardrails** (agent-specific safety/security) and **general AppSec** so the two security sections do not duplicate content.

---

## Section 1 — Observability & LLM Observability

### Comfortable bar
Candidate treats the three signals (logs, metrics, traces) as distinct and can map them to production incidents. Knows Google SRE's **four golden signals** (latency, traffic, errors, saturation) and the **RED method** (Rate, Errors, Duration — coined by Tom Wilkie in 2015 while at Weaveworks and first presented at a Prometheus meetup in London: *"The RED Method — For every service, monitor request: Rate, Errors, Duration"*), and that RED is essentially the golden signals minus saturation. Can name LLM-specific metrics: TTFT (time to first token), inter-token/time-per-output-token latency, tokens/sec throughput, and per-request token counts and dollar cost. Understands prompt/response logging as ground truth for incident investigation.

### Strong bar
Candidate knows the **OpenTelemetry GenAI semantic conventions** by name and that they are still experimental — per a July 2026 review of the `open-telemetry/semantic-conventions-genai` repo, *"As of July 17, 2026, no GenAI-specific span, event, metric, or attribute in the dedicated repository is marked Stable; the GenAI conventions remain Development"* (HTTP conventions, by contrast, stabilized in v1.23.0 in Nov 2023). Can cite the actual convention: `gen_ai.client.operation.duration` (per the SemConv 1.40.0 cheat sheet, April 2026, *"gen_ai.client.operation.duration is required. gen_ai.client.token.usage is recommended when token counts are available"* — filter `token.usage` by `gen_ai.token.type` = input/output), server-side `gen_ai.server.time_to_first_token` and `gen_ai.server.time_per_output_token`, and span attributes `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.finish_reasons`. Understands that a single LLM interaction is a trace spanning prompt construction → retrieval → model call → parse, and that in agent chains each call can be 200 OK while the overall chain fails (compound failure). Treats p99 TTFT carefully because latency is non-deterministic with token count and KV-cache/batching. For RAG, insists on **provenance**: which chunks/documents/data-source IDs (`gen_ai.data_source.id`) fed a given answer, for both debugging and attribution. Knows that streaming breaks naive span timing — the span must stay open until stream completion, and cost is derived from token counts × per-token price.

### 5 probing questions
1. Walk me through the spans and attributes you'd emit for one RAG request. Where does TTFT get measured, and how do you keep the span correct under streaming?
2. Your p99 latency doubled but error rate is flat. How do you tell a model-provider regression from a prompt-length shift from a batching/KV-cache effect?
3. How do you track cost per request and per user/session, and where does the dollar figure actually come from?
4. What do you log for prompts and responses, and how do you keep that log both useful and compliant?
5. An agent chain "succeeds" on every step but produces a wrong final answer. What observability catches this that request-level metrics miss?

### False-confidence signals
- Reciting "logs, metrics, traces" but collapsing them into "we send everything to Datadog" with no signal design.
- Claiming OTel GenAI conventions are stable/GA (they remain Development) or inventing attribute names.
- Treating average latency as sufficient; no percentile or distribution reasoning.
- "We log the full prompt and response" with no mention of PII redaction or sampling cost.
- Equating LLM observability with an eval dashboard (quality) while ignoring operational/economic signals.

### Anti-goals (don't reward)
- Over-indexing on a specific vendor tool as if it were the standard.
- Building a bespoke tracing schema when OTel GenAI conventions exist.
- Logging raw full-content on 100% of traffic with no redaction/sampling — expensive and a liability.
- Vanity dashboards (token counts with no SLO or alert attached).

---

## Section 2 — AppSec + LLM Security

### Comfortable bar
Candidate knows the **OWASP Top 10 (2021)** for web — Broken Access Control (#1), Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable/Outdated Components, Identification & Authentication Failures, Software & Data Integrity Failures, Security Logging & Monitoring Failures, SSRF (#10) — and can talk through OAuth2 flows, JWT validation (verify signature, `exp`, `aud`, `iss`), short-lived access tokens + refresh token rotation, and secrets management (no secrets in client/code, rotation). Knows the **OWASP Top 10 for LLM Applications 2025** (v2025, doc v4.2.0a, released Nov 2024): LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data & Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector & Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption (broadened from the 2023 "Model Denial of Service" entry to cover token-flood, "denial of wallet" cost inflation, and model-extraction). Can explain direct vs. indirect prompt injection and basic PII redaction.

### Strong bar
Candidate articulates why prompt injection is not fully solvable ("LLMs process instructions and data in the same channel") and defends in depth: input/retrieval filtering, output allow-listing, segregating untrusted content, and treating model output as untrusted (LLM05 → downstream injection). Explains **indirect prompt injection** precisely: malicious instructions embedded in retrieved documents or tool outputs, invisible at the UI, one poisoned document affecting every user who triggers retrieval, and that defenses built for direct injection fail here because the content looks like legitimate data. Knows PII redaction is a deterministic gateway concern (regex + NER, e.g. Presidio), that masking (irreversible) vs. tokenization (reversible, still GDPR-regulated) is a real design choice, and that redacting before logging is defense-in-depth, not a substitute for access control. Maps LLM02 (sensitive disclosure) and LLM10 (unbounded consumption / "denial of wallet") to concrete controls: token-level rate limits, output scanning, egress control. Understands **SSRF** as a classic web risk AND its amplified agent form.

### 5 probing questions
1. A user pastes a doc into your RAG assistant and it starts leaking another tenant's data. Which OWASP-LLM risks are in play and what's your fix order?
2. Direct vs. indirect prompt injection — which is harder to defend, and why do input filters fail against one of them?
3. Walk me through JWT validation for a service-to-service call. What do you check, and what's the failure mode if you skip `aud`?
4. Where do you enforce PII redaction, and when does masking beat tokenization?
5. How is "Improper Output Handling" (LLM05) different from prompt injection, and what breaks if you trust model output downstream?

### False-confidence signals
- "We tell the model in the system prompt to ignore injections" as a complete defense.
- Treating a WAF or a single classifier as sufficient against prompt injection.
- Confusing authentication with authorization; assuming a valid JWT implies authorized action.
- "We redact PII with a regex" with no NER, no testing for false negatives, no mention of where in the pipeline.
- Listing OWASP categories by rote without mapping to their own architecture.

### Anti-goals (don't reward)
- Security theater: elaborate prompt-level "jailbreak defenses" while ignoring output handling and authz.
- Rolling custom crypto or custom JWT parsing instead of vetted libraries.
- Blocklist-based SSRF/PII defenses presented as complete.
- Over-scoping model access to "just in case" broad permissions (excessive agency).

---

## Section 3 — Serving LLM Streams Securely (FAILURE MODES)

*Focus is exclusively on failure modes, not feature tours.*

### Comfortable bar
Candidate picks **SSE for one-way token streaming** and **WebSockets only for bidirectional** needs (mid-stream interruption, human-in-the-loop approval, voice). Knows SSE auto-reconnects (EventSource) while WebSockets need custom reconnect with exponential backoff. Recognizes the headline failure mode: when a client disconnects from a `StreamingResponse`, the server does not automatically stop — the generator keeps running (and keeps the upstream LLM call and DB session alive) unless you check `await request.is_disconnected()` (or handle `WebSocketDisconnect`). Knows retries need exponential backoff + jitter and must not retry non-idempotent operations.

### Strong bar
Candidate treats client disconnect as a **first-class event**: aborts the upstream LLM call, and does post-stream DB writes on a *fresh* session (a long stream holds an idle transaction open — a real production failure). Discusses **backpressure**: a slow client causes buffers to grow; you must throttle upstream consumption (respect drain / `bufferedAmount`). Uses a **typed event protocol** (token, error, usage, done) rather than overloading `data:`, so mid-stream errors are distinguishable from content. Sizes connection limits for **concurrent active connections**, not RPS. On **stream auth**: passes a short-lived token at handshake (URL param or first message) so unauthenticated connections are rejected before resources are allocated, and handles the hard case — **token expiry mid-stream** on a long-lived connection — via in-band renewal (send fresh token over the existing connection) vs. reconnect-with-new-token, choosing based on state complexity. On **retries with httpx/tenacity**: retries only idempotent/transient failures (timeouts, connection errors, 5xx, 429 with `Retry-After`), never 4xx or non-idempotent POSTs without idempotency keys; wraps with `wait_exponential_jitter` + `stop_after_attempt`; and critically understands **you cannot naively retry a half-consumed stream** — once tokens are emitted, a retry restarts generation and duplicates/charges twice. Knows retries without budgets create retry storms; alerts on retry exhaustion, not first failure.

### 5 probing questions
1. A client closes the tab mid-stream. Walk through everything that keeps running server-side and how you stop it. What happens to your DB transaction?
2. Your JWT expires 3 minutes into a 10-minute stream. What are your options and what do you pick?
3. When is it safe to retry an LLM streaming call, and when does a retry duplicate work or double-charge?
4. A slow consumer is reading your stream. What fails first, and how do backpressure signals help?
5. SSE vs WebSocket for a chat UX with mid-stream cancellation — which, and what's the failure trade-off?

### False-confidence signals
- "Starlette/FastAPI cancels the generator automatically on disconnect" — unreliable across versions; must check explicitly.
- Wrapping the entire streaming call in a blanket `@retry` (re-runs generation, double-bills, duplicates tokens).
- Putting the auth token only in a query string with no note on logging exposure / short TTL.
- Retrying 4xx or non-idempotent POSTs; retrying with no jitter or stop condition.
- Treating SSE and WebSocket as interchangeable without the bidirectional distinction.

### Anti-goals (don't reward)
- Reaching for WebSockets by default when SSE suffices (needless protocol complexity).
- Building a custom retry framework instead of tenacity/httpx transport retries.
- Infinite retries or unbounded reconnect loops (thundering herd).
- Over-engineering a bespoke streaming protocol when a typed SSE event schema is enough.

---

## Cross-Cutting: Agentic Guardrails vs. General AppSec

To avoid double-counting between Sections 2 and 3, grade these as **distinct buckets**:

**General AppSec (standard OWASP Top 10 web).** Applies to any web service regardless of AI: Broken Access Control, authn/authz (OAuth2/JWT), Cryptographic Failures, Injection (SQL/command/XSS), Security Misconfiguration, Vulnerable Components, Logging & Monitoring Failures, and *classic* SSRF (a user-supplied URL parameter reaching a fetcher). Mitigations are the mature, well-understood ones: parameterized queries, least-privilege access control, secrets management, dependency scanning, egress allow-lists, IMDSv2. A senior candidate should treat these as table stakes that **do not change** because an LLM is in the stack.

**Agentic guardrails (agent-specific).** Applies only when the LLM can *act* — call tools, retrieve, or execute. These are the concerns that general AppSec does not cover:
- **Tool-use permissioning / least agency (LLM06 Excessive Agency):** per-tool scoped permissions, task-scoped and time-bound credentials, per-action authorization via a policy engine, human-in-the-loop for high-impact actions. The failure is an agent "working as designed" taking actions a human wouldn't approve.
- **Agent-initiated SSRF:** distinct from classic SSRF because the *model chooses the URL at runtime* — there is no fixed parameter to validate, the fetch tool exists precisely to retrieve arbitrary things, and an attacker can steer it via any content that reaches context. Fetched content returns into the model's context, turning SSRF into a read/exfiltration primitive (169.254.169.254 metadata, localhost services). Defenses: egress allow-lists (not blocklists), resolve-then-connect post-resolution IP validation to close the DNS-rebinding TOCTOU gap, scheme allow-listing, IMDSv2 + network-layer metadata blocking.
- **Indirect prompt injection via tool/retrieval outputs:** malicious instructions in retrieved docs, web pages, MCP tool metadata, or tool results. Broader blast radius than chat injection because agents chain tool calls and act with less oversight — InjecAgent (Zhan et al., UIUC, ACL Findings 2024, arXiv:2403.02691) showed ReAct-prompted GPT-4 had a 24% attack success rate in the base setting, *"nearly doubling to 47% in the enhanced setting"* with a hacking prompt, across a benchmark of 1,054 test cases, 17 user tools, and 62 attacker tools.
- **Agent identity & memory:** isolated per-agent identities, memory-poisoning defenses, authenticated inter-agent communication, circuit breakers for cascading multi-agent failures. See the **OWASP Top 10 for Agentic Applications 2026** (OWASP GenAI Security Project), announced at Black Hat Europe 2025 / the OWASP Agentic Security Summit, using ASI01–ASI10 identifiers (ASI01 Agent Goal Hijack through ASI10 Rogue Agents; memory poisoning is ASI06).

**Grading rule:** a candidate who solves agentic risks with only general-AppSec tools (e.g., "we validate the URL parameter") has missed the point; one who reinvents web-AppSec basics under an "AI security" banner is over-engineering. Reward candidates who apply mature AppSec where it fits and add agentic controls *only* where the agent's ability to act creates genuinely new surface.

---

## How to Use This Rubric

- **Weighting by role:** For an LLM platform/infra role, weight Sections 1 and 3 heavily. For an AI application security role, weight Section 2 and the cross-cutting section. A candidate should clear the Comfortable bar in all three and the Strong bar in at least their specialty.
- **Calibrate to architecture:** A read-only chat assistant rarely needs deep LLM06/agentic answers; a RAG or tool-using agent must. Penalize candidates who apply the agentic checklist to a system that doesn't warrant it (over-engineering) and those who ignore it when the system clearly does (blind spot).
- **Caveat on sources:** OWASP LLM/agentic lists and OTel GenAI conventions are moving targets — the OTel GenAI conventions are still "Development" (not stable) as of mid-2026, and exact attribute/metric names may change. Reward candidates who name conventions *and* acknowledge their experimental status over those who quote them as immutable fact.
