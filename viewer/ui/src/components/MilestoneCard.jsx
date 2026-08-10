import ProgressBar from './ProgressBar.jsx'
import Markdown from './Markdown.jsx'
import { clampPercent, formatPercent } from '../lib/derive.js'
import { statusMeta } from '../lib/status.js'

// derived_status -> badge chrome + progress bar tint. The backend owns the
// judgement; this map only decides how it looks.
const DERIVED_META = {
  done: { label: 'Done', chip: 'border-ok-line bg-ok-soft text-ok-ink', bar: 'bg-ok-solid' },
  'on-track': { label: 'On track', chip: 'border-ok-line bg-surface-2 text-ok-ink', bar: 'bg-ok-solid' },
  'at-risk': { label: 'At risk', chip: 'border-warn-line bg-warn-soft text-warn-ink', bar: 'bg-warn-solid' },
  overdue: { label: 'Overdue', chip: 'border-danger-line bg-danger-soft text-danger-ink', bar: 'bg-danger-solid' },
  blocked: { label: 'Blocked', chip: 'border-danger-line bg-surface-2 text-danger-ink', bar: 'bg-danger-solid' },
  planned: { label: 'Planned', chip: 'border-line bg-surface-2 text-ink-2', bar: 'bg-accent-solid' },
}

const DERIVED_FALLBACK = {
  label: 'Unknown',
  chip: 'border-line bg-surface-2 text-ink-3',
  bar: 'bg-accent-solid',
}

function derivedMeta(status) {
  return DERIVED_META[status] || DERIVED_FALLBACK
}

// `days_remaining` is negative once the target has passed.
function daysLabel(days) {
  if (typeof days !== 'number' || Number.isNaN(days)) return null
  if (days === 0) return 'today'
  if (days > 0) return `${days} day${days === 1 ? '' : 's'} left`
  const overdue = Math.abs(days)
  return `${overdue} day${overdue === 1 ? '' : 's'} overdue`
}

function TopicChip({ topic, onSelectTopic }) {
  const meta = statusMeta(topic && topic.status)
  const title = topic?.title || topic?.id || 'Untitled topic'

  const tooltip = [
    title,
    topic?.skill_name ? `Skill: ${topic.skill_name}` : null,
    `Status: ${meta.label}`,
    topic?.min_required ? 'Minimum required ★' : null,
    topic?.focus ? 'In focus' : null,
  ]
    .filter(Boolean)
    .join('\n')

  const clickable = typeof onSelectTopic === 'function'

  return (
    <button
      type="button"
      disabled={!clickable}
      onClick={clickable ? () => onSelectTopic(topic) : undefined}
      title={tooltip}
      className={`inline-flex max-w-[190px] items-center gap-1 rounded-md border px-1.5 py-0.5 text-[11px] leading-tight font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-accent ${meta.box} ${
        topic?.focus ? 'ring-1 ring-accent-line' : ''
      } ${clickable ? '' : 'cursor-default'}`}
    >
      {topic?.min_required ? (
        <span aria-label="minimum required" className="shrink-0 text-warn-solid">
          ★
        </span>
      ) : null}
      <span className="truncate">{title}</span>
    </button>
  )
}

export default function MilestoneCard({ milestone, onSelectTopic }) {
  if (!milestone) return null

  const meta = derivedMeta(milestone.derived_status)
  const progress = milestone.progress || {}
  const percent = clampPercent(progress.percent)
  const complete = typeof progress.complete === 'number' ? progress.complete : 0
  const total = typeof progress.total === 'number' ? progress.total : 0

  const topics = Array.isArray(milestone.topics) ? milestone.topics : []
  const missing = Array.isArray(milestone.missing_topic_ids) ? milestone.missing_topic_ids : []
  const days = daysLabel(milestone.days_remaining)

  return (
    <article className="rounded-lg border border-line bg-surface-2 p-3">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0">
          <h4 className="truncate text-sm font-semibold text-ink">
            {milestone.title || milestone.id}
          </h4>
          <p className="mt-0.5 text-xs text-ink-3">
            {milestone.target ? `Target ${milestone.target}` : 'No target date'}
            {days ? ` · ${days}` : ''}
          </p>
        </div>

        <span
          className={`shrink-0 rounded-full border px-2 py-0.5 text-[11px] font-medium ${meta.chip}`}
        >
          {meta.label}
        </span>
      </div>

      <div className="mt-2.5 flex items-center gap-3">
        <ProgressBar percent={percent} className="flex-1" barClass={meta.bar} />
        <span className="shrink-0 text-xs text-ink-2">
          {complete}/{total} topics
        </span>
        <span className="w-12 shrink-0 text-right text-xs font-semibold text-ink">
          {formatPercent(percent)}
        </span>
      </div>

      {milestone.description_md ? (
        <div className="mt-1">
          <Markdown>{milestone.description_md}</Markdown>
        </div>
      ) : null}

      {topics.length > 0 ? (
        <div className="mt-2.5 flex flex-wrap gap-1.5">
          {topics.map((topic, idx) => (
            <TopicChip
              key={topic?.id || `${milestone.id}-topic-${idx}`}
              topic={topic}
              onSelectTopic={onSelectTopic}
            />
          ))}
        </div>
      ) : (
        <p className="mt-2.5 text-xs text-ink-3 italic">No topics attached to this milestone.</p>
      )}

      {missing.length > 0 ? (
        <p className="mt-2.5 rounded-md border border-warn-line bg-warn-soft px-2 py-1 text-[11px] text-warn-ink">
          {missing.length} referenced topic{missing.length === 1 ? '' : 's'} no longer exist
          {missing.length === 1 ? 's' : ''}:{' '}
          <span className="font-mono break-all">{missing.join(', ')}</span>
        </p>
      ) : null}
    </article>
  )
}
