# Skill Tracker

A local-first, git-synced tool for tracking skill and topic proficiency while preparing for interviews and upskilling.

The design principle is that **the app has no brain**. The viewer parses markdown and draws coloured boxes; the MCP server reads and writes markdown. All the intelligence — judging whether you actually know something, deciding what to study next, weighing job descriptions — comes from an agent (Claude Code, Cursor, …) connected over MCP. See [MASTER.md](MASTER.md), which is the agent's operating manual.

Your data is the repo. Syncing between machines is `git push` / `git pull`. No database, no hosting, no accounts, no API keys.

---

## Quick start

```bash
./scripts/launch.sh          # macOS / Linux
python scripts/launch.py     # any platform
```

That syncs Python dependencies, builds the UI if it is stale, serves on <http://localhost:8749>, and opens a browser.

Prerequisites: [uv](https://docs.astral.sh/uv/) and Node.js 18+.

Useful flags:

| Flag | Effect |
|---|---|
| `--dev` | Also run the Vite dev server (hot reload) on port 5174 |
| `--no-open` | Do not open a browser |
| `--rebuild` | Force a UI rebuild |
| `--port N` | Serve the backend on a different port |

---

## Registering the MCP server

The server talks stdio and needs the repo path. Substitute your own path for `/path/to/skill-tracker`.

### Claude Code

```bash
claude mcp add skill-tracker \
  --env SKILL_TRACKER_REPO=/path/to/skill-tracker \
  -- uv run --project /path/to/skill-tracker python -m skilltracker_mcp
```

Then, in a session: *"Read MASTER.md, then give me an overview."*

### Cursor

`.cursor/mcp.json`, either in the project or at `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skill-tracker": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/skill-tracker", "python", "-m", "skilltracker_mcp"],
      "env": { "SKILL_TRACKER_REPO": "/path/to/skill-tracker" }
    }
  }
}
```

`SKILL_TRACKER_REPO` is what lets the server find the repo regardless of the working directory it is started in.

---

## Everyday use

Talk to your agent; watch the viewer update live.

| You say | The agent does |
|---|---|
| "I worked through LangGraph checkpointing" | Reads the topic's criteria, **asks you probing questions**, then sets the status honestly and logs what you demonstrated |
| "What should I focus on next?" | Reads every topic, reasons about min-bar gaps and priority, flags 1–3 topics as focus (they pulse in the UI), and tells you why |
| "Plan my next four weeks" | Creates milestones with target dates; the viewer shows a timeline, a burn-up chart and whether you are on track |
| "Am I going to make it?" | Reads the event log, measures your actual pace, and projects a completion date — or tells you there isn't enough history yet |
| "I pasted a new JD into evidence/raw/jd/" | Diffs file hashes, reads only what is new, updates conclusions incrementally, surfaces contradictions |
| "Add a topic for prompt caching" | Adds it with concrete "what enough looks like" criteria |

The agent will push back on status claims rather than accepting them — that is deliberate, and it is the point of the tool.

---

## Checklists — what to actually do

A topic tells you *what* to learn; its checklist tells you *what to do*, in order. Items are plain GFM task-list lines inside the topic's own markdown:

```markdown
### Checklist
- [x] Explain self-attention (QKV) from memory
- [ ] Implement a toy attention head in numpy
```

Click a milestone in the viewer and a panel opens listing every topic in that week, each with its items in learning order and a checkbox you can tick. The tick is written straight back into the markdown — the checkbox state *is* the file, so there is no second store to drift.

Two badges flag holes in the plan: **needs breakdown** (a topic with no items — "learn X" with nothing actionable under it) and **evidence needed** (a topic whose criteria nothing in `evidence/` supports). Both show in the viewer and as validator warnings, and `get_coverage_gaps` hands the agent the list sorted by which milestone is due soonest.

Coverage and status are reported as **separate numbers everywhere**, deliberately. Ticking every box records work done; it does not make you `comfortable`. That judgement still goes through the agent probing you.

> **One deliberate exception to the read-only rule.** The viewer has exactly one write endpoint, `POST /api/checklist`, taking one item id and one boolean. Routing "I just finished this problem" through an agent would be worse than useless. Everything else — statuses, topics, milestones, conclusions — is still MCP-only. A test asserts this endpoint is the only non-GET route, so a second cannot appear by accident.

---

## Roadmap and forecasting

`data/roadmap.md` holds milestones. A milestone **references** topics and skills rather than copying their state, so its progress is derived from live topic statuses and can never drift out of sync with reality. Each one gets a schedule verdict — `on-track`, `at-risk`, `overdue`, `done`, `blocked` — computed from outstanding topics against the target date. Declaring a milestone `done` while its topics say otherwise does not work; the topics win.

Every progress-affecting write appends a timestamped line to `data/history.jsonl` and regenerates `ROADMAP.md` at the repo root. Both are plain text, so `git log -p ROADMAP.md` becomes a readable record of how the month actually went.

From that log the viewer computes your pace and projects a finish date, drawn as a burn-up chart: what you have actually done, the straight line you would need to follow to hit the target, and a dashed projection at your current rate.

**The forecast refuses to lie to you.** It will not project a date from fewer than 3 status changes, or from changes that all land on fewer than 3 distinct days — one productive afternoon is not a weekly rate. When it declines, it says why, and it always reports the sample size and a confidence level. A projection is arithmetic on what you recorded, not encouragement.

Neither `ROADMAP.md` nor `data/history.jsonl` should be hand-edited: the first is regenerated from scratch on every write, the second is append-only.

---

## The data

```
ROADMAP.md                    GENERATED status report — regenerated on every write
data/
  role.md                     target role, level, skill display order
  roadmap.md                  milestones and target dates (the plan)
  history.jsonl               append-only event log — the basis for velocity
  skills/<skill-id>/
    _skill.md                 skill metadata + description
    topics.md                 all topics for the skill (any number of *.md files)
evidence/
  raw/jd/*.md                 job descriptions you have pasted in
  raw/research/*.md           research output
  CONCLUSIONS.md              agent-compiled: priorities, minimum bar, contradictions
```

Every file is plain markdown and meant to be read, hand-edited, and diffed. The exact format is documented in [MASTER.md](MASTER.md#2-file-formats).

**The seed data is a worked example.** The four skills are real topics for an Agentic AI Engineer, but the job descriptions in `evidence/raw/` are fictional placeholders and are labelled as such. Replace them with real postings and ask your agent to recompile conclusions before trusting any of it.

### Statuses

| Status | Colour in the UI |
|---|---|
| `not-started` | grey |
| `learning` | amber |
| `comfortable` | deep green |
| `strong` | bright green |

A pulsing border means `focus: true`. A ★ badge means `min_required: true` — part of the minimum bar for the role, per the evidence.

### Theming

The viewer is dark, always — there is no toggle and no OS-preference sniffing, so it looks the same on every machine. The whole palette is a block of semantic tokens at the top of [`viewer/ui/src/index.css`](viewer/ui/src/index.css) (`--color-surface`, `--color-ink-2`, `--color-st-strong`, …), and components only ever reference those tokens. Retheming — including adding a light mode — means overriding that block, not touching components.

---

## Checking the repo

```bash
uv run skilltracker validate    # unique ids, valid statuses, evidence refs resolve, ordering consistent
uv run skilltracker overview    # progress summary in the terminal
uv run skilltracker state       # full parsed model as JSON
uv run pytest                   # test suite
```

`validate` exits non-zero if there are errors, so it works as a pre-commit hook. The viewer shows the same issues in a banner rather than crashing.

---

## Architecture

Two processes over one repo, with no direct link between them:

```
   agent (Claude Code / Cursor)          you, in an editor
              │                                  │
              │ MCP tools (stdio)                │
              ▼                                  ▼
        ┌───────────────────────────────────────────┐
        │  markdown files in data/ and evidence/    │
        └───────────────────────────────────────────┘
                             │ watchdog sees the change
                             ▼
              FastAPI backend ──SSE──▶ React UI
```

The MCP server never talks to the viewer. The viewer watches the filesystem, so an edit made by the agent — or by you in an editor — turns up in the browser within a second either way.

| Layer | Choice |
|---|---|
| UI | React + Vite + Tailwind v4, read-only |
| Viewer backend | FastAPI + watchdog + SSE, one uvicorn process serving API and static UI |
| MCP server | Python, official `mcp` SDK, stdio |
| Shared | `core/` — markdown parsing, writing and validation, used by both |

`core/` is the only place that knows the file format, so parsing exists exactly once.

### Layout

```
core/          shared parse/write/validate
mcp-server/    MCP server (src/skilltracker_mcp)
viewer/
  backend/     FastAPI app (skilltracker_viewer)
  ui/          React app
scripts/       launcher
```

All three Python packages are declared in the single root `pyproject.toml` rather than one per directory, so `uv sync` sets everything up in one step.

---

## Deliberate non-goals

No hosting, no auth, no multi-user. No database. No LLM calls or API keys anywhere in this repo — the connected agent is the only intelligence. No editing in the UI. No automatic git operations; the viewer shows git status read-only and nothing more.

The backend is stateless over files, so hosting *could* be added later, but it is not built and is not wanted now.
