"use client";

import { Price } from "@/types/data";
import React, { createContext, useContext, useEffect, useState } from "react";

interface WebSocketContextType {
  webSocket: WebSocket | null;
  messages: Price[];
}

type WebsockettProviderProps = {
  children: React.ReactNode;
};

const WebSocketContext = createContext<WebSocketContextType | null>(null);

export const useWebSocket = (): WebSocketContextType => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error("useWebSocket must be used within a WebSocketProvider");
  }
  return context;
};

export default function WebSocketProvider({
  children,
}: WebsockettProviderProps) {
  const [webSocket, setWebSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<Price[]>([]);

  useEffect(() => {
    const url = "ws://localhost:8000/ws/coinbase/prices";
    const socket = new WebSocket(url); // WebSocket server address

    socket.onopen = () => {
      console.log("WebSocket connection established.");
    };

    socket.onmessage = (event: MessageEvent) => {
      const data = JSON.parse(event.data) as { prices: Price[] };
      const { prices } = data;
      setMessages(prices); // Update messages state with prices
    };

    socket.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    setWebSocket(socket);

    return () => {
      socket.close();
    };
  }, []);

  const contextValue: WebSocketContextType = { webSocket, messages };

  return (
    <WebSocketContext.Provider value={contextValue}>
      {children}
    </WebSocketContext.Provider>
  );
}
