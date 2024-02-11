import { Price } from "@/types/data";
import { useEffect, useRef, useState } from "react";

const usePriceData = (url: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const [priceData, setPriceData] = useState<Price[]>([]);

  useEffect(() => {
    console.log("url: ", url);
    try {
      const socket = new WebSocket(url);
      socketRef.current = socket;
      console.log("this part ran socket: ", socket);
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
    } catch (error) {
      console.log("Error establishing WebSocket connection: " + String(error));
    }
  }, [url]);

  return priceData;
};

export default usePriceData;
