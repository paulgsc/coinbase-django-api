import { useWebSocket } from "@/context/ws-context";
import { useSearchParams } from "next/navigation";
import { useEffect } from "react";

const usePriceData = () => {
  const { webSocket, messages } = useWebSocket();
  const searchParams = useSearchParams();

  useEffect(() => {
    if (webSocket && webSocket.readyState === WebSocket.OPEN) {
      const selectedCoin = searchParams.get("coin");
      if (selectedCoin) {
        webSocket.send(
          JSON.stringify({
            action: "select_coin",
            coin_symbol: selectedCoin,
          })
        );
      }
    }
  }, [webSocket, searchParams]);

  return messages;
};

export default usePriceData;
