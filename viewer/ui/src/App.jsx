import { useCallback, useMemo, useState } from 'react'
import Header from './components/Header.jsx'
import IssuesBanner from './components/IssuesBanner.jsx'
import FocusStrip from './components/FocusStrip.jsx'
import SkillRow from './components/SkillRow.jsx'
import TopicDrawer from './components/TopicDrawer.jsx'
import Conclusions from './components/Conclusions.jsx'
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

      <FocusStrip focus={view.focus} onSelect={setSelected} />

      <main className="mx-auto w-full max-w-[1400px] flex-1 px-6 py-6">
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
                onSelectTopic={setSelected}
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

      <TopicDrawer topic={selected} onClose={closeDrawer} />
    </div>
  )
}
