import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

// Explicit Tailwind classes per element — deliberately not relying on
// @tailwindcss/typography, which is not installed.
const components = {
  h1: (p) => <h1 className="mt-5 mb-2 text-lg font-semibold text-slate-900" {...p} />,
  h2: (p) => <h2 className="mt-5 mb-2 text-base font-semibold text-slate-900" {...p} />,
  h3: (p) => <h3 className="mt-4 mb-1.5 text-sm font-semibold text-slate-900" {...p} />,
  h4: (p) => <h4 className="mt-3 mb-1 text-sm font-semibold text-slate-700" {...p} />,
  p: (p) => <p className="my-2 text-sm leading-relaxed text-slate-700" {...p} />,
  ul: (p) => <ul className="my-2 list-disc space-y-1 pl-5 text-sm text-slate-700" {...p} />,
  ol: (p) => <ol className="my-2 list-decimal space-y-1 pl-5 text-sm text-slate-700" {...p} />,
  li: (p) => <li className="leading-relaxed" {...p} />,
  a: (p) => (
    <a
      className="text-blue-700 underline underline-offset-2 hover:text-blue-900"
      target="_blank"
      rel="noreferrer noopener"
      {...p}
    />
  ),
  strong: (p) => <strong className="font-semibold text-slate-900" {...p} />,
  em: (p) => <em className="italic" {...p} />,
  code: ({ inline, className, children, ...rest }) =>
    inline ? (
      <code
        className="rounded bg-slate-100 px-1 py-0.5 font-mono text-[12px] text-slate-800"
        {...rest}
      >
        {children}
      </code>
    ) : (
      <code className={`font-mono text-[12px] ${className || ''}`} {...rest}>
        {children}
      </code>
    ),
  pre: (p) => (
    <pre
      className="my-3 overflow-x-auto rounded-lg border border-slate-200 bg-slate-50 p-3 text-[12px] leading-relaxed"
      {...p}
    />
  ),
  blockquote: (p) => (
    <blockquote
      className="my-3 border-l-4 border-slate-300 pl-3 text-sm text-slate-600 italic"
      {...p}
    />
  ),
  hr: () => <hr className="my-4 border-slate-200" />,
  table: (p) => (
    <div className="my-3 overflow-x-auto">
      <table className="w-full border-collapse text-sm" {...p} />
    </div>
  ),
  thead: (p) => <thead className="bg-slate-50" {...p} />,
  th: (p) => (
    <th
      className="border border-slate-200 px-2 py-1 text-left font-semibold text-slate-800"
      {...p}
    />
  ),
  td: (p) => <td className="border border-slate-200 px-2 py-1 text-slate-700" {...p} />,
  input: (p) =>
    p.type === 'checkbox' ? (
      // GFM task-list checkboxes: rendered but never interactive (read-only UI).
      <input
        {...p}
        disabled
        readOnly
        className="mr-1 align-middle accent-slate-400"
      />
    ) : null,
}

export default function Markdown({ children, className = '' }) {
  if (!children || typeof children !== 'string' || !children.trim()) return null
  return (
    <div className={className}>
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {children}
      </ReactMarkdown>
    </div>
  )
}
