import React from "react";
import { Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";
import usePriceData from "@/hooks/use-price-data";
import { Price } from "@/types/data";

type ProcessedPriceData = {
  timestamp: number;
  amount: string;
};

export function Overview() {
  const socketUrl = "ws://localhost:8000/ws/coinbase/prices";
  const priceData = usePriceData(socketUrl, "BTC");

  // Preprocess the data
  const processData = (data: Price[]): ProcessedPriceData[] => {
    const newData: ProcessedPriceData[] = [];
    const intervals: Record<number, { timestamp: number; amount: number[] }> =
      {};

    // Group data into 5-minute intervals
    data.forEach((item) => {
      const timestamp = Math.floor(item.timestamp / 300) * 300; // Round to 5-minute interval
      if (!intervals[timestamp]) {
        intervals[timestamp] = {
          timestamp,
          amount: [],
        };
      }
      intervals[timestamp].amount.push(parseFloat(item.amount));
    });

    // Calculate average price for each interval
    for (const timestamp in intervals) {
      const averagePrice =
        intervals[timestamp].amount.reduce((a, b) => a + b, 0) /
        intervals[timestamp].amount.length;
      newData.push({
        timestamp: parseInt(timestamp),
        amount: averagePrice.toFixed(2),
      });
    }

    return newData;
  };

  const processedData = processData(priceData);

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={processedData}>
        <XAxis
          dataKey="timestamp"
          type="number"
          domain={["dataMin", "dataMax"]}
          tickFormatter={(timestamp) => {
            const dateObject = new Date(timestamp * 1000);
            return dateObject.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });
          }}
        />
        <YAxis
          type="number"
          domain={["auto", "auto"]}
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
