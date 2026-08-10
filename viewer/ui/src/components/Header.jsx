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
      className="inline-flex max-w-[280px] items-center gap-1.5 rounded-md border border-line bg-surface px-2 py-1 text-xs text-ink-2"
    >
      <span className="font-medium text-ink">{branch}</span>
      {git.dirty ? (
        <span
          className="inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-warn-solid"
          aria-label="dirty working tree"
        />
      ) : null}
      {commit ? <span className="truncate text-ink-3">{commit}</span> : null}
    </span>
  )
}

function ConnectionChip({ connected }) {
  return (
    <span
      title={connected ? 'Live — receiving updates' : 'Disconnected — retrying'}
      className={`inline-flex items-center gap-1.5 rounded-md border px-2 py-1 text-xs font-medium ${
        connected
          ? 'border-ok-line bg-ok-soft text-ok-ink'
          : 'border-danger-line bg-danger-soft text-danger-ink'
      }`}
    >
      <span
        className={`inline-block h-1.5 w-1.5 rounded-full ${
          connected ? 'bg-ok-solid' : 'bg-danger-solid'
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
    <header className="sticky top-0 z-20 border-b border-line bg-surface/95 backdrop-blur">
      <div className="mx-auto max-w-[1400px] px-6 py-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="min-w-0">
            {hasRole ? (
              <>
                <h1 className="truncate text-xl font-semibold text-ink">
                  {role.role || 'Untitled role'}
                  {role.level ? (
                    <span className="ml-2 rounded-md bg-surface-2 px-2 py-0.5 text-sm font-medium text-ink-2">
                      {role.level}
                    </span>
                  ) : null}
                </h1>
                <p className="mt-0.5 text-xs text-ink-3">
                  {role.updated ? `Updated ${role.updated}` : 'No update date'}
                  {generatedAt ? ` · generated ${generatedAt}` : ''}
                </p>
              </>
            ) : (
              <>
                <h1 className="text-xl font-semibold text-ink">Skill Tracker</h1>
                <p className="mt-0.5 text-xs text-warn-ink">
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
              <span className="text-xs font-medium tracking-wide text-ink-3 uppercase">
                Overall progress
              </span>
              <span className="text-sm font-semibold text-ink">
                {formatPercent(summary.overall_percent)}
                <span className="ml-2 text-xs font-normal text-ink-3">
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
                  ? 'border-accent-line bg-accent-soft text-accent-ink'
                  : 'border-line bg-surface text-ink-2 hover:bg-surface-2'
              }`}
            >
              <span
                className={`inline-flex h-4 w-7 shrink-0 items-center rounded-full px-0.5 transition-colors ${
                  minOnly ? 'bg-accent-solid' : 'bg-line-strong'
                }`}
              >
                <span
                  className={`inline-block h-3 w-3 rounded-full bg-surface transition-transform ${
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
          <p className="mt-2 text-xs text-accent-ink">
            Showing minimum-required topics only — progress and counts below reflect the filtered set.
          </p>
        ) : null}
      </div>
    </header>
  )
}
