import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import App from "../App";

describe("Application Shell and Navigation", () => {
  it("renders the application and defaults to Live page", async () => {
    render(<App />);
    expect(screen.getByText("PRESYN")).toBeInTheDocument();
    expect(screen.getByText("Waiting for camera feed")).toBeInTheDocument();
  });

  it("navigates across product areas", async () => {
    render(<App />);

    // Click on Attendance nav link
    const attendanceLinks = screen.getAllByRole("link", { name: /attendance/i });
    fireEvent.click(attendanceLinks[0]);
    expect(screen.getByText("No attendance records yet")).toBeInTheDocument();

    // Click on People nav link
    const peopleLinks = screen.getAllByRole("link", { name: /people/i });
    fireEvent.click(peopleLinks[0]);
    expect(screen.getByText("No employees enrolled")).toBeInTheDocument();

    // Click on Security nav link
    const securityLinks = screen.getAllByRole("link", { name: /security/i });
    fireEvent.click(securityLinks[0]);
    expect(screen.getByText("No security events yet")).toBeInTheDocument();

    // Click on Analytics nav link
    const analyticsLinks = screen.getAllByRole("link", { name: /analytics/i });
    fireEvent.click(analyticsLinks[0]);
    expect(screen.getByText("No analytics data yet")).toBeInTheDocument();
  });

  it("navigates to Privacy Policy via footer link", async () => {
    render(<App />);
    const privacyLink = screen.getByRole("link", { name: /privacy policy/i });
    fireEvent.click(privacyLink);
    expect(screen.getByText("Presyn Privacy Policy")).toBeInTheDocument();
    expect(screen.getByText("PRESYN-DESIGN-010")).toBeInTheDocument();
  });

  it("navigates to Terms & Conditions via footer link", async () => {
    render(<App />);
    const termsLink = screen.getByRole("link", { name: /terms & conditions/i });
    fireEvent.click(termsLink);
    expect(screen.getByText("Presyn Terms & Conditions")).toBeInTheDocument();
    expect(screen.getByText("PRESYN-DESIGN-011")).toBeInTheDocument();
  });

  it("strictly prohibits 'Made with AI' and 'Powered by AI' badges", () => {
    const { container } = render(<App />);
    const textContent = container.textContent || "";
    expect(textContent).not.toContain("Made with AI");
    expect(textContent).not.toContain("Powered by AI");
  });
});
