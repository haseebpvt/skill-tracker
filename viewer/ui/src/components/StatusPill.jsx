import { statusMeta } from '../lib/status.js'

export default function StatusPill({ status, className = '' }) {
  const meta = statusMeta(status)
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium ${meta.pill} ${className}`}
    >
      {meta.label}
    </span>
  )
}
