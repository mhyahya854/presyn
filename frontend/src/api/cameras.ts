import type {
  Camera,
  CameraCreate,
  CameraTestResult,
  CameraTelemetry,
  CameraUpdate,
} from "../types/camera";
import { ApiError } from "./client";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

export async function fetchCameras(): Promise<Camera[]> {
  const res = await fetch(`${API_BASE}/api/v1/cameras`, {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
  return await res.json();
}

export async function fetchCamera(id: number): Promise<Camera> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}`, {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
  return await res.json();
}

export async function createCamera(payload: CameraCreate): Promise<Camera> {
  const res = await fetch(`${API_BASE}/api/v1/cameras`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    const detail = errorData?.detail;
    let message = `HTTP ${res.status}: ${res.statusText}`;
    if (typeof detail === "string") {
      message = detail;
    } else if (Array.isArray(detail)) {
      message = detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
    } else if (detail?.message) {
      message = detail.message;
    }
    throw new ApiError(message, res.status);
  }
  return await res.json();
}

export async function updateCamera(id: number, payload: CameraUpdate): Promise<Camera> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    const detail = errorData?.detail;
    let message = `HTTP ${res.status}: ${res.statusText}`;
    if (typeof detail === "string") {
      message = detail;
    } else if (Array.isArray(detail)) {
      message = detail.map((d) => d.msg || JSON.stringify(d)).join("; ");
    } else if (detail?.message) {
      message = detail.message;
    }
    throw new ApiError(message, res.status);
  }
  return await res.json();
}

export async function deleteCamera(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
}

export async function testCamera(id: number): Promise<CameraTestResult> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}/test`, {
    method: "POST",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
  return await res.json();
}

export async function startCamera(id: number): Promise<Camera> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}/start`, {
    method: "POST",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
  return await res.json();
}

export async function stopCamera(id: number): Promise<Camera> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}/stop`, {
    method: "POST",
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
  return await res.json();
}

export async function fetchCameraTelemetry(id: number): Promise<CameraTelemetry> {
  const res = await fetch(`${API_BASE}/api/v1/cameras/${id}/telemetry`, {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    throw new ApiError(errorData?.detail?.message || `HTTP ${res.status}: ${res.statusText}`, res.status);
  }
  return await res.json();
}
