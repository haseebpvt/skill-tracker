import { useEffect, useRef } from 'react'
import Markdown from './Markdown.jsx'
import StatusPill from './StatusPill.jsx'
import Checklist from './Checklist.jsx'
import { useState } from 'react'

function Meta({ label, children }) {
  return (
    <div>
      <dt className="text-[11px] font-medium tracking-wide text-ink-3 uppercase">{label}</dt>
      <dd className="mt-0.5 text-sm text-ink">{children}</dd>
    </div>
  )
}

export default function TopicDrawer({ topic, onClose, onToggleItem }) {
  const closeRef = useRef(null)
  const [busyIds, setBusyIds] = useState(() => new Set())

  // Esc to close, and move focus into the panel when it opens.
  useEffect(() => {
    if (!topic) return undefined
    const onKey = (e) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)
    if (closeRef.current) closeRef.current.focus()
    return () => document.removeEventListener('keydown', onKey)
  }, [topic, onClose])

  // Lock background scroll while open.
  useEffect(() => {
    if (!topic) return undefined
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = prev
    }
  }, [topic])

  if (!topic) return null

  const evidence = Array.isArray(topic.evidence) ? topic.evidence.filter(Boolean) : []
  const hasBody = !!(topic.body_md && topic.body_md.trim())

  const toggleItem = async (itemId, checked) => {
    if (typeof onToggleItem !== 'function') return
    setBusyIds((prev) => new Set(prev).add(itemId))
    try {
      await onToggleItem(topic.skill_id, topic.id, itemId, checked)
    } finally {
      setBusyIds((prev) => {
        const next = new Set(prev)
        next.delete(itemId)
        return next
      })
    }
  }

  return (
    <div className="fixed inset-0 z-40">
      <div
        className="absolute inset-0 bg-black/60"
        onClick={onClose}
        aria-hidden="true"
      />

      <aside
        role="dialog"
        aria-modal="true"
        aria-label={topic.title || 'Topic detail'}
        className="absolute top-0 right-0 flex h-full w-full max-w-[560px] flex-col border-l border-line bg-surface shadow-xl"
      >
        <div className="flex items-start justify-between gap-4 border-b border-line px-5 py-4">
          <div className="min-w-0">
            {topic.skill_name ? (
              <p className="text-xs font-medium text-ink-3">{topic.skill_name}</p>
            ) : null}
            <h2 className="mt-0.5 text-lg font-semibold break-words text-ink">
              {topic.title || topic.id}
            </h2>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <StatusPill status={topic.status} />
              {topic.min_required ? (
                <span className="inline-flex items-center gap-1 rounded-full border border-warn-line bg-warn-soft px-2 py-0.5 text-xs font-medium text-warn-ink">
                  ★ Min required
                </span>
              ) : null}
              {topic.focus ? (
                <span className="inline-flex items-center gap-1 rounded-full border border-accent-line bg-accent-soft px-2 py-0.5 text-xs font-medium text-accent-ink">
                  In focus
                </span>
              ) : null}
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
          <dl className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            <Meta label="Priority">
              {typeof topic.priority === 'number' ? topic.priority : '—'}
            </Meta>
            <Meta label="Updated">{topic.updated || '—'}</Meta>
            <Meta label="Topic id">
              <code className="font-mono text-xs break-all text-ink-2">
                {topic.id || '—'}
              </code>
            </Meta>
          </dl>

          <div className="mt-5">
            <h3 className="text-[11px] font-medium tracking-wide text-ink-3 uppercase">
              Evidence
            </h3>
            {evidence.length > 0 ? (
              <ul className="mt-1.5 space-y-1">
                {evidence.map((path, idx) => (
                  <li key={`${path}-${idx}`}>
                    <code className="font-mono text-xs break-all text-ink-2">{path}</code>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-1 text-sm text-ink-3 italic">No evidence linked.</p>
            )}
          </div>

          <div className="mt-5">
            <h3 className="text-[11px] font-medium tracking-wide text-ink-3 uppercase">
              Checklist
            </h3>
            <div className="mt-1.5">
              <Checklist topic={topic} onToggle={toggleItem} busyIds={busyIds} />
            </div>
          </div>

          <hr className="my-5 border-line" />

          {hasBody ? (
            <Markdown>{topic.body_md}</Markdown>
          ) : (
            <>
              {/* Fall back to the individual sections when body_md is absent. */}
              {topic.enough_md ? (
                <div className="mb-4">
                  <h3 className="text-sm font-semibold text-ink">
                    What enough looks like
                  </h3>
                  <Markdown>{topic.enough_md}</Markdown>
                </div>
              ) : null}
              {topic.log_md ? (
                <div>
                  <h3 className="text-sm font-semibold text-ink">Notes / log</h3>
                  <Markdown>{topic.log_md}</Markdown>
                </div>
              ) : null}
              {!topic.enough_md && !topic.log_md ? (
                <p className="text-sm text-ink-3 italic">No details recorded yet.</p>
              ) : null}
            </>
          )}
        </div>
      </aside>
    </div>
  )
}
