import type { HealthResponse, SystemMetadataResponse } from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

export class ApiError extends Error {
  public statusCode?: number;

  constructor(message: string, statusCode?: number) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
  }
}

export async function fetchHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE}/api/v1/health`, {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const detail = errorData?.detail || `HTTP ${response.status}: ${response.statusText}`;
      throw new ApiError(detail, response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError("Backend unavailable");
  }
}

export async function fetchSystemMetadata(): Promise<SystemMetadataResponse> {
  try {
    const response = await fetch(`${API_BASE}/api/v1/system`, {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const detail = errorData?.detail || `HTTP ${response.status}: ${response.statusText}`;
      throw new ApiError(detail, response.status);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError("Backend unavailable");
  }
}
