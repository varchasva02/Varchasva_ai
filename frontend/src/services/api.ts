import type { AskResponse } from "../types/chat";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

const REQUEST_TIMEOUT_MS = 30_000;

class ApiError extends Error {
  statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
  }
}

/**
 * Send a question to the Varchasva AI backend and return the answer.
 */
export async function askVarchasva(question: string): Promise<string> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const response = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const message =
        errorData?.error || `Request failed with status ${response.status}`;
      throw new ApiError(message, response.status);
    }

    const data: AskResponse = await response.json();

    if (!data.answer || data.answer.trim().length === 0) {
      throw new ApiError("Received an empty response.");
    }

    return data.answer;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("Request timed out. Please try again.");
    }

    if (error instanceof TypeError) {
      // Network errors (backend unavailable, CORS, etc.)
      throw new ApiError(
        "Could not connect to the server. Please make sure the backend is running."
      );
    }

    throw new ApiError("Something went wrong. Please try again.");
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Check if the backend API is reachable.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/`, {
      method: "GET",
      signal: AbortSignal.timeout(5000),
    });
    const data = await response.json();
    return data.status === "online";
  } catch {
    return false;
  }
}
