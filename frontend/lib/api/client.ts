import { config } from "@/lib/config";
import type { ApiErrorResponse } from "@/types/api";

export class ApiError extends Error {
  readonly status: number;
  readonly details: ApiErrorResponse | null;

  constructor(
    message: string,
    status: number,
    details: ApiErrorResponse | null = null,
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

function buildUrl(path: string): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${config.apiBaseUrl}${normalizedPath}`;
}

function extractErrorMessage(
  payload: ApiErrorResponse | null,
  fallbackMessage: string,
): string {
  if (!payload) {
    return fallbackMessage;
  }

  if (typeof payload.detail === "string") {
    return payload.detail;
  }

  if (Array.isArray(payload.detail) && payload.detail.length > 0) {
    const messages = payload.detail
      .map((item) => item.msg)
      .filter((message): message is string => Boolean(message));

    if (messages.length > 0) {
      return messages.join(" ");
    }
  }

  return payload.message ?? payload.error ?? fallbackMessage;
}

async function parseJsonSafely<T>(response: Response): Promise<T | null> {
  const contentType = response.headers.get("content-type");

  if (!contentType?.includes("application/json")) {
    return null;
  }

  try {
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(buildUrl(path), {
      ...init,
      headers: {
        Accept: "application/json",
        ...init.headers,
      },
    });
  } catch {
    throw new ApiError(
      "Unable to connect to the Bridge AI API. Confirm that the backend is running and the API URL is configured correctly.",
      0,
    );
  }

  if (!response.ok) {
    const payload = await parseJsonSafely<ApiErrorResponse>(response);
    const fallbackMessage = `The request failed with status ${response.status}.`;

    throw new ApiError(
      extractErrorMessage(payload, fallbackMessage),
      response.status,
      payload,
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  const payload = await parseJsonSafely<T>(response);

  if (payload === null) {
    throw new ApiError(
      "The Bridge AI API returned an unexpected response.",
      response.status,
    );
  }

  return payload;
}