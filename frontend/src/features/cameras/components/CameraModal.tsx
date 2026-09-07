import React, { useState, useEffect } from "react";
import { X, ShieldAlert } from "lucide-react";
import type { Camera, CameraCreate, CameraSourceType } from "../../../types/camera";

interface CameraModalProps {
  isOpen: boolean;
  camera: Camera | null; // Null if adding, non-null if editing
  onClose: () => void;
  onSubmit: (data: CameraCreate) => Promise<void>;
}

export const CameraModal: React.FC<CameraModalProps> = ({
  isOpen,
  camera,
  onClose,
  onSubmit,
}) => {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [sourceType, setSourceType] = useState<CameraSourceType>("WEBCAM");
  const [deviceIndex, setDeviceIndex] = useState<number>(0);
  const [rtspUrl, setRtspUrl] = useState("");
  const [credentialRef, setCredentialRef] = useState("");
  const [targetFps, setTargetFps] = useState<number>(5);
  const [reconnectDelay, setReconnectDelay] = useState<number>(5);

  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (camera) {
      setName(camera.name);
      setLocation(camera.location || "");
      setSourceType(camera.source_type);
      setDeviceIndex(camera.device_index ?? 0);
      setRtspUrl(camera.rtsp_url || "");
      setCredentialRef(camera.credential_ref || "");
      setTargetFps(camera.target_fps);
      setReconnectDelay(camera.reconnect_delay);
    } else {
      setName("");
      setLocation("");
      setSourceType("WEBCAM");
      setDeviceIndex(0);
      setRtspUrl("");
      setCredentialRef("");
      setTargetFps(5);
      setReconnectDelay(5);
    }
    setError(null);
  }, [camera, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!name.trim()) {
      setError("Camera name is required.");
      return;
    }

    if (sourceType === "WEBCAM") {
      if (deviceIndex < 0 || isNaN(deviceIndex)) {
        setError("Valid USB device index is required (e.g. 0).");
        return;
      }
    } else if (sourceType === "RTSP") {
      if (!rtspUrl.trim()) {
        setError("RTSP stream URL is required.");
        return;
      }
      if (rtspUrl.includes("@")) {
        setError("RTSP URL must not contain embedded user credentials. Use credential reference instead.");
        return;
      }
      if (credentialRef.trim() && !/^[A-Z0-9_]+$/.test(credentialRef.trim())) {
        setError("Credential reference must contain only uppercase alphanumeric characters and underscores.");
        return;
      }
    }

    const payload: CameraCreate = {
      name: name.trim(),
      location: location.trim() || undefined,
      source_type: sourceType,
      device_index: sourceType === "WEBCAM" ? Number(deviceIndex) : null,
      rtsp_url: sourceType === "RTSP" ? rtspUrl.trim() : null,
      credential_ref: sourceType === "RTSP" && credentialRef.trim() ? credentialRef.trim().toUpperCase() : null,
      target_fps: Number(targetFps),
      reconnect_delay: Number(reconnectDelay),
    };

    try {
      setIsSubmitting(true);
      await onSubmit(payload);
      onClose();
    } catch (err: any) {
      setError(err?.message || "Failed to save camera configuration.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="camera-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
    >
      <div className="panel max-w-lg w-full bg-[#111726] border border-slate-800 rounded shadow-xl space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h2 id="camera-modal-title" className="text-base font-semibold text-slate-100">
            {camera ? "Edit Camera Configuration" : "Add Camera Configuration"}
          </h2>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {error && (
          <div className="p-3 rounded bg-red-950/40 border border-red-900/60 text-xs text-red-300 flex items-start gap-2">
            <ShieldAlert className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {/* Camera Name */}
          <div>
            <label htmlFor="cam-name" className="block text-slate-300 font-medium mb-1">
              Camera Name <span className="text-red-400">*</span>
            </label>
            <input
              id="cam-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Main Entrance Gate"
              className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-500"
              required
            />
          </div>

          {/* Physical Location */}
          <div>
            <label htmlFor="cam-location" className="block text-slate-300 font-medium mb-1">
              Location (Optional)
            </label>
            <input
              id="cam-location"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Building A, 1st Floor Reception"
              className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          {/* Source Type Selection */}
          <div>
            <label className="block text-slate-300 font-medium mb-1">Source Type</label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setSourceType("WEBCAM")}
                className={`py-2 px-3 rounded border text-center font-medium transition-colors ${
                  sourceType === "WEBCAM"
                    ? "bg-blue-950/50 border-blue-600 text-blue-300"
                    : "bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-850"
                }`}
              >
                USB Webcam (DirectShow / V4L2)
              </button>
              <button
                type="button"
                onClick={() => setSourceType("RTSP")}
                className={`py-2 px-3 rounded border text-center font-medium transition-colors ${
                  sourceType === "RTSP"
                    ? "bg-blue-950/50 border-blue-600 text-blue-300"
                    : "bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-850"
                }`}
              >
                RTSP Stream (IP Camera)
              </button>
            </div>
          </div>

          {/* Conditional WEBCAM Field */}
          {sourceType === "WEBCAM" && (
            <div>
              <label htmlFor="cam-device-index" className="block text-slate-300 font-medium mb-1">
                Device Index <span className="text-red-400">*</span>
              </label>
              <input
                id="cam-device-index"
                type="number"
                min="0"
                max="16"
                value={deviceIndex}
                onChange={(e) => setDeviceIndex(parseInt(e.target.value, 10))}
                className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono"
                required
              />
              <p className="text-[11px] text-slate-500 mt-1">
                System camera device index (0 is typically the default built-in or primary USB camera).
              </p>
            </div>
          )}

          {/* Conditional RTSP Fields */}
          {sourceType === "RTSP" && (
            <div className="space-y-3">
              <div>
                <label htmlFor="cam-rtsp-url" className="block text-slate-300 font-medium mb-1">
                  RTSP Stream URL <span className="text-red-400">*</span>
                </label>
                <input
                  id="cam-rtsp-url"
                  type="text"
                  value={rtspUrl}
                  onChange={(e) => setRtspUrl(e.target.value)}
                  placeholder="rtsp://192.168.1.100:554/live/ch0"
                  className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono"
                  required
                />
                <p className="text-[11px] text-slate-500 mt-1">
                  Credential-free RTSP address. Do not embed user credentials or sensitive tokens in the URL.
                </p>
              </div>

              <div>
                <label htmlFor="cam-credential-ref" className="block text-slate-300 font-medium mb-1">
                  Credential Reference (Optional)
                </label>
                <input
                  id="cam-credential-ref"
                  type="text"
                  value={credentialRef}
                  onChange={(e) => setCredentialRef(e.target.value.toUpperCase())}
                  placeholder="e.g. MAIN_GATE_CAM"
                  className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 focus:outline-none focus:ring-1 focus:ring-blue-500 font-mono uppercase"
                />
                <div className="p-2.5 rounded bg-slate-900/60 border border-slate-800 text-[11px] text-slate-400 mt-1.5 leading-relaxed">
                  Camera credentials are resolved locally at runtime and are not stored in Presyn's database. Set{" "}
                  <code className="text-slate-300 font-mono">PRESYN_CAMERA_[REF]_USERNAME</code> and{" "}
                  <code className="text-slate-300 font-mono">PRESYN_CAMERA_[REF]_PASSWORD</code> in the local environment.
                </div>
              </div>
            </div>
          )}

          {/* Target FPS & Reconnect */}
          <div className="grid grid-cols-2 gap-3 pt-1 border-t border-slate-800/60">
            <div>
              <label htmlFor="cam-target-fps" className="block text-slate-400 font-medium mb-1">
                Target Processing FPS
              </label>
              <input
                id="cam-target-fps"
                type="number"
                min="1"
                max="30"
                value={targetFps}
                onChange={(e) => setTargetFps(parseInt(e.target.value, 10))}
                className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 font-mono"
              />
            </div>
            <div>
              <label htmlFor="cam-reconnect-delay" className="block text-slate-400 font-medium mb-1">
                Initial Reconnect (sec)
              </label>
              <input
                id="cam-reconnect-delay"
                type="number"
                min="1"
                max="60"
                value={reconnectDelay}
                onChange={(e) => setReconnectDelay(parseInt(e.target.value, 10))}
                className="w-full px-3 py-2 rounded bg-slate-900 border border-slate-700 text-slate-100 font-mono"
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary px-4 py-2"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn-primary px-4 py-2"
              disabled={isSubmitting}
            >
              {isSubmitting ? "Saving..." : camera ? "Save Changes" : "Register Camera"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
