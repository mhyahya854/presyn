import React from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Activity,
  Cpu,
  Database,
  HardDrive,
  RefreshCw,
  Server,
  AlertTriangle,
  CheckCircle2,
  XCircle,
} from "lucide-react";
import { fetchHealth, fetchSystemMetadata } from "../api/client";

export const SystemPage: React.FC = () => {
  const healthQuery = useQuery({
    queryKey: ["systemHealth"],
    queryFn: fetchHealth,
    refetchInterval: 10000,
  });

  const metadataQuery = useQuery({
    queryKey: ["systemMetadata"],
    queryFn: fetchSystemMetadata,
  });

  const isError = healthQuery.isError || metadataQuery.isError;
  const isLoading = (healthQuery.isLoading || metadataQuery.isLoading) && !isError;

  const handleRefresh = () => {
    healthQuery.refetch();
    metadataQuery.refetch();
  };

  const formatBytes = (bytes: number) => {
    const gb = bytes / (1024 * 1024 * 1024);
    return `${gb.toFixed(1)} GB`;
  };

  const formatUptime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hrs}h ${mins}m ${secs}s`;
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 tracking-tight">System Telemetry & Architecture</h1>
          <p className="text-xs text-slate-400 mt-1">Live process metrics, database connectivity, and subsystem status</p>
        </div>
        <button
          onClick={handleRefresh}
          className="btn-secondary self-start sm:self-auto space-x-2"
          aria-label="Refresh telemetry data"
          disabled={isLoading}
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
          <span>Refresh</span>
        </button>
      </div>

      {isLoading && !healthQuery.data && (
        <div className="panel flex items-center justify-center p-12 text-slate-400 text-sm">
          <RefreshCw className="w-5 h-5 animate-spin mr-3 text-blue-500" />
          <span>Querying backend telemetry...</span>
        </div>
      )}

      {isError && (
        <div className="panel border-red-900/50 bg-red-950/20 p-6 rounded text-slate-200">
          <div className="flex items-start space-x-3">
            <XCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
            <div>
              <h2 className="text-sm font-semibold text-red-400">Backend unavailable</h2>
              <p className="text-xs text-slate-400 mt-1">
                Failed to communicate with FastAPI backend. Ensure the Presyn backend server is running on port 8000.
              </p>
            </div>
          </div>
        </div>
      )}

      {healthQuery.data && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Status Card */}
          <div className="panel p-4 flex items-center space-x-3">
            <div className="p-2.5 rounded bg-slate-900 border border-slate-800 shrink-0">
              {healthQuery.data.status === "healthy" ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-500" />
              ) : (
                <AlertTriangle className="w-5 h-5 text-amber-500" />
              )}
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Core API Status</p>
              <p className="text-sm font-semibold uppercase text-slate-100 tracking-wide mt-0.5">
                {healthQuery.data.status}
              </p>
            </div>
          </div>

          {/* Database Card */}
          <div className="panel p-4 flex items-center space-x-3">
            <div className="p-2.5 rounded bg-slate-900 border border-slate-800 shrink-0">
              <Database className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">SQLite Database</p>
              <p className="text-sm font-semibold text-slate-100 mt-0.5 capitalize">
                {healthQuery.data.database.status}
                {healthQuery.data.database.probe_latency_ms !== null && (
                  <span className="text-xs text-slate-400 font-normal ml-1.5 font-mono">
                    ({healthQuery.data.database.probe_latency_ms.toFixed(1)}ms)
                  </span>
                )}
              </p>
            </div>
          </div>

          {/* CPU Card */}
          <div className="panel p-4 flex items-center space-x-3">
            <div className="p-2.5 rounded bg-slate-900 border border-slate-800 shrink-0">
              <Cpu className="w-5 h-5 text-amber-500" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Host CPU Utilization</p>
              <p className="text-sm font-semibold text-slate-100 font-mono mt-0.5">
                {healthQuery.data.system.cpu_utilization_percent.toFixed(1)}%
              </p>
            </div>
          </div>

          {/* Memory Card */}
          <div className="panel p-4 flex items-center space-x-3">
            <div className="p-2.5 rounded bg-slate-900 border border-slate-800 shrink-0">
              <HardDrive className="w-5 h-5 text-indigo-400" />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-medium">Host Memory Usage</p>
              <p className="text-sm font-semibold text-slate-100 font-mono mt-0.5">
                {healthQuery.data.system.memory_utilization_percent.toFixed(1)}%
                <span className="text-xs text-slate-400 font-normal ml-1">
                  ({formatBytes(healthQuery.data.system.memory_available_bytes)} free)
                </span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Metadata & Subsystem Grids */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Runtime Environment */}
        <div className="panel space-y-4">
          <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
            <Server className="w-4 h-4 text-blue-500" />
            <h2 className="text-sm font-semibold text-slate-200">Runtime Environment</h2>
          </div>
          {metadataQuery.data ? (
            <dl className="grid grid-cols-2 gap-y-3 gap-x-4 text-xs">
              <div>
                <dt className="text-slate-400">Application</dt>
                <dd className="font-mono text-slate-200 mt-0.5">{metadataQuery.data.application}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Version</dt>
                <dd className="font-mono text-slate-200 mt-0.5">{metadataQuery.data.version}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Environment</dt>
                <dd className="font-mono text-slate-200 mt-0.5">{metadataQuery.data.environment}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Python Runtime</dt>
                <dd className="font-mono text-slate-200 mt-0.5">{metadataQuery.data.architecture.python_version}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Platform OS</dt>
                <dd className="font-mono text-slate-200 mt-0.5">{metadataQuery.data.architecture.platform}</dd>
              </div>
              <div>
                <dt className="text-slate-400">Process Uptime</dt>
                <dd className="font-mono text-slate-200 mt-0.5">
                  {healthQuery.data ? formatUptime(healthQuery.data.uptime_seconds) : "Unknown"}
                </dd>
              </div>
            </dl>
          ) : (
            <p className="text-xs text-slate-400">Runtime telemetry pending backend response.</p>
          )}
        </div>

        {/* Planned Subsystems Inventory */}
        <div className="panel space-y-4">
          <div className="flex items-center space-x-2 border-b border-slate-800 pb-3">
            <Activity className="w-4 h-4 text-slate-400" />
            <h2 className="text-sm font-semibold text-slate-200">Planned Subsystem Status</h2>
          </div>
          {metadataQuery.data ? (
            <div className="space-y-2.5">
              {Object.entries(metadataQuery.data.subsystems).map(([name, status]) => (
                <div
                  key={name}
                  className="flex items-center justify-between p-2 rounded bg-slate-900/60 border border-slate-800 text-xs"
                >
                  <span className="font-mono text-slate-300 capitalize">
                    {name.replace(/_/g, " ")}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[11px] font-mono bg-slate-800 text-slate-400 border border-slate-700">
                    {status}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-xs text-slate-400">Subsystem status pending backend response.</p>
          )}
        </div>
      </div>
    </div>
  );
};
