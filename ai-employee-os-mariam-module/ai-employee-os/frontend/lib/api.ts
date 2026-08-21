const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(/(?:^|; )access_token=([^;]*)/);
  return match ? decodeURIComponent(match[1]) : null;
}

export function setToken(token: string) {
  // httpOnly cookies should be set server-side in production; this is a
  // client-readable cookie for local/dev wiring.
  document.cookie = `access_token=${token}; path=/; samesite=lax`;
}

export function clearToken() {
  document.cookie = "access_token=; path=/; max-age=0";
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export const api = {
  register: (data: { email: string; password: string; full_name: string; organization_name: string }) =>
    request<{ access_token: string; refresh_token: string }>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  login: (data: { email: string; password: string }) =>
    request<{ access_token: string; refresh_token: string; mfa_required: boolean }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  me: () => request<{ email: string; full_name: string; role: string }>("/api/auth/me"),

  usage: () =>
    request<{ plan_tier: string; ai_requests_used: number; ai_requests_limit: number | null; seats_used: number; seats_limit: number | null }>(
      "/api/pricing/usage"
    ),
};
