import React from "react";
import { BarChart2 } from "lucide-react";
import { EmptyState } from "../components/common/EmptyState";

export const AnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100 tracking-tight">Spatial & Presence Analytics</h1>
        <p className="text-xs text-slate-400 mt-1">Occupancy trends, dwell time distributions, and department presence summaries</p>
      </div>

      <EmptyState
        icon={BarChart2}
        title="No analytics data yet"
        description="Aggregated occupancy analysis, zone heatmaps, and attendance metrics reporting activate in Phase 11. No synthetic charts are rendered."
        plannedPhase="Phase 11 (Analytics & Reporting)"
      />
    </div>
  );
};
