import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Plus, RefreshCw, Video } from "lucide-react";
import type { Camera, CameraCreate } from "../types/camera";
import { createCamera, deleteCamera, fetchCameras, updateCamera } from "../api/cameras";
import { CameraCard } from "../features/cameras/components/CameraCard";
import { CameraModal } from "../features/cameras/components/CameraModal";
import { DeleteCameraDialog } from "../features/cameras/components/DeleteCameraDialog";
import { useLiveEvents } from "../features/cameras/hooks/useLiveEvents";

export const LivePage: React.FC = () => {
  const queryClient = useQueryClient();
  useLiveEvents(); // Connect global WebSocket for dynamic state sync

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCamera, setEditingCamera] = useState<Camera | null>(null);
  const [deletingCamera, setDeletingCamera] = useState<Camera | null>(null);

  const camerasQuery = useQuery({
    queryKey: ["cameras"],
    queryFn: fetchCameras,
  });

  const createMutation = useMutation({
    mutationFn: (payload: CameraCreate) => {
      if (editingCamera) {
        return updateCamera(editingCamera.id, payload);
      }
      return createCamera(payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cameras"] });
      queryClient.invalidateQueries({ queryKey: ["systemHealth"] });
      setIsModalOpen(false);
      setEditingCamera(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (camera: Camera) => deleteCamera(camera.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cameras"] });
      queryClient.invalidateQueries({ queryKey: ["systemHealth"] });
      setDeletingCamera(null);
    },
  });

  const handleOpenAdd = () => {
    setEditingCamera(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (camera: Camera) => {
    setEditingCamera(camera);
    setIsModalOpen(true);
  };

  const handleOpenDelete = (camera: Camera) => {
    setDeletingCamera(camera);
  };

  const cameras = camerasQuery.data || [];
  const isLoading = camerasQuery.isLoading;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 tracking-tight">Live Ingestion & Monitoring</h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time camera feed processing and spatial inference pipeline
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => camerasQuery.refetch()}
            disabled={isLoading}
            className="btn-secondary space-x-1.5"
            aria-label="Refresh camera list"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
          <button
            onClick={handleOpenAdd}
            className="btn-primary space-x-1.5"
            aria-label="Add camera"
          >
            <Plus className="w-4 h-4" />
            <span>Add camera</span>
          </button>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="panel flex items-center justify-center p-12 text-slate-400 text-sm">
          <RefreshCw className="w-5 h-5 animate-spin mr-3 text-blue-500" />
          <span>Loading configured cameras...</span>
        </div>
      )}

      {/* Empty State when zero cameras configured */}
      {!isLoading && cameras.length === 0 && (
        <div className="panel flex flex-col items-center justify-center p-12 text-center max-w-lg mx-auto space-y-4">
          <div className="p-3 rounded bg-slate-900 border border-slate-800 text-slate-400">
            <Video className="w-8 h-8" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-slate-100">No cameras configured</h2>
            <p className="text-xs text-slate-400 mt-1.5 max-w-sm">
              Configure a USB webcam or RTSP network stream to begin live ingestion and spatial processing.
            </p>
          </div>
          <button
            onClick={handleOpenAdd}
            className="btn-primary space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Add camera</span>
          </button>
        </div>
      )}

      {/* Camera Grid when cameras exist */}
      {!isLoading && cameras.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {cameras.map((camera) => (
            <CameraCard
              key={camera.id}
              camera={camera}
              onEdit={handleOpenEdit}
              onDelete={handleOpenDelete}
            />
          ))}
        </div>
      )}

      {/* Modals */}
      <CameraModal
        isOpen={isModalOpen}
        camera={editingCamera}
        onClose={() => {
          setIsModalOpen(false);
          setEditingCamera(null);
        }}
        onSubmit={async (payload) => {
          await createMutation.mutateAsync(payload);
        }}
      />

      <DeleteCameraDialog
        isOpen={deletingCamera !== null}
        camera={deletingCamera}
        onClose={() => setDeletingCamera(null)}
        onConfirm={async (cam) => {
          await deleteMutation.mutateAsync(cam);
        }}
      />
    </div>
  );
};
