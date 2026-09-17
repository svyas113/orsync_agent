import { useCallback, useEffect, useRef, useState } from 'react'
import './ChatWidget.css'

const API_BASE = (import.meta.env.VITE_AGENT_API_URL || 'http://localhost:8003').replace(/\/$/, '')

const STORAGE_KEYS = {
  channelId: 'orsync_visitor_channel_id',
  accessToken: 'orsync_visitor_access_token',
  refreshToken: 'orsync_visitor_refresh_token',
}

const STARTUP_ACTION = {
  command_name: 'set_root_context',
  command: '',
  parameters: {},
}

const SUGGESTIONS = [
  { label: 'What are AI agents?', query: 'I have no idea what AI agents are or what you do' },
  { label: 'About Or-sync', query: 'Tell me about your company and brand' },
  { label: 'Try a demo agent', query: 'Chat with a random demo agent' },
  { label: 'Request a demo', query: 'I want to request a demo' },
]

function getOrCreateChannelId() {
  let id = localStorage.getItem(STORAGE_KEYS.channelId)
  if (!id) {
    id = `web-${crypto.randomUUID()}`
    localStorage.setItem(STORAGE_KEYS.channelId, id)
  }
  return id
}

function readTokens() {
  return {
    accessToken: sessionStorage.getItem(STORAGE_KEYS.accessToken),
    refreshToken: sessionStorage.getItem(STORAGE_KEYS.refreshToken),
  }
}

function writeTokens(accessToken, refreshToken) {
  if (accessToken) sessionStorage.setItem(STORAGE_KEYS.accessToken, accessToken)
  else sessionStorage.removeItem(STORAGE_KEYS.accessToken)
  if (refreshToken) sessionStorage.setItem(STORAGE_KEYS.refreshToken, refreshToken)
  else sessionStorage.removeItem(STORAGE_KEYS.refreshToken)
}

function extractText(output) {
  if (!output) return ''
  const responses = output.command_responses || []
  const parts = responses
    .map((r) => (typeof r === 'string' ? r : r?.response || r?.text || ''))
    .filter(Boolean)
  if (parts.length) return parts.join('\n\n')
  if (typeof output.response === 'string') return output.response
  if (typeof output.message === 'string') return output.message
  return ''
}

const FLUX_RE = /\bflux(?:\s*designer)?\b/i
const SAFE_REPLY =
  'I can help with Or-sync company info, our services, public demos (Spyran, Zebrata, RVD Jewels), or a private demo request. What would you like to explore?'

function scrubClient(text) {
  if (!text) return text
  return FLUX_RE.test(text) ? SAFE_REPLY : text
}

function toBrowserText(text) {
  if (!text) return text
  let out = text
  // [label](url) → label or url
  out = out.replace(/\[([^\]]*)\]\(([^)]+)\)/g, (_, label, url) => {
    const l = (label || '').trim()
    const u = (url || '').trim()
    if (!u) return l
    if (!l || l === u || l.startsWith(u) || u.startsWith(l)) return u
    return `${l}: ${u}`
  })
  out = out.replace(/\*\*(.+?)\*\*|__(.+?)__/g, (_, a, b) => a || b || '')
  out = out.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)|(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g, (_, a, b) => a || b || '')
  out = out.replace(/`([^`]*)`/g, '$1')
  out = out.replace(/^#{1,6}\s+/gm, '')
  out = out.replace(/\*\*/g, '').replace(/__/g, '')
  out = out.replace(/\n{3,}/g, '\n\n')
  return out.trim()
}

function linkify(text) {
  const urlRe = /(https?:\/\/[^\s)]+)/g
  const nodes = []
  let last = 0
  let match
  let key = 0
  while ((match = urlRe.exec(text)) !== null) {
    if (match.index > last) nodes.push(text.slice(last, match.index))
    const url = match[1]
    nodes.push(
      <a key={`u-${key++}`} href={url} target="_blank" rel="noopener noreferrer">
        {url}
      </a>,
    )
    last = match.index + url.length
  }
  if (last < text.length) nodes.push(text.slice(last))
  return nodes
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [ready, setReady] = useState(false)
  const [sending, setSending] = useState(false)
  const [status, setStatus] = useState('Offline')
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const initPromise = useRef(null)
  const listRef = useRef(null)

  const append = useCallback((role, text) => {
    let cleaned = (text || '').trim()
    if (!cleaned) return
    if (role === 'assistant') cleaned = toBrowserText(scrubClient(cleaned))
    setMessages((prev) => [...prev, { id: crypto.randomUUID(), role, text: cleaned }])
  }, [])

  useEffect(() => {
    if (!listRef.current) return
    listRef.current.scrollTop = listRef.current.scrollHeight
  }, [messages, open])

  const refreshAccessToken = useCallback(async (refreshToken) => {
    try {
      const res = await fetch(`${API_BASE}/refresh_token`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${refreshToken}` },
      })
      if (!res.ok) return false
      const data = await res.json()
      writeTokens(data.access_token, data.refresh_token)
      return true
    } catch {
      return false
    }
  }, [])

  const initializeSession = useCallback(
    async ({ silent = false } = {}) => {
      if (initPromise.current) return initPromise.current

      initPromise.current = (async () => {
        if (!silent) setStatus('Connecting…')
        setReady(false)

        const res = await fetch(`${API_BASE}/initialize`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            channel_id: getOrCreateChannelId(),
            user_id: 'website-visitor',
            startup_action: STARTUP_ACTION,
          }),
        })

        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw new Error(err.detail || `Initialize failed (${res.status})`)
        }

        const data = await res.json()
        if (!data.access_token || !data.refresh_token) {
          throw new Error('Initialize succeeded but did not return auth tokens')
        }

        writeTokens(data.access_token, data.refresh_token)
        setReady(true)
        setStatus('Online')

        if (!silent) {
          const welcome = extractText(data.startup_output)
          if (welcome) append('assistant', welcome)
          else {
            append(
              'assistant',
              "Hi — I'm the Or-sync assistant. Ask about AI agents, our company, try a demo, or request a private demo.",
            )
          }
        }
      })()

      try {
        await initPromise.current
      } finally {
        initPromise.current = null
      }
    },
    [append],
  )

  const apiFetch = useCallback(
    async (path, options = {}, retryState = { refresh: true, reinit: true }) => {
      const { accessToken, refreshToken } = readTokens()
      const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
      }
      if (accessToken && !path.includes('/initialize') && !path.includes('/refresh_token')) {
        headers.Authorization = `Bearer ${accessToken}`
      }

      const res = await fetch(`${API_BASE}${path}`, { ...options, headers })
      if (res.status !== 401) return res

      if (retryState.refresh && refreshToken) {
        const refreshed = await refreshAccessToken(refreshToken)
        if (refreshed) {
          return apiFetch(path, options, { refresh: false, reinit: retryState.reinit })
        }
      }

      if (retryState.reinit && !path.includes('/initialize')) {
        await initializeSession({ silent: true })
        if (readTokens().accessToken) {
          return apiFetch(path, options, { refresh: false, reinit: false })
        }
      }

      return res
    },
    [initializeSession, refreshAccessToken],
  )

  const ensureReady = useCallback(async () => {
    if (ready && readTokens().accessToken) return
    await initializeSession({ silent: messages.length > 0 })
  }, [initializeSession, messages.length, ready])

  const sendMessage = useCallback(
    async (raw) => {
      const query = (raw || '').trim()
      if (!query || sending) return

      setSending(true)
      append('user', query)
      setInput('')

      try {
        await ensureReady()
        const res = await apiFetch('/invoke_agent', {
          method: 'POST',
          body: JSON.stringify({ user_query: query, timeout_seconds: 120 }),
        })
        if (!res.ok) {
          const err = await res.json().catch(() => ({}))
          throw new Error(err.detail || `Request failed (${res.status})`)
        }
        const output = await res.json()
        const reply = extractText(output) || "I couldn't generate a reply. Please try again."
        append('assistant', reply)
      } catch (err) {
        append('assistant', `Sorry — ${err.message || 'something went wrong'}.`)
        setStatus('Error')
      } finally {
        setSending(false)
      }
    },
    [apiFetch, append, ensureReady, sending],
  )

  const handleOpen = async () => {
    const next = !open
    setOpen(next)
    if (next && !ready) {
      try {
        await initializeSession({ silent: false })
      } catch (err) {
        setStatus('Offline')
        append('assistant', `Could not connect to the assistant (${err.message}).`)
      }
    }
  }

  return (
    <div className="orsync-chat">
      {open && (
        <section className="orsync-chat__panel" aria-label="Or-sync chat assistant">
          <header className="orsync-chat__header">
            <div>
              <strong>Or-sync Assistant</strong>
              <span className={`orsync-chat__status ${ready ? 'is-online' : ''}`}>{status}</span>
            </div>
            <button type="button" className="orsync-chat__icon-btn" onClick={() => setOpen(false)} aria-label="Close chat">
              ×
            </button>
          </header>

          <div className="orsync-chat__messages" ref={listRef}>
            {messages.map((msg) => (
              <div key={msg.id} className={`orsync-chat__bubble orsync-chat__bubble--${msg.role}`}>
                {linkify(msg.text)}
              </div>
            ))}
          </div>

          {messages.length <= 1 && (
            <div className="orsync-chat__suggestions">
              {SUGGESTIONS.map((chip) => (
                <button
                  key={chip.label}
                  type="button"
                  className="orsync-chat__chip"
                  disabled={sending || !ready}
                  onClick={() => sendMessage(chip.query)}
                >
                  {chip.label}
                </button>
              ))}
            </div>
          )}

          <form
            className="orsync-chat__composer"
            onSubmit={(e) => {
              e.preventDefault()
              sendMessage(input)
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Or-sync, demos, or book a call…"
              disabled={sending}
              aria-label="Message"
            />
            <button type="submit" disabled={sending || !input.trim()}>
              {sending ? '…' : 'Send'}
            </button>
          </form>
        </section>
      )}

      <button
        type="button"
        className={`orsync-chat__launcher ${open ? 'is-open' : ''}`}
        onClick={handleOpen}
        aria-expanded={open}
        aria-label={open ? 'Close Or-sync chat' : 'Open Or-sync chat'}
      >
        {open ? '×' : 'Chat'}
      </button>
    </div>
  )
}
