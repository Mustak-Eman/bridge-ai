const DEFAULT_API_BASE_URL = "http://localhost:8000/api/v1";

function normalizeApiBaseUrl(value: string): string {
  return value.replace(/\/+$/, "");
}

export const config = {
  apiBaseUrl: normalizeApiBaseUrl(
    process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL,
  ),
} as const;