import { useCallback, useMemo, useState } from 'react'
import Header from './components/Header.jsx'
import IssuesBanner from './components/IssuesBanner.jsx'
import FocusStrip from './components/FocusStrip.jsx'
import SkillRow from './components/SkillRow.jsx'
import TopicDrawer from './components/TopicDrawer.jsx'
import Conclusions from './components/Conclusions.jsx'
import Roadmap from './components/Roadmap.jsx'
import MilestonePanel from './components/MilestonePanel.jsx'
import Legend from './components/Legend.jsx'
import Markdown from './components/Markdown.jsx'
import { useSkillState } from './lib/useSkillState.js'
import { deriveView } from './lib/derive.js'

function Centered({ children }) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center px-6">
      <div className="max-w-md text-center">{children}</div>
    </div>
  )
}

export default function App() {
  const { state, connected, loading, error } = useSkillState()
  const [minOnly, setMinOnly] = useState(false)
  const [selected, setSelected] = useState(null)

  const view = useMemo(() => deriveView(state, minOnly), [state, minOnly])

  const closeDrawer = useCallback(() => setSelected(null), [])
  const toggleMinOnly = useCallback(() => setMinOnly((v) => !v), [])

  // Milestone chips carry a trimmed topic shape (no body_md / enough_md), so
  // resolve back to the full topic by id before opening the drawer.
  const topicsById = useMemo(() => {
    const index = new Map()
    for (const skill of state?.skills || []) {
      for (const topic of skill.topics || []) index.set(topic.id, topic)
    }
    return index
  }, [state])

  const selectTopic = useCallback(
    (topic) => setSelected((topic && topicsById.get(topic.id)) || topic),
    [topicsById]
  )

  // Keep the open milestone in sync with incoming SSE state rather than
  // holding a stale snapshot, so ticking a box updates the panel behind it.
  const [openMilestoneId, setOpenMilestoneId] = useState(null)
  const openMilestone = useMemo(() => {
    const list = state?.roadmap?.milestones || []
    return list.find((m) => m.id === openMilestoneId) || null
  }, [state, openMilestoneId])

  // The panel wants full topic objects (with checklists) in milestone order.
  const openMilestoneTopics = useMemo(() => {
    if (!openMilestone) return []
    return (openMilestone.topics || []).map((t) => topicsById.get(t.id) || t)
  }, [openMilestone, topicsById])

  const toggleChecklistItem = useCallback(async (skillId, topicId, itemId, checked) => {
    const response = await fetch('/api/checklist', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill_id: skillId, topic_id: topicId, item_id: itemId, checked }),
    })
    if (!response.ok) {
      let detail = `HTTP ${response.status}`
      try {
        detail = (await response.json()).error || detail
      } catch {
        /* keep the status code */
      }
      throw new Error(detail)
    }
    // No local state update needed: the backend publishes fresh state over SSE.
    return response.json()
  }, [])

  // Backend unreachable and nothing cached — show a readable error, not a blank page.
  if (!state) {
    if (loading) {
      return (
        <Centered>
          <p className="text-sm text-ink-3">Loading…</p>
        </Centered>
      )
    }
    return (
      <Centered>
        <h1 className="text-lg font-semibold text-ink">Can't reach the tracker backend</h1>
        <p className="mt-2 text-sm text-ink-2">
          The viewer couldn't load <code className="font-mono">/api/state</code>
          {error ? ` (${error})` : ''}. Make sure the local server is running, then this page will
          reconnect on its own.
        </p>
      </Centered>
    )
  }

  const hasSkills = view.skills.length > 0

  return (
    <div className="flex min-h-full flex-col">
      <IssuesBanner issues={state.issues} />

      <Header
        role={state.role}
        summary={view.summary}
        minBar={view.minBar}
        git={state.git}
        connected={connected}
        minOnly={minOnly}
        onToggleMinOnly={toggleMinOnly}
        generatedAt={state.generated_at}
      />

      <FocusStrip focus={view.focus} onSelect={selectTopic} />

      <main className="mx-auto w-full max-w-[1400px] flex-1 px-6 py-6">
        <div className="mb-5">
          <Roadmap
            roadmap={state.roadmap}
            velocity={state.velocity}
            history={state.history}
            onSelectTopic={selectTopic}
            onOpenMilestone={(milestone) => setOpenMilestoneId(milestone?.id || null)}
          />
        </div>

        {state.role && state.role.notes_md ? (
          <details className="mb-5 rounded-xl border border-line bg-surface px-4 py-3 shadow-sm">
            <summary className="cursor-pointer text-sm font-medium text-ink-2">
              Role notes
            </summary>
            <div className="mt-1">
              <Markdown>{state.role.notes_md}</Markdown>
            </div>
          </details>
        ) : null}

        {hasSkills ? (
          <div className="space-y-4">
            {view.skills.map((skill, idx) => (
              <SkillRow
                key={skill.id || idx}
                skill={skill}
                onSelectTopic={selectTopic}
              />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-dashed border-line-strong bg-surface px-6 py-12 text-center">
            <p className="text-sm text-ink-2">
              {minOnly
                ? 'No minimum-required topics match the current filter.'
                : 'No skills defined yet.'}
            </p>
          </div>
        )}

        <div className="mt-6">
          <Conclusions
            conclusions={state.conclusions}
            evidenceStatus={state.evidence_status}
          />
        </div>
      </main>

      <Legend />

      <MilestonePanel
        milestone={openMilestone}
        topics={openMilestoneTopics}
        onToggle={toggleChecklistItem}
        onOpenTopic={selectTopic}
        onClose={() => setOpenMilestoneId(null)}
      />

      <TopicDrawer topic={selected} onClose={closeDrawer} onToggleItem={toggleChecklistItem} />
    </div>
  )
}
