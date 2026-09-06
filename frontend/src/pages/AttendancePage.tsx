import React from "react";
import { Clock } from "lucide-react";
import { EmptyState } from "../components/common/EmptyState";

export const AttendancePage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100 tracking-tight">Attendance Records</h1>
        <p className="text-xs text-slate-400 mt-1">Daily verification sessions, first-seen/last-seen timestamps, and shift logs</p>
      </div>

      <EmptyState
        icon={Clock}
        title="No attendance records yet"
        description="Attendance computation engine and daily shift reconciliation begin in Phase 06. The database schema foundation is initialized."
        plannedPhase="Phase 06 (Attendance Core)"
      />
    </div>
  );
};
