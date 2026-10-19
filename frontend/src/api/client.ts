const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8010/api/v1'
).replace(/\/$/, '')

export type HealthResponse = { status: string; version?: string; [key: string]: unknown }

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...init?.headers },
    })
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        `Backend unavailable at ${API_BASE_URL}. Start FastAPI with ".venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8010".`,
      )
    }
    throw error
  }
  if (!response.ok) throw new Error(`API request failed (${response.status})`)
  return response.json() as Promise<T>
}

export async function checkHealth(): Promise<HealthResponse> {
  return apiRequest<HealthResponse>('/health')
}

export { API_BASE_URL }
