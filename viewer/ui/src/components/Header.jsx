import ProgressBar from './ProgressBar.jsx'
import { formatPercent } from '../lib/derive.js'

function GitChip({ git }) {
  // Hidden entirely when git is unavailable, per spec.
  if (!git || !git.available) return null
  const branch = git.branch || 'unknown'
  const commit = git.last_commit || ''
  const tooltip = [`branch: ${branch}`, commit ? `last commit: ${commit}` : null, git.dirty ? 'working tree dirty' : 'working tree clean']
    .filter(Boolean)
    .join('\n')

  return (
    <span
      title={tooltip}
      className="inline-flex max-w-[280px] items-center gap-1.5 rounded-md border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600"
    >
      <span className="font-medium text-slate-800">{branch}</span>
      {git.dirty ? (
        <span
          className="inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500"
          aria-label="dirty working tree"
        />
      ) : null}
      {commit ? <span className="truncate text-slate-500">{commit}</span> : null}
    </span>
  )
}

function ConnectionChip({ connected }) {
  return (
    <span
      title={connected ? 'Live — receiving updates' : 'Disconnected — retrying'}
      className={`inline-flex items-center gap-1.5 rounded-md border px-2 py-1 text-xs font-medium ${
        connected
          ? 'border-green-200 bg-green-50 text-green-800'
          : 'border-red-200 bg-red-50 text-red-800'
      }`}
    >
      <span
        className={`inline-block h-1.5 w-1.5 rounded-full ${
          connected ? 'bg-green-600' : 'bg-red-500'
        }`}
      />
      {connected ? 'Live' : 'Disconnected'}
    </span>
  )
}

export default function Header({
  role,
  summary,
  minBar,
  git,
  connected,
  minOnly,
  onToggleMinOnly,
  generatedAt,
}) {
  const hasRole = !!role
  const met = minBar && typeof minBar.met === 'number' ? minBar.met : null
  const totalBar = minBar && typeof minBar.total === 'number' ? minBar.total : null
  const barComplete = met !== null && totalBar !== null && totalBar > 0 && met >= totalBar

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/95 backdrop-blur">
      <div className="mx-auto max-w-[1400px] px-6 py-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0">
            {hasRole ? (
              <>
                <h1 className="truncate text-xl font-semibold text-slate-900">
                  {role.role || 'Untitled role'}
                  {role.level ? (
                    <span className="ml-2 rounded-md bg-slate-100 px-2 py-0.5 text-sm font-medium text-slate-600">
                      {role.level}
                    </span>
                  ) : null}
                </h1>
                <p className="mt-0.5 text-xs text-slate-500">
                  {role.updated ? `Updated ${role.updated}` : 'No update date'}
                  {generatedAt ? ` · generated ${generatedAt}` : ''}
                </p>
              </>
            ) : (
              <>
                <h1 className="text-xl font-semibold text-slate-900">Skill Tracker</h1>
                <p className="mt-0.5 text-xs text-amber-700">
                  No role defined — add <code className="font-mono">data/role.md</code> to set a target.
                </p>
              </>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <GitChip git={git} />
            <ConnectionChip connected={connected} />
          </div>
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-6">
          <div className="min-w-[280px] flex-1">
            <div className="mb-1 flex items-baseline justify-between gap-3">
              <span className="text-xs font-medium tracking-wide text-slate-500 uppercase">
                Overall progress
              </span>
              <span className="text-sm font-semibold text-slate-900">
                {formatPercent(summary.overall_percent)}
                <span className="ml-2 text-xs font-normal text-slate-500">
                  {summary.total_topics} topic{summary.total_topics === 1 ? '' : 's'}
                </span>
              </span>
            </div>
            <ProgressBar percent={summary.overall_percent} height="h-2.5" />
          </div>

          {minBar ? (
            <button
              type="button"
              onClick={onToggleMinOnly}
              aria-pressed={minOnly}
              title="Filter the whole view to minimum-required topics only"
              className={`inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium transition-colors ${
                minOnly
                  ? 'border-blue-300 bg-blue-50 text-blue-900'
                  : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
              }`}
            >
              <span
                className={`inline-flex h-4 w-7 shrink-0 items-center rounded-full px-0.5 transition-colors ${
                  minOnly ? 'bg-blue-600' : 'bg-slate-300'
                }`}
              >
                <span
                  className={`inline-block h-3 w-3 rounded-full bg-white transition-transform ${
                    minOnly ? 'translate-x-3' : 'translate-x-0'
                  }`}
                />
              </span>
              <span>
                Min bar: {met ?? '—'}/{totalBar ?? '—'}
                {barComplete ? ' ✓' : ''}
              </span>
            </button>
          ) : null}
        </div>

        {minOnly ? (
          <p className="mt-2 text-xs text-blue-800">
            Showing minimum-required topics only — progress and counts below reflect the filtered set.
          </p>
        ) : null}
      </div>
    </header>
  )
}
