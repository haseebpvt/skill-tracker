import ProgressBar from './ProgressBar.jsx'
import { clampPercent } from '../lib/derive.js'

// The one interactive surface in the app. Everything else renders state; this
// writes it. Items are rendered strictly in array order — that order is the
// intended learning sequence and must never be re-sorted.

function sectionsOf(checklist) {
  const sections = Array.isArray(checklist && checklist.sections) ? checklist.sections : []
  // Drop malformed sections rather than throwing on a bad payload.
  return sections
    .filter(Boolean)
    .map((s) => ({
      heading: typeof s.heading === 'string' ? s.heading : '',
      items: Array.isArray(s.items) ? s.items.filter((i) => i && i.id) : [],
    }))
    .filter((s) => s.items.length > 0)
}

// A single section label is noise when it just says "Checklist" above a
// checklist inside a panel that already names the topic.
function showHeading(sections, index) {
  const s = sections[index]
  if (!s || !s.heading) return false
  if (sections.length === 1 && s.heading === 'Checklist') return false
  return true
}

function Callout({ tone = 'warn', children, className = '' }) {
  const chrome =
    tone === 'danger'
      ? 'border-danger-line bg-danger-soft text-danger-ink'
      : 'border-warn-line bg-warn-soft text-warn-ink'
  return (
    <div className={`rounded-md border px-2.5 py-2 text-xs leading-relaxed ${chrome} ${className}`}>
      {children}
    </div>
  )
}

function ChecklistItem({ item, index, busy, error, onActivate }) {
  const checked = !!item.checked

  const handleKeyDown = (e) => {
    // Space and Enter both toggle: role="checkbox" wants Space, but the row
    // reads as a button to most people, so honour Enter too.
    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault()
      if (!busy) onActivate()
    }
  }

  return (
    <li>
      <div
        role="checkbox"
        aria-checked={checked}
        aria-disabled={busy || undefined}
        tabIndex={busy ? -1 : 0}
        onClick={busy ? undefined : onActivate}
        onKeyDown={handleKeyDown}
        className={`group flex w-full items-start gap-2.5 rounded-md px-2 py-1.5 text-left transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-accent ${
          busy ? 'cursor-progress opacity-60' : 'cursor-pointer hover:bg-surface-3'
        }`}
      >
        <span className="mt-[3px] w-4 shrink-0 text-right font-mono text-[11px] leading-none text-ink-3 tabular-nums">
          {index + 1}.
        </span>

        <span
          aria-hidden="true"
          className={`mt-px flex h-4 w-4 shrink-0 items-center justify-center rounded border text-[10px] leading-none transition-colors ${
            checked
              ? 'border-ok-line bg-ok-solid text-canvas'
              : 'border-line-strong bg-surface-2 text-transparent group-hover:border-accent-line'
          }`}
        >
          {busy ? (
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-ink-3" />
          ) : checked ? (
            '✓'
          ) : null}
        </span>

        <span
          className={`min-w-0 flex-1 text-sm leading-relaxed ${
            checked ? 'text-ink-3 line-through' : 'text-ink-2'
          }`}
        >
          {item.text || item.id}
        </span>
      </div>

      {error ? (
        <p className="mt-0.5 ml-[42px] text-[11px] text-danger-ink">{error}</p>
      ) : null}
    </li>
  )
}

export default function Checklist({ topic, onToggle, busyIds, errors }) {
  if (!topic) return null

  const checklist = topic.checklist || {}
  const sections = sectionsOf(checklist)

  const total = typeof checklist.total === 'number' ? checklist.total : 0
  const done = typeof checklist.done === 'number' ? checklist.done : 0
  const percent = clampPercent(
    typeof checklist.percent === 'number'
      ? checklist.percent
      : total > 0
        ? (done / total) * 100
        : 0
  )

  const needsBreakdown = !!topic.needs_breakdown || total === 0 || sections.length === 0
  const needsEvidence = !!topic.needs_evidence

  const isBusy = (id) => !!(busyIds && typeof busyIds.has === 'function' && busyIds.has(id))
  const errorFor = (id) => (errors && typeof errors.get === 'function' ? errors.get(id) : null)

  const activate = (item) => {
    if (typeof onToggle !== 'function') return
    onToggle(item.id, !item.checked)
  }

  return (
    <div>
      {needsBreakdown ? (
        <Callout>
          No breakdown yet. Ask your agent to break this topic into concrete items.
        </Callout>
      ) : (
        <>
          <div className="flex items-center gap-3">
            <ProgressBar
              percent={percent}
              height="h-1.5"
              className="flex-1"
              barClass={percent >= 100 ? 'bg-ok-solid' : 'bg-accent-solid'}
            />
            <span className="shrink-0 text-[11px] text-ink-3 tabular-nums">
              {done}/{total} · {Math.round(percent)}%
            </span>
          </div>

          <div className="mt-2 space-y-3">
            {sections.map((section, si) => (
              <div key={`${section.heading || 'section'}-${si}`}>
                {showHeading(sections, si) ? (
                  <h4 className="mb-1 px-2 text-[11px] font-medium tracking-wide text-ink-3 uppercase">
                    {section.heading}
                  </h4>
                ) : null}
                <ul className="space-y-0.5">
                  {section.items.map((item, ii) => (
                    <ChecklistItem
                      key={item.id}
                      item={item}
                      index={ii}
                      busy={isBusy(item.id)}
                      error={errorFor(item.id)}
                      onActivate={() => activate(item)}
                    />
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </>
      )}

      {needsEvidence ? (
        <Callout className="mt-2">
          Evidence needed — no source material backs this topic yet.
        </Callout>
      ) : null}
    </div>
  )
}
