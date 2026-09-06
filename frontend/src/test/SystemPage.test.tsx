import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { SystemPage } from "../pages/SystemPage";
import * as client from "../api/client";
import type { HealthResponse, SystemMetadataResponse } from "../types/api";

describe("SystemPage Telemetry & States", () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    vi.restoreAllMocks();
  });

  const mockHealth: HealthResponse = {
    status: "healthy",
    application: "Presyn API",
    version: "0.1.0",
    environment: "development",
    database: {
      status: "connected",
      probe_latency_ms: 1.25,
    },
    system: {
      cpu_utilization_percent: 18.5,
      memory_utilization_percent: 42.0,
      memory_total_bytes: 16000000000,
      memory_available_bytes: 9280000000,
    },
    uptime_seconds: 3600,
    timestamp: "2026-09-06T20:00:00Z",
  };

  const mockMetadata: SystemMetadataResponse = {
    application: "Presyn API",
    version: "0.1.0",
    environment: "development",
    architecture: {
      platform: "Windows",
      python_version: "3.10.20",
      cpu_architecture: "AMD64",
    },
    subsystems: {
      camera_ingestion: "not_implemented",
      face_detection: "not_implemented",
      recognition: "not_implemented",
      tracking: "not_implemented",
      zones: "not_implemented",
      attendance: "not_implemented",
    },
    timestamp: "2026-09-06T20:00:00Z",
  };

  it("renders live telemetry data upon successful API response", async () => {
    vi.spyOn(client, "fetchHealth").mockResolvedValue(mockHealth);
    vi.spyOn(client, "fetchSystemMetadata").mockResolvedValue(mockMetadata);

    render(
      <QueryClientProvider client={queryClient}>
        <SystemPage />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("healthy")).toBeInTheDocument();
      expect(screen.getByText(/18.5%/)).toBeInTheDocument();
      expect(screen.getByText(/42.0%/)).toBeInTheDocument();
      expect(screen.getByText("3.10.20")).toBeInTheDocument();
      expect(screen.getAllByText("not_implemented").length).toBeGreaterThan(0);
    });
  });

  it("renders truthful error state when backend is unavailable", async () => {
    vi.spyOn(client, "fetchHealth").mockRejectedValue(new Error("Backend unavailable"));
    vi.spyOn(client, "fetchSystemMetadata").mockRejectedValue(new Error("Backend unavailable"));

    render(
      <QueryClientProvider client={queryClient}>
        <SystemPage />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("Backend unavailable")).toBeInTheDocument();
      expect(screen.getByText(/Failed to communicate with FastAPI backend/i)).toBeInTheDocument();
    });
  });
});
