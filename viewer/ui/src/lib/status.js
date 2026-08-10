// Fixed status -> color mapping. Do not improvise: these four are the contract.
//   not-started -> gray, learning -> yellow, comfortable -> light green, strong -> full green
//
// Colours come from the semantic tokens in index.css, so the ramp is tuned for
// the dark theme in exactly one place.

export const STATUSES = ['not-started', 'learning', 'comfortable', 'strong']

export const STATUS_META = {
  'not-started': {
    label: 'Not started',
    box: 'bg-st-none border-st-none-line text-st-none-ink hover:bg-surface-3',
    swatch: 'bg-st-none border-st-none-line',
    pill: 'bg-st-none text-st-none-ink border-st-none-line',
    bar: 'bg-st-none-line',
  },
  learning: {
    label: 'Learning',
    box: 'bg-st-learn border-st-learn-line text-st-learn-ink hover:bg-st-learn-line',
    swatch: 'bg-st-learn border-st-learn-line',
    pill: 'bg-st-learn text-st-learn-ink border-st-learn-line',
    bar: 'bg-st-learn-line',
  },
  comfortable: {
    label: 'Comfortable',
    box: 'bg-st-comf border-st-comf-line text-st-comf-ink hover:bg-st-comf-line',
    swatch: 'bg-st-comf border-st-comf-line',
    pill: 'bg-st-comf text-st-comf-ink border-st-comf-line',
    bar: 'bg-st-comf-line',
  },
  strong: {
    label: 'Strong',
    box: 'bg-st-strong border-st-strong-line text-st-strong-ink hover:bg-st-strong-line',
    swatch: 'bg-st-strong border-st-strong-line',
    pill: 'bg-st-strong text-st-strong-ink border-st-strong-line',
    bar: 'bg-st-strong',
  },
}

const FALLBACK = {
  label: 'Unknown',
  box: 'bg-surface-2 border-line text-ink-3 hover:bg-surface-3',
  swatch: 'bg-surface-2 border-line',
  pill: 'bg-surface-2 text-ink-3 border-line',
  bar: 'bg-line-strong',
}

// Tolerates null / unexpected statuses rather than throwing.
export function statusMeta(status) {
  return STATUS_META[status] || FALLBACK
}
