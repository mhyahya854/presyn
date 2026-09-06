import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { LivePage } from "../pages/LivePage";
import { AttendancePage } from "../pages/AttendancePage";
import { PeoplePage } from "../pages/PeoplePage";
import { SecurityPage } from "../pages/SecurityPage";
import { AnalyticsPage } from "../pages/AnalyticsPage";

describe("Phase 01 Truthful Empty States", () => {
  it("renders Live page with truthful empty state", () => {
    render(<LivePage />);
    expect(screen.getByText("Waiting for camera feed")).toBeInTheDocument();
    expect(screen.getByText(/RTSP and webcam stream ingestion/i)).toBeInTheDocument();
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
