import { useState } from 'react'
import TopicBox from './TopicBox.jsx'
import ProgressBar from './ProgressBar.jsx'
import Markdown from './Markdown.jsx'
import { formatPercent } from '../lib/derive.js'
import { STATUSES, statusMeta } from '../lib/status.js'

function CountBreakdown({ counts }) {
  return (
    <div className="flex flex-wrap items-center gap-2.5">
      {STATUSES.map((s) => {
        const meta = statusMeta(s)
        const n = (counts && counts[s]) || 0
        return (
          <span
            key={s}
            title={`${n} ${meta.label.toLowerCase()}`}
            className={`inline-flex items-center gap-1 text-xs ${
              n === 0 ? 'text-slate-400' : 'text-slate-600'
            }`}
          >
            <span className={`inline-block h-2 w-2 rounded-sm border ${meta.swatch}`} />
            {n}
          </span>
        )
      })}
    </div>
  )
}

export default function SkillRow({ skill, onSelectTopic }) {
  const [expanded, setExpanded] = useState(false)
  const view = skill.view
  const hasDescription = !!(skill.description_md && skill.description_md.trim())

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h2 className="truncate text-base font-semibold text-slate-900">
              {skill.name || skill.id}
            </h2>
            {hasDescription ? (
              <button
                type="button"
                onClick={() => setExpanded((v) => !v)}
                aria-expanded={expanded}
                title="Show skill description"
                className="rounded border border-slate-200 px-1.5 py-0.5 text-[11px] text-slate-500 transition-colors hover:bg-slate-50 hover:text-slate-700"
              >
                {expanded ? 'Hide info' : 'Info'}
              </button>
            ) : null}
          </div>
          <p className="mt-0.5 text-xs text-slate-500">
            {view.done}/{view.total} at comfortable or better
            {skill.updated ? ` · updated ${skill.updated}` : ''}
          </p>
        </div>

        <div className="flex min-w-[260px] flex-1 flex-col items-end gap-1.5">
          <div className="flex w-full items-center gap-3">
            <ProgressBar percent={view.percent} className="flex-1" />
            <span className="w-14 shrink-0 text-right text-sm font-semibold text-slate-900">
              {formatPercent(view.percent)}
            </span>
          </div>
          <CountBreakdown counts={view.counts} />
        </div>
      </div>

      {expanded && hasDescription ? (
        <div className="mt-3 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1">
          <Markdown>{skill.description_md}</Markdown>
        </div>
      ) : null}

      {skill.topics.length > 0 ? (
        <div className="mt-4 flex flex-wrap gap-2">
          {skill.topics.map((topic, idx) => (
            <TopicBox
              key={topic.id || `${skill.id}-${idx}`}
              topic={topic}
              onSelect={onSelectTopic}
            />
          ))}
        </div>
      ) : (
        <p className="mt-4 text-sm text-slate-400 italic">No topics.</p>
      )}
    </section>
  )
}
