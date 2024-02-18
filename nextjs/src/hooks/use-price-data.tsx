import { Price } from "@/types/data";
import { useEffect, useRef, useState } from "react";

const usePriceData = (url: string, selectedCoin: string) => {
  const socketRef = useRef<WebSocket | null>(null);
  const [priceData, setPriceData] = useState<Price[]>([]);

  useEffect(() => {
    try {
      const connectSocket = () => {
        const socket = new WebSocket(url);
        socketRef.current = socket;

        socket.onopen = () => {
          console.log("WebSocket connection established.");
          if (selectedCoin) {
            socket.send(
              JSON.stringify({
                action: "select_coin",
                coin_symbol: selectedCoin,
              })
            );
          }
        };
      };

      if (
        !socketRef.current ||
        socketRef.current.readyState !== WebSocket.OPEN
      ) {
        // Create a new connection if no connection exists or it's not open

        connectSocket();
      } else if (selectedCoin) {
        // Send the selected coin event if the connection exists
        socketRef.current.send(
          JSON.stringify({
            action: "select_coin",
            coin_symbol: selectedCoin,
          })
        );
      }

      const handleMessage = (event: MessageEvent) => {
        const data = JSON.parse(event.data) as { prices: Price[] };
        const { prices } = data;
        setPriceData(prices);
      };

      const handleClose = () => {
        console.log("WebSocket connection closed.");
      };

      if (socketRef.current) {
        socketRef.current.onmessage = handleMessage;
        socketRef.current.onclose = handleClose;
      }

      return () => {
        if (socketRef.current) {
          socketRef.current.close();
        }
      };
    } catch (error) {
      console.log("Error establishing WebSocket connection: " + String(error));
    }
  }, [url, selectedCoin]);

  return priceData;
};

export default usePriceData;
