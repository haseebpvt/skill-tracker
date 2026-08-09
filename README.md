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
| "I pasted a new JD into evidence/raw/jd/" | Diffs file hashes, reads only what is new, updates conclusions incrementally, surfaces contradictions |
| "Add a topic for prompt caching" | Adds it with concrete "what enough looks like" criteria |

The agent will push back on status claims rather than accepting them — that is deliberate, and it is the point of the tool.

---

## The data

```
data/
  role.md                     target role, level, skill display order
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
| `learning` | yellow |
| `comfortable` | light green |
| `strong` | full green |

A pulsing border means `focus: true`. A ★ badge means `min_required: true` — part of the minimum bar for the role, per the evidence.

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
