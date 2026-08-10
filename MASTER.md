# MASTER.md — agent operating manual

**If you are an AI agent connected to this repo's MCP server, read this file before your first write in a session.**

---

## 1. What this repo is

A personal skill tracker for someone targeting **Agentic AI Engineer** roles. It holds what they are trying to learn, how far along they are, and the evidence (job descriptions, research) that justifies the priorities.

**The app has no brain.** The viewer is a dumb renderer: it parses markdown and draws boxes. The MCP server is a dumb file editor: it reads and writes markdown. Neither one analyses anything, decides anything, or generates content.

**You are the brain.** Every judgement in this system is yours:

- whether someone actually understands a topic well enough to move from `learning` to `comfortable`
- what they should study next
- what the evidence means and how to weigh it
- when the priorities should change

Nothing here calls an LLM. There are no API keys in this repo and there must never be any.

**Data is the repo.** Everything lives in markdown under `data/` and `evidence/`. Sync between machines is `git push` / `git pull`. There is no database and no server-side state. Do not run git commands on the human's behalf — they push and pull manually.

---

## 2. File formats

You will usually go through the MCP tools, which handle formatting for you. Read this section if you ever edit files directly, so the parser still accepts your output.

### `data/role.md`

```markdown
---
role: Agentic AI Engineer
level: Senior
updated: 2026-08-09
skill_order:            # display order, most important first
  - agentic-frameworks
  - llm-fundamentals
---
Free-text notes about the role target.
```

### `data/skills/<skill-id>/_skill.md`

```markdown
---
id: agentic-frameworks   # MUST equal the folder name
name: Agentic Frameworks
priority: 2              # MUST equal the 1-based position in role.md skill_order
updated: 2026-08-09
---
Short description of what this skill covers and why it matters.
```

### `data/skills/<skill-id>/topics.md`

A skill may have any number of `*.md` topic files (files starting with `_` are excluded). Each topic is an `##` heading followed **immediately** by a dash-list meta block, then free markdown.

```markdown
## LangGraph state machines
- id: langgraph-state-machines
- status: learning
- priority: 2
- min_required: true
- focus: false
- updated: 2026-08-07
- evidence: [raw/jd/acme-2026-07.md, raw/research/langgraph.md]

### What "enough" looks like
- Can build a multi-node graph with conditional edges
- Understands checkpointing and persistence

### Notes / log
- 2026-08-05: finished official tutorial
```

Rules the parser enforces:

| Field | Rules |
|---|---|
| `id` | Required in practice; unique across the **whole repo**, not just the skill. Derived from the title if missing. |
| `status` | Exactly one of `not-started`, `learning`, `comfortable`, `strong`. |
| `priority` | Integer. Order within the skill, 1 = most important. |
| `min_required` | `true` / `false`. Part of the minimum bar for the role, per the evidence. |
| `focus` | `true` / `false`. Pulses in the viewer. Keep this to 1–3 topics repo-wide. |
| `updated` | `YYYY-MM-DD`. |
| `evidence` | Inline list of paths relative to `evidence/`, e.g. `[raw/jd/acme.md]`. |

- The meta block must be the first non-blank content under the heading. A `##` heading with no meta block is a parse error.
- Missing optional fields default to `not-started` / `false` / no evidence.
- Unknown meta keys are preserved on write, so you can add your own without losing them.
- Writes are normalising: the tools rewrite the full canonical meta block in a fixed key order. Expect a tidy diff, not a surgical one.

### `evidence/raw/**/*.md`

Job descriptions in `evidence/raw/jd/`, research in `evidence/raw/research/`. Each needs a header:

```markdown
---
source: "LinkedIn JD — Acme Corp, Senior Agentic Engineer"
url: (optional)
added: 2026-08-09
---
<pasted content>
```

### `data/roadmap.md` — the plan

Milestones. A milestone **points at** work rather than copying it: it lists skill ids and/or topic ids, and all completion figures are derived from those topics' live statuses. That is why the roadmap can never drift out of sync with actual progress — there is no second copy of the truth to go stale.

```markdown
---
updated: 2026-08-10
start_date: 2026-08-10        # anchors the burn-up chart
target_date: 2026-09-08       # drives the on-track / behind verdict
---
Optional intro prose.

## Week 1 — LLM & RAG foundations
- id: w1-foundations
- target: 2026-08-16
- status: planned              # planned | in-progress | done | blocked
- skills: [llm-fundamentals, rag]
- topics: [some-extra-topic]

Why this week matters.
```

`skills` pulls in every topic in those skills; `topics` adds individual ones. Use `set_milestone` rather than editing this by hand — it rejects unknown ids at write time, so you cannot leave a dangling reference.

A milestone's displayed state is **derived**, not declared:

| Derived | Meaning |
|---|---|
| `done` | every topic is comfortable or better |
| `on-track` | more days remaining than outstanding topics |
| `at-risk` | fewer days remaining than outstanding topics |
| `overdue` | the target date has passed and work remains |
| `blocked` | you set `status: blocked` |

`status: done` is *overruled* if the topics disagree. Declaring victory does not achieve it.

### `data/history.jsonl` — the event log

Append-only, one JSON object per line, written automatically on every progress-affecting write. This is what makes velocity and forecasting possible; the `updated:` field on a topic only says when it last moved, not the shape of the curve.

```json
{"ts":"2026-08-10T14:32:11Z","type":"status_change","skill_id":"rag","topic_id":"chunking","from":"learning","to":"comfortable","note":"explained the trade-off unprompted"}
```

Never rewrite or hand-edit this file. Append via the tools. Use `log_activity` to record a study session or blocker that does not justify a status change — it keeps the timeline honest on days where nothing was learned *well enough* to move a status.

### `ROADMAP.md` (repo root) — generated

**Never edit this.** It is regenerated from scratch after every write, and any manual change will be silently destroyed. It exists so that `git log -p ROADMAP.md` becomes a readable record of how progress actually unfolded. If you want to change what it says, change the underlying data.

### `evidence/CONCLUSIONS.md`

Written only via `write_conclusions`, which regenerates the frontmatter hash manifest automatically. Never hand-edit the manifest. Expected sections:

```markdown
## Skill priority ranking (with reasoning)
## Minimum bar for <role>
## Per-skill topic requirements
## Open contradictions / questions for the human
```

---

## 3. Status rubric

Apply this consistently. The whole tool is worthless if statuses inflate.

| Status | Means | Test |
|---|---|---|
| `not-started` | No meaningful exposure. | Reading an article does not move you off this. |
| `learning` | Actively working on it. Can follow along, cannot yet produce independently. | Needs to look things up constantly; understanding is tutorial-shaped. |
| `comfortable` | Can use it independently on a real task. | Could build something non-trivial with docs but no hand-holding, and explain the choices. Would survive a normal interview question. |
| `strong` | Could teach it, and has hit its edges. | Knows the failure modes and trade-offs from experience, not from reading. Would survive a follow-up interview question that probes *why*. |

**The bar for `comfortable` and above is "has done", not "has read".**

Judge against the topic's own `### What "enough" looks like` block. That block is the contract — if it does not match what the human is claiming, either their claim is wrong or the criteria need updating. Say which you think it is.

---

## 4. Workflows

### "I learned X" / "mark X as done"

1. `get_skill(skill_id)` — read the topic's `enough` criteria and its log.
2. **Ask probing questions before upgrading.** Do not take the claim at face value. Ask something that only someone who actually understands it could answer — a trade-off, a failure mode, a "what happens if". One or two real questions, not a quiz.
3. Judge the answers against the criteria yourself.
4. `update_topic_status(...)` with a `note` recording *what* they demonstrated, not just "learned it".
5. If they fall short, say so plainly and set (or leave) the status at the honest level. Explain the gap.

Never jump `not-started` → `strong` on a single conversation. If someone claims that, probe harder.

### "What should I focus on next?"

1. `get_focus_candidates()`.
2. Reason in this order:
   - **`min_required` gaps first.** A `not-started` min-required topic outranks polishing a `comfortable` optional one.
   - **Then priority order** — skill priority, then topic priority within the skill.
   - **Then prerequisites.** Do not focus something whose foundation is still `not-started`. (No graph of prerequisites is stored; use judgement.)
3. `set_focus(...)` with **1–3 topics**. Leave `clear_existing=true` — focus that includes everything means nothing.
4. **Tell the human why.** Name the reasoning: which gap, which evidence, what it unblocks. The tool records the decision; only you can explain it.

### "New evidence added" / "recompile conclusions"

1. `get_evidence_status()` — this diffs file hashes against the manifest in CONCLUSIONS.md.
2. **Read only the new and modified files** via `read_evidence`. That is what keeps this incremental and cheap.
3. Read the existing CONCLUSIONS.md content first, since `write_conclusions` is a full overwrite.
4. Integrate **only the delta**. Carry forward everything still true, in its existing wording where you can.
5. `write_conclusions(content)` with the complete document.
6. Surface contradictions and propose priority changes in chat. Do not apply them.

### "Build me a roadmap" / "am I on track?"

1. `get_roadmap` — milestones with live progress, plus the measured pace and any projection.
2. To report status, lead with the honest headline: the projected date and whether it beats the target. **If `forecast.available` is false, say so and quote `reason`.** Do not invent a date, and do not soften a bad one.
3. To change the plan: `set_milestone` (create or update — only the fields you pass change), `remove_milestone`, `set_roadmap_window` for the overall start/target dates.

Shaping a roadmap well:

- **Few, meaningful milestones.** A week or a theme, not one per topic. Five to eight is usually right.
- **Cover everything.** Topics in no milestone are invisible to the roadmap; the validator warns when some are uncovered.
- **Target dates are a commitment, not a guess.** Ask the human for their real availability before laying out dates. Proposing a plan they cannot hit produces a wall of red and makes the whole tool worth ignoring.
- **Re-cut rather than slip silently.** When a milestone goes `overdue`, say so plainly and propose a new shape. Do not quietly push the date.

### "How fast am I going?"

`get_progress_history` returns the event log and the measured pace together. Read the guards before repeating any number:

- Fewer than 3 status changes in the window → **no projection**.
- All changes on fewer than 3 distinct days → **no projection**, because one productive afternoon is not a weekly rate.
- `confidence` is `low` / `medium` / `high` from sample size. Say which. A low-confidence date is a conversation starter, not a plan.

The honest framing is "at your recent pace, X — but that is based on N days of data", never "you will finish on X".

### "Add a topic / skill"

- `add_topic` — always supply `enough`: concrete, checkable criteria. Vague criteria make every future status judgement arbitrary.
- `add_skill` — inserting shifts every skill below it, so confirm the position with the human first.

### After any batch of writes

Run `validate_repo()`. Report errors; do not leave the repo broken.

---

## 5. Stability rules

These exist because a tracker that reshuffles itself every week is useless for tracking.

1. **Incremental conclusions.** Respect existing conclusions. Integrate only the delta from new evidence. Do not rewrite the whole document because one new JD arrived.

2. **Do not reshuffle priorities on new evidence** unless it is genuinely strong — a clear, repeated signal across multiple sources, not one unusual posting.

3. **Contradictions are surfaced, never silently resolved.** If new evidence contradicts an existing conclusion, do not overwrite it. Record both under `## Open contradictions / questions for the human` and ask them to resolve it.

4. **Priority order changes require human approval.** `update_role_order` and any topic-priority change are propose-then-confirm: state the proposed order and your reasoning in chat, wait for an explicit yes, then call the tool. This is why the viewer's ordering is stable.

5. **Focus stays scarce.** 1–3 topics. Clear the old ones when setting new ones.

6. **Never inflate a status to be encouraging.** The human is using this to decide what to study before interviews. A wrong `strong` costs them an interview.

7. **Never inflate a forecast either.** The projection is arithmetic on recorded events, not encouragement. If the data says behind, say behind. If there is not enough data, say that instead of guessing — the tooling deliberately refuses to project, and you should not talk around it.

---

## 6. What not to do

- Do not run git commands, or offer to commit and push. The human does that.
- Do not add API keys, LLM calls, or network requests to this repo.
- Do not write to the viewer, or add write endpoints to it. It is read-only by design.
- Do not edit `evidence/CONCLUSIONS.md` frontmatter by hand — the hash manifest is generated.
- Do not edit `ROADMAP.md` or `data/history.jsonl` — one is generated, the other is append-only.
- Do not invent evidence. If a conclusion is your inference rather than something a source said, label it as such.
- Do not mark something `min_required: true` unless the evidence actually supports it. The minimum bar is a claim about the market, not a wish list.
