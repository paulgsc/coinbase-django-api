"use client";

import usePriceData from "@/hooks/use-price-data";
import { Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

export function Overview() {
  const socketUrl = "ws://localhost:8000/ws/coinbase/prices";

  const priceData = usePriceData(socketUrl, "BTC");

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={priceData}>
        <XAxis
          dataKey="timestamp"
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(timestamp) => {
            // Convert timestamp to milliseconds
            const milliseconds = timestamp * 1000;
            // Create a new Date object with the milliseconds
            const dateObject = new Date(milliseconds);
            // Format the date as desired
            return dateObject.toLocaleString();
          }}
        />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `$${value}`}
        />
        <Line
          type="monotone"
          dataKey="amount"
          stroke="currentColor"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
