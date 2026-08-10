import { clampPercent } from '../lib/derive.js'

// Hand-rolled burn-up chart. No chart library is installed and none should be
// added — the shape of this data (three short series on a shared date axis) is
// simple enough that a couple of scale functions beat a dependency.

const VB_W = 720
const VB_H = 220
const PAD = { top: 12, right: 16, bottom: 26, left: 34 }

const PLOT_W = VB_W - PAD.left - PAD.right
const PLOT_H = VB_H - PAD.top - PAD.bottom

const MS_PER_DAY = 86400000

// Parse "YYYY-MM-DD" (and the date half of an ISO timestamp) as UTC.
// Deliberately not `new Date(str)`: bare date strings parse as UTC but
// timestamps parse as local, so mixing them would shift points by a day
// depending on the viewer's timezone.
function parseDay(value) {
  if (typeof value !== 'string') return null
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(value.trim())
  if (!m) return null
  const t = Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]))
  return Number.isNaN(t) ? null : t
}

function cleanSeries(list) {
  if (!Array.isArray(list)) return []
  return list
    .map((d) => {
      const t = parseDay(d && d.date)
      if (t === null) return null
      return { t, percent: clampPercent(d.percent) }
    })
    .filter(Boolean)
    .sort((a, b) => a.t - b.t)
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

function shortDate(t) {
  const d = new Date(t)
  return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]}`
}

// Verdict drives the projection colour. Unknown stays neutral rather than
// implying a judgement the backend did not make.
function projectionStroke(verdict) {
  if (verdict === 'behind') return 'stroke-danger-solid'
  if (verdict === 'ahead' || verdict === 'on-track') return 'stroke-ok-solid'
  return 'stroke-ink-3'
}

function EmptyChart({ message }) {
  return (
    <div className="rounded-lg border border-line bg-surface-2 px-3 py-6 text-center">
      <p className="text-sm text-ink-3 italic">{message}</p>
    </div>
  )
}

export default function VelocityChart({ velocity }) {
  const series = cleanSeries(velocity && velocity.series)
  const projection = cleanSeries(velocity && velocity.projection)
  const targetLine = cleanSeries(velocity && velocity.target_line)

  if (series.length === 0) {
    return <EmptyChart message="No progress history recorded yet — the chart appears once there is something to plot." />
  }

  // X domain: from the first actual point to the furthest point any series
  // reaches. Guard against a zero-width domain (single point, or every series
  // landing on the same day) so the scale never divides by zero.
  const t0 = series[0].t
  const ends = [
    series[series.length - 1].t,
    projection.length ? projection[projection.length - 1].t : null,
    targetLine.length ? targetLine[targetLine.length - 1].t : null,
  ].filter((v) => typeof v === 'number')

  const tMax = Math.max(...ends, t0)
  const span = tMax - t0 || MS_PER_DAY

  // Both scales clamp to the plot box: a projection or target point that
  // predates series[0] would otherwise map to a negative x and draw outside
  // the viewBox. Percent is already clamped to 0–100 by cleanSeries.
  const x = (t) => {
    const frac = Math.max(0, Math.min(1, (t - t0) / span))
    return PAD.left + frac * PLOT_W
  }
  const y = (percent) => PAD.top + (1 - clampPercent(percent) / 100) * PLOT_H

  const toPoints = (list) => list.map((d) => `${x(d.t).toFixed(2)},${y(d.percent).toFixed(2)}`).join(' ')

  const last = series[series.length - 1]
  const lastX = x(last.t)
  const lastY = y(last.percent)

  // Area under the actual line, closed along the baseline.
  const areaPoints =
    series.length > 1
      ? `${x(t0).toFixed(2)},${y(0).toFixed(2)} ${toPoints(series)} ${lastX.toFixed(2)},${y(0).toFixed(2)}`
      : null

  // Join the projection to the last actual point so the dashed line continues
  // the solid one instead of floating away from it.
  const projPoints =
    projection.length > 0 ? `${lastX.toFixed(2)},${lastY.toFixed(2)} ${toPoints(projection)}` : null

  const verdict = velocity?.forecast?.verdict
  const gridValues = [0, 25, 50, 75, 100]

  // Sparse x labels: first, today, target. Dedupe when they coincide and drop
  // any that would collide, so the axis never turns into mush.
  const targetT = targetLine.length ? targetLine[targetLine.length - 1].t : null
  const rawLabels = [
    { t: t0, text: shortDate(t0), anchor: 'start' },
    { t: last.t, text: 'today', anchor: 'middle' },
    targetT !== null ? { t: targetT, text: shortDate(targetT), anchor: 'end' } : null,
  ].filter(Boolean)

  const labels = []
  for (const label of rawLabels) {
    const px = x(label.t)
    if (labels.some((l) => Math.abs(x(l.t) - px) < 44)) continue
    labels.push(label)
  }

  const summary = `Burn-up chart: ${clampPercent(last.percent).toFixed(1)}% complete as of ${shortDate(
    last.t
  )}${velocity?.forecast?.available && velocity.forecast.projected_date ? `, projected to finish ${velocity.forecast.projected_date}` : ''}.`

  return (
    <figure className="m-0">
      <svg
        viewBox={`0 0 ${VB_W} ${VB_H}`}
        className="h-auto w-full"
        role="img"
        aria-label={summary}
      >
        <title>{summary}</title>

        {gridValues.map((g) => (
          <g key={g}>
            <line
              x1={PAD.left}
              x2={VB_W - PAD.right}
              y1={y(g)}
              y2={y(g)}
              className="stroke-line"
              strokeWidth="1"
            />
            <text
              x={PAD.left - 6}
              y={y(g) + 3.5}
              textAnchor="end"
              className="fill-ink-3"
              fontSize="9"
            >
              {g}%
            </text>
          </g>
        ))}

        {targetLine.length > 1 ? (
          <polyline
            points={toPoints(targetLine)}
            fill="none"
            className="stroke-ink-3"
            strokeWidth="1.25"
            strokeDasharray="5 4"
            opacity="0.75"
          >
            <title>Target pace</title>
          </polyline>
        ) : null}

        {areaPoints ? (
          <polygon points={areaPoints} className="fill-accent" opacity="0.14" />
        ) : null}

        {series.length > 1 ? (
          <polyline
            points={toPoints(series)}
            fill="none"
            className="stroke-accent"
            strokeWidth="2"
            strokeLinejoin="round"
            strokeLinecap="round"
          >
            <title>Actual progress</title>
          </polyline>
        ) : null}

        {projPoints && projection.length > 0 ? (
          <polyline
            points={projPoints}
            fill="none"
            className={projectionStroke(verdict)}
            strokeWidth="1.75"
            strokeDasharray="4 4"
            strokeLinecap="round"
          >
            <title>Projection ({verdict || 'unknown'})</title>
          </polyline>
        ) : null}

        <line
          x1={lastX}
          x2={lastX}
          y1={PAD.top}
          y2={PAD.top + PLOT_H}
          className="stroke-line-strong"
          strokeWidth="1"
          strokeDasharray="2 3"
        />

        <circle cx={lastX} cy={lastY} r="3.5" className="fill-accent">
          <title>
            {shortDate(last.t)}: {clampPercent(last.percent).toFixed(1)}%
          </title>
        </circle>

        {labels.map((l) => (
          <text
            key={`${l.t}-${l.text}`}
            x={x(l.t)}
            y={VB_H - 8}
            textAnchor={l.anchor}
            className="fill-ink-3"
            fontSize="9"
          >
            {l.text}
          </text>
        ))}
      </svg>
    </figure>
  )
}
