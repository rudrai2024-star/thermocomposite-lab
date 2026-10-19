const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8010/api/v1'
).replace(/\/$/, '')

export type HealthResponse = { status: string; version?: string; [key: string]: unknown }

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) throw new Error(`API request failed (${response.status})`)
  return response.json() as Promise<T>
}

export async function checkHealth(): Promise<HealthResponse> {
  return apiRequest<HealthResponse>('/health')
}

export { API_BASE_URL }
