import { statusMeta } from '../lib/status.js'

export default function FocusStrip({ focus, onSelect }) {
  const list = Array.isArray(focus) ? focus.filter(Boolean) : []
  if (list.length === 0) return null

  return (
    <div className="border-b border-line bg-accent-soft/60">
      <div className="mx-auto flex max-w-[1400px] flex-wrap items-center gap-2 px-6 py-2.5">
        <span className="text-xs font-semibold tracking-wide text-accent-ink uppercase">
          Focus now
        </span>
        {list.map((topic, idx) => {
          const meta = statusMeta(topic.status)
          return (
            <button
              key={`${topic.skill_id || ''}-${topic.id || idx}`}
              type="button"
              onClick={() => onSelect(topic)}
              title={`${topic.skill_name || ''} · ${topic.title || ''} — ${meta.label}`}
              className="inline-flex max-w-[320px] items-center gap-1.5 rounded-full border border-accent-line bg-surface px-2.5 py-1 text-xs text-ink-2 transition-colors hover:border-accent hover:bg-accent-soft"
            >
              <span className={`inline-block h-2 w-2 shrink-0 rounded-full border ${meta.swatch}`} />
              <span className="truncate">
                {topic.skill_name ? (
                  <span className="text-ink-3">{topic.skill_name} · </span>
                ) : null}
                <span className="font-medium text-ink">{topic.title || topic.id}</span>
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
