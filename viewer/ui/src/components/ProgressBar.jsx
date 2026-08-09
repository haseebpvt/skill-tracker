import { clampPercent } from '../lib/derive.js'

export default function ProgressBar({ percent, className = '', height = 'h-2', barClass }) {
  const pct = clampPercent(percent)
  return (
    <div
      className={`w-full overflow-hidden rounded-full bg-slate-200 ${height} ${className}`}
      role="progressbar"
      aria-valuenow={Math.round(pct)}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        className={`${height} rounded-full transition-[width] duration-500 ${
          barClass || 'bg-green-600'
        }`}
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}
