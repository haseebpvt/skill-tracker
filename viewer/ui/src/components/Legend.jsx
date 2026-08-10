import { STATUSES, statusMeta } from '../lib/status.js'

export default function Legend() {
  return (
    <div className="border-t border-line bg-surface">
      <div className="mx-auto flex max-w-[1400px] flex-wrap items-center gap-x-5 gap-y-2 px-6 py-3 text-xs text-ink-2">
        <span className="font-semibold tracking-wide text-ink-3 uppercase">Legend</span>

        {STATUSES.map((s) => {
          const meta = statusMeta(s)
          return (
            <span key={s} className="inline-flex items-center gap-1.5">
              <span className={`inline-block h-3 w-5 rounded border ${meta.swatch}`} />
              {meta.label}
            </span>
          )
        })}

        <span className="inline-flex items-center gap-1.5">
          <span className="focus-pulse inline-block h-3 w-5 rounded border border-st-none-line bg-st-none" />
          Focus now
        </span>

        <span className="inline-flex items-center gap-1.5">
          <span className="relative inline-block h-3 w-5 rounded border border-st-none-line bg-st-none">
            <span className="absolute -top-1 -right-1 flex h-3 w-3 items-center justify-center rounded-full border border-line-strong bg-surface text-[7px] text-warn-solid">
              ★
            </span>
          </span>
          Minimum required
        </span>
      </div>
    </div>
  )
}
