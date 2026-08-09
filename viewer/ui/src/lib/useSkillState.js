import { useEffect, useRef, useState } from 'react'

const STATE_URL = 'api/state'
const EVENTS_URL = 'api/events'

// Resolve against the document base so the app works both at the FastAPI root
// and from a subpath when built with `base: './'`.
function url(path) {
  return new URL(path, document.baseURI).toString()
}

/**
 * Subscribes to the backend state.
 *
 * - Does an initial fetch so the page paints even if SSE is slow to open.
 * - Opens an EventSource and applies `state` events directly (no refetch).
 * - `ping` events are keepalives and are ignored.
 * - EventSource auto-reconnects; we surface `connected: false` on error and
 *   clear it on the next message.
 */
export function useSkillState() {
  const [state, setState] = useState(null)
  const [connected, setConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Guards against a slow initial fetch clobbering fresher SSE data.
  const gotEventRef = useRef(false)

  useEffect(() => {
    let cancelled = false

    fetch(url(STATE_URL), { headers: { Accept: 'application/json' } })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data) => {
        if (cancelled || gotEventRef.current) return
        setState(data)
        setError(null)
      })
      .catch((err) => {
        if (cancelled || gotEventRef.current) return
        setError(err && err.message ? err.message : String(err))
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    let es
    try {
      es = new EventSource(url(EVENTS_URL))
    } catch {
      // EventSource unavailable (or blocked) — the initial fetch still stands.
      return () => {
        cancelled = true
      }
    }

    es.addEventListener('open', () => {
      if (!cancelled) setConnected(true)
    })

    es.addEventListener('state', (evt) => {
      if (cancelled) return
      try {
        const data = JSON.parse(evt.data)
        gotEventRef.current = true
        setState(data)
        setError(null)
        setConnected(true)
        setLoading(false)
      } catch {
        // A malformed frame should not take the page down.
      }
    })

    // Keepalive. Presence of traffic means we are still live.
    es.addEventListener('ping', () => {
      if (!cancelled) setConnected(true)
    })

    es.addEventListener('error', () => {
      // EventSource retries on its own; just reflect the drop in the UI.
      if (!cancelled) setConnected(false)
    })

    return () => {
      cancelled = true
      if (es) es.close()
    }
  }, [])

  return { state, connected, loading, error }
}
