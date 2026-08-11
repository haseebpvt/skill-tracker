import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import Markdown from './Markdown.jsx'
import ProgressBar from './ProgressBar.jsx'
import StatusPill from './StatusPill.jsx'
import Checklist from './Checklist.jsx'
import { clampPercent, formatPercent } from '../lib/derive.js'

// derived_status -> badge chrome + bar tint. Mirrors the map in MilestoneCard so
// a milestone looks the same on the board and in the panel.
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

function checklistOf(topic) {
  const c = (topic && topic.checklist) || {}
  const total = typeof c.total === 'number' ? c.total : 0
  const done = typeof c.done === 'number' ? c.done : 0
  return { total, done, complete: total > 0 && done >= total }
}

function Stat({ label, hint, percent, barClass, countLine }) {
  return (
    <div className="rounded-lg border border-line bg-surface-2 p-3">
      <p className="text-[11px] font-medium tracking-wide text-ink-3 uppercase">{label}</p>
      <p className="mt-0.5 text-xs text-ink-3">{hint}</p>
      <div className="mt-2 flex items-baseline justify-between gap-2">
        <span className="text-sm text-ink-2 tabular-nums">{countLine}</span>
        <span className="text-sm font-semibold text-ink tabular-nums">
          {formatPercent(percent)}
        </span>
      </div>
      <ProgressBar percent={percent} height="h-1.5" className="mt-1.5" barClass={barClass} />
    </div>
  )
}

function TopicSection({ topic, expanded, onToggleExpanded, onOpenTopic, busyIds, errors, onToggleItem }) {
  const { total, done } = checklistOf(topic)
  const title = topic.title || topic.id
  const bodyId = `milestone-topic-body-${topic.id}`

  return (
    <div className="overflow-hidden rounded-lg border border-line bg-surface-2">
      <div className="flex items-start gap-2 px-3 py-2.5">
        <button
          type="button"
          onClick={onToggleExpanded}
          aria-expanded={expanded}
          aria-controls={bodyId}
          className="flex min-w-0 flex-1 items-start gap-2 text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          <span
            aria-hidden="true"
            className={`mt-1 shrink-0 text-[10px] text-ink-3 transition-transform ${
              expanded ? 'rotate-90' : ''
            }`}
          >
            ▶
          </span>

          <span className="min-w-0 flex-1">
            <span className="flex flex-wrap items-center gap-1.5">
              {topic.min_required ? (
                <span aria-label="minimum required" title="Minimum required" className="text-warn-solid">
                  ★
                </span>
              ) : null}
              {topic.focus ? (
                <span
                  aria-label="in focus"
                  title="In focus"
                  className="h-1.5 w-1.5 shrink-0 rounded-full bg-accent-solid"
                />
              ) : null}
              <span className="text-sm font-medium break-words text-ink">{title}</span>
            </span>
            <span className="mt-1 flex flex-wrap items-center gap-2">
              <StatusPill status={topic.status} />
              <span className="text-[11px] text-ink-3 tabular-nums">
                {total > 0 ? `${done}/${total} items` : 'no items'}
              </span>
            </span>
          </span>
        </button>

        <button
          type="button"
          onClick={() => {
            if (typeof onOpenTopic === 'function') onOpenTopic(topic)
          }}
          title="Open topic detail"
          className="shrink-0 rounded-md border border-line px-1.5 py-0.5 text-[11px] text-ink-3 transition-colors hover:bg-surface-3 hover:text-ink focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
        >
          Open ↗
        </button>
      </div>

      {expanded ? (
        <div id={bodyId} className="border-t border-line px-3 py-2.5">
          <Checklist
            topic={topic}
            onToggle={onToggleItem}
            busyIds={busyIds}
            errors={errors}
          />
        </div>
      ) : null}
    </div>
  )
}

export default function MilestonePanel({ milestone, topics, onToggle, onOpenTopic, onClose }) {
  const closeRef = useRef(null)
  const [busyIds, setBusyIds] = useState(() => new Set())
  const [errors, setErrors] = useState(() => new Map())
  const [collapsed, setCollapsed] = useState(() => new Set())

  const list = useMemo(
    () => (Array.isArray(topics) ? topics.filter((t) => t && t.id) : []),
    [topics]
  )

  const milestoneId = milestone ? milestone.id : null

  // Esc to close, and move focus into the panel when it opens.
  useEffect(() => {
    if (!milestone) return undefined
    const onKey = (e) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)
    if (closeRef.current) closeRef.current.focus()
    return () => document.removeEventListener('keydown', onKey)
  }, [milestone, onClose])

  // Lock background scroll while open.
  useEffect(() => {
    if (!milestone) return undefined
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = prev
    }
  }, [milestone])

  // Open on what is left to do: finished topics start collapsed. Recomputed
  // only when the milestone changes, so a toggle mid-session does not fold the
  // section the user is working in.
  useEffect(() => {
    if (!milestoneId) return
    const done = list.filter((t) => checklistOf(t).complete).map((t) => t.id)
    // If everything is complete there is nothing "left"; show it all.
    setCollapsed(done.length === list.length ? new Set() : new Set(done))
    setErrors(new Map())
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [milestoneId])

  const toggleExpanded = useCallback((topicId) => {
    setCollapsed((prev) => {
      const next = new Set(prev)
      if (next.has(topicId)) next.delete(topicId)
      else next.add(topicId)
      return next
    })
  }, [])

  // The parent owns the data, so we never mutate the item here — we only track
  // which write is in flight and surface a failure next to the item.
  const handleToggle = useCallback(
    async (skillId, topicId, itemId, nextChecked) => {
      if (typeof onToggle !== 'function') return
      setBusyIds((prev) => new Set(prev).add(itemId))
      setErrors((prev) => {
        if (!prev.has(itemId)) return prev
        const next = new Map(prev)
        next.delete(itemId)
        return next
      })
      try {
        await onToggle(skillId, topicId, itemId, nextChecked)
      } catch (err) {
        const message = (err && err.message) || 'Could not save that change.'
        setErrors((prev) => new Map(prev).set(itemId, message))
      } finally {
        setBusyIds((prev) => {
          const next = new Set(prev)
          next.delete(itemId)
          return next
        })
      }
    },
    [onToggle]
  )

  if (!milestone) return null

  const meta = derivedMeta(milestone.derived_status)
  const days = daysLabel(milestone.days_remaining)

  const progress = milestone.progress || {}
  const topicPercent = clampPercent(progress.percent)
  const topicComplete = typeof progress.complete === 'number' ? progress.complete : 0
  const topicTotal = typeof progress.total === 'number' ? progress.total : list.length

  const coverage = milestone.coverage || {}
  const coveragePercent = clampPercent(coverage.percent)
  const coverageDone = typeof coverage.done === 'number' ? coverage.done : 0
  const coverageTotal = typeof coverage.total === 'number' ? coverage.total : 0
  const needingBreakdown =
    typeof coverage.topics_needing_breakdown === 'number' ? coverage.topics_needing_breakdown : 0

  return (
    <div className="fixed inset-0 z-40">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} aria-hidden="true" />

      <aside
        role="dialog"
        aria-modal="true"
        aria-label={milestone.title || 'Milestone detail'}
        className="absolute top-0 right-0 flex h-full w-full max-w-[720px] flex-col border-l border-line bg-surface shadow-xl"
      >
        <div className="flex items-start justify-between gap-4 border-b border-line px-5 py-4">
          <div className="min-w-0">
            <h2 className="text-lg font-semibold break-words text-ink">
              {milestone.title || milestone.id}
            </h2>
            <div className="mt-1.5 flex flex-wrap items-center gap-2">
              <span
                className={`rounded-full border px-2 py-0.5 text-[11px] font-medium ${meta.chip}`}
              >
                {meta.label}
              </span>
              <span className="text-xs text-ink-3">
                {milestone.target ? `Target ${milestone.target}` : 'No target date'}
                {days ? ` · ${days}` : ''}
              </span>
            </div>
          </div>

          <button
            ref={closeRef}
            type="button"
            onClick={onClose}
            aria-label="Close panel"
            className="shrink-0 rounded-md border border-line px-2 py-1 text-ink-3 transition-colors hover:bg-surface-2 hover:text-ink focus:outline-none focus-visible:ring-2 focus-visible:ring-accent"
          >
            ✕
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-4">
          {/* Two different measures: topic status vs. checklist items done. */}
          <div className="grid gap-3 sm:grid-cols-2">
            <Stat
              label="Topics"
              hint="Status-weighted across topics"
              percent={topicPercent}
              barClass={meta.bar}
              countLine={`${topicComplete}/${topicTotal} complete`}
            />
            <Stat
              label="Checklist coverage"
              hint="Individual items checked off"
              percent={coveragePercent}
              barClass={coveragePercent >= 100 ? 'bg-ok-solid' : 'bg-accent-solid'}
              countLine={`${coverageDone}/${coverageTotal} items`}
            />
          </div>

          {needingBreakdown > 0 ? (
            <p className="mt-3 rounded-md border border-warn-line bg-warn-soft px-2.5 py-2 text-xs text-warn-ink">
              {needingBreakdown} topic{needingBreakdown === 1 ? '' : 's'} have no breakdown yet.
            </p>
          ) : null}

          {milestone.description_md ? (
            <div className="mt-1">
              <Markdown>{milestone.description_md}</Markdown>
            </div>
          ) : null}

          <hr className="my-4 border-line" />

          {list.length > 0 ? (
            <div className="space-y-2">
              {list.map((topic) => (
                <TopicSection
                  key={topic.id}
                  topic={topic}
                  expanded={!collapsed.has(topic.id)}
                  onToggleExpanded={() => toggleExpanded(topic.id)}
                  onOpenTopic={onOpenTopic}
                  busyIds={busyIds}
                  errors={errors}
                  onToggleItem={(itemId, nextChecked) =>
                    handleToggle(topic.skill_id, topic.id, itemId, nextChecked)
                  }
                />
              ))}
            </div>
          ) : (
            <p className="text-sm text-ink-3 italic">No topics attached to this milestone.</p>
          )}
        </div>
      </aside>
    </div>
  )
}
