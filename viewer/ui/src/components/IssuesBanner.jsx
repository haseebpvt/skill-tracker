import { useState } from 'react'

function levelOf(issue) {
  const l = (issue && issue.level ? String(issue.level) : 'warning').toLowerCase()
  return l === 'error' ? 'error' : 'warning'
}

export default function IssuesBanner({ issues }) {
  const [open, setOpen] = useState(true)
  const list = Array.isArray(issues) ? issues.filter(Boolean) : []
  if (list.length === 0) return null

  const errors = list.filter((i) => levelOf(i) === 'error')
  const warnings = list.filter((i) => levelOf(i) === 'warning')
  const hasErrors = errors.length > 0

  return (
    <div
      className={`border-b ${
        hasErrors ? 'border-danger-line bg-danger-soft' : 'border-warn-line bg-warn-soft'
      }`}
    >
      <div className="mx-auto max-w-[1400px] px-6 py-2.5">
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          className={`flex w-full items-center gap-2 text-left text-sm font-medium ${
            hasErrors ? 'text-danger-ink' : 'text-warn-ink'
          }`}
        >
          <span className={`transition-transform ${open ? 'rotate-90' : ''}`}>›</span>
          <span>
            {errors.length > 0 ? `${errors.length} error${errors.length === 1 ? '' : 's'}` : ''}
            {errors.length > 0 && warnings.length > 0 ? ' · ' : ''}
            {warnings.length > 0
              ? `${warnings.length} warning${warnings.length === 1 ? '' : 's'}`
              : ''}
          </span>
          <span className="font-normal opacity-70">
            {open ? '' : '— click to expand'}
          </span>
        </button>

        {open ? (
          <ul className="mt-2 space-y-1">
            {list.map((issue, idx) => {
              const level = levelOf(issue)
              return (
                <li
                  key={`${issue.path || 'issue'}-${idx}`}
                  className="flex flex-wrap items-baseline gap-2 text-sm"
                >
                  <span
                    className={`shrink-0 rounded px-1.5 py-0.5 text-[11px] font-semibold uppercase ${
                      level === 'error'
                        ? 'bg-danger-line text-danger-ink'
                        : 'bg-warn-line text-warn-ink'
                    }`}
                  >
                    {level}
                  </span>
                  {issue.path ? (
                    <code className="font-mono text-xs text-ink-2">{issue.path}</code>
                  ) : null}
                  <span className={level === 'error' ? 'text-danger-ink' : 'text-warn-ink'}>
                    {issue.message || 'Unknown issue'}
                  </span>
                </li>
              )
            })}
          </ul>
        ) : null}
      </div>
    </div>
  )
}
