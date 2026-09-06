import React from "react";
import { Users } from "lucide-react";
import { EmptyState } from "../components/common/EmptyState";

export const PeoplePage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100 tracking-tight">Personnel Directory</h1>
        <p className="text-xs text-slate-400 mt-1">Employee identities, biometric enrollment profiles, and department associations</p>
      </div>

      <EmptyState
        icon={Users}
        title="No employees enrolled"
        description="Employee registration and multi-angle face enrollment pipeline begin implementation in Phase 05. Demo accounts are strictly prohibited."
        plannedPhase="Phase 05 (Enrollment & Recognition)"
      />
    </div>
  );
};
