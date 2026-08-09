import { STATUSES } from './status.js'

// Weight each status toward "done". Mirrors the intent of the server's percent
// so the filtered view stays visually consistent with the unfiltered one.
const WEIGHTS = {
  'not-started': 0,
  learning: 0.34,
  comfortable: 0.67,
  strong: 1,
}

export function emptyCounts() {
  return { 'not-started': 0, learning: 0, comfortable: 0, strong: 0 }
}

export function countByStatus(topics) {
  const counts = emptyCounts()
  for (const t of topics || []) {
    const s = t && t.status
    if (s in counts) counts[s] += 1
  }
  return counts
}

export function percentFor(topics) {
  const list = topics || []
  if (list.length === 0) return 0
  let sum = 0
  for (const t of list) sum += WEIGHTS[t && t.status] ?? 0
  return (sum / list.length) * 100
}

function topicsOf(skill) {
  return Array.isArray(skill && skill.topics) ? skill.topics : []
}

/**
 * Build the view model.
 *
 * When `minOnly` is on we recompute every progress number from the filtered
 * topic set instead of reusing `skill.progress` / `summary`, so the bars and
 * counts actually reflect what is on screen. When it is off we prefer the
 * server-supplied numbers and only fall back to local computation if they are
 * missing, so the display matches the backend exactly.
 */
export function deriveView(state, minOnly) {
  const rawSkills = Array.isArray(state && state.skills) ? state.skills : []

  const skills = rawSkills.map((skill) => {
    const all = topicsOf(skill)
    const topics = minOnly ? all.filter((t) => t && t.min_required) : all
    const sorted = sortByPriority(topics)
    const counts = countByStatus(topics)

    let percent
    let total
    if (minOnly) {
      percent = percentFor(topics)
      total = topics.length
    } else {
      const p = skill && skill.progress
      percent = typeof p?.percent === 'number' ? p.percent : percentFor(topics)
      total = typeof p?.total === 'number' ? p.total : topics.length
    }

    const serverCounts = skill?.progress?.counts
    const displayCounts = minOnly ? counts : serverCounts || counts

    // "done" = comfortable + strong, used for the n/total readout.
    const done = (displayCounts.comfortable || 0) + (displayCounts.strong || 0)

    return {
      ...skill,
      topics: sorted,
      view: { percent: clampPercent(percent), total, counts: displayCounts, done },
    }
  })

  // Skills whose topics all filtered away are dropped in min-only mode.
  const visibleSkills = minOnly ? skills.filter((s) => s.topics.length > 0) : skills

  const allVisibleTopics = visibleSkills.flatMap((s) => s.topics)

  let summary
  if (minOnly) {
    const counts = countByStatus(allVisibleTopics)
    summary = {
      overall_percent: clampPercent(percentFor(allVisibleTopics)),
      total_topics: allVisibleTopics.length,
      counts,
    }
  } else {
    const s = state && state.summary
    const counts = s?.counts || countByStatus(rawSkills.flatMap(topicsOf))
    summary = {
      overall_percent: clampPercent(
        typeof s?.overall_percent === 'number'
          ? s.overall_percent
          : percentFor(rawSkills.flatMap(topicsOf))
      ),
      total_topics:
        typeof s?.total_topics === 'number'
          ? s.total_topics
          : rawSkills.flatMap(topicsOf).length,
      counts,
    }
  }

  // Prefer the server's min_bar. If it is absent but min_required topics exist,
  // derive it locally so the filter toggle stays available.
  let minBar = state?.summary?.min_bar || null
  if (!minBar) {
    const required = rawSkills.flatMap(topicsOf).filter((t) => t && t.min_required)
    if (required.length > 0) {
      const met = required.filter(
        (t) => t.status === 'comfortable' || t.status === 'strong'
      ).length
      minBar = { total: required.length, met }
    }
  }

  const focus = Array.isArray(state && state.focus) ? state.focus.filter(Boolean) : []
  const visibleFocus = minOnly ? focus.filter((t) => t && t.min_required) : focus

  return { skills: visibleSkills, summary, minBar, focus: visibleFocus }
}

// Stable sort by priority ascending; missing priorities sink to the bottom but
// otherwise keep their original relative order.
export function sortByPriority(topics) {
  return (topics || [])
    .map((t, i) => ({ t, i }))
    .sort((a, b) => {
      const pa = typeof a.t?.priority === 'number' ? a.t.priority : Number.POSITIVE_INFINITY
      const pb = typeof b.t?.priority === 'number' ? b.t.priority : Number.POSITIVE_INFINITY
      if (pa !== pb) return pa - pb
      return a.i - b.i
    })
    .map((x) => x.t)
}

export function clampPercent(n) {
  if (typeof n !== 'number' || Number.isNaN(n)) return 0
  return Math.max(0, Math.min(100, n))
}

export function formatPercent(n) {
  return `${clampPercent(n).toFixed(1)}%`
}

export function countsLine(counts) {
  const c = counts || emptyCounts()
  return STATUSES.map((s) => `${c[s] || 0} ${s}`).join(' · ')
}

// Pull a short plain-text gist out of a markdown blob for the hover tooltip.
export function summarizeMarkdown(md, maxLen = 260) {
  if (!md || typeof md !== 'string') return ''
  const text = md
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/^\s*[-*+]\s+/gm, '• ')
    .replace(/^#{1,6}\s+/gm, '')
    .replace(/[*_`>]/g, '')
    .split('\n')
    .map((l) => l.trim())
    .filter(Boolean)
    .join('\n')
  if (text.length <= maxLen) return text
  return text.slice(0, maxLen).trimEnd() + '…'
}

export function evidenceStatusLine(ev) {
  if (!ev) return { text: '', stale: false }
  const n = (k) => (Array.isArray(ev[k]) ? ev[k].length : 0)
  const unchanged = n('unchanged')
  const added = n('new')
  const modified = n('modified')
  const deleted = n('deleted')
  const stale = added > 0 || modified > 0 || deleted > 0
  const parts = [`${unchanged} unchanged`, `${added} new`, `${modified} modified`]
  if (deleted > 0) parts.push(`${deleted} deleted`)
  return { text: parts.join(', '), stale }
}
