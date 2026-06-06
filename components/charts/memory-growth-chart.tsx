"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const data = [
  { day: "W1", value: 14 },
  { day: "W2", value: 22 },
  { day: "W3", value: 29 },
  { day: "W4", value: 40 },
  { day: "W5", value: 52 },
  { day: "W6", value: 68 }
];

export function MemoryGrowthChart() {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <CartesianGrid stroke="rgba(255,255,255,0.08)" vertical={false} />
        <XAxis dataKey="day" stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <YAxis stroke="rgba(148,163,184,0.7)" tickLine={false} axisLine={false} />
        <Tooltip contentStyle={{ background: "rgba(2, 6, 23, 0.95)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 16, color: "#fff" }} />
        <Line type="monotone" dataKey="value" stroke="#34d399" strokeWidth={3} dot={{ r: 4, fill: "#34d399" }} />
      </LineChart>
    </ResponsiveContainer>
  );
}