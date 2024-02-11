"use client";

import usePriceData from "@/hooks/use-price-data";
import { Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

export function Overview() {
  const socketUrl = "ws://localhost:8000/ws/coinbase/prices";

  const priceData = usePriceData(socketUrl);

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
            // Format timestamp as desired (e.g., convert to date)
            return new Date(timestamp).toLocaleString();
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
