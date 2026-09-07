export interface DatabaseHealth {
  status: "connected" | "disconnected" | "error";
  probe_latency_ms: number | null;
  detail?: string;
}

export interface MachineTelemetry {
  cpu_utilization_percent: number;
  memory_utilization_percent: number;
  memory_total_bytes: number;
  memory_available_bytes: number;
}

export interface CameraSubsystemHealth {
  status: string;
  configured: number;
  running: number;
  online: number;
  degraded: number;
  offline: number;
}

export interface HealthResponse {
  status: "healthy" | "degraded" | "unhealthy";
  application: string;
  version: string;
  environment: string;
  database: DatabaseHealth;
  system: MachineTelemetry;
  uptime_seconds: number;
  timestamp: string;
  camera_subsystem?: CameraSubsystemHealth;
}

export interface ArchitectureInfo {
  platform: string;
  python_version: string;
  cpu_architecture: string;
}

export interface SubsystemStatus {
  camera_ingestion: string;
  face_detection: string;
  recognition: string;
  tracking: string;
  zones: string;
  attendance: string;
}

export interface SystemMetadataResponse {
  application: string;
  version: string;
  environment: string;
  architecture: ArchitectureInfo;
  subsystems: SubsystemStatus;
  timestamp: string;
}
