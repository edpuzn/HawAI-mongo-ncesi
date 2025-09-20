export class RateLimitError extends Error {}

const API_URL = import.meta.env.VITE_API_URL
const API_KEY = import.meta.env.VITE_API_KEY

if (!API_URL) throw new Error('VITE_API_URL tanımlı değil (.env)')
if (!API_KEY) console.warn('VITE_API_KEY tanımlı değil; X-API-Key header gönderilmeyecek')

async function request(path: string, opts: RequestInit = {}) {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(API_KEY ? { 'X-API-Key': API_KEY } : {}),
    ...(opts.headers || {})
  }
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 20000)
  try {
    const res = await fetch(`${API_URL}${path}`, { ...opts, headers, signal: controller.signal })
    if (res.status === 429) {
      throw new RateLimitError('Rate limit')
    }
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      return { ok: false, error: data?.detail || 'Hata', status: res.status }
    }
    return { ok: true, data }
  } catch (e: any) {
    if (e instanceof RateLimitError) {
      return { ok: false, rateLimited: true }
    }
    if (e?.name === 'AbortError') {
      return { ok: false, error: 'Zaman aşımı' }
    }
    return { ok: false, error: e?.message || 'Ağ hatası' }
  } finally {
    clearTimeout(timeout)
  }
}

export async function chat(message: string) {
  return request('/chat', { method: 'POST', body: JSON.stringify({ message }) })
}

export async function health() {
  return request('/healthz')
}
