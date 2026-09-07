import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LivePage } from "../pages/LivePage";
import { CameraCard } from "../features/cameras/components/CameraCard";
import { CameraModal } from "../features/cameras/components/CameraModal";
import * as cameraApi from "../api/cameras";
import type { Camera, CameraTestResult, CameraTelemetry } from "../types/camera";

describe("Phase 02 Camera Features & Console", () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
    vi.restoreAllMocks();
  });

  const mockCameras: Camera[] = [
    {
      id: 1,
      name: "Reception Desk Webcam",
      location: "Building A Reception",
      source_type: "WEBCAM",
      device_index: 0,
      rtsp_url: null,
      credential_ref: null,
      is_active: true,
      status: "ONLINE",
      target_fps: 5,
      reconnect_delay: 5,
    },
    {
      id: 2,
      name: "Perimeter Gate RTSP",
      location: "East Gate",
      source_type: "RTSP",
      device_index: null,
      rtsp_url: "rtsp://192.168.1.120:554/live",
      credential_ref: "EAST_GATE_CAM",
      is_active: false,
      status: "DISABLED",
      target_fps: 5,
      reconnect_delay: 5,
    },
  ];

  const mockTelemetry: CameraTelemetry = {
    camera_id: 1,
    camera_name: "Reception Desk Webcam",
    source_type: "WEBCAM",
    runtime_status: "ONLINE",
    capture_fps: 14.8,
    preview_fps: 9.9,
    inference_fps: null, // Truthfully null in Phase 02
    frames_decoded: 152,
    frames_published: 98,
    frames_dropped_or_replaced: 54,
    last_frame_at: "2026-09-07T11:00:00Z",
    last_frame_age_ms: 85.0,
    last_successful_open_at: "2026-09-07T10:55:00Z",
    last_error_at: null,
    safe_error_code: null,
    read_failures: 0,
    reconnect_count: 0,
    current_backoff_seconds: 0.0,
    frame_width: 640,
    frame_height: 480,
    worker_running: true,
  };

  it("renders camera grid when configured cameras exist", async () => {
    vi.spyOn(cameraApi, "fetchCameras").mockResolvedValue(mockCameras);
    vi.spyOn(cameraApi, "fetchCameraTelemetry").mockResolvedValue(mockTelemetry);

    render(
      <QueryClientProvider client={queryClient}>
        <LivePage />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("Reception Desk Webcam")).toBeInTheDocument();
      expect(screen.getByText("Perimeter Gate RTSP")).toBeInTheDocument();
      expect(screen.getByText("ONLINE")).toBeInTheDocument();
      expect(screen.getByText("DISABLED")).toBeInTheDocument();
      expect(screen.getByText("Building A Reception")).toBeInTheDocument();
      expect(screen.getByText("East Gate")).toBeInTheDocument();
    });
  });

  it("renders CameraCard with truthful empty/waiting states without fake people or face boxes", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <CameraCard
          camera={mockCameras[1]} // Disabled/offline camera
          onEdit={vi.fn()}
          onDelete={vi.fn()}
        />
      </QueryClientProvider>
    );

    expect(screen.getByText("Perimeter Gate RTSP")).toBeInTheDocument();
    expect(screen.getByText("Camera unavailable")).toBeInTheDocument();
    expect(screen.queryByText(/face/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/confidence/i)).not.toBeInTheDocument();
  });

  it("executes connection probe and displays probe result", async () => {
    const probeResult: CameraTestResult = {
      success: true,
      source_type: "WEBCAM",
      elapsed_ms: 120.5,
      camera_id: 1,
      frame_width: 640,
      frame_height: 480,
      safe_error_code: null,
      message: "Probe succeeded",
    };
    const testSpy = vi.spyOn(cameraApi, "testCamera").mockResolvedValue(probeResult);

    render(
      <QueryClientProvider client={queryClient}>
        <CameraCard
          camera={mockCameras[0]}
          onEdit={vi.fn()}
          onDelete={vi.fn()}
        />
      </QueryClientProvider>
    );

    const testButton = screen.getByRole("button", { name: /Test connection for Reception Desk Webcam/i });
    fireEvent.click(testButton);

    await waitFor(() => {
      expect(testSpy).toHaveBeenCalledWith(1);
      expect(screen.getByText(/Probe OK \(120.5ms, 640x480\)/i)).toBeInTheDocument();
    });
  });

  it("renders Add Camera modal with webcam/RTSP toggle and credential reference explanation", () => {
    render(
      <CameraModal
        isOpen={true}
        camera={null}
        onClose={vi.fn()}
        onSubmit={vi.fn()}
      />
    );

    expect(screen.getByText("Add Camera Configuration")).toBeInTheDocument();
    expect(screen.getByText(/USB Webcam/i)).toBeInTheDocument();
    expect(screen.getByText(/RTSP Stream/i)).toBeInTheDocument();

    // Switch to RTSP mode
    fireEvent.click(screen.getByText(/RTSP Stream/i));
    expect(screen.getByLabelText(/RTSP Stream URL/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Credential Reference/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Camera credentials are resolved locally at runtime and are not stored in Presyn's database/i)
    ).toBeInTheDocument();
  });

  it("validates that RTSP URL does not contain inline credentials", async () => {
    const submitSpy = vi.fn();
    render(
      <CameraModal
        isOpen={true}
        camera={null}
        onClose={vi.fn()}
        onSubmit={submitSpy}
      />
    );

    // Fill camera name
    fireEvent.change(screen.getByLabelText(/Camera Name/i), { target: { value: "Gate Cam" } });

    // Switch to RTSP
    fireEvent.click(screen.getByText(/RTSP Stream/i));

    // Enter inline credentials
    fireEvent.change(screen.getByLabelText(/RTSP Stream URL/i), {
      target: { value: "rtsp://user:pass@192.168.1.50/live" },
    });

    fireEvent.click(screen.getByRole("button", { name: "Register Camera" }));

    await waitFor(() => {
      expect(screen.getByText(/RTSP URL must not contain embedded user credentials/i)).toBeInTheDocument();
      expect(submitSpy).not.toHaveBeenCalled();
    });
  });

  it("revokes Blob URLs to prevent memory leaks in preview hook", () => {
    const originalCreate = window.URL.createObjectURL;
    const originalRevoke = window.URL.revokeObjectURL;

    const mockCreate = vi.fn().mockReturnValue("blob:http://localhost/test-uuid");
    const mockRevoke = vi.fn();

    window.URL.createObjectURL = mockCreate;
    window.URL.revokeObjectURL = mockRevoke;

    try {
      const blob = new Blob(["fake-jpeg-bytes"], { type: "image/jpeg" });
      const url = window.URL.createObjectURL(blob);
      expect(mockCreate).toHaveBeenCalledWith(blob);

      window.URL.revokeObjectURL(url);
      expect(mockRevoke).toHaveBeenCalledWith("blob:http://localhost/test-uuid");
    } finally {
      window.URL.createObjectURL = originalCreate;
      window.URL.revokeObjectURL = originalRevoke;
    }
  });
});
