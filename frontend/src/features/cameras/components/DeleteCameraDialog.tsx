import React, { useState } from "react";
import { AlertTriangle, X } from "lucide-react";
import type { Camera } from "../../../types/camera";

interface DeleteCameraDialogProps {
  isOpen: boolean;
  camera: Camera | null;
  onClose: () => void;
  onConfirm: (camera: Camera) => Promise<void>;
}

export const DeleteCameraDialog: React.FC<DeleteCameraDialogProps> = ({
  isOpen,
  camera,
  onClose,
  onConfirm,
}) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen || !camera) return null;

  const handleConfirm = async () => {
    setError(null);
    try {
      setIsDeleting(true);
      await onConfirm(camera);
      onClose();
    } catch (err: any) {
      setError(err?.message || "Failed to delete camera.");
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="delete-camera-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
    >
      <div className="panel max-w-md w-full bg-[#111726] border border-red-900/40 rounded shadow-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2 text-red-400">
            <AlertTriangle className="w-5 h-5" />
            <h2 id="delete-camera-title" className="text-sm font-semibold text-slate-100">
              Delete Camera Configuration
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {error && (
          <div className="p-3 rounded bg-red-950/40 border border-red-900/60 text-xs text-red-300">
            {error}
          </div>
        )}

        <div className="space-y-3 text-xs text-slate-300 leading-relaxed">
          <p>
            Are you sure you want to delete <strong className="text-slate-100">{camera.name}</strong>?
          </p>
          <p className="text-slate-400">
            This stops its live connection and removes its Presyn camera record. It does not delete footage from an external NVR.
          </p>
        </div>

        <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
          <button
            type="button"
            onClick={onClose}
            className="btn-secondary px-3 py-1.5 text-xs"
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            className="inline-flex items-center justify-center px-3 py-1.5 text-xs font-medium text-white bg-red-600 hover:bg-red-700 rounded border border-red-500 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-500 disabled:opacity-50"
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Delete Camera"}
          </button>
        </div>
      </div>
    </div>
  );
};
