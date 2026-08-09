import { statusMeta } from '../lib/status.js'
import { summarizeMarkdown } from '../lib/derive.js'

export default function TopicBox({ topic, onSelect }) {
  const meta = statusMeta(topic.status)

  // Rich native tooltip: title, status, what "enough" looks like, last updated.
  const enough = summarizeMarkdown(topic.enough_md, 240)
  const tooltip = [
    topic.title || topic.id,
    `Status: ${meta.label}`,
    topic.min_required ? 'Minimum required ★' : null,
    topic.focus ? 'In focus' : null,
    enough ? `\nWhat enough looks like:\n${enough}` : null,
    topic.updated ? `\nUpdated ${topic.updated}` : null,
  ]
    .filter(Boolean)
    .join('\n')

  return (
    <button
      type="button"
      onClick={() => onSelect(topic)}
      title={tooltip}
      className={`relative flex h-[58px] w-[150px] shrink-0 items-center rounded-lg border px-2.5 py-2 text-left transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-1 ${
        meta.box
      } ${topic.focus ? 'focus-pulse' : ''}`}
    >
      <span className="line-clamp-3 text-[11.5px] leading-tight font-medium break-words">
        {topic.title || topic.id}
      </span>

      {topic.min_required ? (
        <span
          aria-label="minimum required"
          className="pointer-events-none absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full border border-slate-300 bg-white text-[9px] leading-none text-amber-600 shadow-sm"
        >
          ★
        </span>
      ) : null}
    </button>
  )
}
