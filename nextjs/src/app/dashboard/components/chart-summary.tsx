import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useWebSocket } from "@/context/ws-context";
import { Price } from "@/types/data";
import React from "react";

const ChartSummary = () => {
  const { messages } = useWebSocket();
  // Define the default Price object with default values for each property
  const defaultPrice: Price = {
    amount: "0",
    base: "",
    currency: "",
    timestamp: 0,
    symbol: "",
    full_name: "",
  };

  // Ensure latestPrice is of type Price and provide a default value
  const latestPrice: Price =
    messages.length > 0 ? messages[messages.length - 1] : defaultPrice;
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium uppercase">
          {latestPrice.full_name}
        </CardTitle>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="2"
          className="h-4 w-4 text-muted-foreground"
        >
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        </svg>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{latestPrice.amount}</div>
        <p className="text-xs text-muted-foreground">+20.1% from last month</p>
      </CardContent>
    </Card>
  );
};

export default ChartSummary;
