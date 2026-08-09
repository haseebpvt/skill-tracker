import { useState } from 'react'
import Markdown from './Markdown.jsx'
import { evidenceStatusLine } from '../lib/derive.js'

export default function Conclusions({ conclusions, evidenceStatus }) {
  const [open, setOpen] = useState(false)

  const exists = !!(conclusions && conclusions.exists)
  const { text: evidenceText, stale } = evidenceStatusLine(evidenceStatus)
  const sections = Array.isArray(conclusions?.sections) ? conclusions.sections : []
  const considered = Array.isArray(conclusions?.evidence_files_considered)
    ? conclusions.evidence_files_considered
    : []

  return (
    <section className="rounded-xl border border-slate-200 bg-white shadow-sm">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-4 px-4 py-3 text-left"
      >
        <span className="flex items-center gap-2">
          <span
            className={`text-slate-400 transition-transform ${open ? 'rotate-90' : ''}`}
          >
            ›
          </span>
          <span className="text-base font-semibold text-slate-900">Conclusions</span>
          {conclusions?.updated ? (
            <span className="text-xs text-slate-500">updated {conclusions.updated}</span>
          ) : null}
        </span>

        {evidenceText ? (
          <span
            title={
              stale
                ? 'Evidence has changed since these conclusions were written — they may be stale.'
                : 'Evidence unchanged since these conclusions were written.'
            }
            className={`shrink-0 rounded-md border px-2 py-1 text-xs ${
              stale
                ? 'border-amber-300 bg-amber-50 text-amber-900'
                : 'border-slate-200 bg-slate-50 text-slate-600'
            }`}
          >
            {evidenceText}
            {stale ? ' — may be stale' : ''}
          </span>
        ) : null}
      </button>

      {open ? (
        <div className="border-t border-slate-200 px-4 py-3">
          {!exists ? (
            <p className="text-sm text-slate-500 italic">
              No conclusions file yet. Add <code className="font-mono">evidence/CONCLUSIONS.md</code>{' '}
              to record your reasoning.
            </p>
          ) : (
            <>
              {sections.length > 0 ? (
                <div className="mb-3 flex flex-wrap gap-1.5">
                  {sections.map((s, idx) => (
                    <span
                      key={`${s}-${idx}`}
                      className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] text-slate-600"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              ) : null}

              <Markdown>{conclusions.content_md}</Markdown>

              {considered.length > 0 ? (
                <details className="mt-4">
                  <summary className="cursor-pointer text-xs text-slate-500 hover:text-slate-700">
                    Evidence files considered ({considered.length})
                  </summary>
                  <ul className="mt-1.5 space-y-1">
                    {considered.map((f, idx) => (
                      <li key={`${f?.path || idx}`} className="text-xs">
                        <code className="font-mono break-all text-slate-700">
                          {f?.path || '—'}
                        </code>
                        {f?.hash ? (
                          <span className="ml-2 font-mono text-slate-400">
                            {String(f.hash).slice(0, 12)}
                          </span>
                        ) : null}
                      </li>
                    ))}
                  </ul>
                </details>
              ) : null}
            </>
          )}
        </div>
      ) : null}
    </section>
  )
}
