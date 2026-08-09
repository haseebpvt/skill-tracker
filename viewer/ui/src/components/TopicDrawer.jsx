import { useEffect, useRef } from 'react'
import Markdown from './Markdown.jsx'
import StatusPill from './StatusPill.jsx'

function Meta({ label, children }) {
  return (
    <div>
      <dt className="text-[11px] font-medium tracking-wide text-slate-500 uppercase">{label}</dt>
      <dd className="mt-0.5 text-sm text-slate-800">{children}</dd>
    </div>
  )
}

export default function TopicDrawer({ topic, onClose }) {
  const closeRef = useRef(null)

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

  return (
    <div className="fixed inset-0 z-40">
      <div
        className="absolute inset-0 bg-slate-900/25"
        onClick={onClose}
        aria-hidden="true"
      />

      <aside
        role="dialog"
        aria-modal="true"
        aria-label={topic.title || 'Topic detail'}
        className="absolute top-0 right-0 flex h-full w-full max-w-[560px] flex-col border-l border-slate-200 bg-white shadow-xl"
      >
        <div className="flex items-start justify-between gap-4 border-b border-slate-200 px-5 py-4">
          <div className="min-w-0">
            {topic.skill_name ? (
              <p className="text-xs font-medium text-slate-500">{topic.skill_name}</p>
            ) : null}
            <h2 className="mt-0.5 text-lg font-semibold break-words text-slate-900">
              {topic.title || topic.id}
            </h2>
            <div className="mt-2 flex flex-wrap items-center gap-2">
              <StatusPill status={topic.status} />
              {topic.min_required ? (
                <span className="inline-flex items-center gap-1 rounded-full border border-amber-300 bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-900">
                  ★ Min required
                </span>
              ) : null}
              {topic.focus ? (
                <span className="inline-flex items-center gap-1 rounded-full border border-blue-300 bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-900">
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
            className="shrink-0 rounded-md border border-slate-200 px-2 py-1 text-slate-500 transition-colors hover:bg-slate-50 hover:text-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
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
              <code className="font-mono text-xs break-all text-slate-600">
                {topic.id || '—'}
              </code>
            </Meta>
          </dl>

          <div className="mt-5">
            <h3 className="text-[11px] font-medium tracking-wide text-slate-500 uppercase">
              Evidence
            </h3>
            {evidence.length > 0 ? (
              <ul className="mt-1.5 space-y-1">
                {evidence.map((path, idx) => (
                  <li key={`${path}-${idx}`}>
                    <code className="font-mono text-xs break-all text-slate-700">{path}</code>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-1 text-sm text-slate-400 italic">No evidence linked.</p>
            )}
          </div>

          <hr className="my-5 border-slate-200" />

          {hasBody ? (
            <Markdown>{topic.body_md}</Markdown>
          ) : (
            <>
              {/* Fall back to the individual sections when body_md is absent. */}
              {topic.enough_md ? (
                <div className="mb-4">
                  <h3 className="text-sm font-semibold text-slate-900">
                    What enough looks like
                  </h3>
                  <Markdown>{topic.enough_md}</Markdown>
                </div>
              ) : null}
              {topic.log_md ? (
                <div>
                  <h3 className="text-sm font-semibold text-slate-900">Notes / log</h3>
                  <Markdown>{topic.log_md}</Markdown>
                </div>
              ) : null}
              {!topic.enough_md && !topic.log_md ? (
                <p className="text-sm text-slate-400 italic">No details recorded yet.</p>
              ) : null}
            </>
          )}
        </div>
      </aside>
    </div>
  )
}
