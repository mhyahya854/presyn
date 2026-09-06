import React from "react";
import { Shield } from "lucide-react";
import { EmptyState } from "../components/common/EmptyState";

export const SecurityPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100 tracking-tight">Security & Access Audits</h1>
        <p className="text-xs text-slate-400 mt-1">Unknown person detections, unauthorized zone breaches, and audit trails</p>
      </div>

      <EmptyState
        icon={Shield}
        title="No security events yet"
        description="Unknown person clustering, zone breach detection, and security alerting engines activate in Phase 07 and Phase 09."
        plannedPhase="Phase 07 (Visitors & Unknowns)"
      />
    </div>
  );
};
