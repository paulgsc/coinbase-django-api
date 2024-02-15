import { Price } from "@/types/data";
import { useEffect, useRef, useState } from "react";

const usePriceData = (url: string, selectedCoin: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const [priceData, setPriceData] = useState<Price[]>([]);

  useEffect(() => {
    try {
      const socket = new WebSocket(url);
      socketRef.current = socket;

      const handleOpen = () => {
        console.log("WebSocket connection established.");
        // Send the selected coin symbol when the WebSocket connection is established
        if (selectedCoin) {
          socket.send(
            JSON.stringify({
              action: "select_coin",
              coin_symbol: selectedCoin,
            })
          );
        }
      };

      const handleMessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data) as { prices: Price[] };
        const { prices } = data;
        setPriceData(prices);
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
