export type CameraSourceType = "WEBCAM" | "RTSP";

export type CameraStatus =
  | "ONLINE"
  | "CONNECTING"
  | "DEGRADED"
  | "OFFLINE"
  | "DISABLED"
  | "ERROR";

export interface Camera {
  id: number;
  name: string;
  location: string | null;
  source_type: CameraSourceType;
  device_index: number | null;
  rtsp_url: string | null;
  credential_ref: string | null;
  is_active: boolean;
  status: CameraStatus;
  target_fps: number;
  reconnect_delay: number;
  created_at?: string;
  updated_at?: string;
}

export interface CameraCreate {
  name: string;
  location?: string;
  source_type: CameraSourceType;
  device_index?: number | null;
  rtsp_url?: string | null;
  credential_ref?: string | null;
  target_fps?: number;
  reconnect_delay?: number;
}

export interface CameraUpdate {
  name?: string;
  location?: string;
  source_type?: CameraSourceType;
  device_index?: number | null;
  rtsp_url?: string | null;
  credential_ref?: string | null;
  is_active?: boolean;
  target_fps?: number;
  reconnect_delay?: number;
}

export interface CameraTelemetry {
  camera_id: number;
  camera_name: string;
  source_type: string;
  runtime_status: string;
  capture_fps: number;
  preview_fps: number;
  inference_fps: number | null;
  frames_decoded: number;
  frames_published: number;
  frames_dropped_or_replaced: number;
  last_frame_at: string | null;
  last_frame_age_ms: number | null;
  last_successful_open_at: string | null;
  last_error_at: string | null;
  safe_error_code: string | null;
  read_failures: number;
  reconnect_count: number;
  current_backoff_seconds: number;
  frame_width: number | null;
  frame_height: number | null;
  worker_running: boolean;
}

export interface CameraTestResult {
  success: boolean;
  source_type: string;
  elapsed_ms: number;
  camera_id?: number | null;
  frame_width?: number | null;
  frame_height?: number | null;
  safe_error_code?: string | null;
  message: string;
}

export interface CameraRuntimeEvent {
  event_id: string;
  event_type: string;
  timestamp: string;
  camera_id: number;
  camera_name: string;
  payload: Record<string, unknown>;
}
