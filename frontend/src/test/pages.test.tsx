import { describe, it, expect, vi } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LivePage } from "../pages/LivePage";
import { AttendancePage } from "../pages/AttendancePage";
import { PeoplePage } from "../pages/PeoplePage";
import { SecurityPage } from "../pages/SecurityPage";
import { AnalyticsPage } from "../pages/AnalyticsPage";
import * as cameraApi from "../api/cameras";

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

describe("Truthful Empty States", () => {
  it("renders Live page with truthful zero-camera empty state", async () => {
    vi.spyOn(cameraApi, "fetchCameras").mockResolvedValue([]);
    render(
      <QueryClientProvider client={queryClient}>
        <LivePage />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText("No cameras configured")).toBeInTheDocument();
      expect(screen.getByText(/Configure a USB webcam or RTSP network stream/i)).toBeInTheDocument();
      expect(screen.getAllByRole("button", { name: /add camera/i }).length).toBeGreaterThanOrEqual(1);
    });
    expect(screen.queryByText(/fake/i)).not.toBeInTheDocument();
  });

  it("renders Attendance page with truthful empty state", () => {
    render(<AttendancePage />);
    expect(screen.getByText("No attendance records yet")).toBeInTheDocument();
    expect(screen.getByText(/Attendance computation engine/i)).toBeInTheDocument();
  });

  it("renders People page with truthful empty state", () => {
    render(<PeoplePage />);
    expect(screen.getByText("No employees enrolled")).toBeInTheDocument();
    expect(screen.getByText(/Employee registration and multi-angle face enrollment/i)).toBeInTheDocument();
  });

  it("renders Security page with truthful empty state", () => {
    render(<SecurityPage />);
    expect(screen.getByText("No security events yet")).toBeInTheDocument();
    expect(screen.getByText(/Unknown person clustering/i)).toBeInTheDocument();
  });

  it("renders Analytics page with truthful empty state", () => {
    render(<AnalyticsPage />);
    expect(screen.getByText("No analytics data yet")).toBeInTheDocument();
    expect(screen.getByText(/Aggregated occupancy analysis/i)).toBeInTheDocument();
  });
});
