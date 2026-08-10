import { useState } from 'react'
import MilestoneCard from './MilestoneCard.jsx'
import VelocityChart from './VelocityChart.jsx'
import ActivityFeed from './ActivityFeed.jsx'
import Markdown from './Markdown.jsx'
import { clampPercent, formatPercent } from '../lib/derive.js'

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

// "2026-09-14" -> "14 Sep". Parsed by hand to avoid timezone drift on bare
// date strings; returns the input untouched if it is not the expected shape.
function shortDate(value) {
  if (typeof value !== 'string') return '—'
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(value.trim())
  if (!m) return value
  const month = MONTHS[Number(m[2]) - 1]
  if (!month) return value
  return `${Number(m[3])} ${month}`
}

const VERDICT_CHIP = {
  behind: 'border-danger-line bg-danger-soft text-danger-ink',
  ahead: 'border-ok-line bg-ok-soft text-ok-ink',
  'on-track': 'border-ok-line bg-ok-soft text-ok-ink',
  unknown: 'border-line bg-surface-2 text-ink-2',
}

// The headline chip. When there is no forecast we say so in the backend's own
// words (`reason`) instead of inventing a date.
function headline(velocity) {
  const forecast = velocity && velocity.forecast

  if (!velocity || !velocity.has_data || !forecast || !forecast.available) {
    const reason = forecast && forecast.reason ? forecast.reason : null
    return {
      text: 'Not enough history to forecast yet',
      detail: reason,
      chip: VERDICT_CHIP.unknown,
    }
  }

  const verdict = forecast.verdict || 'unknown'
  const projected = forecast.projected_date ? shortDate(forecast.projected_date) : null
  const delta = typeof forecast.days_vs_target === 'number' ? forecast.days_vs_target : null

  let tail = ''
  if (delta !== null && forecast.target_date) {
    const n = Math.abs(delta)
    const unit = `${n} day${n === 1 ? '' : 's'}`
    if (delta > 0) tail = ` — ${unit} behind target`
    else if (delta < 0) tail = ` — ${unit} ahead of target`
    else tail = ' — on target'
  }

  return {
    text: projected ? `Projected ${projected}${tail}` : `Forecast: ${verdict}`,
    detail:
      forecast.confidence
        ? `${forecast.confidence} confidence${forecast.reason ? ` — ${forecast.reason}` : ''}`
        : forecast.reason || null,
    chip: VERDICT_CHIP[verdict] || VERDICT_CHIP.unknown,
  }
}

function Stat({ label, value, hint }) {
  return (
    <div className="min-w-0">
      <dt className="text-[11px] tracking-wide text-ink-3 uppercase">{label}</dt>
      <dd className="mt-0.5 truncate text-sm font-semibold text-ink" title={hint || undefined}>
        {value}
      </dd>
    </div>
  )
}

// "1 done · 1 on track · 1 at risk · 1 overdue" — zero-valued buckets are
// dropped so the line stays readable.
function summaryLine(summary) {
  if (!summary) return null
  const parts = [
    ['done', summary.done],
    ['on track', summary.on_track],
    ['at risk', summary.at_risk],
    ['overdue', summary.overdue],
    ['blocked', summary.blocked],
  ]
    .filter(([, n]) => typeof n === 'number' && n > 0)
    .map(([label, n]) => `${n} ${label}`)

  return parts.length > 0 ? parts.join(' · ') : null
}

// Sort by target date ascending; milestones without a target sink to the end
// but keep their relative order.
function byTargetDate(milestones) {
  return milestones
    .map((m, i) => ({ m, i }))
    .sort((a, b) => {
      const ta = typeof a.m?.target === 'string' ? a.m.target : null
      const tb = typeof b.m?.target === 'string' ? b.m.target : null
      if (ta && tb && ta !== tb) return ta < tb ? -1 : 1
      if (ta && !tb) return -1
      if (!ta && tb) return 1
      return a.i - b.i
    })
    .map((x) => x.m)
}

export default function Roadmap({ roadmap, velocity, history, onSelectTopic }) {
  const [showActivity, setShowActivity] = useState(false)

  const exists = !!(roadmap && roadmap.exists)

  if (!exists) {
    return (
      <section className="rounded-xl border border-line bg-surface shadow-sm">
        <div className="px-4 py-3">
          <h3 className="text-base font-semibold text-ink">Roadmap</h3>
        </div>
        <div className="border-t border-line px-4 py-4">
          <p className="text-sm text-ink-3 italic">
            No roadmap has been created yet. Once milestones are set — with target dates and the
            topics each one covers — this section shows progress, a burn-up chart and a projected
            finish date. The connected agent can create one for you.
          </p>
        </div>
      </section>
    )
  }

  const milestones = Array.isArray(roadmap.milestones) ? roadmap.milestones.filter(Boolean) : []
  const ordered = byTargetDate(milestones)
  const head = headline(velocity)
  const counts = summaryLine(roadmap.summary)

  const percent = typeof velocity?.percent === 'number' ? clampPercent(velocity.percent) : null
  const perWeek = typeof velocity?.topics_per_week === 'number' ? velocity.topics_per_week : null
  const projected =
    velocity?.forecast?.available && velocity.forecast.projected_date
      ? shortDate(velocity.forecast.projected_date)
      : null

  const hasActivity = Array.isArray(history?.recent) && history.recent.length > 0

  return (
    <section className="rounded-xl border border-line bg-surface shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3 px-4 py-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="text-base font-semibold text-ink">Roadmap</h3>
            {roadmap.target_date ? (
              <span className="text-xs text-ink-3">target {roadmap.target_date}</span>
            ) : null}
            {roadmap.updated ? (
              <span className="text-xs text-ink-3">· updated {roadmap.updated}</span>
            ) : null}
          </div>
          {head.detail ? <p className="mt-1 text-xs text-ink-3">{head.detail}</p> : null}
        </div>

        <span
          className={`shrink-0 rounded-md border px-2 py-1 text-xs font-medium ${head.chip}`}
          title={head.detail || undefined}
        >
          {head.text}
        </span>
      </div>

      <div className="border-t border-line px-4 py-3">
        <dl className="grid grid-cols-2 gap-x-4 gap-y-3 sm:grid-cols-4">
          <Stat label="Overall" value={percent === null ? '—' : formatPercent(percent)} />
          <Stat
            label="Topics / week"
            value={perWeek === null ? '—' : perWeek.toFixed(1)}
            hint={
              typeof velocity?.events_in_window === 'number'
                ? `${velocity.events_in_window} events in the last ${velocity.window_days ?? '—'} days`
                : undefined
            }
          />
          <Stat label="Projected" value={projected || 'No forecast'} />
          <Stat label="Milestones" value={counts || `${milestones.length} total`} hint={counts || undefined} />
        </dl>

        {roadmap.notes_md ? (
          <div className="mt-1">
            <Markdown>{roadmap.notes_md}</Markdown>
          </div>
        ) : null}

        <div className="mt-3">
          <VelocityChart velocity={velocity} />
        </div>

        {ordered.length > 0 ? (
          <div className="mt-4 space-y-2.5">
            {ordered.map((milestone, idx) => (
              <MilestoneCard
                key={milestone.id || `milestone-${idx}`}
                milestone={milestone}
                onSelectTopic={onSelectTopic}
              />
            ))}
          </div>
        ) : (
          <p className="mt-4 text-sm text-ink-3 italic">No milestones defined yet.</p>
        )}
      </div>

      <div className="border-t border-line">
        <button
          type="button"
          onClick={() => setShowActivity((v) => !v)}
          aria-expanded={showActivity}
          className="flex w-full items-center gap-2 px-4 py-2.5 text-left"
        >
          <span className={`text-ink-3 transition-transform ${showActivity ? 'rotate-90' : ''}`}>
            ›
          </span>
          <span className="text-sm font-medium text-ink">Recent activity</span>
          {hasActivity && typeof history?.total_events === 'number' ? (
            <span className="text-xs text-ink-3">{history.total_events} events</span>
          ) : null}
        </button>

        {showActivity ? (
          <div className="px-4 pt-1 pb-3">
            <ActivityFeed history={history} />
          </div>
        ) : null}
      </div>
    </section>
  )
}
