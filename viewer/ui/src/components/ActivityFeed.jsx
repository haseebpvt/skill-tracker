import { statusMeta } from '../lib/status.js'

// Small date helpers rather than a date library — the formatting needs here are
// shallow and adding a dependency for them is not worth it.

const MS_PER_MIN = 60000
const MS_PER_HOUR = 3600000
const MS_PER_DAY = 86400000

function parseTs(ts) {
  if (typeof ts !== 'string') return null
  const t = Date.parse(ts)
  return Number.isNaN(t) ? null : t
}

function startOfDay(t) {
  const d = new Date(t)
  d.setHours(0, 0, 0, 0)
  return d.getTime()
}

// Whole calendar days between two instants, not elapsed 24h periods. Counting
// elapsed periods would let two events in the same day group read "3d ago" and
// "4d ago" depending on the hour they happened.
function calendarDaysAgo(t, now) {
  return Math.round((startOfDay(now) - startOfDay(t)) / MS_PER_DAY)
}

// "2h ago" / "yesterday" / "3d ago". Falls back to an absolute date past a
// fortnight, where relative phrasing stops being informative.
function relativeTime(t, now) {
  if (t === null) return ''
  const diff = now - t
  if (diff < MS_PER_MIN) return 'just now'

  const days = calendarDaysAgo(t, now)
  if (days <= 0) {
    if (diff < MS_PER_HOUR) return `${Math.floor(diff / MS_PER_MIN)}m ago`
    return `${Math.floor(diff / MS_PER_HOUR)}h ago`
  }
  if (days === 1) return 'yesterday'
  if (days < 14) return `${days}d ago`
  return dayKey(t)
}

function dayKey(t) {
  const d = new Date(t)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd}`
}

// Heading per day group: "Today" / "Yesterday" / "Mon 10 Aug".
const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

function dayHeading(t, now) {
  if (dayKey(t) === dayKey(now)) return 'Today'
  if (dayKey(t) === dayKey(now - MS_PER_DAY)) return 'Yesterday'
  const d = new Date(t)
  return `${WEEKDAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`
}

const TYPE_META = {
  status_change: { icon: '◆', label: 'Status' },
  topic_added: { icon: '+', label: 'Topic added' },
  skill_added: { icon: '+', label: 'Skill added' },
  focus_set: { icon: '◎', label: 'Focus' },
  milestone_set: { icon: '▣', label: 'Milestone' },
  milestone_removed: { icon: '▢', label: 'Milestone removed' },
  conclusions_updated: { icon: '✎', label: 'Conclusions' },
  note: { icon: '“', label: 'Note' },
}

function typeMeta(type) {
  return TYPE_META[type] || { icon: '•', label: type || 'Event' }
}

function StatusWord({ status }) {
  const meta = statusMeta(status)
  return <span className={`rounded px-1 py-px ${meta.pill} border`}>{meta.label}</span>
}

// Every field other than ts/type is optional, so each branch degrades to
// whatever is actually present rather than printing "undefined".
function EventSentence({ event }) {
  const subject = event.topic_title || event.topic_id || event.skill_name || event.skill_id

  if (event.type === 'status_change' && (event.from || event.to)) {
    return (
      <span className="text-ink-2">
        {subject ? <span className="font-medium text-ink">{subject}</span> : 'A topic'}:{' '}
        {event.from ? <StatusWord status={event.from} /> : '—'}
        <span className="mx-1 text-ink-3">→</span>
        {event.to ? <StatusWord status={event.to} /> : '—'}
      </span>
    )
  }

  if (event.type === 'topic_added') {
    return (
      <span className="text-ink-2">
        Added <span className="font-medium text-ink">{subject || 'a topic'}</span>
        {event.skill_name ? ` to ${event.skill_name}` : ''}
      </span>
    )
  }

  if (event.type === 'skill_added') {
    return (
      <span className="text-ink-2">
        Added skill{' '}
        <span className="font-medium text-ink">{event.skill_name || event.skill_id || '—'}</span>
      </span>
    )
  }

  if (event.type === 'focus_set') {
    return (
      <span className="text-ink-2">
        Focus set to <span className="font-medium text-ink">{subject || '—'}</span>
      </span>
    )
  }

  if (event.type === 'milestone_set') {
    return (
      <span className="text-ink-2">
        Milestone updated{subject ? ': ' : ''}
        {subject ? <span className="font-medium text-ink">{subject}</span> : null}
      </span>
    )
  }

  if (event.type === 'milestone_removed') {
    return (
      <span className="text-ink-2">
        Milestone removed{subject ? ': ' : ''}
        {subject ? <span className="font-medium text-ink">{subject}</span> : null}
      </span>
    )
  }

  if (event.type === 'conclusions_updated') {
    return <span className="text-ink-2">Conclusions updated</span>
  }

  // `note` and any unrecognised future type: the note body carries the meaning,
  // and it is already rendered underneath, so avoid repeating it here.
  return (
    <span className="text-ink-2">
      {subject ? <span className="font-medium text-ink">{subject}</span> : typeMeta(event.type).label}
    </span>
  )
}

export default function ActivityFeed({ history, limit = 12 }) {
  const recent = Array.isArray(history && history.recent) ? history.recent.filter(Boolean) : []

  if (recent.length === 0) {
    return <p className="text-sm text-ink-3 italic">No activity recorded yet.</p>
  }

  const now = Date.now()

  // Reverse-chronological. Events without a parsable ts sink to the bottom
  // rather than being dropped, so nothing silently disappears.
  const sorted = recent
    .map((event, idx) => ({ event, idx, t: parseTs(event.ts) }))
    .sort((a, b) => {
      if (a.t === null && b.t === null) return a.idx - b.idx
      if (a.t === null) return 1
      if (b.t === null) return -1
      if (b.t !== a.t) return b.t - a.t
      return a.idx - b.idx
    })
    .slice(0, limit)

  // Group consecutive runs by day, preserving the sorted order.
  const groups = []
  for (const item of sorted) {
    const heading = item.t === null ? 'Undated' : dayHeading(item.t, now)
    const tail = groups[groups.length - 1]
    if (tail && tail.heading === heading) tail.items.push(item)
    else groups.push({ heading, items: [item] })
  }

  const total = typeof history?.total_events === 'number' ? history.total_events : null

  return (
    <div>
      {groups.map((group) => (
        <div key={group.heading} className="mb-3 last:mb-0">
          <h5 className="mb-1.5 text-[11px] font-semibold tracking-wide text-ink-3 uppercase">
            {group.heading}
          </h5>

          <ul className="space-y-1.5">
            {group.items.map(({ event, idx, t }) => {
              const meta = typeMeta(event.type)
              return (
                <li
                  key={`${event.ts || 'no-ts'}-${idx}`}
                  className="flex items-start gap-2 rounded-md border border-line bg-surface-2 px-2.5 py-1.5"
                >
                  <span
                    aria-hidden="true"
                    title={meta.label}
                    className="mt-px w-4 shrink-0 text-center text-xs text-ink-3"
                  >
                    {meta.icon}
                  </span>

                  <div className="min-w-0 flex-1">
                    <div className="text-xs leading-relaxed">
                      <EventSentence event={event} />
                    </div>
                    {event.note ? (
                      <p className="mt-0.5 text-[11px] leading-relaxed text-ink-3">{event.note}</p>
                    ) : null}
                  </div>

                  <span
                    title={event.ts || ''}
                    className="mt-px shrink-0 text-[11px] whitespace-nowrap text-ink-3"
                  >
                    {relativeTime(t, now)}
                  </span>
                </li>
              )
            })}
          </ul>
        </div>
      ))}

      {total !== null && total > sorted.length ? (
        <p className="mt-2 text-[11px] text-ink-3">
          Showing {sorted.length} of {total} recorded events.
        </p>
      ) : null}
    </div>
  )
}
