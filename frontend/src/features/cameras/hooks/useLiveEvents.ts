import { useEffect, useRef, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import type { CameraRuntimeEvent, CameraStatus } from "../../../types/camera";

export function useLiveEvents() {
  const queryClient = useQueryClient();
  const [lastEvent, setLastEvent] = useState<CameraRuntimeEvent | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryCountRef = useRef<number>(0);
  const isMountedRef = useRef<boolean>(true);

  useEffect(() => {
    isMountedRef.current = true;

    const connect = () => {
      if (!isMountedRef.current) return;

      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const host = window.location.host;
      const apiBase = import.meta.env.VITE_API_BASE_URL || "";
      let wsUrl: string;

      if (apiBase.startsWith("http://")) {
        wsUrl = `${apiBase.replace("http://", "ws://")}/api/v1/ws/live`;
      } else if (apiBase.startsWith("https://")) {
        wsUrl = `${apiBase.replace("https://", "wss://")}/api/v1/ws/live`;
      } else {
        wsUrl = `${protocol}//${host}/api/v1/ws/live`;
      }

      try {
        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
          if (!isMountedRef.current) return;
          setIsConnected(true);
          retryCountRef.current = 0;
        };

        ws.onmessage = (message) => {
          if (!isMountedRef.current) return;

          try {
            const data: CameraRuntimeEvent = JSON.parse(message.data);
            if (data.event_type && data.camera_id) {
              setLastEvent(data);

              // Update camera status in React Query cache if it's a camera lifecycle event
              if (data.event_type.startsWith("CAMERA_")) {
                const newStatus = data.event_type.replace("CAMERA_", "") as CameraStatus;
                queryClient.setQueryData(["cameras"], (old: any) => {
                  if (!Array.isArray(old)) return old;
                  return old.map((cam) =>
                    cam.id === data.camera_id ? { ...cam, status: newStatus } : cam
                  );
                });
                queryClient.invalidateQueries({ queryKey: ["cameraTelemetry", data.camera_id] });
                queryClient.invalidateQueries({ queryKey: ["systemHealth"] });
              }
            }
          } catch {
            // Ignore non-JSON or handshake messages
          }
        };

        ws.onclose = () => {
          if (!isMountedRef.current) return;
          setIsConnected(false);
          const delay = Math.min(1000 * Math.pow(2, retryCountRef.current), 15000);
          retryCountRef.current += 1;
          reconnectTimeoutRef.current = setTimeout(connect, delay);
        };

        ws.onerror = () => {
          try {
            ws.close();
          } catch {
            // Ignore error
          }
        };
      } catch {
        const delay = Math.min(1000 * Math.pow(2, retryCountRef.current), 15000);
        retryCountRef.current += 1;
        reconnectTimeoutRef.current = setTimeout(connect, delay);
      }
    };

    connect();

    return () => {
      isMountedRef.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [queryClient]);

  return { isConnected, lastEvent };
}
