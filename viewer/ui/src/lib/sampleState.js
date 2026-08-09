// Development fixture only. NOT imported by the running app — the app always
// reads live data from /api/state and /api/events. Kept for manual checks:
// temporarily `import sampleState from './lib/sampleState.js'` in App.jsx and
// seed it into state if you want to render without the backend.

const topic = (over) => ({
  id: 'topic',
  skill_id: 'dsa',
  skill_name: 'DSA',
  title: 'Untitled',
  status: 'not-started',
  priority: 1,
  min_required: false,
  focus: false,
  updated: '2026-08-01',
  evidence: [],
  enough_md: '',
  log_md: '',
  body_md: '',
  extra: {},
  ...over,
})

const sampleState = {
  generated_at: '2026-08-09T12:00:00Z',
  role: {
    role: 'Agentic AI Engineer',
    level: 'Senior',
    updated: '2026-08-09',
    skill_order: ['dsa', 'agentic-frameworks'],
    notes_md: 'Targeting **senior** agentic roles. Emphasis on production systems.',
  },
  skills: [
    {
      id: 'dsa',
      name: 'Data Structures & Algorithms',
      priority: 1,
      updated: '2026-08-08',
      description_md: 'Core problem-solving foundation for interviews.',
      progress: {
        percent: 55.5,
        total: 4,
        counts: { 'not-started': 1, learning: 1, comfortable: 1, strong: 1 },
        min_required_total: 3,
        min_required_met: 2,
      },
      topics: [
        topic({
          id: 'arrays',
          title: 'Arrays and two pointers',
          status: 'strong',
          priority: 1,
          min_required: true,
          body_md: '### What enough looks like\n- Solve medium problems in 20 min\n\n### Notes / log\n- 2026-07-02: done',
        }),
        topic({
          id: 'graphs',
          title: 'Graph traversal (BFS/DFS)',
          status: 'comfortable',
          priority: 2,
          min_required: true,
          enough_md: '- Can implement BFS/DFS from scratch',
        }),
        topic({
          id: 'dp',
          title: 'Dynamic programming',
          status: 'learning',
          priority: 3,
          min_required: true,
          focus: true,
          evidence: ['raw/jd/acme.md'],
        }),
        topic({ id: 'tries', title: 'Tries', status: 'not-started', priority: 4 }),
      ],
    },
    {
      id: 'agentic-frameworks',
      name: 'Agentic Frameworks',
      priority: 2,
      updated: '2026-08-09',
      description_md: 'LangGraph, tool calling, orchestration patterns.',
      progress: {
        percent: 25.0,
        total: 3,
        counts: { 'not-started': 2, learning: 1, comfortable: 0, strong: 0 },
        min_required_total: 2,
        min_required_met: 0,
      },
      topics: [
        topic({
          id: 'langgraph-state-machines',
          skill_id: 'agentic-frameworks',
          skill_name: 'Agentic Frameworks',
          title: 'LangGraph state machines',
          status: 'learning',
          priority: 1,
          min_required: true,
          focus: true,
          updated: '2026-08-07',
          evidence: ['jd/acme-2026-07.md'],
          enough_md: '- Can build a multi-node graph\n- Understands checkpointing',
          log_md: '- 2026-08-05: finished official tutorial',
          body_md:
            '### What enough looks like\n- Can build a multi-node graph\n- Understands checkpointing\n\n### Notes / log\n- 2026-08-05: finished official tutorial',
        }),
        topic({
          id: 'tool-calling',
          skill_id: 'agentic-frameworks',
          skill_name: 'Agentic Frameworks',
          title: 'Tool calling and schemas',
          status: 'not-started',
          priority: 2,
          min_required: true,
        }),
        topic({
          id: 'evals',
          skill_id: 'agentic-frameworks',
          skill_name: 'Agentic Frameworks',
          title: 'Agent evaluation harnesses',
          status: 'not-started',
          priority: 3,
        }),
      ],
    },
  ],
  focus: [],
  summary: {
    overall_percent: 41.3,
    total_topics: 7,
    counts: { 'not-started': 3, learning: 2, comfortable: 1, strong: 1 },
    min_bar: { total: 5, met: 2 },
  },
  conclusions: {
    exists: true,
    updated: '2026-08-09',
    content_md:
      '## Skill priority ranking\n\n1. **DSA** — gates every interview loop.\n2. **Agentic frameworks** — the differentiator.\n\n## Minimum bar\n\nAt least *comfortable* on all starred topics.',
    sections: ['Skill priority ranking (with reasoning)', 'Minimum bar'],
    evidence_files_considered: [{ path: 'raw/jd/acme.md', hash: 'ab12cd34ef56' }],
  },
  evidence_status: {
    new: ['raw/jd/new.md'],
    modified: [],
    deleted: [],
    unchanged: ['raw/jd/acme.md'],
  },
  git: { available: true, branch: 'main', dirty: true, last_commit: 'abc1234 initial commit' },
  issues: [
    { level: 'warning', path: 'data/skills/dsa/topics.md', message: 'topic "tries" has no enough_md' },
  ],
}

// Focus array mirrors the focused topics across skills.
sampleState.focus = sampleState.skills.flatMap((s) => s.topics.filter((t) => t.focus))

export default sampleState
