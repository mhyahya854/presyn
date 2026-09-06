import React from "react";
import { Video } from "lucide-react";
import { EmptyState } from "../components/common/EmptyState";

export const LivePage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="border-b border-slate-800 pb-4">
        <h1 className="text-xl font-bold text-slate-100 tracking-tight">Live Ingestion & Monitoring</h1>
        <p className="text-xs text-slate-400 mt-1">Real-time camera feed processing and spatial inference pipeline</p>
      </div>

      <EmptyState
        icon={Video}
        title="Waiting for camera feed"
        description="RTSP and webcam stream ingestion infrastructure begins implementation in Phase 02. No synthetic or simulated camera streams are rendered."
        plannedPhase="Phase 02 (Camera Ingestion Engine)"
      />
    </div>
  );
};
