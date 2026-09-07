import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Activity,
  Edit2,
  MapPin,
  Play,
  RefreshCw,
  Square,
  Trash2,
  Video,
  VideoOff,
} from "lucide-react";
import type { Camera, CameraStatus } from "../../../types/camera";
import { fetchCameraTelemetry, startCamera, stopCamera, testCamera } from "../../../api/cameras";
import { useCameraPreview } from "../hooks/useCameraPreview";

interface CameraCardProps {
  camera: Camera;
  onEdit: (camera: Camera) => void;
  onDelete: (camera: Camera) => void;
}

export const CameraCard: React.FC<CameraCardProps> = ({
  camera,
  onEdit,
  onDelete,
}) => {
  const queryClient = useQueryClient();
  const [testMessage, setTestMessage] = useState<string | null>(null);

  const { frameUrl } = useCameraPreview(
    camera.id,
    camera.is_active && (camera.status === "ONLINE" || camera.status === "DEGRADED")
  );

  const telemetryQuery = useQuery({
    queryKey: ["cameraTelemetry", camera.id],
    queryFn: () => fetchCameraTelemetry(camera.id),
    enabled: camera.is_active,
    refetchInterval: camera.is_active ? 3000 : false,
  });

  const startMutation = useMutation({
    mutationFn: () => startCamera(camera.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cameras"] });
      queryClient.invalidateQueries({ queryKey: ["cameraTelemetry", camera.id] });
      queryClient.invalidateQueries({ queryKey: ["systemHealth"] });
    },
  });

  const stopMutation = useMutation({
    mutationFn: () => stopCamera(camera.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cameras"] });
      queryClient.invalidateQueries({ queryKey: ["cameraTelemetry", camera.id] });
      queryClient.invalidateQueries({ queryKey: ["systemHealth"] });
    },
  });

  const testMutation = useMutation({
    mutationFn: () => testCamera(camera.id),
    onSuccess: (result) => {
      setTestMessage(
        result.success
          ? `Probe OK (${result.elapsed_ms}ms, ${result.frame_width}x${result.frame_height})`
          : `Probe failed: ${result.safe_error_code || "Error"}`
      );
      setTimeout(() => setTestMessage(null), 5000);
    },
    onError: () => {
      setTestMessage("Probe request failed");
      setTimeout(() => setTestMessage(null), 5000);
    },
  });

  const getStatusBadge = (status: CameraStatus) => {
    switch (status) {
      case "ONLINE":
        return "bg-emerald-950/40 text-emerald-400 border-emerald-800/50";
      case "CONNECTING":
        return "bg-amber-950/40 text-amber-400 border-amber-800/50";
      case "DEGRADED":
        return "bg-amber-950/40 text-amber-400 border-amber-800/50";
      case "ERROR":
        return "bg-red-950/40 text-red-400 border-red-800/50";
      case "DISABLED":
      case "OFFLINE":
      default:
        return "bg-slate-900 text-slate-400 border-slate-700";
    }
  };

  const isOperating = startMutation.isPending || stopMutation.isPending;
  const telemetry = telemetryQuery.data;

  return (
    <div className="panel p-4 flex flex-col justify-between space-y-3 bg-[#111726] border border-slate-800 rounded">
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div>
          <h2 className="text-sm font-semibold text-slate-100 tracking-tight">{camera.name}</h2>
          <div className="flex items-center gap-2 mt-0.5 text-xs text-slate-400">
            {camera.location && (
              <span className="flex items-center gap-1">
                <MapPin className="w-3 h-3 text-slate-500" />
                {camera.location}
              </span>
            )}
            <span className="font-mono text-[11px] text-slate-500 uppercase">
              {camera.source_type}
              {camera.source_type === "WEBCAM" && camera.device_index !== null && ` (#${camera.device_index})`}
            </span>
          </div>
        </div>
        <span className={`badge uppercase text-[10px] font-mono tracking-wider ${getStatusBadge(camera.status)}`}>
          {camera.status}
        </span>
      </div>

      {/* Video Preview Body */}
      <div className="relative w-full h-48 bg-slate-950 rounded border border-slate-800/80 overflow-hidden flex items-center justify-center">
        {frameUrl && (camera.status === "ONLINE" || camera.status === "DEGRADED") ? (
          <img
            src={frameUrl}
            alt={`Live feed for ${camera.name}`}
            className="w-full h-full object-cover"
          />
        ) : camera.status === "CONNECTING" ? (
          <div className="flex flex-col items-center justify-center text-amber-400 text-xs">
            <RefreshCw className="w-5 h-5 mb-2 animate-spin text-amber-500" />
            <span>Connecting</span>
          </div>
        ) : camera.status === "ONLINE" ? (
          <div className="flex flex-col items-center justify-center text-slate-400 text-xs">
            <Video className="w-5 h-5 mb-2 text-blue-500 animate-pulse" />
            <span>Waiting for camera feed</span>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center text-slate-500 text-xs">
            <VideoOff className="w-5 h-5 mb-2 text-slate-600" />
            <span>Camera unavailable</span>
          </div>
        )}

        {/* Live FPS Tag over frame if online */}
        {camera.status === "ONLINE" && telemetry && (
          <div className="absolute top-2 right-2 px-1.5 py-0.5 rounded bg-slate-900/80 border border-slate-700/60 font-mono text-[10px] text-slate-300">
            {telemetry.capture_fps.toFixed(1)} FPS
          </div>
        )}
      </div>

      {/* Real Ingestion Metrics */}
      <div className="grid grid-cols-2 gap-2 text-xs font-mono text-slate-400 pt-1 border-t border-slate-800/60">
        <div>
          <span className="text-[11px] text-slate-500">Capture: </span>
          <span className="text-slate-200">
            {telemetry ? `${telemetry.capture_fps.toFixed(1)} FPS` : "0.0 FPS"}
          </span>
        </div>
        <div>
          <span className="text-[11px] text-slate-500">Preview: </span>
          <span className="text-slate-200">
            {telemetry ? `${telemetry.preview_fps.toFixed(1)} FPS` : "0.0 FPS"}
          </span>
        </div>
        <div>
          <span className="text-[11px] text-slate-500">Decoded: </span>
          <span className="text-slate-200">{telemetry ? telemetry.frames_decoded : 0}</span>
        </div>
        <div>
          <span className="text-[11px] text-slate-500">Dropped: </span>
          <span className="text-slate-200">{telemetry ? telemetry.frames_dropped_or_replaced : 0}</span>
        </div>
      </div>

      {/* Probe Message Banner */}
      {testMessage && (
        <div className="p-2 rounded bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-300">
          {testMessage}
        </div>
      )}

      {/* Action Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 gap-2">
        <div className="flex items-center gap-1.5">
          {camera.is_active ? (
            <button
              onClick={() => stopMutation.mutate()}
              disabled={isOperating}
              className="btn-secondary px-2.5 py-1 text-xs space-x-1"
              title="Stop camera capture worker"
              aria-label={`Stop camera ${camera.name}`}
            >
              <Square className="w-3 h-3 text-red-400" />
              <span>Stop</span>
            </button>
          ) : (
            <button
              onClick={() => startMutation.mutate()}
              disabled={isOperating}
              className="btn-secondary px-2.5 py-1 text-xs space-x-1"
              title="Start camera capture worker"
              aria-label={`Start camera ${camera.name}`}
            >
              <Play className="w-3 h-3 text-emerald-400" />
              <span>Start</span>
            </button>
          )}

          <button
            onClick={() => testMutation.mutate()}
            disabled={testMutation.isPending}
            className="btn-secondary px-2.5 py-1 text-xs space-x-1"
            title="Probe camera connection"
            aria-label={`Test connection for ${camera.name}`}
          >
            <Activity className={`w-3 h-3 text-blue-400 ${testMutation.isPending ? "animate-spin" : ""}`} />
            <span>Test</span>
          </button>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={() => onEdit(camera)}
            className="p-1.5 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            title="Edit camera configuration"
            aria-label={`Edit ${camera.name}`}
          >
            <Edit2 className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onDelete(camera)}
            className="p-1.5 rounded text-slate-400 hover:text-red-400 hover:bg-slate-800 transition-colors"
            title="Delete camera configuration"
            aria-label={`Delete ${camera.name}`}
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
