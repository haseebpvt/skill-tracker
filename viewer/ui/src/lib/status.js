// Fixed status -> color mapping. Do not improvise: these four are the contract.
//   not-started -> gray, learning -> yellow, comfortable -> light green, strong -> saturated green

export const STATUSES = ['not-started', 'learning', 'comfortable', 'strong']

export const STATUS_META = {
  'not-started': {
    label: 'Not started',
    box: 'bg-slate-200 border-slate-300 text-slate-700 hover:bg-slate-300',
    swatch: 'bg-slate-200 border-slate-300',
    pill: 'bg-slate-100 text-slate-700 border-slate-300',
    bar: 'bg-slate-400',
  },
  learning: {
    label: 'Learning',
    box: 'bg-amber-200 border-amber-300 text-amber-900 hover:bg-amber-300',
    swatch: 'bg-amber-200 border-amber-300',
    pill: 'bg-amber-100 text-amber-900 border-amber-300',
    bar: 'bg-amber-400',
  },
  comfortable: {
    label: 'Comfortable',
    box: 'bg-green-200 border-green-300 text-green-900 hover:bg-green-300',
    swatch: 'bg-green-200 border-green-300',
    pill: 'bg-green-100 text-green-900 border-green-300',
    bar: 'bg-green-400',
  },
  strong: {
    label: 'Strong',
    box: 'bg-green-600 border-green-700 text-white hover:bg-green-700',
    swatch: 'bg-green-600 border-green-700',
    pill: 'bg-green-600 text-white border-green-700',
    bar: 'bg-green-600',
  },
}

const FALLBACK = {
  label: 'Unknown',
  box: 'bg-slate-100 border-slate-300 text-slate-500 hover:bg-slate-200',
  swatch: 'bg-slate-100 border-slate-300',
  pill: 'bg-slate-100 text-slate-600 border-slate-300',
  bar: 'bg-slate-300',
}

// Tolerates null / unexpected statuses rather than throwing.
export function statusMeta(status) {
  return STATUS_META[status] || FALLBACK
}
