import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppShell } from "./components/layout/AppShell";
import { LivePage } from "./pages/LivePage";
import { AttendancePage } from "./pages/AttendancePage";
import { PeoplePage } from "./pages/PeoplePage";
import { SecurityPage } from "./pages/SecurityPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { SystemPage } from "./pages/SystemPage";
import { PrivacyPage } from "./pages/PrivacyPage";
import { TermsPage } from "./pages/TermsPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5000,
    },
  },
});

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppShell />}>
            <Route index element={<Navigate to="/live" replace />} />
            <Route path="live" element={<LivePage />} />
            <Route path="attendance" element={<AttendancePage />} />
            <Route path="people" element={<PeoplePage />} />
            <Route path="security" element={<SecurityPage />} />
            <Route path="analytics" element={<AnalyticsPage />} />
            <Route path="system" element={<SystemPage />} />
            <Route path="privacy" element={<PrivacyPage />} />
            <Route path="terms" element={<TermsPage />} />
            <Route path="*" element={<Navigate to="/live" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
