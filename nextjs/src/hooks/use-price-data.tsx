import { Price } from "@/app/types/data";
import { useEffect, useRef, useState } from "react";

const usePriceData = (url: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const [priceData, setPriceData] = useState<Price[]>([]);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    const handleOpen = () => {
      console.log("WebSocket connection established.");
    };

    const handleMessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data) as Price[];
      setPriceData(data);
    };

    const handleClose = () => {
      console.log("WebSocket connection closed.");
    };

    socket.onopen = handleOpen;
    socket.onmessage = handleMessage;
    socket.onclose = handleClose;

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [url]);

  return priceData;
};

export default usePriceData;
