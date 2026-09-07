import { useEffect, useRef, useState } from "react";

export function useCameraPreview(cameraId: number, enabled: boolean = true) {
  const [frameUrl, setFrameUrl] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const activeBlobUrlRef = useRef<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryCountRef = useRef<number>(0);
  const isMountedRef = useRef<boolean>(true);

  useEffect(() => {
    isMountedRef.current = true;
    if (!enabled || !cameraId) {
      return;
    }

    const connect = () => {
      if (!isMountedRef.current) return;

      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      const host = window.location.host;
      const apiBase = import.meta.env.VITE_API_BASE_URL || "";
      let wsUrl: string;

      if (apiBase.startsWith("http://")) {
        wsUrl = `${apiBase.replace("http://", "ws://")}/api/v1/ws/cameras/${cameraId}/frames`;
      } else if (apiBase.startsWith("https://")) {
        wsUrl = `${apiBase.replace("https://", "wss://")}/api/v1/ws/cameras/${cameraId}/frames`;
      } else {
        wsUrl = `${protocol}//${host}/api/v1/ws/cameras/${cameraId}/frames`;
      }

      try {
        const ws = new WebSocket(wsUrl);
        ws.binaryType = "blob";
        wsRef.current = ws;

        ws.onopen = () => {
          if (!isMountedRef.current) return;
          setIsConnected(true);
          retryCountRef.current = 0;
        };

        ws.onmessage = (event) => {
          if (!isMountedRef.current) return;

          if (event.data instanceof Blob) {
            const newUrl = URL.createObjectURL(event.data);
            if (activeBlobUrlRef.current) {
              URL.revokeObjectURL(activeBlobUrlRef.current);
            }
            activeBlobUrlRef.current = newUrl;
            setFrameUrl(newUrl);
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
            // Ignore close error
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
      if (activeBlobUrlRef.current) {
        URL.revokeObjectURL(activeBlobUrlRef.current);
        activeBlobUrlRef.current = null;
      }
    };
  }, [cameraId, enabled]);

  return { frameUrl, isConnected };
}
